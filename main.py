from module.get_rooms import get_room_list
import huya

if __name__ == '__main__':
    get_room_list()
    huya = huya.Huya_Sipder()
    huya.main()