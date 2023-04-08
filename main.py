import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import file_downloader
import file_writer
from gui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tracking = None
        self._startPos = None
        self._endPos = None
        self.setupUi(self)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.pushButton_3.clicked.connect(self.download)

    def mouseMoveEvent(self, e: QMouseEvent):
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None
            self._endPos = None

    def download(self):
        url = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}.png"
        HEADERS = {
            "accept": "application/json, text/plain, */*",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54 "
        }
        x1 = int(self.lineEdit.text())
        x2 = int(self.lineEdit_2.text())
        y1 = int(self.lineEdit_3.text())
        y2 = int(self.lineEdit_4.text())
        scale = int(self.lineEdit_5.text())
        maps_index = []
        count = 0
        step = int(40075014 / 2 ** scale)
        for x in range(x1, x2, step):
            for y in range(y1, y2, step):
                col, row = file_downloader.cal_col_and_row(x, y, scale)
                maps_index.append([col, row])
                count += 1
        maps_index = file_downloader.no_same_element_list(maps_index)
        for indexs in maps_index:
            pic = file_downloader.download_map(url, 15, indexs[1], indexs[0], HEADERS)
            picname = "scale={}_row={}_col={}".format(scale, indexs[1], indexs[0])
            file_writer.write_map(pic, picname)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
