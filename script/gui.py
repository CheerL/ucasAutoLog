import sys
import os
import parallel as pl
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox, QWidget, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtGui import QIcon
from ui.main_ui import Ui_MainWindow
from ui.dlg_ui import Ui_Dialog
from ui.pro_ui import Ui_Dialog as Ui_pro
from base import PATH, STATUS, SYSTEM
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

        if SYSTEM in ['Windows', 'Linux']:
            self.icon_path = os.path.join(PATH, 'src', 'icon', 'icon.ico')
            self.setWindowIcon(QIcon(self.icon_path))
            self.tray_icon = TrayIcon(self, self.icon_path)
        else:
            self.new.pushButton.hide()

    def run_auto_login(self):
        STATUS.RUN = True
        pl.run_thread([(auto_login, ())], name='auto_run', is_lock=False)
        QMessageBox.information(self, '提示', '程序开始运行', QMessageBox.Yes)

    def stop_auto_login(self):
        STATUS.RUN = False
        pl.kill_thread(name='auto_run')
        QMessageBox.information(self, '提示', '程序停止运行', QMessageBox.Yes)

    def list_update(self):
        self.update_dlg = Update_dlg()
        self.update_dlg.show()

    def user_info_table_update(self):
        with open(os.path.join(PATH, 'src', 'success.txt')) as file:
            lines = file.read().split('\n')
            lines_num = len(lines) if lines[-1] else len(lines) - 1
            self.new.user_info_table.setRowCount(lines_num)
            for index, line in enumerate(lines):
                if line:
                    user, _, flow = line.split('\t')
                    self.new.user_info_table.setItem(
                        index, 0, QTableWidgetItem(user))
                    self.new.user_info_table.setItem(
                        index, 1, QTableWidgetItem(flow))
            self.num = lines_num

    def info_update(self):
        self.new.user_name_label.setText(STATUS.USER)
        self.new.flow_label.setText(STATUS.FLOW)
        self.new.login_status_label.setText('在线' if STATUS.LOGIN else '离线')
        self.new.run_status_label.setText('运行中' if STATUS.RUN else '未运行')

    def show_update_result(self):
        title = '更新结果'
        msg = '更新完毕， 共有%s个可用账号' % self.num
        QMessageBox.information(self, title, msg, QMessageBox.Yes)

    def minimize(self):
        self.tray_icon.show_or_hide()


class Update_dlg(QWidget):
    def __init__(self):
        super().__init__()
        self.dlg = Ui_Dialog()
        self.dlg.setupUi(self)
        STATUS.UPDATE_DLG = self

    def full_update(self):
        self.pro = Update_pro()
        self.pro.show()
        pl.run_thread([(update, ('full',))], 'update', False)

    def fast_update(self):
        self.pro = Update_pro()
        self.pro.show()
        pl.run_thread([(update, ('fast',))], 'update', False)


class Update_pro(QWidget):
    def __init__(self):
        super().__init__()
        self.main = Ui_pro()
        self.main.setupUi(self)
        STATUS.UPDATE = self.main
        self.step = 0
        self.finish = None
        self.timer = QBasicTimer()
        self.timer.start(100, self)

    def cancel_update(self):
        if not self.finish:
            reply = QMessageBox.question(
                self, '取消确认', '是否取消更新？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                pl.kill_thread(name='update')
                self.timer.stop()
                STATUS.UPDATE, STATUS.UPDATE_ALL, STATUS.UPDATE_NOW = None, 0, 0
                self.close()
        else:
            self.close()

        if STATUS.UPDATE_DLG:
            STATUS.UPDATE_DLG.close()
            STATUS.UPDATE_DLG = None
        if STATUS.MAIN:
            STATUS.MAIN.user_info_table_update()
            STATUS.MAIN.show_update_result()

    def timerEvent(self, event):
        if STATUS.UPDATE and STATUS.UPDATE_ALL:
            if self.finish is None:
                self.finish = False
            self.step = int(100 * STATUS.UPDATE_NOW / STATUS.UPDATE_ALL)
            self.main.pro_bar.setValue(self.step)
        elif self.finish is False:
            self.finish = True
            self.main.pro_bar.setValue(100)
            self.main.btn.setText('完成')
            self.timer.stop()

class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None, icon_path=''):
        super(TrayIcon, self).__init__(parent)
        self.icon_path = icon_path
        self.showMenu()
        self.activated.connect(self.iconClied)
        self.setIcon(QIcon(self.icon_path))
        self.icon = self.MessageIcon()
        self.show()

    def showMenu(self):
        "设计托盘的菜单，这里我实现了一个二级菜单"
        self.menu = QMenu()
        self.quitAction = QAction("退出", self, triggered=self.quit)
        self.show_or_hide_Action = QAction("隐藏", self, triggered=self.show_or_hide)
        self.menu.addAction(self.quitAction)
        self.menu.addAction(self.show_or_hide_Action)
        self.setContextMenu(self.menu)

    def iconClied(self, reason):
        "鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击"
        if reason == 2 or reason == 3:
            self.show_or_hide()

    def quit(self):
        "保险起见，为了完整的退出"
        self.setVisible(False)
        self.parent().close()

    def show_or_hide(self):
        pw = self.parent()
        if pw.isVisible():
            pw.hide()
            self.show_or_hide_Action.setText('显示')
        else:
            pw.show()
            self.show_or_hide_Action.setText('隐藏')

def main():
    app = QApplication(sys.argv)
    main_window = Main_window()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
