##################### IMPORTANDO AS BIBLIOTECAS E FUNÇÕES ################################
import sys
from datetime import datetime, date
from time import sleep
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QLabel, QLineEdit, QTableWidget, \
    QAbstractItemView, QTableView
from PyQt5.QtGui import QIcon, QPixmap

import sqlite3

"""banco = sqlite3.connect("Banco.db")
cursor = banco.cursor()"""

"""""
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
Alimentacao_maquina = 12
led = 16
GPIO.setup(Alimentacao_maquina, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)

GPIO.output(Alimentacao_maquina, False)
GPIO.output(led, True)
"""""

# placeholder linedit
# ##################### IMPORTANDO AS CLASSES DOS ARQUIVOS DE TELAS ################################
from Menu01 import Ui_Menu01
from Menu01_LIBERADO import Ui_Menu01_Liberado
from Menu02 import Ui_Menu02
from Caderno_Verde_Atencao import Ui_Atencao
from Liberação_Segurança import Ui_Liberacao_Seguranca
from Liberação_Meio_Ambiente import Ui_Liberacao_Meio_Ambiente
from Documentos_Menu import Ui_documentos_menu
from Documentos_Documentos_de_pecas_menuu import Ui_documentos_documentos_de_pecas_menu
from documentos_documentos_de_pecas_1 import Ui_peca01
from documentos_documentos_de_pecas_2 import Ui_peca02
from documentos_documentos_de_pecas_3 import Ui_peca03
from documentos_diagrama_eletrico_imagens import Ui_documentos_diagrama_eletrico
from Documentos_mapa_de_risco import Ui_mapa_de_riscos
from Aviso_liberacao import Ui_Aviso_Liberacao
from Interface_didatica_menu import Ui_interface_didatica_menu
from Interface_didatica_menu_botoes_botoeira import Ui_interface_didatica_menu_botoes
from Interface_didatica_finalidade import Ui_interface_didatica_finalidade
from Interface_didatica_menu_botao_emergencia import Ui_interface_didatica_menu_botao_emergencia
from Registros_menu import Ui_Registros_menu
from Cadastros_menu import Ui_cadastros_menu
from Cadastros_menu_adicionar import Ui_cadastros_classes
from Cadastros_adicionar_ficha01 import Ui_cadastros_adicionar_ficha01
from Usuario_registrado import Ui_Usuario_registrado
from Editar_cadastro import Ui_Editar_cadastro
from aproxime_cracha import Ui_Aproxime_cartao
from Registros_historico_utilizacao import Ui_cadastros_historico_utilizacao
from standby import Ui_Standby

colaborador = "Dorigon"  # cursor.execute("SELECT Nome FROM Dados WHERE ID = 2")
# banco.commit()
edv = "92896201"
verifica = bool

hoje = (date.today())
dataFormatada = hoje.strftime('%d/%m/%Y')
print(dataFormatada)


class Connection:

    # Construtor da class faz a conexão
    def __init__(self, db):
        self.banco = sqlite3.connect(db)

    # Veriica se o usuario esta no banco de dados
    def pesquisar_colaborador(self, idcard):
        cursor = self.banco.cursor()
        # função do SQL de seleção de dados
        consulta = f"SELECT Nome,ID_Usuario, EDV FROM Usuarios WHERE ID_Card ='{int(idcard)}'"
        cursor.execute(consulta)
        nome = cursor.fetchall()

        cursor.close()
        print(nome)
        print(nome[0])
        return nome[0]

    def coleta_dados(self):  # Retorna o Nome, EDV e a Classe para criar a tabela da tela cadastros_menu
        cursor = self.banco.cursor()
        consulta = ("SELECT Nome, EDV, Classe FROM Usuarios")
        cursor.execute(consulta)
        lista = cursor.fetchall()
        cursor.close()
        print("lista:", lista)
        return lista

    def ID_User(self, edv):  # Estou usando essa função por enquanto
        cursor = self.banco.cursor()
        consulta = f"SELECT ID_Usuario FROM Usuarios WHERE EDV ='{str(edv)}'"
        cursor.execute(consulta)
        ID_user = cursor.fetchone()
        cursor.close()
        print(ID_user)
        return ID_user[0]

    def adicionar_cadastro(self, tag_cartao, nome, edv, classe, data_nascimento):
        cursor = self.banco.cursor()
        adicionar = (
                    "INSERT INTO Usuarios (ID_Card, Nome, Classe, EDV, Data_Nascimento)  VALUES ('" + tag_cartao + "','" + nome + "','" + classe + "','" + edv + "','" + data_nascimento + "')")  # inserir Dados
        cursor.execute(adicionar)
        self.banco.commit()
        cursor.close()
        return print("Adicionado")

    def atualizar_cadastro(self, nome, data_nascimento, edv, ID):
        cursor = self.banco.cursor()
        adicionar = f"UPDATE Usuarios SET Nome = '{nome}' , Data_Nascimento= {data_nascimento} , EDV= {edv}   WHERE ID_Usuario = {ID}; "  # inserir Dados
        cursor.execute(adicionar)
        self.banco.commit()
        cursor.close()
        return print("Atualizado")

    def Data_nascimento(self, ID):  # Estou usando essa função por enquanto
        cursor = self.banco.cursor()
        consulta = f"SELECT Data_Nascimento FROM Usuarios WHERE ID_Usuario ='{ID}'"
        cursor.execute(consulta)
        Data_Nascimento = cursor.fetchone()
        cursor.close()
        print(Data_Nascimento)
        return Data_Nascimento[0]

    def update_tag(self, tag, ID):
        cursor = self.banco.cursor()
        tag = f"UPDATE Usuarios SET Nome = '{tag}' WHERE ID_Usuario = {ID}; "  # inserir Dados
        cursor.execute(tag)
        self.banco.commit()
        cursor.close()
        return print("Tag_Atualizada")


