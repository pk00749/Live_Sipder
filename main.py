from module.get_rooms import get_room_list
import login

if __name__ == '__main__':
    get_room_list()
    huya = login.Huya_Sipder()
    huya.main()