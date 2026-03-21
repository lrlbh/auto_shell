# 扫描后，优先连接信号最好的wifi
wifi信息组 = {"12345678": "12345678",
           "CMCC-Ef6Z": "ddtzpts9",
           "CMCC-vKWf": "7vzpycp6",
           "CMCC-luoyuan": "A13466179775"}

# 直接连接指定wifi，不扫描可以加快连接速度
# 不指定传None
ssid = "CMCC-Ef6Z"
pwd = "ddtzpts9"

# 强烈建议配置静态IP，开发时加快重启后wifi连接速度
静态ip = True
ip = "192.168.1.188"
dns_server = "192.168.1.1"
网关 = "192.168.1.1"
子网掩码 = "255.255.255.0"

# 默认文件读写速度只有1MiB左右
# 为了避免启动时，字库、图片之类资源，计算本地hash浪费太多时间
忽略的文件和目录 = [
    # "lib_lsl",
    # "boot.py",
    # "boot_run.py",


    "__pycache__",
    ".vscode",
    "Readme.md",
    "readme.md",
    "README.md",
    "README.md",
    "README.md",
    "LICENSE",
    ".gitignore",
]

# 广播端口,自动发现服务器地址，然后获取其他必备数据
广播端口 = 50000
