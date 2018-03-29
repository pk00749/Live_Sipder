from module.get_rooms import get_room_list
from module.admin_excel import AdminWorkbook
import huya


# def main():
#     workbook = AdminWorkbook('huya.xlsx')
#
#     def __login_info(self):
#         self.workbook.load_workbook()
#         username = self.workbook.read_cell('登录', 'A2')
#         password = self.workbook.read_cell('登录', 'B2')
#
#         # for i in range(10):
#         #     room["A%d" % (i+1)].value = i + 1
#         # return login_info['username'], login['password']
#         return username, password

if __name__ == '__main__':
    get_room_list()
    huya = huya.Huya_Sipder()
    huya.main()