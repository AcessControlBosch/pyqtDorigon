################################ IMPORTANDO AS BIBLIOTECAS E FUNÇÕES ################################
import sys
from datetime import datetime, date
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QLabel, QLineEdit, QTableWidget, QAbstractItemView, QTableView
from PyQt5.QtGui import QIcon, QPixmap
#import textwrap

import sqlite3
"""
value = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

wrapper = textwrap.TextWrapper(width=10)
string = wrapper.fill(text=value)

print(string)"""

#LIBERAÇÃO
    #DESENHAR TELA DE RELATAR DEFEITO
    #ARRUMAR NO BANCO O CAMPO DE RELATÓRIO DE DEFEITOS
    #DESENHAR O CADEADO VERMELHO PARA O ESTADO DE MANUTENÇÃO
    #BLOQUEAR O ACESSO DO USUÁRIO SE ESTIVER EM MANUT

#INTERFACE DIDÁTICA
    #ARRUMAR A TELA DE BOTÃO DE EMEREGÊNCIA
    #QUANDO SAIR RESETAR A ESCRITA DOS BOTÕES
    #PEGAR A DEFINIÇÃO DOS BOTÕES SEGUNDO O MANUAL
    #ARRUMAR A TELA DE FINALIDADE
    #FAZER OS VÍDEOS DA PARTE DE MODO DE UTILIZAR

#DOCUMENTOS
    #DESENHAR APENAS UMA TELA PARA AS PEÇAS
    #ESCANEAR O DIAGRAMA ELÉTRICO DA MÁQUINA
    #ESCANEAR O MAPA DE RISCOS

#REGISTROS
    #CRIAR FUNÇÃO PARA FILTRAR A TABELA
    #DEIXAR A TABELA CLICÁVEL PARA ANALISAR

#MANUTENÇÃO:
    #ENERGIZAR PAINEL
    #ARRUMAR ESTADO DE MANUTENÇÃO
    #DELIMITAR ACESSO DO MANUTENTOR
    #CRIAR COMUNICAÇÃO COM O BANCO DE DADOS
        #SETAR ESTADO DE MANUTENÇÃO
        #SETAR SAÍDAS DIGITAIS DA RASPBERRY
        #VERIFICAR NO INÍCIO DO PROGRAMA SE A MÁQUINA ESTÁ EM MANUTENÇÃO
        #INTERDITAR ACESSO IF == TRUE

#CADASTROS
    #ALTERAR A TELA E ADICIONAR A LIXEIRA
    #CRIAR FUNÇÃO DO BD PARA EXCLUIR USUÁRIO

#GERAL
    #DELIMITAR O ACESSO DE MANUTENTOR
    #ADICIONAR AS SAÍDAS DIGITAIS PARA ALTERAR AS LEDS, COMUTAR O CONTATOR E LIBERAR A TRAVA
    #DESENHAR CADEADO VERMELHO E TALVEZ ESCREVER MÁQUINA EM MANUTENÇÃO AO INVES DE MENU OU EM OUTRO LUGAR
    #TERMINAR DE COMENTAR
    #PADRONIZAR A PROGRAMAÇÃO
    #INTEGRAR COM A PROGRAMAÇÃO DO OUTRO GRUPO

################################ IMPORTANDO AS CLASSES DOS ARQUIVOS DE TELAS ################################
from Menu01 import Ui_Menu01
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
from Manutencao import Ui_Manutencao
from Relatos_liberacao import Ui_Relatos_liberacao
################################ DECLARAÇÃO DE PORTAS DA RASPYBERRY E BIBLIOTECAS ################################
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

################################ VARIÁVEIS GLOBAIS ################################
colaborador = "Dorigon"
edv = "92896201"
serra_de_perfil = "1"
maquina_manutencao = False
"""
hoje = date.today()
certo = hoje.strftime("%d/%m/%Y")
now = datetime.now()
inicio = now.strftime("%H:%M %p")"""


################################ CLASSE CONEXÃO COM O BANCO DE DADOS ################################
class Connection:
    def __init__(self, db):
        self.banco = sqlite3.connect(db)