class Standby(QMainWindow, Ui_Standby):  # primeira tela que faz a validação da tag do crachá
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.lineEdit_tag.setFocus()
        self.lineEdit_tag.returnPressed.connect(self.comeca)
        self.lineEdit_tag.setText("")
        self.botao_imagem.clicked.connect(self.mousePressEvent)
        #self.label_titulo.pressed.connect(self.comeca)
        # self.centralwidget.mouseReleaseEvent = lambda event: self.clica

    def mousePressEvent(self, e):
        self.lineEdit_tag.setFocus()
        print("Cliquei")

    def comeca(self):
        self.tag_cartao = self.lineEdit_tag.text()
        try:
            self.colaborador = banco_dados.pesquisar_colaborador(self.tag_cartao)[0]
            self.colaborador2 = self.colaborador.split(" ")
            self.configurar()

        except:
            self.lineEdit_tag.setFocus()
            self.lineEdit_tag.setText("")
            self.label_titulo.setText("ERRO DE LEITURA\nTENTE NOVAMENTE")
            print("Cliquei")
            pass

    def configurar(self):
        Menu01.Label_Colaborador.setText(f'COLABORADOR: {self.colaborador2[0]} {self.colaborador2[-1]}')
        Menu01.Label_EDV.setText(f"EDV: {banco_dados.pesquisar_colaborador(self.tag_cartao)[-1]}")
        Menu02.Label_Colaborador.setText(f'COLABORADOR: {self.colaborador2[0]} {self.colaborador2[-1]}')
        Menu02.Label_EDV.setText(f"EDV: {banco_dados.pesquisar_colaborador(self.tag_cartao)[-1]}")
        print("Passei por aqui")
        Menu01.show()
        standby.hide()


##################### MENU 01 ################################
class Primeiro_Menu(QMainWindow, Ui_Menu01):
    def __init__(self):  # FUNÇÃO QUE INICIA A TELA E DECLARA OS BOTÕES,LABELS,ETC.
        super().__init__()  # COMANDO PARA INICIAR A TELA.
        super().setupUi(self)  # COMANDO PARA INICIAR A TELA.
        self.maquina_liberada = False
        self.Botao_Seta_Direita.clicked.connect(
            self.proxima_tela)  # DEFINE A FUNÇÃO QUE SERÁ CHAMADA QUANDO A SETA P/ DIREITA FOR CLICADA.
        self.Botao_Liberar_Maquina.clicked.connect(
            self.liberacao_de_maquina)  # DEFINE A FUNÇÃO QUE SERÁ CHAMADA QUANDO O BOTÃO DE LIBERAR A MÁQUINA FOR CLICADO.
        self.Botao_Interface_Didatica.clicked.connect(self.interface_didatica)
        self.Botao_Documentos.clicked.connect(
            self.menu_documentos)  # DEFINE A FUNÇÃO QUE SERÁ CHAMADA QUANDO O BOTÃO DE DOCUMENTOS FOR CLICADO.
        self.Botao_Registros.clicked.connect(self.menu_registros)
        self.Label_Colaborador.setText(f"COLABORADOR: {colaborador}")  # DEFINE A LABEL COM O NOME DO COLABORADOR.
        self.Label_EDV.setText(f"EDV: {edv}")  # DEFINE A LABEL COM O EDV DO COLABORADOR.

    def proxima_tela(self):  # FUNÇÃO QUE CHAMA O MENU 02.
        Menu02.show()
        Menu01.hide()

    def liberacao_de_maquina(self):  # FUNÇÃO QUE INICIA O PROCESSO DE LIBERAÇÃO DE MÁQUINA.
        if self.maquina_liberada == False:
            aviso_liberacao.label_texto.setText(
                "<html><head/><body><p align=\"center\">O(s) seguinte(s) item(s) de Segurança não foram </p><p align=\"center\">marcado(s), o que significa que ele(s) apresenta(m) </p><p align=\"center\">não conformidade:</p></body></html>")
            liberacao_atencao.show()
            Menu01.hide()

        else:
            print("Oiiiii")

    def menu_documentos(self):  # FUNÇÃO QUE CHAMA A TELA DE MENU DE DOCUMENTOS
        documentos_menu.show()
        Menu01.hide()

    def interface_didatica(self):  # FUNÇÃO QUE CHAMA A TELA DE MENU DE INTERFACE DIDÁTICA
        interface_menu.show()
        Menu01.hide()

    def menu_registros(self):  # FUNÇÃO QUE CHAMA A TELA DE MENU DE REGISTROS
        registros_menu.show()
        Menu01.hide()


