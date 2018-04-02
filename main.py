import sys
from module.huya import huya_spider
import module.admin_log


if __name__ == '__main__':
    # logging.info('this is a loggging info message')
    huya_file = 'huya.xlsx'
    if str(sys.argv[1]):
        ch = str(sys.argv[1])
    else:
        ch = None
    huya_spider(huya_file, ch)