################################ FUNÇÕES DO BANCO DE DADOS ################################

    #Pesquisar Usuário a partir do ID_Card.
    def pesquisar_colaborador(self, idcard):
        cursor = self.banco.cursor()
        consulta = f"SELECT Nome,ID_Usuario, EDV FROM Usuarios WHERE ID_Card ='{int(idcard)}'"
        cursor.execute(consulta)
        nome = cursor.fetchall()
        cursor.close()
        return nome[0]

    #Coleta os usuários cadastrados no BD.
    def tabela_cadastros(self):
        cursor = self.banco.cursor()
        consulta = ("SELECT Nome, EDV, Classe FROM Usuarios")
        cursor.execute(consulta)
        lista = cursor.fetchall()
        cursor.close()
        return lista

    #Pesquisa o ID_User a partir do EDV.
    def ID_User(self, edv):
        cursor = self.banco.cursor()
        consulta = f"SELECT ID_Usuario FROM Usuarios WHERE EDV ='{str(edv)}'"
        cursor.execute(consulta)
        ID_user = cursor.fetchone()
        cursor.close()
        return ID_user[0]

    #Adiciona o novo usuário no BD.
    def adicionar_cadastro(self, tag_cartao, nome, edv, classe, data_nascimento):
        cursor = self.banco.cursor()
        adicionar = ("INSERT INTO Usuarios (ID_Card, Nome, Classe, EDV, Data_Nascimento)  VALUES ('" + tag_cartao + "','" + nome + "','" + classe + "','" + edv + "','" + data_nascimento + "')")  # inserir Dados
        cursor.execute(adicionar)
        self.banco.commit()
        cursor.close()
        return print("Adicionado")

    #Atualiza ficha de usuário.
    def atualizar_cadastro(self, nome, data_nascimento, edv, ID):
        cursor = self.banco.cursor()
        adicionar = f"UPDATE Usuarios SET Nome = '{nome}' , Data_Nascimento= {data_nascimento} , EDV= {edv}   WHERE ID_Usuario = {ID}; "  # inserir Dados
        cursor.execute(adicionar)
        self.banco.commit()
        cursor.close()
        return print("Atualizado")

    #Pesquisa a data de nascimento do Usuário a partir do ID_Usuário.
    def Data_nascimento(self, ID):
        cursor = self.banco.cursor()
        consulta = f"SELECT Data_Nascimento FROM Usuarios WHERE ID_Usuario ='{ID}'"
        cursor.execute(consulta)
        Data_Nascimento = cursor.fetchone()
        cursor.close()
        return Data_Nascimento[0]

    #Atualiza a tag do cartão (ID_Card).
    def update_tag(self, tag, EDV):
        cursor = self.banco.cursor()
        tag = f"UPDATE Usuarios SET ID_Card = '{tag}' WHERE EDV = {EDV}; "
        cursor.execute(tag)
        self.banco.commit()
        cursor.close()
        return print("Tag_Atualizada")

    #Seleciona a classe do usuário a partir do ID_Card.
    def verifica_classe(self, ID):
        cursor = self.banco.cursor()
        consulta = f"SELECT Classe FROM Usuarios WHERE ID_Card ='{ID}' "
        cursor.execute(consulta)
        Classe = cursor.fetchone()
        cursor.close()
        return Classe[0]

    #Altera a classe do usuário a partir do EDV.
    def alterar_classe(self, Classe, EDV):
        cursor = self.banco.cursor()
        Classe = f"UPDATE Usuarios SET Classe = '{Classe}' WHERE EDV = {EDV}; "
        cursor.execute(Classe)
        self.banco.commit()
        cursor.close()
        return print("Classe_Atualizada")

    #Registra a liberação de máquina
    def registrar_utilizacao(self, Colaborador, Data, Hora, Exame, EDV, Resultado):
        cursor = self.banco.cursor()
        adicionar = ("INSERT INTO Registros (Colaborador, EDV, DATA, HORA, EXAME, RESULTADO)  VALUES ('" + Colaborador + "','" + Data + "','" + Hora + "','" + Exame + "','" + EDV + "','" + Resultado + "')")  # inserir Dados
        cursor.execute(adicionar)
        ID = cursor.lastrowid
        self.banco.commit()
        cursor.close()
        return str(ID)

    #Coleta todos os registros de utilização
    def chama_registros(self):
        cursor = self.banco.cursor()
        consulta = ("SELECT * FROM Registros")
        cursor.execute(consulta)
        registros = cursor.fetchall()
        cursor.close()
        return registros

    #Registra o horário de saída
    def marcar_horario_saida(self, horario_saida, Registro):
        cursor = self.banco.cursor()
        tag = f"UPDATE Registros SET HORA = '{horario_saida}' WHERE ID_Liberacao = '" + Registro + "'; "
        cursor.execute(tag)
        self.banco.commit()
        cursor.close()
        return print("Hora_Atualizada")

    def Verifica_estado_de_manutencao(self, id_maquina):
        cursor = self.banco.cursor()
        consulta = f"SELECT Manutencao FROM Maquinas WHERE ID_maquina ='{id_maquina}'"
        cursor.execute(consulta)
        estado_manutencao = cursor.fetchone()
        cursor.close()
        return estado_manutencao[0]

    def estado_manutencao(self, bool, maquina):
        cursor = self.banco.cursor()
        alterar = f"UPDATE Maquinas SET Manutencao = '{bool}'  WHERE ID_Maquina = {maquina}; "
        cursor.execute(alterar)
        self.banco.commit()
        cursor.close()
        return print("Atualizado")




################################ TELA DE ENTRADA E STANDBY ################################
#Tela que ocorre a validação do ID_Card do colaborador.
class Standby(QMainWindow, Ui_Standby):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.lineEdit_tag.setFocus()
        self.lineEdit_tag.returnPressed.connect(self.comeca)
        self.lineEdit_tag.setText("")
        self.botao_imagem.clicked.connect(self.mousePressEvent)

    #Função caso clique na tela, ainda garante que a tag seja escrita na lineEdit_tag.
    def mousePressEvent(self, e):
        self.lineEdit_tag.setFocus()

    #Função que é chamada para fazer a verificação da tag do usuário após passar o crachá sobre o leitor/ENTER for pressionado.
    def comeca(self):
        self.tag_cartao = self.lineEdit_tag.text()
        try:
            self.colaborador = banco_dados.pesquisar_colaborador(self.tag_cartao)[0]
            self.colaborador2 = self.colaborador.split(" ")
            self.classe = banco_dados.verifica_classe(self.tag_cartao)
            print(self.classe)
            self.configurar()

        except Exception as erro:
            print(erro)
            self.lineEdit_tag.setFocus()
            self.lineEdit_tag.setText("")
            self.label_titulo.setText("ERRO DE LEITURA\nTENTE NOVAMENTE")

    #Funçao que personaliza o menu com os dados do usuário, Nome, Edv e Classe
    def configurar(self):
        Menu01.Label_Colaborador.setText(f'COLABORADOR: {self.colaborador2[0]} {self.colaborador2[-1]}')
        Menu01.Label_EDV.setText(f"EDV: {banco_dados.pesquisar_colaborador(self.tag_cartao)[-1]}")
        Menu02.Label_Colaborador.setText(f'COLABORADOR: {self.colaborador2[0]} {self.colaborador2[-1]}')
        Menu02.Label_EDV.setText(f"EDV: {banco_dados.pesquisar_colaborador(self.tag_cartao)[-1]}")

        if (self.classe == "Aprendiz") or (self.classe == "Meio Oficial"):
            Menu01.Botao_Seta_Direita.setDisabled(True)
            Menu01.Botao_Seta_Esquerda.setDisabled(True)
            Menu01.Botao_Seta_Direita.setIcon(Menu01.imagem_branca)
            Menu01.Botao_Seta_Esquerda.setIcon(Menu01.imagem_branca)

        if (self.classe == "Responsável") or (self.classe == "Manutentor"):
            Menu01.Botao_Seta_Direita.setDisabled(False)
            Menu01.Botao_Seta_Esquerda.setDisabled(False)
            Menu01.Botao_Seta_Direita.setIcon(Menu01.seta_preta_direita)
            Menu01.Botao_Seta_Esquerda.setIcon(Menu01.seta_branca_esquerda)

        Menu01.show()
        standby.hide()


