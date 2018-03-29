import openpyxl
import os
# 新建文件
# workbook = openpyxl.Workbook()
 # 写入文件
# workbook.create_sheet('登录')
# workbook.create_sheet('房间')


class AdminWorkbook:

    def __init__(self, workbook_name):
        self.workbook_name = workbook_name
        self.workbook = self.load_workbook()

    def load_workbook(self):
        workbook = openpyxl.load_workbook(self.workbook_name)
        return workbook

    def read_cell(self, sheet_name, cell):
        sheet = self.workbook.get_sheet_by_name(sheet_name)
        return sheet[cell].value

    def write_cell(self, sheet_name, cell, value):
        sheet = self.workbook.get_sheet_by_name(sheet_name)
        sheet[cell] = value
        self.save_workbook()
#
    def save_workbook(self):
        self.workbook.save(self.workbook_name)

# test = admin_workbook('huya.xlsx')
# test.load_workbook()
# test.write_cell('房间', 'C2', 'www.baidu.com')
# print(test.read_cell('登录', 'A1'))


# sheet_login = workbook.get_sheet_by_name('登录')
# print(sheet_login['A1'].value)
# workbook = openpyxl.load_workbook(os.path.join('../','huya.xlsx'))
# sheet_login = workbook.get_sheet_by_name('登录')
# sheet_login['A1'] = '登录名'
# sheet_login['B1'] = '密码'
#
#
#
# room = workbook.get_sheet_by_name('房间')
# # sheet.title = "New Shit"
# room['A1']='A1'
# room['C3'] = 'Hello world!'
# for i in range(10):
#     room["A%d" % (i+1)].value = i + 1
#
#
# print(sheet_login['A1'].value)
#  # 保存文件
# workbook.save('../huya.xlsx')






# import xlsxwriter as xw
# #新建excel
# workbook  = xw.Workbook('huya.xlsx')
# #新建工作薄
# sheet_login = workbook.add_worksheet()
# #写入数据
# sheet_login.write('A1', '登录名')
# sheet_login.write('B1', '密码')
# #关闭保存
# workbook.close()



# # import csv
# #
# # with open('names.csv', 'w') as csvfile:
# #     fieldnames = ['first_name', 'last_name']
# #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
# #
# #     writer.writeheader()
# #     writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
# #     # writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
# #     # writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
# #
# #
# # import csv
# # fname = 'testcsv.csv'
# # with open(fname,'w', newline='') as csvfile: # 解决写入空行问题 使用wb不会再每一行后面插入空行
# #     csvwriter = csv.writer(csvfile)
# #     lst= [[1,2,3],[4,5,6]]
# #     csvwriter.writerows(lst)
#
# # import csv
# # with open('eggs.csv', 'w', newline='') as csvfile:
# #     spamwriter = csv.writer(csvfile, delimiter=' ',
# #                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
# #     spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
# #     spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
#
# import csv
#
# #python2可以用file替代open
# with open("test.csv","w") as csvfile:
#     writer = csv.writer(csvfile)
#
#     #先写入columns_name
#     writer.writerow(["index","a_name","b_name"])
#     #写入多行用writerows
#     writer.writerows([[0,1,3],[1,2,3],[2,3,4]])


