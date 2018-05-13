from PyQt5.QtWidgets import QMainWindow
from huya.ui.main import Ui_MainWindow
from huya.spiders.huya_main import start_huya_spider
import pickle, time

class LiveSpiderWindow(QMainWindow, Ui_MainWindow):
    print("ui_middleware")
    def __init__(self):
        super(LiveSpiderWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_start.clicked.connect(self.get_start)

        self.is_clicked_rb_1 = False
        self.is_clicked_rb_2 = False
        self.is_clicked_rb_3 = False
        self.is_clicked_rb_4 = False
        self.is_clicked_rb_5 = False
        self.user_name = ''


    def get_start(self):
        self.get_radio_status()
        # status = self.get_radio_status()
        # for user in range(5):
        #     if status[user]:
        #         self.ui.textEdit.append("%s checked" % (user + 1))
        #         self.get_user_name(user)
        #     else:
        #         print("%s unchecked" % (user + 1))
        # print(self.is_clicked_rb_1)
        if self.is_clicked_rb_1:
            self.save_json()
            start_huya_spider()
        else:
            print("Please check!")

    # def get_user_name(self, user):
    def get_user_name(self):
        self.user_name = str(self.ui.table_info.item(0, 1).text())
        print("middle_get: "+ self.user_name)


    def get_radio_status(self):
        self.is_clicked_rb_1 = self.ui.rb_1.isChecked()
        self.is_clicked_rb_2 = self.ui.rb_2.isChecked()
        self.is_clicked_rb_3 = self.ui.rb_3.isChecked()
        self.is_clicked_rb_4 = self.ui.rb_4.isChecked()
        self.is_clicked_rb_5 = self.ui.rb_5.isChecked()
        return [self.is_clicked_rb_1,self.is_clicked_rb_2, self.is_clicked_rb_3, self.is_clicked_rb_4, self.is_clicked_rb_5]


    def save_json(self):
        meta = {'no': 1,
                'name': str(self.ui.table_info.item(0, 1).text()),
                'password': str(self.ui.table_info.item(0, 2).text())
                }
        pickle.dump(meta, open("./json/1.pkl", "wb"))

    # def check_input_stock_code(self):
    #     self.ui.input_stock_code.selectAll()
    #     if len(self.ui.input_stock_code.selectedText()) == 0:
    #         self.ui.textEdit.append("Please input stock code")
    #         return False
    #     return True
    #
    # """By Stock Code"""
    # def get_stock_info_dao(self):
    #     if self.check_input_stock_code():
    #         result = get_stock_info(self.ui.input_stock_code.text())
    #         self.ui.textEdit.append(str(result))
    #
    # def update_k_data_dao(self):
    #     if self.check_input_stock_code():
    #         result = AdminDatabase.update_db_k_data(self.ui.input_stock_code.text())
    #         self.ui.textEdit.append(str(result))
    #         print(result)
    #
    # def calendar_dao(self):
    #     if self.check_input_stock_code():
    #         date = self.ui.input_from_date.text()
    #         value = QueryDatabase.get_k_value(self.ui.input_stock_code.text(), date)
    #         self.ui.output_close_price.setText(str(value))
    #
    # def calendar_period_dao(self):
    #     if self.check_input_stock_code():
    #         # date = self.ui.calendarWidget.selectedDate().toString(Qt.ISODate) #.toPyDate()
    #         data, index = QueryDatabase.get_k_value_period(self.ui.input_stock_code.text(),
    #                                           self.ui.input_from_date.text(), self.ui.input_to_date.text())
    #         Draw.draw_k_data_period(data, index)
    #
    # """Statement"""
    # def update_statement_dao(self):
    #     if self.check_input_stock_code():
    #         if self.ui.rdb_bs.isChecked():
    #             result = AdminDatabase.update_db_consolidated_statement_data(self.ui.input_stock_code.text(), 'BS')
    #             self.ui.textEdit.append(result)
    #             print(result)
    #         elif self.ui.rdb_cash.isChecked():
    #             result = AdminDatabase.update_db_consolidated_statement_data(self.ui.input_stock_code.text(), 'Cash')
    #             self.ui.textEdit.append(result)
    #             print(result)
    #         elif self.ui.rdb_pl.isChecked():
    #             result = AdminDatabase.update_db_consolidated_statement_data(self.ui.input_stock_code.text(), 'PL')
    #             self.ui.textEdit.append(result)
    #             print(result)
    #         else:
    #             self.ui.textEdit.append("Please choose one type")
    #