class Segundo_Menu(QMainWindow, Ui_Menu02):  # SEGUNDO MENU
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.Botao_Seta_Esquerda.clicked.connect(self.tela_anterior)
        self.Botao_Cadastros.clicked.connect(self.cadastros)
        self.Botao_Sair.clicked.connect(self.sair)
        self.cadeado_fechado = QIcon("imagens/CADEADO_FECHADO.png")

        self.Label_Colaborador.setText(f"COLABORADOR: {colaborador}")
        self.Label_EDV.setText(f"EDV: {edv}")

    def tela_anterior(self):
        print(colaborador)
        Menu01.show()
        Menu02.hide()

    def cadastros(self):
        cadastros_menu.load_tabela()
        cadastros_menu.show()
        Menu02.hide()

    def sair(self):
        # standby.mousePressEvent.connect(standby.mousePressEvent())

        Menu01.maquina_liberada = False
        self.clear_checkboxes()
        standby.lineEdit_tag.setText("")
        standby.label_titulo.setText("APROXIME O CRACHÁ\nSOBRE O LEITOR")
        """""  
        GPIO.output(Alimentacao_maquina, False) 
        GPIO.output(led, True)   
        """""
        standby.show()
        Menu02.hide()

    def clear_checkboxes(self):
        Menu01.maquina_liberada = False
        self.checkboxes = [liberacao_seguranca.checkBox_1, liberacao_seguranca.checkBox_2,
                           liberacao_seguranca.checkBox_3,
                           liberacao_seguranca.checkBox_4, liberacao_seguranca.checkBox_5,
                           liberacao_seguranca.checkBox_6,
                           liberacao_seguranca.checkBox_7, liberacao_seguranca.checkBox_8,
                           liberacao_seguranca.checkBox_9,
                           liberacao_meio_ambiente.checkBox_1]
        for i in self.checkboxes:
            i.setChecked(False)
        Menu01.Botao_Liberar_Maquina.setIcon(self.cadeado_fechado)


class Liberacao_atencao(QMainWindow, Ui_Atencao):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_continuar.clicked.connect(self.tela_de_seguranca)
        self.botao_home.clicked.connect(self.home)

    def tela_de_seguranca(self):
        liberacao_seguranca.show()
        liberacao_atencao.hide()

    def home(self):
        Menu01.show()
        liberacao_atencao.hide()


class Liberacao_seguranca(QMainWindow, Ui_Liberacao_Seguranca):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)
        self.botao_continuar.clicked.connect(self.tela_meio_ambiente)

        self.checkBox_1.clicked.connect(self.item01)
        self.checkBox_2.clicked.connect(self.item02)
        self.checkBox_3.clicked.connect(self.item03)
        self.checkBox_4.clicked.connect(self.item04)
        self.checkBox_5.clicked.connect(self.item05)
        self.checkBox_6.clicked.connect(self.item06)
        self.checkBox_7.clicked.connect(self.item07)
        self.checkBox_8.clicked.connect(self.item08)
        self.checkBox_9.clicked.connect(self.item09)
        self.allcheckBox = [self.checkBox_1, self.checkBox_2, self.checkBox_3, self.checkBox_4, self.checkBox_5,
                            self.checkBox_6, self.checkBox_7, self.checkBox_8, self.checkBox_9]

        self.lista_real = []
        self.lista_erros = []
        self.texto = []
        self.contador = 0

    def verifica_checkBox(self):

        for i in self.allcheckBox:
            if i.isChecked():
                self.contador = self.contador + 1
                self.lista_real.append(self.contador)

            else:
                self.lista_real.remove(self.contador)

    def home(self):

        Menu01.show()
        liberacao_seguranca.hide()

    def item01(self):
        if self.checkBox_1.isChecked():
            self.lista_real.append(1)

        else:
            self.lista_real.remove(1)

    def item02(self):
        if self.checkBox_2.isChecked():
            self.lista_real.append(2)

        else:
            self.lista_real.remove(2)

    def item03(self):
        if self.checkBox_3.isChecked():
            self.lista_real.append(3)

        else:
            self.lista_real.remove(3)

    def item04(self):
        if self.checkBox_4.isChecked():
            self.lista_real.append(4)

        else:
            self.lista_real.remove(4)

    def item05(self):
        if self.checkBox_5.isChecked():
            self.lista_real.append(5)

        else:
            self.lista_real.remove(5)

    def item06(self):
        if self.checkBox_6.isChecked():
            self.lista_real.append(6)

        else:
            self.lista_real.remove(6)

    def item07(self):
        if self.checkBox_7.isChecked():
            self.lista_real.append(7)

        else:
            self.lista_real.remove(7)

    def item08(self):
        if self.checkBox_8.isChecked():
            self.lista_real.append(8)

        else:
            self.lista_real.remove(8)

    def item09(self):
        if self.checkBox_9.isChecked():
            self.lista_real.append(9)

        else:
            self.lista_real.remove(9)

    def resposta(self):
        for i in range(1, 10):
            if i not in self.lista_real:
                self.lista_erros.append(i)

        if len(self.lista_erros) != 0:
            self.texto = str(self.lista_erros)
            return False

        else:
            return True

    def tela_meio_ambiente(self):
        if self.resposta() == True:
            aviso_liberacao.seguranca = True
            liberacao_meio_ambiente.show()
            liberacao_seguranca.hide()


        else:
            aviso_liberacao.label_itens_desmarcados.setText(f"<html><head/><body><p align=\"center\">{self.texto}")
            aviso_liberacao.seguranca = False
            aviso_liberacao.show()
            liberacao_seguranca.hide()


