import sys
import os
import parallel as pl
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from main_ui import Ui_MainWindow
from dlg_ui import Ui_Dialog
from base import PATH, STATUS
from run import main as auto_login
from list_update import update


class Main_window(QMainWindow):
    def __init__(self):
        super(Main_window, self).__init__()
        self.new = Ui_MainWindow()
        self.new.setupUi(self)
        STATUS.GUI = True
        STATUS.MAIN = self
        self.new.user_info_table.setColumnWidth(0, 180)
        self.new.user_info_table.setColumnWidth(1, 150)
        self.user_info_table_update()
        self.info_update()

    def run_auto_login(self):
        STATUS.RUN = True
        pl.run_thread([(auto_login, ())], name='__auto_run', is_lock=False)

    def stop_auto_login(self):
        STATUS.RUN = False
        pl.kill_thread(name='__auto_run')

    def list_update(self):
        self.message = QMessageBox()
        self.message.show()

    def user_info_table_update(self):
        with open(os.path.join(PATH, 'src', 'success.txt')) as file:
            lines = file.read().split('\n')
            self.new.user_info_table.setRowCount(
                len(lines) if lines[-1] else len(lines) - 1)
            for index, line in enumerate(lines):
                if line:
                    user, _, flow = line.split('\t')
                    self.new.user_info_table.setItem(
                        index, 0, QTableWidgetItem(user))
                    self.new.user_info_table.setItem(
                        index, 1, QTableWidgetItem(flow))

    def info_update(self):
        self.new.user_name_label.setText(STATUS.USER)
        self.new.flow_label.setText(STATUS.FLOW)
        self.new.login_status_label.setText('在线' if STATUS.LOGIN else '离线')
        self.new.run_status_label.setText('运行中' if STATUS.RUN else '未运行')

# class Dlg(Ui_Dialog)

def main():
    app = QApplication(sys.argv)
    main_window = Main_window()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
