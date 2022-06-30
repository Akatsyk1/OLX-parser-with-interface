import webbrowser
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QListWidgetItem, QGridLayout
from parsingolxinterface import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from parsinganddimage import *
import json

class MyWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MyWin, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tableWidget.verticalHeader().setMinimumSectionSize(10)

        self.ui.pushButton.clicked.connect(self.a_parsing)


    def createCellWidget(self, pix, text, btn, url):
        layout = QtWidgets.QGridLayout()
        frame = QtWidgets.QFrame()
        frame.setLayout(layout)
        picture = QtWidgets.QLabel()
        picture.setPixmap(pix)
        layout.addWidget(picture, 0, 0, 2, 1)
        layout.addWidget(QtWidgets.QLabel(text), 0, 1)
        button = QtWidgets.QPushButton(btn)
        button.setStyleSheet("border-radius: 12px;\n"
            "color: rgb(0, 255, 38);\n"
            "background-color: rgb(0, 0, 0);\n"
            "border: 1px solid #00ff00;")

        button.clicked.connect(lambda: webbrowser.open(f'{url}'))
        button.resize(50, 50)
        layout.addWidget(button, 1, 1)
        return frame





    def a_parsing(self):
        page = self.ui.l_page.text()
        request = self.ui.l_request.text()
        page = int(page)
        parsing_olx(page=page, request=request)

        with open(f'data_{request}/resultparsingolx_{request}.json', 'r', encoding='utf8') as file:
            list_ads = json.load(file)

        for i, ad in enumerate(list_ads):
            url = ad.get('ad_url')
            pixmap = QPixmap(f'data_{request}/{ad.get("ad_title")}.png').scaled(100, 100)
            widget = self.createCellWidget(pixmap, f'{ad.get("ad_title")}', f'URL', url)
            self.ui.tableWidget.setCellWidget(i, 0, widget)
            #QGridLayout.addWidget(self.ui.tableWidget, 0, 0)


        try:
            shutil.rmtree(f'data_{request}')
        except:
            pass

    # def _parsing(self):
    #     self.ui.listWidget.clear()
    #     page = self.ui.l_page.text()
    #     request = self.ui.l_request.text()
    #     page = int(page)
    #     parsing_olx(page=page, request=request)
    #
    #     with open(f'data_{request}/resultparsingolx_{request}.json', 'r', encoding='utf8') as file:
    #         list_ads = json.load(file)
    #
    #     for i, ad in enumerate(list_ads):
    #         item = QListWidgetItem()
    #         icon = QIcon(f'data_{request}/{ad.get("ad_title")}.png')
    #         text = f"{ad.get('ad_title')} \n {ad.get('ad_url')} \n \n"
    #         item.setIcon(icon)
    #         item.setText(text)
    #         self.ui.listWidget.addItem(item)
    #         self.ui.listWidget.setIconSize(QSize(100, 100))
    #
    #     try:
    #         shutil.rmtree(f'data_{request}')
    #     except:
    #         pass



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
