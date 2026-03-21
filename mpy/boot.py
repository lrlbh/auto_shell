import machine
import time
import _thread
import json
import socket
import json
import struct
import asyncio

try:
    # 非系统依赖
    import lib_lsl
    import lib_lsl.tl
    import boot_run
except:
    pass


def get_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("0.0.0.0", boot_run.广播端口))
        while True:
            data, addr = sock.recvfrom(1024)
            data = json.loads(data.decode())
            return addr[0], data["更新端口"], data["日志端口"]
    finally:
        sock.close()


# 收: 4字节文件个数 + [4字节文件名长度 + 文件名 + 4字节文件内容长度 + 文件内容] * 文件个数
async def read(r):
    '''
    暂不处理，但别忘了
        - 非S3,文件太大爆内存
        - 存在大量数据重复拷贝
    '''

    while True:
        # 文件个数
        file_n = await r.readexactly(4)
        file_n = struct.unpack('>I', file_n)[0]
        lib_lsl.send_war(f"需要更新文件数量:{file_n}")
        if file_n == 0:
            lib_lsl.send_war(f"文件数量0, 不更新")
            continue
        # 遍历文件
        for _ in range(file_n):
            t0 = time.ticks_ms()
            # 获取文件名
            file_name = await r.readexactly(struct.unpack('>I', await r.readexactly(4))[0])
            file_name_str = file_name.decode("utf-8")  # 文件名转字符串方便发送日志查看
            lib_lsl.tl.mkdir(file_name_str)  # 确保目录存在

            # 创建文件
            with open(file_name,  "wb") as f:
                t = f.write(await r.readexactly(struct.unpack('>I', await r.readexactly(4))[0]))
                # f.flush()

            lib_lsl.send_war(
                f"{file_name_str} -> size: {t/1024:0.2f}KiB -> 耗时:{time.ticks_diff(time.ticks_ms(), t0)}ms")

        lib_lsl.send_war("更新成功")
        await asyncio.sleep_ms(20)
        machine.reset()


async def send(w, file_md5):
    while True:
        await w.awrite(file_md5)
        await asyncio.sleep(3)  # 心跳间隔


async def 多任务():
    # 1、连接wifi
    t0 = time.ticks_ms()
    wifi = lib_lsl.WIFI(account=boot_run.wifi信息组, static=boot_run.静态ip,
                        ip=boot_run.ip, 子网掩码=boot_run.子网掩码,
                        网关=boot_run.网关, dns_server=boot_run.dns_server)
    wifi.conn_one(boot_run.ssid, boot_run.pwd)    # 人为阻塞连一下，为了计算耗时
    asyncio.create_task(wifi.conn_async(
        boot_run.ssid, boot_run.pwd))  # 携程中维护wifi连接
    await asyncio.sleep_ms(0)   # 让出一次时间，给携程创建
    t_log = f"连接wifi耗时: {time.ticks_diff(time.ticks_ms(), t0)} ms"

    # 2、获取广播的服务器IP地址
    t0 = time.ticks_ms()
    ip, 更新端口, 日志端口 = None, None, None
    while True:
        try:
            ip, 更新端口, 日志端口 = get_ip()
            break
        except Exception as e:
            await asyncio.sleep_ms(500)

    更新端口 = int(更新端口)
    日志端口 = int(日志端口)
    lib_lsl.set_addr(ip, 日志端口)
    lib_lsl._ul.udp_print = True
    lib_lsl.send_war("\n\n\n\n\n")
    lib_lsl.send_war(t_log)
    # lib_lsl.send_war(id(wifi))
    lib_lsl.send_war(
        f"获取server_ip耗时: {time.ticks_diff(time.ticks_ms(), t0)} ms")

    # 3、获取本地文件hash,并且补个头
    t0 = time.ticks_ms()
    file_md5 = lib_lsl.tl.get_files_md5("/")
    # for key in lib_lsl.tl.get_files_md5("/"):
    #     lib_lsl.send_err(key," --> ",lib_lsl.tl.get_files_md5("/")[key])
    file_md5 = json.dumps(file_md5).encode('utf-8')
    file_md5 = struct.pack('!I', len(file_md5)) + file_md5
    lib_lsl.send_war(
        f"获取md5耗时: {time.ticks_diff(time.ticks_ms(), t0)} ms")

    # 4、连接服务器
    while True:
        lib_lsl.send_war("尝试一次tcp连接")
        try:
            # 一段时间后会解除阻塞,此时建立连接失败也不ERROR,比较奇怪,强制释放一下算了
            r, w = await asyncio.open_connection(ip, 更新端口)
            # 创建收发任务
            t1 = asyncio.create_task(send(w, file_md5))
            t2 = asyncio.create_task(read(r))

            # 等待收发任务死亡
            try:
                await asyncio.gather(t1, t2)
            except Exception as e:
                t1.cancel()  # 可以重复释放  # t1.done()
                t2.cancel()
                lib_lsl.send_war("tcp断开: ", lib_lsl.tl.get_完整错误信息(e))
                # ul.send

        except Exception as e:
            lib_lsl.send_err(f"tcp意外错误: {e}")
        finally:
            try:
                w.close()
                await w.wait_closed()
            except:
                pass

        await asyncio.sleep(0.3)


# 子线程
def 子线程():
    asyncio.run(多任务())


def run():
    # 子线程用于更新
    # 子线程()
    _thread.start_new_thread(子线程, ())

    # 获取到server_ip后在运行main
    while lib_lsl._ul.ip is None:
        time.sleep(0.1)

    # 主线程运行main
    try:
        import main
    except Exception as e:
        # 用户错误返回完整错误信息
        lib_lsl.send_err(lib_lsl.tl.get_完整错误信息(e))

    raise Exception("正常结束,但避免系统调用main")


# 通过判断 boot_run.py 文件是否存在，决定是否执行boot.py
if __name__ == "__main__":
    # or lib_lsl.tl.file_exists("/Alr/boot_run.py"):
    if lib_lsl.tl.file_exists("/boot_run.py"):
        run()
