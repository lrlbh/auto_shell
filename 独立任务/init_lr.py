import threading

import 独立任务.更新线程
import 独立任务.广播线程
import 独立任务.日志线程

def run():
    threading.Thread(target=独立任务.更新线程.run,  daemon=True).start()
    threading.Thread(target=独立任务.广播线程.run,  daemon=True).start()
    threading.Thread(target=独立任务.日志线程.run,  daemon=True).start()
