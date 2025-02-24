import sys
import datetime
from colorama import init, Fore, Style

init(autoreset=True)

LEVEL_COLORS = {
    'INFO': Fore.BLUE,
    'WARNING': Fore.YELLOW,
    'ERROR': Fore.RED,
    'SUCCESS': Fore.GREEN
}

LOG_DATE_FORMAT = "%m.%d %H:%M:%S"

def _log(level, message):
    now = datetime.datetime.now().strftime(LOG_DATE_FORMAT)
    prefix = f"[{now}][{level}]"
    color = LEVEL_COLORS.get(level, '')
    # Split message into lines and add prefix for each line.
    lines = message.split('\n')
    for line in lines:
        sys.stdout.write(f"{color}{prefix}{Style.RESET_ALL} {line}\n")

def info(message):
    _log('INFO', message)

def warning(message):
    _log('WARNING', message)

def error(message):
    _log('ERROR', message)

def success(message):
    _log('SUCCESS', message)

def exception(error):
    _log('ERROR', str(error))

if __name__ == '__main__':
    info("这是一个信息日志\n带有换行测试")
    warning("警告！注意事项\n详细信息")
    error("错误出现了\n请检查代码")
    success("操作成功\n继续下一步")