class Aviso_liberacao(QMainWindow, Ui_Aviso_Liberacao):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.seguranca = False
        self.botao_voltar.clicked.connect(self.voltar_check_list)
        self.botao_relatar_problema.clicked.connect(self.boletim)

    def voltar_check_list(self):

        if self.seguranca == False:
            liberacao_seguranca.lista_erros = []
            liberacao_seguranca.show()
            aviso_liberacao.hide()


        else:
            liberacao_meio_ambiente.show()
            aviso_liberacao.hide()

    def boletim(self):
        print("Agora só falta a tela")


class Liberacao_meio_ambiente(QMainWindow, Ui_Liberacao_Meio_Ambiente):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)
        self.botao_continuar.clicked.connect(self.resposta)
        self.img2 = QIcon("imagens/CADEADO_ABERTO.png")

    def home(self):
        Menu01.show()
        liberacao_meio_ambiente.hide()

    def resposta(self):
        if self.checkBox_1.isChecked():
            Menu01.maquina_liberada = True
            """""                                  
            GPIO.output(Alimentacao_maquina, True)
            GPIO.output(led, True)                 
            """""
            Menu01.Botao_Liberar_Maquina.setIcon(self.img2)
            Menu01.show()
            liberacao_meio_ambiente.hide()

        else:
            aviso_liberacao.label_texto.setText(
                "<html><head/><body><p align=\"center\">O(s) seguinte(s) item(s) de Meio Ambiente não foram </p><p align=\"center\"> marcado(s), o que significa que ele(s) apresenta(m)</p><p align=\"center\"> não conformidade:</p></body></html>")
            aviso_liberacao.label_itens_desmarcados.setText(f"<html><head/><body><p align=\"center\">1")
            aviso_liberacao.show()
            liberacao_meio_ambiente.hide()


class Documentos_menu(QMainWindow, Ui_documentos_menu):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)
        self.botao_documentos_de_pecas01.clicked.connect(self.documentos_de_pecas)
        self.botao_documentos_de_pecas02.clicked.connect(self.documentos_de_pecas)
        self.botao_diagrama_eletrico01.clicked.connect(self.diagrama_eletrico)
        self.botao_diagrama_eletrico02.clicked.connect(self.diagrama_eletrico)
        self.botao_mae01.clicked.connect(self.mapa_de_riscos)
        self.botao_mae02.clicked.connect(self.mapa_de_riscos)

    def home(self):
        Menu01.show()
        documentos_menu.hide()

    def documentos_de_pecas(self):
        documentos_de_pecas_menu.show()
        documentos_menu.hide()

    def diagrama_eletrico(self):
        diagrama_eletrico.show()
        documentos_menu.hide()

    def mapa_de_riscos(self):
        mapa_de_riscos.show()
        documentos_menu.hide()


class Documentos_documentos_de_pecas_menu(QMainWindow, Ui_documentos_documentos_de_pecas_menu):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)
        self.botao_peca01_1.clicked.connect(self.peca01)
        self.botao_peca01_2.clicked.connect(self.peca01)
        self.botao_peca02_1.clicked.connect(self.peca02)
        self.botao_peca02_2.clicked.connect(self.peca02)
        self.botao_peca03_1.clicked.connect(self.peca03)
        self.botao_peca03_2.clicked.connect(self.peca03)

    def home(self):
        documentos_menu.show()
        documentos_de_pecas_menu.hide()

    def peca01(self):
        peca01.show()
        documentos_de_pecas_menu.hide()

    def peca02(self):
        peca02.show()
        documentos_de_pecas_menu.hide()

    def peca03(self):
        peca03.show()
        documentos_de_pecas_menu.hide()


class Documentos_de_peca_peca01(QMainWindow, Ui_peca01):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)

    def home(self):
        documentos_de_pecas_menu.show()
        peca01.hide()


class Documentos_de_peca_peca02(QMainWindow, Ui_peca02):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)

    def home(self):
        documentos_de_pecas_menu.show()
        peca02.hide()


class Documentos_de_peca_peca03(QMainWindow, Ui_peca03):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)

    def home(self):
        documentos_de_pecas_menu.show()
        peca03.hide()