################################ MENU 01 ################################
#Menu de interface para os usuários.
class Primeiro_Menu(QMainWindow, Ui_Menu01):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.Botao_Seta_Direita.clicked.connect(self.proxima_tela)
        self.Botao_Liberar_Maquina.clicked.connect(self.liberacao_de_maquina)
        self.Botao_Interface_Didatica.clicked.connect(self.interface_didatica_menu)
        self.Botao_Sair.clicked.connect(self.sair)
        self.Botao_Documentos.clicked.connect(self.menu_documentos)
        self.Botao_Registros.clicked.connect(self.menu_registros)

        # ******************************* CONFIGURAÇÕES *******************************

        self.Label_Colaborador.setText(f"COLABORADOR: {colaborador}")
        self.Label_EDV.setText(f"EDV: {edv}")

        # ******************************* VARIÁVEIS *******************************

        self.maquina_liberada = False  #Variável que determina se a máquina está ligada ou não.
        self.imagem_branca = QIcon("imagens/Branco.png")
        self.seta_branca_esquerda = QIcon("imagens/Seta Branca para esquerda.png")
        self.seta_preta_direita = QIcon("imagens/Seta Preta para direita.png")
        self.estado_manutencao = banco_dados.Verifica_estado_de_manutencao(serra_de_perfil)
        print(self.estado_manutencao)


        # ******************************* FUNÇÕES DA CLASSE *******************************

    #Função de Logout.
    def sair(self):
        Menu02.sair()

    #Função que avança para o Menu02.
    def proxima_tela(self):
        Menu02.show()
        Menu01.hide()

    #Função que inicia o processo de liberação de máquina.
    def liberacao_de_maquina(self):
        if maquina_manutencao == False:
            if self.maquina_liberada == False:
                liberacao_atencao.show()
                Menu01.hide()
            else:
                pass
        else:
            pass

    #Função que chama a tela de Menu de Documentos.
    def menu_documentos(self):
        documentos_menu.show()
        Menu01.hide()

    #Função que chama a tela de Interface Didática Menu.
    def interface_didatica_menu(self):
        interface_menu.show()
        Menu01.hide()

    #Função que chama a tela de Menu de Registros.
    def menu_registros(self):
        registros_menu.show()
        Menu01.hide()

################################ TELA DE INSTRUÇÕES PARA LIBERAÇÃO ################################
#Tela de advertência sobre o processo de libreação de máquina.
class Liberacao_atencao(QMainWindow, Ui_Atencao):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_continuar.clicked.connect(self.tela_de_seguranca)
        self.botao_home.clicked.connect(self.home)

        # ******************************* FUNÇÕES DA CLASSE *******************************

    #Função que avança para a Liberação_Segurança.
    def tela_de_seguranca(self):
        liberacao_seguranca.show()
        liberacao_atencao.hide()

    #Função que retorna para o Menu01 (HOME).
    def home(self):
        Menu01.show()
        liberacao_atencao.hide()

################################ TELA DE LIBERAÇÃO DOS REQUISITOS DE SEGURANÇA ################################
#Tela que o usuário verifica os requisitos de segurança.
class Liberacao_seguranca(QMainWindow, Ui_Liberacao_Seguranca):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        #******************************* AÇÕES *******************************

        self.botao_home.clicked.connect(self.home)
        self.botao_continuar.clicked.connect(self.tela_meio_ambiente)
        self.allcheckBox = [self.checkBox_1, self.checkBox_2, self.checkBox_3, self.checkBox_4, self.checkBox_5,
                            self.checkBox_6, self.checkBox_7, self.checkBox_8, self.checkBox_9]

        # ******************************* VARIÁVEIS *******************************
        self.liberacao_seguranca = False
        self.lista_real = [] #Lista de Check_Boxes checados.
        self.lista_erros = [] #Lista de Check_Boxes não checados.
        self.texto = [] #Texto  indicando os Check_boxes não checados.
        self.contador = 0 #Contador auxiliar.
        self.inconformidades = []
        self.item01 = "\nProteções;\n"
        self.item02 = "\nParafusos de Fixação;\n"
        self.item03 = "\nFiação;\n"
        self.item04 = "\nMangueiras;\n"
        self.item05 = "\nBotão de Emergência;\n"
        self.item06 = "\nBotões de Comando;\n"
        self.item07 = "\nChave Geral;\n"
        self.item08 = "\nPainel Elétrico Fechado;\n"
        self.item09 = "\nFixação de Ferramental;\n"
        self.item10 = "\nIsento de vazamento de óleo;\n"

        self.string_da_lista = ""


        # ******************************* FUNÇÕES DA CLASSE *******************************

    #Função que retorna para o Menu01 (HOME)
    def home(self):
        Menu01.show()
        liberacao_seguranca.hide()

    #Função que valida se todos os Check_Boxes estão checados
    def verifica_checkBox(self):
        self.lista_real=[]
        self.contador = 0
        for i in self.allcheckBox:
            if i.isChecked():
                self.contador = self.contador+1
                self.lista_real.append(self.contador)
            else:
                self.contador = self.contador+1

        if 1 not in self.lista_real:
            self.inconformidades.append(self.item01)

        if 2 not in self.lista_real:
            self.inconformidades.append(self.item02)

        if 3 not in self.lista_real:
            self.inconformidades.append(self.item03)

        if 4 not in self.lista_real:
            self.inconformidades.append(self.item04)

        if 5 not in self.lista_real:
            self.inconformidades.append(self.item05)

        if 6 not in self.lista_real:
            self.inconformidades.append(self.item06)

        if 7 not in self.lista_real:
            self.inconformidades.append(self.item07)

        if 8 not in self.lista_real:
            self.inconformidades.append(self.item08)

        if 9 not in self.lista_real:
            self.inconformidades.append(self.item09)



    #Função que verifica os Checkboxes de segurança.
    def verifica_check_boxes_seguranca(self):
        for i in range(1, 10):
            if i not in self.lista_real:
                self.lista_erros.append(i)

        if len(self.lista_erros) != 0:
            self.texto = str(self.lista_erros)
            return False
        else:
            return True

    #Função que passa para a tela de meio-ambiente caso todos os checkboxes de segurança estiverem checados.
    def tela_meio_ambiente(self):
        self.verifica_checkBox()
        if self.verifica_check_boxes_seguranca() == True:
            self.liberacao_seguranca = True
            aviso_liberacao.label_itens_seguranca.setText("OK")

        else:
            aviso_liberacao.label_itens_seguranca.setText(f"<html><head/><body><p align=\"center\">{self.texto}")
            self.liberacao_seguranca = False

        liberacao_meio_ambiente.show()
        liberacao_seguranca.hide()

