# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import webbrowser,os
import main

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.win=MainWindow
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(135, 478)
        MainWindow.move(50,20)
        MainWindow.setWindowTitle(_fromUtf8(""))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 390, 91, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 250, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(30, 280, 75, 23))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.checkBox_4 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_4.setGeometry(QtCore.QRect(30, 190, 75, 23))
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 130, 111, 51))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(212, 212, 212))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
    
        self.frame.setPalette(palette)
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.pushButton_5 = QtGui.QPushButton(self.frame)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 20, 31, 23))
        self.pushButton_5.setAutoRepeat(True)
        self.pushButton_5.setAutoRepeatDelay(100)
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_6 = QtGui.QPushButton(self.frame)
        self.pushButton_6.setGeometry(QtCore.QRect(70, 20, 31, 23))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_6.setAutoRepeat(True)
        self.pushButton_6.setAutoRepeatDelay(100)
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 0, 101, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 0, 101, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(10, 70, 111, 51))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(212, 212, 212))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
 
        self.frame_2.setPalette(palette)
        self.frame_2.setAutoFillBackground(True)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.pushButton_7 = QtGui.QPushButton(self.frame_2)
        self.pushButton_7.setGeometry(QtCore.QRect(10, 20, 31, 23))
        self.pushButton_7.setAutoRepeat(True)
        self.pushButton_7.setAutoRepeatDelay(100)
        self.pushButton_7.setObjectName(_fromUtf8("pushButton_7"))
        self.pushButton_8 = QtGui.QPushButton(self.frame_2)
        self.pushButton_8.setGeometry(QtCore.QRect(70, 20, 31, 23))
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.label_4 = QtGui.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(20, 0, 101, 20))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.frame_3 = QtGui.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(10, 10, 111, 51))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(212, 212, 212))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
 
        self.frame_3.setPalette(palette)
        self.frame_3.setAutoFillBackground(True)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.pushButton_9 = QtGui.QPushButton(self.frame_3)
        self.pushButton_9.setGeometry(QtCore.QRect(10, 20, 31, 23))
        self.pushButton_9.setAutoRepeat(True)
        self.pushButton_9.setAutoRepeatDelay(100)
        self.pushButton_9.setObjectName(_fromUtf8("pushButton_9"))
        self.pushButton_10 = QtGui.QPushButton(self.frame_3)
        self.pushButton_10.setGeometry(QtCore.QRect(70, 20, 31, 23))
        self.pushButton_10.setObjectName(_fromUtf8("pushButton_10"))
        self.label_5 = QtGui.QLabel(self.frame_3)
        self.label_5.setGeometry(QtCore.QRect(30, 0, 51, 20))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.pushButton_11 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_11.setGeometry(QtCore.QRect(20, 360, 91, 23))
        self.pushButton_11.setObjectName(_fromUtf8("pushButton_11"))
        self.checkBox_12 = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_12.setGeometry(QtCore.QRect(30, 210, 75, 23))
        self.checkBox_12.setObjectName(_fromUtf8("checkBox_12"))
        self.checkBox_12.setChecked(True)
        self.pushButton_13 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_13.setGeometry(QtCore.QRect(50, 430, 31, 23))
 
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_13.setFont(font)
        self.pushButton_13.setAutoFillBackground(False)
        self.pushButton_13.setStyleSheet(_fromUtf8("QPushButton{\n"
"color: white;\n"
"background-color:rgb(85, 85, 127)\n"
"}"))
        self.pushButton_13.setObjectName(_fromUtf8("pushButton_13"))
        self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(30, 310, 75, 23))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton_13.raise_()
        self.retranslateUi(MainWindow)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        QtCore.QObject.connect(self.pushButton  , QtCore.SIGNAL(_fromUtf8("clicked()")), self.start_fullscreen)
        QtCore.QObject.connect(self.pushButton_5, QtCore.SIGNAL(_fromUtf8("pressed()")), self.cycle_down)
        QtCore.QObject.connect(self.pushButton_6, QtCore.SIGNAL(_fromUtf8("pressed()")), self.cycleup)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), self.runzoom)
        QtCore.QObject.connect(self.checkBox_4,   QtCore.SIGNAL(_fromUtf8("clicked()")), self.juliamode)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), self.newpalette)
        QtCore.QObject.connect(self.pushButton_7, QtCore.SIGNAL(_fromUtf8("clicked()")), self.palette_up)
        QtCore.QObject.connect(self.pushButton_8, QtCore.SIGNAL(_fromUtf8("clicked()")), self.palette_down)
        QtCore.QObject.connect(self.pushButton_9, QtCore.SIGNAL(_fromUtf8("clicked()")), self.iters_down)
        QtCore.QObject.connect(self.pushButton_10, QtCore.SIGNAL(_fromUtf8("clicked()")), self.iters_up)
        QtCore.QObject.connect(self.pushButton_11, QtCore.SIGNAL(_fromUtf8("clicked()")), self.reset)
        QtCore.QObject.connect(self.pushButton_4, QtCore.SIGNAL(_fromUtf8("clicked()")), self.screenshot)
        QtCore.QObject.connect(self.pushButton_13, QtCore.SIGNAL(_fromUtf8("clicked()")), lambda : webbrowser.open("file://"+os.getcwd()+"/resources/help.html"))
        QtCore.QObject.connect(self.checkBox_12, QtCore.SIGNAL(_fromUtf8("clicked()")), self.toggle_cycle)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.start()

    def retranslateUi(self, MainWindow):
        self.pushButton.setText(_translate("MainWindow", "Start fullscreen", None))
        self.pushButton_2.setText(_translate("MainWindow", "New palette", None))
        self.pushButton_3.setText(_translate("MainWindow", "Run zoom", None))
        self.checkBox_4.setText(_translate("MainWindow", "Julia mode", None))
        self.pushButton_5.setText(_translate("MainWindow", "-", None))
        self.pushButton_6.setText(_translate("MainWindow", "+", None))
        self.label.setText(_translate("MainWindow", " Color cycle speed", None))
        self.pushButton_7.setText(_translate("MainWindow", "-", None))
        self.pushButton_8.setText(_translate("MainWindow", "+", None))
        self.label_4.setText(_translate("MainWindow", " Palette rate", None))
        self.pushButton_9.setText(_translate("MainWindow", "-", None))
        self.pushButton_10.setText(_translate("MainWindow", "+", None))
        self.label_5.setText(_translate("MainWindow", "Iterations", None))
        self.checkBox_12.setText(_translate("MainWindow", "ColorCycle", None))
        self.pushButton_11.setText(_translate("MainWindow", "Reset", None))
        self.pushButton_13.setText(_translate("MainWindow", "?", None))
        self.pushButton_4.setText(_translate("MainWindow", "Screenshot", None))
        
    def start(self):
        
        self.app=main.App(main.WINDOWED)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        QtCore.QObject.connect(self.timer,QtCore.SIGNAL('timeout()'), self.update)
        self.timer.start()
    
    def start_fullscreen(self):
        app=main.App(main.FULLSCREEN)
        app.run()
    
    def screenshot(self):
        
        name=self.app.screenshot()
        msg=QtGui.QMessageBox()
        msg.setText("Image saved in "+name)
        msg.exec_()
        
    def cycleup(self):
    
        self.app.step*=1.1
        
    def cycle_down(self):
        
        self.app.step/=1.1
    
    def palette_up(self):
    
        self.app.palette_up()
        
    def palette_down(self):
        
        self.app.palette_down()
            
    def newpalette(self):
        
        self.app.mandelbrot2.new_colours()
        
    def iters_up(self):
        
        self.app.iters+=200
        self.app.mode="calc"
        
    def iters_down(self):
        
        self.app.iters-=200
        self.app.mode="calc"
        
    def toggle_cycle(self):
        
        if self.checkBox_12.isChecked():
            self.app.cycle_switch = True
        else:
            self.app.cycle_switch = False 
       
    
    def reset(self):
        
        self.app.init()
        
    def update(self):
        
        if not self.app.update():
            self.timer.stop()
            self.win.close()
            
    def runzoom(self):
        
        self.app.mode="init_display_list"
    
    def juliamode(self):
        
        if self.checkBox_4.isChecked():
            self.app.mode="julia"
             
        else:
            self.app.mode="user_zoom"
             

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())