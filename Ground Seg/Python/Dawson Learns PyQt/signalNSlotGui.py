import sys
from PyQt4 import QtGui, QtCore

class Communicate(QtCore.QObject):

    changeColor = QtCore.pyqtSignal()


class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        lcd = QtGui.QLCDNumber(self)
        lcd.setSegmentStyle(QtGui.QLCDNumber.Flat)
        palette = lcd.palette()
        palette.setColor(palette.WindowText, QtGui.QColor(255, 0, 0))
        lcd.setPalette(palette)

        self.c = Communicate()
        self.c.changeColor.connect(palette.setColor(palette.WindowText, QtGui.QColor(0, 0, 255)))

        sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)

        if(lcd.value()) > 50:
            palette.setColor(palette.WindowText, QtGui.QColor(255, 0, 0))
        else:
            palette.setColor(palette.WindowText, QtGui.QColor(0, 255, 0))
        lcd.setPalette(palette)

        self.setLayout(vbox)
        sld.valueChanged.connect(lcd.display)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle("Signal & Slot")

        self.show()


    def mousePressEvent(self, event):

        self.c.changeColor.emit()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