class diagrama_eletrico(QMainWindow, Ui_documentos_diagrama_eletrico):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        self.contador = 1

        self.botao_home.clicked.connect(self.home)
        self.botao_seta_direita.clicked.connect(self.proxima_pagina)
        self.botao_seta_esquerda.clicked.connect(self.pagina_anterior)

        self.pagina1 = QPixmap("imagens/cachorro.png")
        self.pagina2 = QPixmap("imagens/jacare.png")
        self.pagina3 = QPixmap("imagens/MANUTENCAO.png")
        self.label_imagem.setPixmap(self.pagina1)

        if self.botao_seta_esquerda.clicked:
            print("oi")

    def home(self):
        documentos_menu.show()
        diagrama_eletrico.hide()

    def proxima_pagina(self):
        if self.contador < 3:
            self.contador += 1

        if self.contador == 2:
            self.label_imagem.setPixmap(self.pagina2)
            self.label_paginas.setText("PÁGINA 02/03")

        if self.contador == 3:
            self.label_imagem.setPixmap(self.pagina3)
            self.label_paginas.setText("PÁGINA 03/03")

    def pagina_anterior(self):
        if self.contador > 1:
            self.contador -= 1

        if self.contador == 1:
            self.label_imagem.setPixmap(self.pagina1)
            self.label_paginas.setText("PÁGINA 01/03")

        if self.contador == 2:
            self.label_imagem.setPixmap(self.pagina2)
            self.label_paginas.setText("PÁGINA 02/03")


class Mapa_de_riscos(QMainWindow, Ui_mapa_de_riscos):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)

    def home(self):
        documentos_menu.show()
        mapa_de_riscos.hide()


class Interface_menu(QMainWindow, Ui_interface_didatica_menu):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_botoes.clicked.connect(self.botoes)
        self.botao_finalidades.clicked.connect(self.finalidade)
        self.botao_home.clicked.connect(self.home)

    def finalidade(self):
        interface_menu_finalidade.show()
        interface_menu.hide()

    def botoes(self):
        interface_menu_botoes.show()
        interface_menu.hide()

    def home(self):
        Menu01.show()
        interface_menu.hide()


class Interface_botoes(QMainWindow, Ui_interface_didatica_menu_botoes):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_1.clicked.connect(self.botao_01)
        self.botao_2.clicked.connect(self.botao_02)
        self.botao_3.clicked.connect(self.botao_03)
        self.botao_4.clicked.connect(self.botao_04)
        self.botao_5.clicked.connect(self.botao_05)
        self.botao_home.clicked.connect(self.home)
        self.botao_seta_dirteita.clicked.connect(self.botao_emergencia)

    def botao_01(self):
        self.label_indicacao.setText("1")
        self.label_titulo.setStyleSheet(
            "border-style: outset;\n" "border-color: rgb(0, 0, 0);\n""border-width:6px;\n""\n""\n""font: 75 30pt \"Bosch Sans Bold\";\n""background-color: rgb(0,0,0);")
        self.label_titulo.setText(
            "<html><head/><body><p align=\"center\"><span style=\" color:#FFC000;\">BOTÃO LIGA A SERRA</span></p></body></html>")
        self.label_caixa_de_texto.setText(
            "             Botão responsável por iniciar o processo de \ncorte do perfil se a porta estiver trancada e a peça \ntravada. \n")

    def botao_02(self):
        self.label_titulo.setStyleSheet(
            "border-style: outset;\n" "border-color: rgb(0, 0, 0);\n""border-width:6px;\n""\n""\n""font: 75 30pt \"Bosch Sans Bold\";\n""background-color: rgb(0,0,0);")
        self.label_indicacao.setText("2")
        self.label_titulo.setText(
            "<html><head/><body><p align=\"center\"><span style=\" color:#FFC000;\">CHAVE SELETORA DE PERFIL 30/45</span></p></body></html>")
        self.label_caixa_de_texto.setText(
            "             Chave seletora responsável por definir se o \nperfil a ser cortado é de 30 ou 45 para estabelecer a \ndistância que a serra deverá cortar para ultrapassar o \nperfil de 30/45 completamente.")

    def botao_03(self):
        self.label_indicacao.setText("3")
        self.label_titulo.setStyleSheet(
            "border-style: outset;\n" "border-color: rgb(0, 0, 0);\n""border-width:6px;\n""\n""\n""font: 75 28pt \"Bosch Sans Bold\";\n""background-color: rgb(0,0,0);")
        self.label_titulo.setText(
            "<html><head/><body><p align=\"center\"><span style=\" color:#FFC000;\">CHAVE SELETORA DE PORTA TRANCADA</span></p></body></html>")
        self.label_caixa_de_texto.setText(
            "             Chave seletora responsável por garantir o \ntravamento da porta.\n\n")

    def botao_04(self):
        self.label_indicacao.setText("4")
        self.label_titulo.setStyleSheet(
            "border-style: outset;\n" "border-color: rgb(0, 0, 0);\n""border-width:6px;\n""\n""\n""font: 75 30pt \"Bosch Sans Bold\";\n""background-color: rgb(0,0,0);")
        self.label_titulo.setText(
            "<html><head/><body><p align=\"center\"><span style=\" color:#FFC000;\">BOTÃO PARA TRAVAR PEÇA</span></p></body></html>")
        self.label_caixa_de_texto.setText(
            "             Ao pressionar o botão, dois pistões pneumáticos \ntravam a peça na posição estabelecida pelo usuário.\n\n")

    def botao_05(self):
        self.label_indicacao.setText("5")
        self.label_titulo.setStyleSheet(
            "border-style: outset;\n" "border-color: rgb(0, 0, 0);\n""border-width:6px;\n""\n""\n""font: 75 30pt \"Bosch Sans Bold\";\n""background-color: rgb(0,0,0);")
        self.label_titulo.setText(
            "<html><head/><body><p align=\"center\"><span style=\" color:#FFC000;\">BOTÃO RESET</span></p></body></html>")
        self.label_caixa_de_texto.setText(
            "             Botão necessário para reiniciar os processos da \nmáquina caso ocorra alguma falha, como a tentativa de \nabrir as portas de segurança durante a operação, ou ao \npressionar o botão de emergência.")

    def botao_emergencia(self):
        interface_menu_botao_emergencia.show()
        interface_menu_botoes.hide()

    def home(self):
        interface_menu.show()
        interface_menu_botoes.hide()