################################ TELA DE LIBERAÇÃO DOS REQUISITOS DE MEIO-AMBIENTE ################################
#Tela que o usuário verifica os requisitos de meio-ambiente.
class Liberacao_meio_ambiente(QMainWindow, Ui_Liberacao_Meio_Ambiente):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_home.clicked.connect(self.home)
        self.botao_continuar.clicked.connect(self.Verifica_checkboxes)

        # ******************************* VARIÁVEIS *******************************

        self.liberacao_meio_ambiente = False
        self.img2 = QIcon("imagens/CADEADO_ABERTO.png")
        self.cadeado_manutencao = QIcon("imagens/CADEADO_MANUTENCAO.png")

    # ******************************* FUNÇÕES DA CLASSE *******************************

    #Função que retorna para o Menu.
    def home(self):
        Menu01.show()
        liberacao_meio_ambiente.hide()

    #Função que verifica os Chechboxes de meio-ambiente e envia o sinal de uma porta analógica da Raspberry para comutar o contator elétrico caso o status da liberação seja OK.
    #Se a liberação for "Não OK" e o colaborador identificar algum problema na integridade e funcionamento da máquina, abre-se uma ficha para que o incidente seja relatado.
    def Verifica_checkboxes(self):
        if self.checkBox_1.isChecked():
            self.liberacao_meio_ambiente = True
            aviso_liberacao.label_itens_meio_ambiente.setText("OK")

        else:

            liberacao_seguranca.inconformidades.append(liberacao_seguranca.item10)

            self.liberacao_meio_ambiente = False
            aviso_liberacao.label_itens_meio_ambiente.setText(f"<html><head/><body><p align=\"center\">1")


        if self.checkBox_1.isChecked() and (liberacao_seguranca.liberacao_seguranca == True):
            Menu01.maquina_liberada = True
            """""                                  
            GPIO.output(Alimentacao_maquina, True)
            GPIO.output(led, True)                 
            """""
            Menu01.Botao_Liberar_Maquina.setIcon(self.img2)

            self.colaborador = f"{standby.colaborador2[0]} {standby.colaborador2[-1]}"
            self.hoje = date.today()
            self.hoje_formatado = self.hoje.strftime("%d/%m/%Y")
            self.now = datetime.now()
            self.horario_liberacao = self.now.strftime("%H:%M")
            self.exames = "A,B"
            self.edv = str(banco_dados.pesquisar_colaborador(standby.tag_cartao)[-1])
            self.resultado = "OK"

            try:
                self.ID_Liberacao = banco_dados.registrar_utilizacao(self.colaborador, self.edv, self.hoje_formatado, self.horario_liberacao, self.exames, self.resultado)
                print(type(self.ID_Liberacao), self.ID_Liberacao)
            except Exception as erro:
                print(f"{erro} AQUI02")

            Menu01.show()
            liberacao_meio_ambiente.hide()

        else:
            aviso_liberacao.show()
            liberacao_meio_ambiente.hide()


################################ TELA DE AVISO ################################
#Tela que adverte o colaborador de que alguns Checkboxes ficaram deschecados, caso seja engano ele pode voltar, e se caso for algum incidente procede para a tela de Relatos de Incidentes.
class Aviso_liberacao(QMainWindow, Ui_Aviso_Liberacao):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_voltar.clicked.connect(self.voltar_check_list)
        self.botao_relatar_problema.clicked.connect(self.relatos_liberacao)

    # ******************************* FUNÇÕES DA CLASSE *******************************

    #Função que retorna para os Checkboxes da respectiva tela de liberação.
    def voltar_check_list(self):
        if liberacao_seguranca.liberacao_seguranca == False:
            liberacao_seguranca.lista_erros = []
            relatos_liberacao.label_itens_nao_conformes.clear()
            liberacao_seguranca.string_da_lista = " "
            liberacao_seguranca.inconformidades.clear()

            liberacao_seguranca.show()
            aviso_liberacao.hide()

        else:
            #self.label_itens_seguranca.setText("OK")
            liberacao_meio_ambiente.show()
            aviso_liberacao.hide()

    #Função qeu chama a tela de relatar incidente.
    def relatos_liberacao(self):
        relatos_liberacao.lineEdit_descricao.setFocus()
        liberacao_seguranca.string_da_lista = " ".join(liberacao_seguranca.inconformidades)

        print(liberacao_seguranca.string_da_lista)

        relatos_liberacao.label_itens_nao_conformes.setText(liberacao_seguranca.string_da_lista)

        relatos_liberacao.show()
        aviso_liberacao.hide()


class Relatos_liberacao(QMainWindow, Ui_Relatos_liberacao):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.lineEdit_descricao.clear()
        self.lineEdit_descricao.setPlaceholderText("Digite aqui uma breve descrição sobre o incidente ou anomalia encontrada.")
        self.botao_cancelar.clicked.connect(self.voltar)
        self.botao_finalizar.clicked.connect(self.salvar)

    def salvar(self):
        self.label_itens_nao_conformes.clear()

    def voltar(self):
        self.label_itens_nao_conformes.clear()
        liberacao_seguranca.string_da_lista = " "
        liberacao_seguranca.inconformidades.clear()
        liberacao_seguranca.lista_erros = []
        print(liberacao_seguranca.lista_real)
        print(liberacao_seguranca.lista_erros)

        liberacao_seguranca.show()
        relatos_liberacao.hide()


################################ TELA MENU DE INTERFACE DIDÁTICA ################################
#Tela que fornece um suporte didático sobre a utilização da máquina para os colaboradores.
class Interface_didatica_menu(QMainWindow, Ui_interface_didatica_menu):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_botoes.clicked.connect(self.botoes)
        self.botao_finalidades.clicked.connect(self.finalidade)
        self.botao_home.clicked.connect(self.home)

        # ******************************* FUNÇÕES DA CLASSE *******************************

    #Função que chama a tela de Finalidade da Máquina.
    def finalidade(self):
        interface_menu_finalidade.show()
        interface_menu.hide()

    #Função que chama a tela que explica os botões existentes na máquina.
    def botoes(self):
        interface_menu_botoes.show()
        interface_menu.hide()

    #Função que volta para o Menu.
    def home(self):
        Menu01.show()
        interface_menu.hide()

