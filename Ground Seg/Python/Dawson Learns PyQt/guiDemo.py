import sys
from PyQt4 import QtGui, QtCore


class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):

        self.timer = QtCore.QBasicTimer()
        self.step = 0

        lcd = QtGui.QLCDNumber(self)
        lcd.setSegmentStyle(QtGui.QLCDNumber.Flat)
        palette = lcd.palette()
        palette.setColor(palette.WindowText, QtGui.QColor(255, 0, 0))
        lcd.setPalette(palette)

        self.setWindowTitle("GUI Demo")

        self.setGeometry(300, 300, 300, 300)

        self.show()

    def timerEvent(self, e):

        self.step += 1
        self.pbar.setValue(self.step)
        # self.lcd.setPalette(palette)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