class Interface_botao_emergencia(QMainWindow, Ui_interface_didatica_menu_botao_emergencia):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)
        self.botao_seta_esquerda.clicked.connect(self.botoeira)

    def home(self):
        interface_menu.show()
        interface_menu_botao_emergencia.hide()

    def botoeira(self):
        interface_menu_botoes.show()
        interface_menu_botao_emergencia.hide()


class Interface_finalidade(QMainWindow, Ui_interface_didatica_finalidade):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)

    def home(self):
        interface_menu.show()
        interface_menu_finalidade.hide()


class Registros_menu(QMainWindow, Ui_Registros_menu):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)
        self.botao_historico_utilizacao_01.clicked.connect(self.caderno_verde)
        self.botao_historico_utilizacao_02.clicked.connect(self.caderno_verde)

    def home(self):
        Menu01.show()
        registros_menu.hide()

    def caderno_verde(self):
        registro_historico_utilizacao.show()
        registros_menu.hide()


class Cadastros_menu(QMainWindow, Ui_cadastros_menu):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        self.imagem_aprendiz2 = QPixmap("imagens\Aprendiz_03.png")
        self.imagem_meio_oficial2 = QPixmap("imagens\Meio_oficial_03.png")
        self.imagem_manutentor2 = QPixmap("imagens\Manutentor_03.png")
        self.imagem_responsavel2 = QPixmap("imagens\Responsavel_03.png")

        self.nome = ""
        self.edv = ""
        self.classe = ""

        self.botao_voltar.clicked.connect(self.home)
        self.botao_adicionar.clicked.connect(self.escolher_classe)
        self.botao_editar.clicked.connect(self.editar)
        self.load_tabela()

    def editar(self):
        self.load_tabela()

        try:
            index = (self.tabela.selectionModel().currentIndex())
            print(index)
            value = index.sibling(index.row(), index.column()).data()
            print(value)

            row = self.tabela.currentItem().row()
            print("row=", row)
            col = self.tabela.currentItem().column()
            print("col=", col)
            item = self.tabela.horizontalHeaderItem(col).text()
            print("item=", item)

            value_02 = index.sibling(row + 1, index.column()).data()
            print(value_02)

            self.nome = index.sibling(row, 0).data()
            self.edv = index.sibling(row, 1).data()
            self.classe = index.sibling(row, 2).data()
            self.ID = str(banco_dados.ID_User(self.edv))
            self.Data_Nasciento = banco_dados.Data_nascimento(self.ID)

            print(self.nome)
            print(self.edv)
            print(self.classe)
            print(self.ID)
            print(self.Data_Nasciento)

            self.ficha()

        except:
            pass

    def ficha(self):
        if self.classe == "Aprendiz":
            cadastros_menu_editar.label_imagem_patente.setPixmap(self.imagem_aprendiz2)

        if self.classe == "Meio Oficial":
            cadastros_menu_editar.label_imagem_patente.setPixmap(self.imagem_meio_oficial2)

        if self.classe == "Responsável":
            cadastros_menu_editar.label_imagem_patente.setPixmap(self.imagem_responsavel2)

        if self.classe == "Manutentor":
            cadastros_menu_editar.label_imagem_patente.setPixmap(self.imagem_manutentor2)

        cadastros_menu_editar.lineEdit_nome.setText(self.nome)
        cadastros_menu_editar.lineEdit_edv.setText(self.edv)
        cadastros_menu_editar.lineEdit_data_nascimento.setText(str(self.Data_Nasciento))

        cadastros_menu_editar.show()
        cadastros_menu.hide()

        print("Nãooo")

    def load_tabela(self):

        self.tabela.setColumnCount(3)
        self.tabela.setColumnWidth(0, 480)
        self.tabela.setColumnWidth(1, 150)
        self.tabela.setColumnWidth(2, 200)

        self.tabela.setHorizontalHeaderLabels(["NOME", "EDV", "CLASSE"])
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectRows)
        lista = banco_dados.coleta_dados()

        self.tabela.setRowCount(len(lista))
        row = 0

        for x in lista:
            self.tabela.setItem(row, 0, QTableWidgetItem((x[0])))
            self.tabela.setItem(row, 1, QTableWidgetItem((str(x[1]))))
            self.tabela.setItem(row, 2, QTableWidgetItem((x[2])))

            row = row + 1

        # https://www.youtube.com/watch?v=YySB6tkjZ7Y
        # https://www.youtube.com/watch?v=xL2NdSubiNY

    def escolher_classe(self):
        cadastros_menu_adicionar.show()
        cadastros_menu.hide()

    def home(self):
        Menu02.show()
        cadastros_menu.hide()