################################ TELA DE BOTÕES DA MÁQUINA ################################
#Tela que Explica a funcionalidade de cada botão existente na sera de perfil.
class Interface_botoes(QMainWindow, Ui_interface_didatica_menu_botoes):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_1.clicked.connect(self.botao_01)
        self.botao_2.clicked.connect(self.botao_02)
        self.botao_3.clicked.connect(self.botao_03)
        self.botao_4.clicked.connect(self.botao_04)
        self.botao_5.clicked.connect(self.botao_05)
        self.botao_home.clicked.connect(self.home)
        self.botao_seta_dirteita.clicked.connect(self.botao_emergencia)

    # ******************************* VARIÁVEIS *******************************

        self.estilo_fonte = "border-style: outset;\n" "border-color: rgb(0, 0, 0);\n""border-width:6px;\n""\n""\n""font: 75 30pt \"Bosch Sans Bold\";\n""background-color: rgb(0,0,0);"

    # ******************************* FUNÇÕES DA CLASSE *******************************
    #Função que configura e descreve a função do Botão Liga.
    def botao_01(self):
        self.label_indicacao.setText("1")
        self.label_titulo.setStyleSheet(self.estilo_fonte)
        self.label_titulo.setText("<html><head/><body><p align=\"center\"><span style=\" color:#FFC000;\">BOTÃO LIGA A SERRA</span></p></body></html>")
        self.label_caixa_de_texto.setText("             Botão responsável por iniciar o processo de \ncorte do perfil se a porta estiver trancada e a peça \ntravada. \n")

    #Função que configura e descreve a função da Chave Seletora.
    def botao_02(self):
        self.label_titulo.setStyleSheet(self.estilo_fonte)
        self.label_indicacao.setText("2")
        self.label_titulo.setText("<html><head/><body><p align=\"center\"><span style=\" color:#FFC000;\">CHAVE SELETORA DE PERFIL 30/45</span></p></body></html>")
        self.label_caixa_de_texto.setText("             Chave seletora responsável por definir se o \nperfil a ser cortado é de 30 ou 45 para estabelecer a \ndistância que a serra deverá cortar para ultrapassar o \nperfil de 30/45 completamente.")

    # Função que configura e descreve a função do Botão Liga.
    def botao_03(self):
        self.label_indicacao.setText("3")
        self.label_titulo.setStyleSheet(self.estilo_fonte)
        self.label_titulo.setText("<html><head/><body><p align=\"center\"><span style=\" color:#FFC000;\">CHAVE SELETORA DE PORTA TRANCADA</span></p></body></html>")
        self.label_caixa_de_texto.setText("             Chave seletora responsável por garantir o \ntravamento da porta.\n\n")

    # Função que configura e descreve a função do Botão de Travar a Peça.
    def botao_04(self):
        self.label_indicacao.setText("4")
        self.label_titulo.setStyleSheet(self.estilo_fonte)
        self.label_titulo.setText("<html><head/><body><p align=\"center\"><span style=\" color:#FFC000;\">BOTÃO PARA TRAVAR PEÇA</span></p></body></html>")
        self.label_caixa_de_texto.setText("             Ao pressionar o botão, dois pistões pneumáticos \ntravam a peça na posição estabelecida pelo usuário.\n\n")

    # Função que configura e descreve a função do Botão Reset
    def botao_05(self):
        self.label_indicacao.setText("5")
        self.label_titulo.setStyleSheet(self.estilo_fonte)
        self.label_titulo.setText("<html><head/><body><p align=\"center\"><span style=\" color:#FFC000;\">BOTÃO RESET</span></p></body></html>")
        self.label_caixa_de_texto.setText("             Botão necessário para reiniciar os processos da \nmáquina caso ocorra alguma falha, como a tentativa de \nabrir as portas de segurança durante a operação, ou ao \npressionar o botão de emergência.")

    # Função que chama a tela de explicação do Botão de Emergência.
    def botao_emergencia(self):
        interface_menu_botao_emergencia.show()
        interface_menu_botoes.hide()

    # Função que volta para o menu interface.
    def home(self):
        interface_menu.show()
        interface_menu_botoes.hide()

################################ TELA DE BOTÃO DE EMERGÊNCIA ################################
#Tela que explica a funcionalidade do botão de emergência.
class Interface_botao_emergencia(QMainWindow, Ui_interface_didatica_menu_botao_emergencia):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_home.clicked.connect(self.home)
        self.botao_seta_esquerda.clicked.connect(self.botoeira)

        # ******************************* FUNÇÕES DA CLASSE *******************************
    #Função que volta para o menu interface.
    def home(self):
        interface_menu.show()
        interface_menu_botao_emergencia.hide()

    #Função que chama a tela de Botões da Máquina.
    def botoeira(self):
        interface_menu_botoes.show()
        interface_menu_botao_emergencia.hide()

################################ TELA DE FINALIDADE DE MÁQUINA ################################
#Tela de explicação sobre a finalidade da serra de perfil.
class Interface_finalidade(QMainWindow, Ui_interface_didatica_finalidade):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_home.clicked.connect(self.home)

    # ******************************* FUNÇÕES DA CLASSE *******************************

    def home(self):
        interface_menu.show()
        interface_menu_finalidade.hide()

################################ TELA DE MENU DE DOCUMENTOS E DESENHOS ################################
#Tela de menu de documentos que contém as peças a serem desenvolvidas, o diagrama elétrico da máquina e o mapa de riscos e danos.
class Documentos_menu(QMainWindow, Ui_documentos_menu):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_home.clicked.connect(self.home)
        self.botao_documentos_de_pecas01.clicked.connect(self.documentos_de_pecas)
        self.botao_documentos_de_pecas02.clicked.connect(self.documentos_de_pecas)
        self.botao_diagrama_eletrico01.clicked.connect(self.diagrama_eletrico)
        self.botao_diagrama_eletrico02.clicked.connect(self.diagrama_eletrico)
        self.botao_mae01.clicked.connect(self.mapa_de_riscos)
        self.botao_mae02.clicked.connect(self.mapa_de_riscos)

    # ******************************* FUNÇÕES DA CLASSE *******************************
    #Função que volta para o menu.
    def home(self):
        Menu01.show()
        documentos_menu.hide()

    #Função que abre o menu de documentos de peças (desenhos).
    def documentos_de_pecas(self):
        documentos_de_pecas_menu.show()
        documentos_menu.hide()

    #Função que abre p diagrama elétrico.
    def diagrama_eletrico(self):
        diagrama_eletrico.show()
        documentos_menu.hide()

    #Função que abre o mapa de riscos e danos.
    def mapa_de_riscos(self):
        mapa_de_riscos.show()
        documentos_menu.hide()

################################ TELA DE MENU DE DESENHOS DE PEÇAS ################################
#Tela que possui os desenhos mecânicos sobre as peças a serem desenvolvidas durante as aulas.
class Documentos_documentos_de_pecas_menu(QMainWindow, Ui_documentos_documentos_de_pecas_menu):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        # ******************************* AÇÕES *******************************
        self.botao_home.clicked.connect(self.home)
        self.botao_peca01_1.clicked.connect(self.peca01)
        self.botao_peca01_2.clicked.connect(self.peca01)
        self.botao_peca02_1.clicked.connect(self.peca02)
        self.botao_peca02_2.clicked.connect(self.peca02)
        self.botao_peca03_1.clicked.connect(self.peca03)
        self.botao_peca03_2.clicked.connect(self.peca03)

    # ******************************* FUNÇÕES DA CLASSE *******************************
    #Função que volta para o menu.
    def home(self):
        documentos_menu.show()
        documentos_de_pecas_menu.hide()

    #Função que abre o desenho da primeira peça.
    def peca01(self):
        peca01.show()
        documentos_de_pecas_menu.hide()

    # Função que abre o desenho da segunda peça.
    def peca02(self):
        peca02.show()
        documentos_de_pecas_menu.hide()

    # Função que abre o desenho da terceira peça.
    def peca03(self):
        peca03.show()
        documentos_de_pecas_menu.hide()

################################ ELA DE DESENHO DA PEÇA 01 ################################
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

