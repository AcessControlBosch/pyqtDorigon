# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Interface_didatica_menu_botao_emergencia.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_interface_didatica_menu_botao_emergencia(object):
    def setupUi(self, interface_didatica_menu_botao_emergencia):
        interface_didatica_menu_botao_emergencia.setObjectName("interface_didatica_menu_botao_emergencia")
        interface_didatica_menu_botao_emergencia.resize(1290, 841)
        interface_didatica_menu_botao_emergencia.setMinimumSize(QtCore.QSize(1290, 841))
        interface_didatica_menu_botao_emergencia.setMaximumSize(QtCore.QSize(1290, 841))
        interface_didatica_menu_botao_emergencia.setStyleSheet("background-color: rgb(255, 255, 255);")
        interface_didatica_menu_botao_emergencia.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(interface_didatica_menu_botao_emergencia)
        self.centralwidget.setObjectName("centralwidget")
        self.Label_Borda = QtWidgets.QLabel(self.centralwidget)
        self.Label_Borda.setGeometry(QtCore.QRect(0, 783, 1290, 18))
        self.Label_Borda.setText("")
        self.Label_Borda.setPixmap(QtGui.QPixmap("Imagens/Borda.png"))
        self.Label_Borda.setScaledContents(True)
        self.Label_Borda.setObjectName("Label_Borda")
        self.botao_home = QtWidgets.QPushButton(self.centralwidget)
        self.botao_home.setGeometry(QtCore.QRect(1140, 0, 131, 131))
        self.botao_home.setStyleSheet("border-style: outset;\n"
"border-color: rgb(0, 0, 0);\n"
"border-width:5px;\n"
"font: 75 65pt \"Bosch Sans Bold\";\n"
"border-radius: 0px;\n"
"background-color: rgb(255, 255, 255);")
        self.botao_home.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("imagens/Home.Interface.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.botao_home.setIcon(icon)
        self.botao_home.setIconSize(QtCore.QSize(110, 110))
        self.botao_home.setObjectName("botao_home")
        self.label_fundo = QtWidgets.QLabel(self.centralwidget)
        self.label_fundo.setGeometry(QtCore.QRect(20, 0, 1251, 761))
        font = QtGui.QFont()
        font.setFamily("Bosch Sans Bold")
        font.setPointSize(65)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_fundo.setFont(font)
        self.label_fundo.setStyleSheet("border-style: outset;\n"
"border-color: rgb(0, 0, 0);\n"
"border-width:7px;\n"
"border-radius: 0px;\n"
"background-color: rgb(255, 255, 255);")
        self.label_fundo.setText("")
        self.label_fundo.setObjectName("label_fundo")
        self.label_imagem = QtWidgets.QLabel(self.centralwidget)
        self.label_imagem.setGeometry(QtCore.QRect(60, 200, 381, 431))
        self.label_imagem.setStyleSheet("")
        self.label_imagem.setText("")
        self.label_imagem.setPixmap(QtGui.QPixmap("imagens/botao_emergencia.png"))
        self.label_imagem.setScaledContents(True)
        self.label_imagem.setObjectName("label_imagem")
        self.label_titulo = QtWidgets.QLabel(self.centralwidget)
        self.label_titulo.setGeometry(QtCore.QRect(20, 0, 1121, 81))
        self.label_titulo.setStyleSheet("border-style: outset;\n"
"border-color: rgb(0, 0, 0);\n"
"border-width:6px;\n"
"\n"
"\n"
"font: 75 37pt \"Bosch Sans Bold\";\n"
"background-color: rgb(0,0,0);")
        self.label_titulo.setObjectName("label_titulo")
        self.label_fundo_verde = QtWidgets.QLabel(self.centralwidget)
        self.label_fundo_verde.setGeometry(QtCore.QRect(20, 75, 461, 685))
        self.label_fundo_verde.setStyleSheet("border-style: outset;\n"
"border-color: rgb(0, 0, 0);\n"
"border-width:6px;\n"
"background-color: rgb(155, 228, 179);\n"
"\n"
"font: 75 80pt \"Bosch Sans Bold\";\n"
"")
        self.label_fundo_verde.setText("")
        self.label_fundo_verde.setScaledContents(True)
        self.label_fundo_verde.setObjectName("label_fundo_verde")
        self.label_caixa_de_texto = QtWidgets.QLabel(self.centralwidget)
        self.label_caixa_de_texto.setGeometry(QtCore.QRect(490, 130, 771, 491))
        self.label_caixa_de_texto.setStyleSheet("font: 75 20pt \"Bosch Sans Bold\";\n"
"\n"
"")
        self.label_caixa_de_texto.setObjectName("label_caixa_de_texto")
        self.botao_seta_esquerda = QtWidgets.QPushButton(self.centralwidget)
        self.botao_seta_esquerda.setGeometry(QtCore.QRect(1040, 630, 98, 117))
        self.botao_seta_esquerda.setStyleSheet("border-style: outset;\n"
"border-color: rgb(0,0,0);\n"
"\n"
"")
        self.botao_seta_esquerda.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("imagens/Seta Preta para esquerda.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.botao_seta_esquerda.setIcon(icon1)
        self.botao_seta_esquerda.setIconSize(QtCore.QSize(120, 120))
        self.botao_seta_esquerda.setShortcut("")
        self.botao_seta_esquerda.setObjectName("botao_seta_esquerda")
        self.botao_seta_dirteita = QtWidgets.QPushButton(self.centralwidget)
        self.botao_seta_dirteita.setGeometry(QtCore.QRect(1160, 630, 96, 115))
        self.botao_seta_dirteita.setStyleSheet("border-style: outset;\n"
"border-color: rgb(0,0,0);\n"
"\n"
"")
        self.botao_seta_dirteita.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("imagens/Seta Branca para direita.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.botao_seta_dirteita.setIcon(icon2)
        self.botao_seta_dirteita.setIconSize(QtCore.QSize(120, 120))
        self.botao_seta_dirteita.setShortcut("")
        self.botao_seta_dirteita.setObjectName("botao_seta_dirteita")
        self.Label_Borda.raise_()
        self.label_fundo.raise_()
        self.botao_home.raise_()
        self.label_titulo.raise_()
        self.label_fundo_verde.raise_()
        self.botao_seta_esquerda.raise_()
        self.botao_seta_dirteita.raise_()
        self.label_imagem.raise_()
        self.label_caixa_de_texto.raise_()
        interface_didatica_menu_botao_emergencia.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(interface_didatica_menu_botao_emergencia)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1290, 21))
        self.menubar.setObjectName("menubar")
        interface_didatica_menu_botao_emergencia.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(interface_didatica_menu_botao_emergencia)
        self.statusbar.setObjectName("statusbar")
        interface_didatica_menu_botao_emergencia.setStatusBar(self.statusbar)

        self.retranslateUi(interface_didatica_menu_botao_emergencia)
        QtCore.QMetaObject.connectSlotsByName(interface_didatica_menu_botao_emergencia)

    def retranslateUi(self, interface_didatica_menu_botao_emergencia):
        _translate = QtCore.QCoreApplication.translate
        interface_didatica_menu_botao_emergencia.setWindowTitle(_translate("interface_didatica_menu_botao_emergencia", "MainWindow"))
        self.label_titulo.setText(_translate("interface_didatica_menu_botao_emergencia", "<html><head/><body><p align=\"center\"><span style=\" color:#ffc000;\">BOTÃO DE PARADA DE EMERGÊNCIA</span></p></body></html>"))
        self.label_caixa_de_texto.setText(_translate("interface_didatica_menu_botao_emergencia", "    Quando pressionado, possui a finalindade de parar \n"
"imediatamente o movinmento da máquina, desabilitando seu \n"
"comando. O botão de parada de emergência deve estar \n"
"em um local visível da máquina e sempre ao alcance \n"
"do operador.\n"
"\n"
"    O mesmo deve ser pressionado caso necessite de \n"
"uma parada imediata, como em casos de acidentes de \n"
"trabalho, ou se a máquina apresentar uma funcionalida-\n"
"de inadequada da qual está programada.  \n"
""))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    interface_didatica_menu_botao_emergencia = QtWidgets.QMainWindow()
    ui = Ui_interface_didatica_menu_botao_emergencia()
    ui.setupUi(interface_didatica_menu_botao_emergencia)
    interface_didatica_menu_botao_emergencia.show()
    sys.exit(app.exec_())