class Cadastros_menu_editar(QMainWindow, Ui_Editar_cadastro):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_cancelar.clicked.connect(self.home)
        self.botao_alterar_tag_cartao.clicked.connect(self.leitor)
        self.botao_atualizar.clicked.connect(self.atualizar)

        self.lineEdit_nome.setText("")
        self.lineEdit_data_nascimento.setText("")
        self.lineEdit_edv.setText("")
        self.lineEdit_nome.setPlaceholderText("NOME COMPLETO")
        self.lineEdit_edv.setPlaceholderText("EDV")
        self.lineEdit_data_nascimento.setPlaceholderText("DATA DE NASCIMENTO")

    def leitor(self):
        cadastros_menu.ficha()
        cadastros_menu_leitor.opcao = False
        cadastros_menu_leitor.show()
        cadastros_menu_editar.hide()

    def home(self):
        cadastros_menu.show()
        cadastros_menu_editar.hide()

    def atualizar(self):
        self.nome = self.lineEdit_nome.text()
        self.data_nascimento = self.lineEdit_data_nascimento.text()
        self.edv = self.lineEdit_edv.text()
        #self.data = datetime.strptime(f'{self.data_nascimento}', '%d/%m/%Y').date()
        #print(self.data, type(self.data))
        #self.dataFormatada = self.data.strftime('%d/%m/%Y')
        #print(self.dataFormatada, type(self.dataFormatada))
        banco_dados.atualizar_cadastro(self.nome, self.data_nascimento, self.edv, cadastros_menu.ID)


class Cadastros_menu_leitor(QMainWindow, Ui_Aproxime_cartao):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.adicionar = bool
        self.lineEdit_tag_cartao.setText("")
        self.lineEdit_tag_cartao.setFocus()
        self.botao_cancelar.clicked.connect(self.voltar)
        self.botao_registrar.clicked.connect(self.registrar)
        self.tag_cartao = " "

    def voltar(self):
        if self.adicionar == True:
            cadastros_menu_adicionar_ficha_01.show()
            cadastros_menu_leitor.hide()

        else:
            cadastros_menu_editar.show()
            cadastros_menu_leitor.hide()

    def registrar(self):
        self.tag_cartao = self.lineEdit_tag_cartao.text()
        print(self.adicionar)

        if not self.tag_cartao == "":
            if self.adicionar == True:
                print(self.tag_cartao, cadastros_menu_adicionar_ficha_01.nome, cadastros_menu_adicionar_ficha_01.classe, cadastros_menu_adicionar_ficha_01.edv, cadastros_menu_adicionar_ficha_01.data_nascimento )
                #banco_dados.adicionar_cadastro(self.tag_cartao, cadastros_menu_adicionar_ficha_01.nome, cadastros_menu_adicionar_ficha_01.edv, cadastros_menu_adicionar_ficha_01.classe, cadastros_menu_adicionar_ficha_01.data_nascimento)
                usuario_registrado.show()
                # AQUI FALTA O DELAY ENTRE AS TELAS
                cadastros_menu.show()
                self.lineEdit_tag_cartao.setText("")
                cadastros_menu_adicionar_ficha_01.lineEdit_edv.setText("")
                cadastros_menu_adicionar_ficha_01.lineEdit_nome.setText("")
                cadastros_menu_adicionar_ficha_01.lineEdit_data_nascimento.setText("")
                usuario_registrado.hide()
                cadastros_menu_leitor.hide()
                cadastros_menu.load_tabela()
                self.lineEdit_tag_cartao.setFocus()

            else:
                self.lineEdit_tag_cartao.setFocus()
                banco_dados.update_tag(self.tag_cartao, )

        else:
            print("Tente novamente")




class Cadastros_menu_adicionar(QMainWindow, Ui_cadastros_classes):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_voltar.clicked.connect(self.home)
        self.botao_aprendiz.clicked.connect(self.aprendiz)
        self.botao_meio_oficial.clicked.connect(self.meio_oficial)
        self.botao_manutentor.clicked.connect(self.manutentor)
        self.botao_responsavel.clicked.connect(self.responsavel)
        self.imagem_aprendiz = QPixmap("imagens\Aprendiz_02.png")
        self.imagem_meio_oficial = QPixmap("imagens\Meio_oficial_02.png")
        self.imagem_manutentor = QPixmap("imagens\Manutentor_02.png")
        self.imagem_responsavel = QPixmap("imagens\Responsavel_02.png")

    def aprendiz(self):
        cadastros_menu_adicionar_ficha_01.classe = "Aprendiz"
        cadastros_menu_adicionar_ficha_01.label_imagem_classe.setPixmap(self.imagem_aprendiz)
        cadastros_menu_adicionar_ficha_01.show()
        cadastros_menu_adicionar.hide()

    def meio_oficial(self):
        cadastros_menu_adicionar_ficha_01.classe = "Meio-Oficial"
        cadastros_menu_adicionar_ficha_01.label_imagem_classe.setPixmap(self.imagem_meio_oficial)
        cadastros_menu_adicionar_ficha_01.show()
        cadastros_menu_adicionar.hide()

    def manutentor(self):
        cadastros_menu_adicionar_ficha_01.classe = "Manutentor"
        cadastros_menu_adicionar_ficha_01.label_imagem_classe.setPixmap(self.imagem_manutentor)
        cadastros_menu_adicionar_ficha_01.show()
        cadastros_menu_adicionar.hide()

    def responsavel(self):
        cadastros_menu_adicionar_ficha_01.classe = "Responsável"
        cadastros_menu_adicionar_ficha_01.label_imagem_classe.setPixmap(self.imagem_responsavel)
        cadastros_menu_adicionar_ficha_01.show()
        cadastros_menu_adicionar.hide()

    def home(self):
        cadastros_menu.show()
        cadastros_menu_adicionar.hide()