################################ ELA DE DIAGRAMA ELÉTRICO ################################
#Tela que contém o diagrama elétrico
class Diagrama_eletrico(QMainWindow, Ui_documentos_diagrama_eletrico):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_home.clicked.connect(self.home)
        self.botao_seta_direita.clicked.connect(self.proxima_pagina)
        self.botao_seta_esquerda.clicked.connect(self.pagina_anterior)

        # ******************************* VARIÁVEIS *******************************

        self.contador = 1 #Contador que representa o número da página
        self.pagina1 = QPixmap("imagens/cachorro.png")
        self.pagina2 = QPixmap("imagens/jacare.png")
        self.pagina3 = QPixmap("imagens/MANUTENCAO.png")

        # ******************************* CONFIGURAÇÕES *******************************

        self.label_imagem.setPixmap(self.pagina1)

        # ******************************* FUNÇÕES DA CLASSE *******************************
    #Função que volta para o menu de documentos
    def home(self):
        documentos_menu.show()
        diagrama_eletrico.hide()

    #Função que muda a imagem do diagrama (Próxima Página)
    def proxima_pagina(self):
        if self.contador < 3:
            self.contador += 1

        if self.contador == 2:
            self.label_imagem.setPixmap(self.pagina2)
            self.label_paginas.setText("PÁGINA 02/03")

        if self.contador == 3:
            self.label_imagem.setPixmap(self.pagina3)
            self.label_paginas.setText("PÁGINA 03/03")

    # Função que muda a imagem do diagrama (Página Anterior)
    def pagina_anterior(self):
        if self.contador > 1:
            self.contador -= 1

        if self.contador == 1:
            self.label_imagem.setPixmap(self.pagina1)
            self.label_paginas.setText("PÁGINA 01/03")

        if self.contador == 2:
            self.label_imagem.setPixmap(self.pagina2)
            self.label_paginas.setText("PÁGINA 02/03")

################################ ELA DE MAPA DE RISCOS E PERIGOS ################################
class Mapa_de_riscos(QMainWindow, Ui_mapa_de_riscos):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_home.clicked.connect(self.home)

    # ******************************* FUNÇÕES DA CLASSE *******************************
    #Função que volta para o menu
    def home(self):
        documentos_menu.show()
        mapa_de_riscos.hide()

################################ TELA DE MENU DE REGISTROS ################################
class Registros_menu(QMainWindow, Ui_Registros_menu):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        # ******************************* AÇÕES *******************************
        self.botao_home.clicked.connect(self.home)
        self.botao_historico_utilizacao_01.clicked.connect(self.resgistros_de_uso)
        self.botao_historico_utilizacao_02.clicked.connect(self.resgistros_de_uso)

        # ******************************* FUNÇÕES DA CLASSE *******************************

    #Função que volta para o menu
    def home(self):
        Menu01.show()
        registros_menu.hide()

    #Função que abre o histórico de utilização
    def resgistros_de_uso(self):
        registro_historico_utilizacao.load_registros()
        registro_historico_utilizacao.show()
        registros_menu.hide()

################################ TELA DE HISTÓRICO DE UTILIZAÇÃO  ################################
#Tela que mostra o histórico de quem e quando foi utilizada a máquina.
class Registro_historico_utilizacao(QMainWindow, Ui_cadastros_historico_utilizacao):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_voltar.clicked.connect(self.voltar)

        # ******************************* CONFIGURAÇÕES *******************************

        self.load_registros()

        # ******************************* FUNÇÕES DA CLASSE *******************************

    #Função que carrega as configurações e dados da tabela de utilização.
    def load_registros(self):
        self.tabela_utilizacao.setColumnCount(7)
        self.tabela_utilizacao.setColumnWidth(0, 50)
        self.tabela_utilizacao.setColumnWidth(1, 360)
        self.tabela_utilizacao.setColumnWidth(2, 150)
        self.tabela_utilizacao.setColumnWidth(3, 170)
        self.tabela_utilizacao.setColumnWidth(4, 180)
        self.tabela_utilizacao.setColumnWidth(5, 120)
        self.tabela_utilizacao.setColumnWidth(6, 180)

        self.tabela_utilizacao.setHorizontalHeaderLabels(["N°", "NOME", "EDV", "DATA", "HORA", "EXAME", "RESULTADO"])
        self.tabela_utilizacao.setSelectionBehavior(QAbstractItemView.SelectRows)
        registros = banco_dados.chama_registros()

        self.tabela_utilizacao.setRowCount(len(registros))
        row = 0

        for x in registros:
            self.tabela_utilizacao.setItem(row, 0, QTableWidgetItem(str((x[0]))))
            self.tabela_utilizacao.setItem(row, 1, QTableWidgetItem((x[1])))
            try:
                self.tabela_utilizacao.setItem(row, 2, QTableWidgetItem(str((x[2]))))
            except Exception as erro:
                print(f"{erro} AQUI02")
            self.tabela_utilizacao.setItem(row, 3, QTableWidgetItem((x[3])))
            self.tabela_utilizacao.setItem(row, 4, QTableWidgetItem((x[4])))
            self.tabela_utilizacao.setItem(row, 5, QTableWidgetItem((x[5])))
            self.tabela_utilizacao.setItem(row, 6, QTableWidgetItem((x[6])))

            row = row + 1



        # row = 0

        # self.tabela_utilizacao.setItem(row, 0, QTableWidgetItem(0,str(self.hoje)))



    def voltar(self):
        self.load_registros()
        registros_menu.show()
        registro_historico_utilizacao.hide()

