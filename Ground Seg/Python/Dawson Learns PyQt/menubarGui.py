import sys
from PyQt4 import QtGui, QtCore

class Example(QtGui.QMainWindow):
    def __init__(self):
        super(Example,self).__init__()

        self.initUI()

    def initUI(self):
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')  # Whoa!  This is super cool!
        exitAction.triggered.connect(QtGui.qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("MenuBar")
        self.show()

def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()