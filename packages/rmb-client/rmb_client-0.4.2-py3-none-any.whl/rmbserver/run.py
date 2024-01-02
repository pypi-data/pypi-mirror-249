# 创建应用实例
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from rmbserver.servers import app


def main():
    try:
        app.run(sys.argv[1], int(sys.argv[2]))
    except:
        app.run('0.0.0.0', 5000)


# 启动Flask Web服务
if __name__ == '__main__':
    main()