class Segundo_Menu(QMainWindow, Ui_Menu02):  # SEGUNDO MENU
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.Botao_Seta_Esquerda.clicked.connect(self.tela_anterior)
        self.Botao_Cadastros.clicked.connect(self.cadastros)
        self.Botao_Sair.clicked.connect(self.sair)
        self.Botao_Manutencao.clicked.connect(self.manutencao)
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

    def manutencao(self):
        manutencao.show()
        Menu02.hide()

    def sair(self):
        if Menu01.maquina_liberada == True:
            self.now = datetime.now()
            self.horario_saida = self.now.strftime("%H:%M")
            self.horario_saida = f"{liberacao_meio_ambiente.horario_liberacao} - {self.horario_saida}"
            print(self.horario_saida)

            try:
                self.ID_liberacao = str(liberacao_meio_ambiente.ID_Liberacao)
                print(self.ID_liberacao)

            except Exception as errro:
                print(errro)

            try:
                banco_dados.marcar_horario_saida(self.horario_saida, self.ID_liberacao)
            except Exception as erro:
                print(erro)

        Menu01.maquina_liberada = False

        self.clear_checkboxes()
        standby.lineEdit_tag.setText("")
        standby.label_titulo.setText("APROXIME O CRACHÁ\nSOBRE O LEITOR")
        """""  
        GPIO.output(Alimentacao_maquina, False) 
        GPIO.output(led, True)   
        """""


        standby.show()
        Menu01.hide()
        Menu02.hide()


    def clear_checkboxes(self):
        Menu01.maquina_liberada = False
        self.checkboxes = [liberacao_seguranca.checkBox_1, liberacao_seguranca.checkBox_2,liberacao_seguranca.checkBox_3,
                           liberacao_seguranca.checkBox_4, liberacao_seguranca.checkBox_5,
                           liberacao_seguranca.checkBox_6,
                           liberacao_seguranca.checkBox_7, liberacao_seguranca.checkBox_8,
                           liberacao_seguranca.checkBox_9,
                           liberacao_meio_ambiente.checkBox_1]
        for i in self.checkboxes:
            i.setChecked(False)
        Menu01.Botao_Liberar_Maquina.setIcon(self.cadeado_fechado)


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
            #print(index)
            value = index.sibling(index.row(), index.column()).data()
            #print(value)

            row = self.tabela.currentItem().row()
            #print("row=", row)
            col = self.tabela.currentItem().column()
            #print("col=", col)
            item = self.tabela.horizontalHeaderItem(col).text()
            #print("item=", item)

            value_02 = index.sibling(row + 1, index.column()).data()
            #print(value_02)

            self.nome = index.sibling(row, 0).data()
            self.edv = index.sibling(row, 1).data()
            self.classe = index.sibling(row, 2).data()
            self.ID = str(banco_dados.ID_User(self.edv))
            self.Data_Nasciento = banco_dados.Data_nascimento(self.ID)
            cadastros_menu_adicionar.alterar_classe = True
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
        lista = banco_dados.tabela_cadastros()

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
        cadastros_menu_leitor.adicionar = True
        cadastros_menu_adicionar.alterar_classe = False
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
        self.botao_alterar_classe.clicked.connect(self.mudar_classe)

        self.lineEdit_nome.setText("")
        self.lineEdit_data_nascimento.setText("")
        self.lineEdit_edv.setText("")
        self.lineEdit_nome.setPlaceholderText("NOME COMPLETO")
        self.lineEdit_edv.setPlaceholderText("EDV")
        self.lineEdit_data_nascimento.setPlaceholderText("DATA DE NASCIMENTO")

    def leitor(self):
        cadastros_menu_leitor.adicionar = False
        cadastros_menu.ficha()
        cadastros_menu_leitor.opcao = False
        cadastros_menu_leitor.show()
        cadastros_menu_editar.hide()

    def mudar_classe(self):
        cadastros_menu_adicionar.show()
        cadastros_menu_editar.hide()
    def home(self):
        cadastros_menu.show()
        cadastros_menu_editar.hide()

    def atualizar(self):
        self.nome = self.lineEdit_nome.text()
        self.data_nascimento = self.lineEdit_data_nascimento.text()
        self.data_nascimento = f"'{self.data_nascimento}'"
        #print(self.data_nascimento)
        self.edv = self.lineEdit_edv.text()

        try:
            banco_dados.atualizar_cadastro(self.nome, self.data_nascimento, self.edv, cadastros_menu.ID)

            cadastros_menu.load_tabela()

        except:
            if self.nome == "":
                print("Preencha o campo NOME!")

            if self.data_nascimento == "":
                print("Preencha o campo DATA DE NASCIMENTO!")

            if self.edv == "":
                print("Preencha o campo EDV!")

            if cadastros_menu.ID == "":
                print("Passe o crachá sobre o leitor!")


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
        try:
            self.tag_cartao = self.lineEdit_tag_cartao.text()
            #print(self.adicionar)

            if not self.tag_cartao == "":
                if self.adicionar == True:
                    print(self.tag_cartao, cadastros_menu_adicionar_ficha_01.nome, cadastros_menu_adicionar_ficha_01.classe, cadastros_menu_adicionar_ficha_01.edv, cadastros_menu_adicionar_ficha_01.data_nascimento )
                    banco_dados.adicionar_cadastro(self.tag_cartao, cadastros_menu_adicionar_ficha_01.nome, cadastros_menu_adicionar_ficha_01.edv, cadastros_menu_adicionar_ficha_01.classe, cadastros_menu_adicionar_ficha_01.data_nascimento)
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
                    banco_dados.update_tag(self.tag_cartao, cadastros_menu_editar.lineEdit_edv.text())
                    cadastros_menu_editar.show()
                    cadastros_menu_leitor.hide()

            else:
                print("Tente novamente")
        except Exception as erro:
            print(erro)




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

        self.alterar_classe = False

    def aprendiz(self):
        if self.alterar_classe == False:
            cadastros_menu_adicionar_ficha_01.classe = "Aprendiz"
            cadastros_menu_adicionar_ficha_01.label_imagem_classe.setPixmap(self.imagem_aprendiz)
            cadastros_menu_adicionar_ficha_01.show()
            cadastros_menu_adicionar.hide()

        else:
            try:
                banco_dados.alterar_classe("Aprendiz",cadastros_menu_editar.lineEdit_edv.text())
                cadastros_menu_editar.label_imagem_patente.setPixmap(cadastros_menu.imagem_aprendiz2)
                cadastros_menu_editar.show()
                cadastros_menu_adicionar.hide()
                cadastros_menu.load_tabela()

            except Exception as erro:
                print(erro)

    def meio_oficial(self):
        if self.alterar_classe == False:
            cadastros_menu_adicionar_ficha_01.classe = "Meio-Oficial"
            cadastros_menu_adicionar_ficha_01.label_imagem_classe.setPixmap(self.imagem_meio_oficial)
            cadastros_menu_adicionar_ficha_01.show()
            cadastros_menu_adicionar.hide()

        else:
            try:
                banco_dados.alterar_classe("Meio Oficial", cadastros_menu_editar.lineEdit_edv.text())
                cadastros_menu_editar.label_imagem_patente.setPixmap(cadastros_menu.imagem_meio_oficial2)
                cadastros_menu_editar.show()
                cadastros_menu_adicionar.hide()
                cadastros_menu.load_tabela()

            except Exception as erro:
                print(erro)

    def manutentor(self):
        if self.alterar_classe == False:
            cadastros_menu_adicionar_ficha_01.classe = "Manutentor"
            cadastros_menu_adicionar_ficha_01.label_imagem_classe.setPixmap(self.imagem_manutentor)
            cadastros_menu_adicionar_ficha_01.show()
            cadastros_menu_adicionar.hide()

        else:
            try:
                banco_dados.alterar_classe("Manutentor", cadastros_menu_editar.lineEdit_edv.text())
                cadastros_menu_editar.label_imagem_patente.setPixmap(cadastros_menu.imagem_manutentor2)
                cadastros_menu_editar.show()
                cadastros_menu_adicionar.hide()
                cadastros_menu.load_tabela()

            except Exception as erro:
                print(erro)

    def responsavel(self):
        if self.alterar_classe == False:
            cadastros_menu_adicionar_ficha_01.classe = "Responsável"
            cadastros_menu_adicionar_ficha_01.label_imagem_classe.setPixmap(self.imagem_responsavel)
            cadastros_menu_adicionar_ficha_01.show()
            cadastros_menu_adicionar.hide()

        else:
            try:
                banco_dados.alterar_classe("Responsável", cadastros_menu_editar.lineEdit_edv.text())
                cadastros_menu_editar.label_imagem_patente.setPixmap(cadastros_menu.imagem_responsavel2)
                cadastros_menu_editar.show()
                cadastros_menu_editar.hide()
                cadastros_menu.load_tabela()

            except Exception as erro:
                print(erro)

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


