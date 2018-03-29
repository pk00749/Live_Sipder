from module.get_rooms import get_room_list
from module.huya import huya_spider


if __name__ == '__main__':
    huya_file = 'huya.xlsx'
    get_room_list()
    huya_spider(huya_file)
