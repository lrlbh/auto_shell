~~~shell
上传boot.py到micropython后boot.py会开启一个线程，用于更新程序

boot_run.py 中保存了WiFi配置，当此文件不存在时，boot.py 不会运行

如果固件不是 https://github.com/lrlbh/cmaera_lr 中下载的，还需要上传lib_lsl目录，因为boot.py 调用了一些lib_lsl中的小工具
~~~



### 缺少的功能

- 显示当前文件是否同步
- 显示单片机是否在线
- ~~加入快捷键~~
- ~~跳转vscode错误行~~
- 心跳内容改为，启动时记录非忽略文件的hash，后续使用目录结构修改
- ~~wifi驱动需要检查修改，可以多次初始化~~
- 为串口提供，烧录固件，同步文件的基础操作，用于新单片机初始化
- 小内存单片机需要分片下载文件，避免大文件爆内存
- 使用引脚决定是否启动boot.py,是否比文件方便？
- 关播地址



### 依赖

~~~python
# 快捷键
pip install keyboard  

# UI 
pip install PyQt6

# VSCODE，不需要了,不需要了,不需要了,URL似乎跳转稍快一点
vscode加入环境变量，可以使用code命令跳转到错误文件
默认安装vscode有时会自动加入有时不会，没有关注什么原因
~~~