class Cadastros_menu_adicionar_ficha01(QMainWindow, Ui_cadastros_adicionar_ficha01):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        self.botao_cancelar.clicked.connect(self.home)
        self.botao_avancar.clicked.connect(self.cadastro01)
        self.classe = " "
        self.data_nascimento = " "
        self.edv = " "
        self.nome = " "

        self.lineEdit_nome.setText("")
        self.lineEdit_data_nascimento.setText("")
        self.lineEdit_edv.setText("")
        self.lineEdit_nome.setPlaceholderText("NOME COMPLETO")
        self.lineEdit_edv.setPlaceholderText("EDV")
        self.lineEdit_data_nascimento.setPlaceholderText("DATA DE NASCIMENTO")

    def cadastro01(self):
        self.nome = self.lineEdit_nome.text()
        self.edv = str(self.lineEdit_edv.text())
        self.data_nascimento = self.lineEdit_data_nascimento.text()

        if (self.nome == "") or (self.edv == "") or (self.data_nascimento == ""):
            print("Tente novamente")

        else:

            cadastros_menu_leitor.opcao = True
            print(self.nome)
            print(self.edv)
            print(self.classe)
            cadastros_menu_leitor.show()
            cadastros_menu_adicionar_ficha_01.hide()

    def home(self):
        cadastros_menu_adicionar.show()
        cadastros_menu_adicionar_ficha_01.hide()


class Usuario_registrado(QMainWindow, Ui_Usuario_registrado):
    def __init__(self):
        super().__init__()
        super().setupUi(self)


class Registro_historico_utilizacao(QMainWindow, Ui_cadastros_historico_utilizacao):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_voltar.clicked.connect(self.voltar)

        self.tabela_utilizacao.setColumnCount(5)
        self.tabela_utilizacao.setColumnWidth(0, 150)
        self.tabela_utilizacao.setColumnWidth(1, 150)
        self.tabela_utilizacao.setColumnWidth(2, 200)
        self.tabela_utilizacao.setColumnWidth(3, 200)
        self.tabela_utilizacao.setColumnWidth(4, 200)

        # row = 0

        # self.tabela_utilizacao.setItem(row, 0, QTableWidgetItem(0,str(self.hoje)))

        self.tabela_utilizacao.setHorizontalHeaderLabels(["DATA", "HORA", "EXAME", "RESULTADO", "EDV"])
        self.tabela_utilizacao.setSelectionBehavior(QAbstractItemView.SelectRows)

    def voltar(self):
        registros_menu.show()
        registro_historico_utilizacao.hide()


ap = QApplication(sys.argv)
ap.setStyle("Fusion")
banco_dados = Connection("Banco.db")
Menu01 = Primeiro_Menu()
liberacao_seguranca = Liberacao_seguranca()
Menu02 = Segundo_Menu()
liberacao_atencao = Liberacao_atencao()
liberacao_meio_ambiente = Liberacao_meio_ambiente()
documentos_menu = Documentos_menu()
documentos_de_pecas_menu = Documentos_documentos_de_pecas_menu()
peca01 = Documentos_de_peca_peca01()
peca02 = Documentos_de_peca_peca02()
peca03 = Documentos_de_peca_peca03()
diagrama_eletrico = diagrama_eletrico()
mapa_de_riscos = Mapa_de_riscos()
aviso_liberacao = Aviso_liberacao()
interface_menu = Interface_menu()
interface_menu_botoes = Interface_botoes()
interface_menu_finalidade = Interface_finalidade()
interface_menu_botao_emergencia = Interface_botao_emergencia()
registros_menu = Registros_menu()
cadastros_menu = Cadastros_menu()
cadastros_menu_editar = Cadastros_menu_editar()
cadastros_menu_leitor = Cadastros_menu_leitor()
cadastros_menu_adicionar = Cadastros_menu_adicionar()
cadastros_menu_adicionar_ficha_01 = Cadastros_menu_adicionar_ficha01()
usuario_registrado = Usuario_registrado()
registro_historico_utilizacao = Registro_historico_utilizacao()

standby = Standby()

# cadastros_menu_leitor.show()
standby.show()
sys.exit(ap.exec())


