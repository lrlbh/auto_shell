import socket


class _tests():
    def __init__(self):

        # try:
        #     with open("/no_delete/ip.txt", "r") as f:
        #         ip = f.read().strip()
        # except:
        #     ip = None

        # # 文件存在才允许发送
        # self.ok = False
        # if tl.file_exists("/boot_run.py") or tl.file_exists("/Alr/boot_run.py"):
        #     self.ok = True

        self.ok = False
        self.ip = None
        self.port = 9001
        self._cnt = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.war = "warning_lr"
        self.err = "error_lr"

    def set_addr(self, ip=None, port=None):
        if ip is not None:
            self.ip = ip
        if port is not None:
            self.port = port

    def send(self, *args):
        if not self.ok:
            return

        self._cnt += 1
        try:
            msg = " ".join(map(str, args))
            self.sock.sendto("{} {}".format(
                self._cnt, msg).encode(), (self.ip, self.port))
        except:
            pass

    def send_war(self, *args):
        if not self.ok:
            return

        self._cnt += 1
        try:
            msg = " ".join(map(str, args))
            self.sock.sendto("{} {} {}".format(
                self.war, self._cnt, msg).encode(), (self.ip, self.port))
        except:
            pass

    def send_err(self, *args):
        if not self.ok:
            return

        self._cnt += 1
        try:
            msg = " ".join(map(str, args))
            self.sock.sendto("{} {} {}".format(
                self.err, self._cnt, msg).encode(), (self.ip, self.port))
        except:
            pass


_test = _tests()


set_addr = _test.set_addr
send = _test.send
send_war = _test.send_war
send_err = _test.send_err


# print("初始化")
# set_addr("sad","asdas","asda")
# send("asdf","sadf")