class Manutencao(QMainWindow, Ui_Manutencao):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.botao_home.clicked.connect(self.home)
        self.botao_energizar_contator_1.clicked.connect(self.energizar_maquina)
        self.botao_energizar_contator_2.clicked.connect(self.energizar_maquina)
        self.botao_liberar_trava1.clicked.connect(self.liberar_trava)
        self.botao_liberar_trava2.clicked.connect(self.liberar_trava)
        self.botao_maquina_manutencao.clicked.connect(self.maquina_em_manutencao)

        self.painel_liberado = False
        self.painel_energizado = False
        self.estado_manutencao = False
        self.maquina_em_manutencao()

    def energizar_maquina(self):
        if self.painel_energizado == False:
            self.painel_energizado = True
            self.label_raio.setStyleSheet("border-style: outset;\n" "color: rgb(0, 0, 0);\n" "border-color: rgb(0, 0, 0);\n" "border-width:6px;\n" "font: 75 34pt \"Bosch Sans Bold\";\n" 
                "background-color: rgb(255,207,0);")
            self.botao_energizar_contator_2.setStyleSheet("border-style: outset;\n" "border-color: rgb(0, 0, 0);\n" "border-width:7px;\n" "border-radius: 0px;\n"
                "background-color: rgb(237, 0, 7);")
        else:
            self.painel_energizado= False
            self.label_raio.setStyleSheet("border-style: outset;\n" "color: rgb(0, 0, 0);\n" "border-color: rgb(0, 0, 0);\n" "border-width:6px;\n" "font: 75 34pt \"Bosch Sans Bold\";\n"
                "background-color: rgb(255,255,255);")
            self.botao_energizar_contator_2.setStyleSheet("border-style: outset;\n" "border-color: rgb(0, 0, 0);\n" "border-width:7px;\n" "border-radius: 0px;\n"
                "background-color: rgb(255, 255, 255);")

    def liberar_trava(self):
        if self.painel_liberado == False:
            self.painel_liberado = True
            self.botao_liberar_trava2.setStyleSheet("border-style: outset;\n" "border-color: rgb(0, 0, 0);\n" "border-width:7px;\n" "border-radius: 0px;\n"
                        "background-color: rgb(237, 0, 7);")
            self.label_trava_solenoide.move(330, 565)
        else:
            self.painel_liberado = False
            self.botao_liberar_trava2.setStyleSheet("border-style: outset;\n" "border-color: rgb(0, 0, 0);\n" "border-width:7px;\n" "border-radius: 0px;\n"
                        "background-color: rgb(255, 255, 255);")
            self.label_trava_solenoide.move(370, 565)


    def maquina_em_manutencao(self):
        if self.estado_manutencao == False:
            banco_dados.estado_manutencao(self.estado_manutencao, serra_de_perfil)
            self.estado_manutencao = True

            self.label_sim_nao.move(580,500)
            self.botao_maquina_manutencao.move(790,500)
            self.label_sim_nao.setText("NÃO")
            self.label_sim_nao.setStyleSheet("border-style: outset;\n" "color: rgb(0, 0, 0);\n" "border-color: rgb(0, 0, 0);\n" "border-width:6px;\n" "border-radius: 0px;\n" "\n" "font: 75 55pt \"Bosch Sans Bold\";\n"
                "background-color: rgb(0, 136, 74);")
            self.label_painel_eletrico.setStyleSheet("\n" "color: rgb(0, 0, 0);\n" "border-color: rgb(0, 0, 0);\n" "border-radius: 90px;\n" "font: 75 28pt \"Bosch Sans Bold\";\n"
                "background-color: rgb(138, 144, 151);")
            self.label_fundo_painel.setStyleSheet("border-style: outset;\n" "color: rgb(0, 0, 0);\n" "border-color: rgb(0, 0, 0);\n" "border-width:6px;\n" "border-radius: 90px;\n" "font: 75 34pt \"Bosch Sans Bold\";\n"
                "background-color: rgb(138, 144, 151);")

        else:
            banco_dados.estado_manutencao(self.estado_manutencao, serra_de_perfil)
            self.estado_manutencao = False

            self.label_sim_nao.move(970, 500)
            self.botao_maquina_manutencao.move(580, 500)
            self.label_sim_nao.setText("SIM")
            self.label_sim_nao.setStyleSheet("border-style: outset;\n" "color: rgb(0, 0, 0);\n" "border-color: rgb(0, 0, 0);\n" "border-width:6px;\n" "border-radius: 0px;\n" "\n" "font: 75 55pt \"Bosch Sans Bold\";\n"
                "background-color: rgb(237, 0, 7);")
            self.label_painel_eletrico.setStyleSheet("\n" "color: rgb(0, 0, 0);\n" "border-color: rgb(0, 0, 0);\n" "border-radius: 90px;\n" "font: 75 28pt \"Bosch Sans Bold\";\n"
                "background-color: rgb(237, 0, 7);")
            self.label_fundo_painel.setStyleSheet("border-style: outset;\n" "color: rgb(0, 0, 0);\n" "border-color: rgb(0, 0, 0);\n" "border-width:6px;\n" "border-radius: 90px;\n" "font: 75 34pt \"Bosch Sans Bold\";\n"
                "background-color: rgb(237, 0, 7);")

    def home(self):
        Menu02.show()
        manutencao.hide()


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
diagrama_eletrico = Diagrama_eletrico()
mapa_de_riscos = Mapa_de_riscos()
aviso_liberacao = Aviso_liberacao()
interface_menu = Interface_didatica_menu()
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
manutencao = Manutencao()
standby = Standby()
relatos_liberacao = Relatos_liberacao()
standby.show()
sys.exit(ap.exec())

        # ******************************* AÇÕES *******************************
        # ******************************* VARIÁVEIS *******************************
        # ******************************* FUNÇÕES DA CLASSE *******************************
