################################ IMPORTANDO AS BIBLIOTECAS E FUNÇÕES ################################
import sys
from datetime import datetime, date
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QLabel, QLineEdit, QTableWidget, QAbstractItemView, QTableView
from PyQt5.QtGui import QIcon, QPixmap, QMovie
from PyQt5 import QtCore
import textwrap
import sqlite3

# GARANTIR QUE A DATA DE NASCIMENTO VÁ CERTA PARA O BANCO
# QUEBRA DE LINHA AUTOMÁTICA
#DEIXA AS NÃO OK PRINTADAS DE AMARELO
#CRIAR UMA TELA PARA EXIBIR TIPO UM RELATÓRIO MOSTRANDO SOBRE A LIBERAÇÃO OK

# INTERFACE DIDÁTICA
# PEGAR A DEFINIÇÃO DOS BOTÕES SEGUNDO O MANUAL
# FAZER OS VÍDEOS DA PARTE DE MODO DE UTILIZAR

# DOCUMENTOS
# ARRUMAR O DIAGRAMA ELÉTRICO DA MÁQUINA

# MANUTENÇÃO:
# CRIAR SCRIPT PARA TEMPORIZADOR DA TRAVA


################################ IMPORTANDO AS CLASSES DOS ARQUIVOS DE TELAS ################################
from Menu01 import Ui_Menu01
from Menu02 import Ui_Menu02
from Caderno_Verde_Atencao import Ui_Atencao
from Liberação_Segurança import Ui_Liberacao_Seguranca
from Liberação_Meio_Ambiente import Ui_Liberacao_Meio_Ambiente
from Documentos_Menu import Ui_documentos_menu
from Documentos_Documentos_de_pecas_menuu import Ui_documentos_documentos_de_pecas_menu
from documentos_documentos_de_pecas_1 import Ui_peca01
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
from Feliz_aniversario import Ui_Feliz_aniversario

################################ DECLARAÇÃO DE PORTAS DA RASPYBERRY E BIBLIOTECAS ################################

"""import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

trava_do_painel = 12
Alimentacao_maquina = 16
led_manutencao = 15

GPIO.setup(Alimentacao_maquina, GPIO.OUT)
GPIO.setup(led_manutencao, GPIO.OUT)
GPIO.setup(trava_do_painel, GPIO.OUT)

GPIO.output(Alimentacao_maquina, False)
GPIO.output(led_manutencao, False)
GPIO.output(trava_do_painel, False)
"""

################################ VARIÁVEIS GLOBAIS ################################
serra_de_perfil = "1"

################################ CLASSE CONEXÃO COM O BANCO DE DADOS ################################

class Connection:
    def __init__(self, db):
        self.banco = sqlite3.connect(db)

    ################################ FUNÇÕES DO BANCO DE DADOS ################################

    # Pesquisar Usuário a partir do ID_Card.
    def pesquisar_colaborador(self, idcard):
        cursor = self.banco.cursor()
        consulta = f"SELECT Nome,ID_Usuario, EDV FROM Usuarios WHERE ID_Card ='{int(idcard)}'"
        cursor.execute(consulta)
        nome = cursor.fetchall()
        cursor.close()
        return nome[0]

    # Coleta os usuários cadastrados no Banco de Dados.
    def tabela_cadastros(self):
        cursor = self.banco.cursor()
        consulta = ("SELECT Nome, EDV, Classe FROM Usuarios")
        cursor.execute(consulta)
        lista = cursor.fetchall()
        cursor.close()
        return lista

    # Pesquisa o ID_User a partir do EDV.
    def ID_User(self, edv):
        cursor = self.banco.cursor()
        consulta = f"SELECT ID_Usuario FROM Usuarios WHERE EDV ='{str(edv)}'"
        cursor.execute(consulta)
        ID_user = cursor.fetchone()
        cursor.close()
        return ID_user[0]

    # Adiciona o novo usuário no Banco de Dados.
    def adicionar_cadastro(self, tag_cartao, nome, edv, classe, data_nascimento):
        cursor = self.banco.cursor()
        adicionar = ("INSERT INTO Usuarios (ID_Card, Nome, Classe, EDV, Data_Nascimento)  VALUES ('" + tag_cartao + "','" + nome + "','" + classe + "','" + edv + "','" + data_nascimento + "')")  # inserir Dados
        cursor.execute(adicionar)
        self.banco.commit()
        cursor.close()
        return print("Adicionado")

    # Atualiza ficha de usuário.
    def atualizar_cadastro(self, nome, data_nascimento, edv, ID):
        cursor = self.banco.cursor()
        adicionar = f"UPDATE Usuarios SET Nome = '{nome}' , Data_Nascimento= {data_nascimento} , EDV= {edv}   WHERE ID_Usuario = {ID}; "  # inserir Dados
        cursor.execute(adicionar)
        self.banco.commit()
        cursor.close()
        return print("Atualizado")

    # Pesquisa a data de nascimento do Usuário a partir do ID_Usuário.
    def Data_nascimento(self, ID):
        cursor = self.banco.cursor()
        consulta = f"SELECT Data_Nascimento FROM Usuarios WHERE ID_Usuario ='{ID}'"
        cursor.execute(consulta)
        Data_Nascimento = cursor.fetchone()
        cursor.close()
        return Data_Nascimento[0]

    # Atualiza a tag do cartão (ID_Card).
    def update_tag(self, tag, EDV):
        cursor = self.banco.cursor()
        tag = f"UPDATE Usuarios SET ID_Card = '{tag}' WHERE EDV = {EDV}; "
        cursor.execute(tag)
        self.banco.commit()
        cursor.close()
        return print("Tag_Atualizada")

    # Seleciona a classe do usuário a partir do ID_Card.
    def verifica_classe(self, ID):
        cursor = self.banco.cursor()
        consulta = f"SELECT Classe FROM Usuarios WHERE ID_Card ='{ID}' "
        cursor.execute(consulta)
        Classe = cursor.fetchone()
        cursor.close()
        return Classe[0]

    # Altera a classe do usuário a partir do EDV.
    def alterar_classe(self, Classe, EDV):
        cursor = self.banco.cursor()
        Classe = f"UPDATE Usuarios SET Classe = '{Classe}' WHERE EDV = {EDV}; "
        cursor.execute(Classe)
        self.banco.commit()
        cursor.close()
        return print("Classe_Atualizada")

    # Registra a liberação de máquina.
    def registrar_utilizacao(self, Colaborador, Data, Hora, Exame, EDV, Resultado):
        cursor = self.banco.cursor()
        adicionar = ("INSERT INTO Registros (Colaborador, EDV, DATA, HORA, EXAME, RESULTADO)  VALUES ('" + Colaborador + "','" + Data + "','" + Hora + "','" + Exame + "','" + EDV + "','" + Resultado + "')")  # inserir Dados
        cursor.execute(adicionar)
        ID = cursor.lastrowid
        self.banco.commit()
        cursor.close()
        return str(ID)

    # Coleta todos os registros de utilização.
    def chama_registros(self):
        cursor = self.banco.cursor()
        consulta = ("SELECT * FROM Registros")
        cursor.execute(consulta)
        registros = cursor.fetchall()
        cursor.close()
        return registros

    # Filtra as liberações que deram "NÃO OK".
    def chama_resgistros_nao_conformes(self):
        cursor = self.banco.cursor()
        consulta = f"SELECT * FROM Registros WHERE RESULTADO = 'NÃO OK'"
        cursor.execute(consulta)
        registros = cursor.fetchall()
        cursor.close()
        return registros

    # Retorna os dados da liberação "NÃO OK".
    def retorna_descricao_registro(self, EDV, HORA, DATA, RESULTADO):
        cursor = self.banco.cursor()
        consulta = f"SELECT Descricao, Inconformidades FROM Registros WHERE (EDV, HORA, DATA, RESULTADO)  = ('" + EDV + "', '" + HORA + "', '" + DATA + "', '" + RESULTADO + "')"
        cursor.execute(consulta)
        dados = cursor.fetchall()
        cursor.close()
        return dados[0]

    # Registra o horário de saída.
    def marcar_horario_saida(self, horario_saida, Registro):
        cursor = self.banco.cursor()
        tag = f"UPDATE Registros SET HORA = '{horario_saida}' WHERE ID_Liberacao = '" + Registro + "'; "
        cursor.execute(tag)
        self.banco.commit()
        cursor.close()
        return print("Hora_Atualizada")

    # Verifica se a máquina está em manutenção.
    def verifica_estado_de_manutencao(self, id_maquina):
        cursor = self.banco.cursor()
        consulta = f"SELECT Manutencao FROM Maquinas WHERE ID_maquina ='{id_maquina}'"
        cursor.execute(consulta)
        estado_manutencao = cursor.fetchone()
        cursor.close()
        if estado_manutencao[0] == "False":
            return False
        else:
            return True

    # Altera no banco o estado de manutenção.
    def estado_manutencao(self, bool, maquina):
        cursor = self.banco.cursor()
        alterar = f"UPDATE Maquinas SET Manutencao = '{bool}'  WHERE ID_Maquina = {maquina}; "
        cursor.execute(alterar)
        self.banco.commit()
        cursor.close()
        return print("Mudou")

    # Salva a liberação no banco de dados.
    def salvar_relato_liberacao(self, Colaborador, Data, Hora, Exame, EDV, Resultado, Descricao, Inconformidades):
        cursor = self.banco.cursor()
        adicionar = ("INSERT INTO Registros (Colaborador, DATA, HORA, EXAME, EDV, RESULTADO, Descricao, Inconformidades)  VALUES ('" + Colaborador + "','" + Data + "','" + Hora + "','" + Exame + "','" + EDV + "','" + Resultado + "','" + Descricao + "','" + Inconformidades + "')")  # inserir Dados
        cursor.execute(adicionar)
        Escrever_no_final = cursor.lastrowid
        self.banco.commit()
        cursor.close()
        return str(Escrever_no_final)

    # Verifica se é aniversário do colaborador.
    def verifica_aniversario (self, EDV):
        cursor = self.banco.cursor()
        consulta = f"SELECT Data_Nascimento FROM Usuarios WHERE EDV ='{EDV}'"
        cursor.execute(consulta)
        data_aniversario = cursor.fetchone()
        cursor.close()
        return data_aniversario

    # Função que deleta usuário.
    def deleta_usuario(self, EDV):
        cursor = self.banco.cursor()
        deletar = f"DELETE FROM Usuarios WHERE EDV = '{EDV}'"
        cursor.execute(deletar)
        self.banco.commit()
        cursor.close()
        return print("Deletou")


################################ TELA DE ENTRADA E STANDBY ################################
class Standby(QMainWindow, Ui_Standby): # Tela que ocorre a validação do ID_Card do colaborador.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.lineEdit_tag.setFocus()
        self.lineEdit_tag.returnPressed.connect(self.comeca)
        self.lineEdit_tag.setText("")
        self.botao_imagem.clicked.connect(self.mousePressEvent)

        # ******************************* VARIÁVEIS *******************************

        self.cadeado_normal = QIcon("imagens/CADEADO_FECHADO.png")
        self.cadeado_manutencao = QIcon("imagens/Cadeado_manutencao.png")
        self.hoje = date.today()
        self.hoje_certo = self.hoje.strftime("%d/%m")
        print(self.hoje_certo)

        # ******************************* FUNÇÕES DA CLASSE *******************************

    def mousePressEvent(self, e): # Função caso clique na tela, ainda garante que a tag seja escrita na lineEdit_tag.
        self.lineEdit_tag.setFocus()

    def comeca(self): # Função que é chamada para fazer a verificação da tag do usuário após passar o crachá sobre o leitor/ENTER for pressionado.
        self.tag_cartao = self.lineEdit_tag.text()
        try:
            self.colaborador = banco_dados.pesquisar_colaborador(self.tag_cartao)[0]
            self.colaborador2 = self.colaborador.split(" ")
            self.classe = banco_dados.verifica_classe(self.tag_cartao)
            self.configurar()

        except Exception as erro:
            print(erro)
            self.lineEdit_tag.setFocus()
            self.lineEdit_tag.setText("")
            self.label_titulo.setText("ERRO DE LEITURA\nTENTE NOVAMENTE")

    def configurar(self): # Função que personaliza o menu com os dados do usuário, Nome, Edv e Classe.
        self.edv = banco_dados.pesquisar_colaborador(self.tag_cartao)[-1]
        Menu01.Label_Colaborador.setText(f'COLABORADOR: {self.colaborador2[0]} {self.colaborador2[-1]}')
        Menu01.Label_EDV.setText(f"EDV: {banco_dados.pesquisar_colaborador(self.tag_cartao)[-1]}")
        Menu02.Label_Colaborador.setText(f'COLABORADOR: {self.colaborador2[0]} {self.colaborador2[-1]}')
        Menu02.Label_EDV.setText(f"EDV: {banco_dados.pesquisar_colaborador(self.tag_cartao)[-1]}")

        # Se o usuário estiver cadastrado como Aprendiz ou Meio Oficial aparece apenas o Menu 01.
        if (self.classe == "Aprendiz") or (self.classe == "Meio Oficial"):
            Menu01.Botao_Seta_Direita.setDisabled(True)
            Menu01.Botao_Seta_Esquerda.setDisabled(True)
            Menu01.Botao_Seta_Direita.setIcon(Menu01.imagem_branca)
            Menu01.Botao_Seta_Esquerda.setIcon(Menu01.imagem_branca)

        # Se o usuário estiver cadastrado como Responsável ele possui acesso a todas as funções.
        if (self.classe == "Responsável"):
            Menu01.Botao_Seta_Direita.setDisabled(False)
            Menu01.Botao_Seta_Esquerda.setDisabled(False)
            Menu02.Botao_Cadastros.setDisabled(False)
            Menu01.Botao_Seta_Direita.setIcon(Menu01.seta_preta_direita)
            Menu01.Botao_Seta_Esquerda.setIcon(Menu01.seta_branca_esquerda)

        # Se o usuário estiver cadastrado como Manutentor, além do Menu 01 ele te acesso à tela de manutenção.
        if (self.classe == "Manutentor"):
            Menu01.Botao_Seta_Direita.setDisabled(False)
            Menu01.Botao_Seta_Esquerda.setDisabled(False)
            Menu02.Botao_Cadastros.setDisabled(True)
            Menu01.Botao_Seta_Direita.setIcon(Menu01.seta_preta_direita)
            Menu01.Botao_Seta_Esquerda.setIcon(Menu01.seta_branca_esquerda)

        # Muda para o ícone de cadeado de manutenção.
        if banco_dados.verifica_estado_de_manutencao(serra_de_perfil) == True:
            Menu01.Botao_Liberar_Maquina.setIcon(self.cadeado_manutencao)
            Menu01.Botao_Liberar_Maquina.setIconSize(QtCore.QSize(231, 231))

        else:
            Menu01.Botao_Liberar_Maquina.setIcon(self.cadeado_normal)
            Menu01.Botao_Liberar_Maquina.setIconSize(QtCore.QSize(220, 220))

        # Verifica se é aniversário do usuário.
        try:
            self.data_aniversario = banco_dados.verifica_aniversario(self.edv)[-1]
            self.data_aniversario = self.data_aniversario[0:5]
            print(self.data_aniversario)
            if self.data_aniversario == self.hoje_certo:
                aniversario.label_nome.setText(f"{self.colaborador2[0]} {self.colaborador2[-1]},")
                aniversario.show()
                standby.hide()
                cadastros_menu_editar.hide()

            else:
                Menu01.show()
                standby.hide()
        except Exception as erro:
            print(erro)




################################ MENU 01 ################################
class Primeiro_Menu(QMainWindow, Ui_Menu01): # Menu de interface para os usuários.
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

        # ******************************* VARIÁVEIS *******************************

        self.maquina_liberada = False  # Variável que determina se a máquina está ligada ou não.
        self.imagem_branca = QIcon("imagens/Branco.png")
        self.seta_branca_esquerda = QIcon("imagens/Seta Branca para esquerda.png")
        self.seta_preta_direita = QIcon("imagens/Seta Preta para direita.png")

        # ******************************* FUNÇÕES DA CLASSE *******************************

    def sair(self): # Função de Logout.
        Menu02.sair()

    def proxima_tela(self):  # Função que avança para o Menu02.
        Menu02.show()
        Menu01.hide()

    def liberacao_de_maquina(self): # Função que inicia o processo de liberação de máquina.
        relatos_liberacao.label_itens_nao_conformes.clear()
        liberacao_seguranca.string_da_lista = " "
        liberacao_seguranca.inconformidades.clear()
        liberacao_seguranca.lista_erros = []

        if banco_dados.verifica_estado_de_manutencao(serra_de_perfil) == False:
            if self.maquina_liberada == False:
                liberacao_atencao.show()
                Menu01.hide()
            else:
                print("segundo else")

        else:
            print("Não deixou entrar")
            pass

    def menu_documentos(self): # Função que chama a tela de Menu de Documentos.
        documentos_menu.show()
        Menu01.hide()

    def interface_didatica_menu(self): # Função que chama a tela de Interface Didática Menu.
        interface_menu.show()
        Menu01.hide()

    def menu_registros(self): # Função que chama a tela de Menu de Registros.
        registros_menu.show()
        Menu01.hide()


################################ TELA DE INSTRUÇÕES PARA LIBERAÇÃO ################################
class Liberacao_atencao(QMainWindow, Ui_Atencao): # Tela de advertência sobre o processo de libreação de máquina.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_continuar.clicked.connect(self.tela_de_seguranca)
        self.botao_home.clicked.connect(self.home)

        # ******************************* FUNÇÕES DA CLASSE *******************************

    def tela_de_seguranca(self): # Função que avança para a Liberação_Segurança.
        liberacao_seguranca.show()
        liberacao_atencao.hide()

    def home(self): # Função que retorna para o Menu01 (HOME).
        Menu01.show()
        liberacao_atencao.hide()

################################ TELA DE LIBERAÇÃO DOS REQUISITOS DE SEGURANÇA ################################
class Liberacao_seguranca(QMainWindow, Ui_Liberacao_Seguranca): # Tela que o usuário verifica os requisitos de segurança.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_home.clicked.connect(self.home)
        self.botao_continuar.clicked.connect(self.tela_meio_ambiente)


        # ******************************* VARIÁVEIS *******************************

        self.liberacao_seguranca = False
        self.allcheckBox = [self.checkBox_1, self.checkBox_2, self.checkBox_3, self.checkBox_4, self.checkBox_5, self.checkBox_6, self.checkBox_7, self.checkBox_8, self.checkBox_9]
        self.lista_real = []  # Lista de Check_Boxes checados.
        self.lista_erros = []  # Lista de Check_Boxes não checados.
        self.texto = []  # Texto  indicando os Check_boxes não checados.
        self.contador = 0  # Contador auxiliar.
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

    def home(self): # Função que retorna para o Menu01 (HOME).
        Menu01.show()
        liberacao_seguranca.hide()

    def verifica_checkBox(self): # Função que valida se todos os Check_Boxes estão checados.
        self.lista_real = []
        self.contador = 0

        for i in self.allcheckBox:

            if i.isChecked():
                self.contador = self.contador + 1
                self.lista_real.append(self.contador)

            else:
                self.contador = self.contador + 1

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

    def verifica_check_boxes_seguranca(self): # Função que verifica os Checkboxes de segurança.
        for i in range(1, 10):
            if i not in self.lista_real:
                self.lista_erros.append(i)

        if len(self.lista_erros) != 0:
            self.texto = str(self.lista_erros)
            return False
        else:
            return True

    def tela_meio_ambiente(self): # Função que passa para a tela de meio-ambiente caso todos os checkboxes de segurança estiverem checados.
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
class Liberacao_meio_ambiente(QMainWindow, Ui_Liberacao_Meio_Ambiente): # Tela que o usuário verifica os requisitos de meio-ambiente.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_home.clicked.connect(self.home)
        self.botao_continuar.clicked.connect(self.Verifica_checkboxes)

        # ******************************* VARIÁVEIS *******************************

        self.liberacao_meio_ambiente = False
        self.img2 = QIcon("imagens/CADEADO_ABERTO.png")

    # ******************************* FUNÇÕES DA CLASSE *******************************

    def home(self): # Função que retorna para o Menu.
        Menu01.show()
        liberacao_meio_ambiente.hide()

    # Função que verifica os Chechboxes de meio-ambiente e envia o sinal de uma porta analógica da Raspberry para comutar o contator elétrico caso o status da liberação seja OK.
    # Se a liberação for "Não OK" e o colaborador identificar algum problema na integridade e funcionamento da máquina, abre-se uma ficha para que o incidente seja relatado.
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
            Menu01.Botao_Liberar_Maquina.setIcon(self.img2)
            #GPIO.output(Alimentacao_maquina, True)

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

            except Exception as erro:
                print(erro)

            Menu01.show()
            liberacao_meio_ambiente.hide()

        else:
            aviso_liberacao.show()
            liberacao_meio_ambiente.hide()


################################ TELA DE AVISO ################################
class Aviso_liberacao(QMainWindow, Ui_Aviso_Liberacao): # Tela que adverte o colaborador de que alguns Checkboxes ficaram deschecados, caso seja engano ele pode voltar, e se caso for algum incidente procede para a tela de Relatos de Incidentes.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_voltar.clicked.connect(self.voltar_check_list)
        self.botao_relatar_problema.clicked.connect(self.relatos_liberacao)

    # ******************************* FUNÇÕES DA CLASSE *******************************

    def voltar_check_list(self): # Função que retorna para os Checkboxes da respectiva tela de liberação.
        if liberacao_seguranca.liberacao_seguranca == False:
            liberacao_seguranca.lista_erros = []
            relatos_liberacao.label_itens_nao_conformes.clear()
            liberacao_seguranca.string_da_lista = " "
            liberacao_seguranca.inconformidades.clear()

            liberacao_seguranca.show()
            aviso_liberacao.hide()

        else:
            liberacao_meio_ambiente.show()
            aviso_liberacao.hide()

    def relatos_liberacao(self): # Função qeu chama a tela de relatar incidente.
        relatos_liberacao.voltar_registros_ou_liberacao = False
        relatos_liberacao.botao_finalizar.setDisabled(False)
        relatos_liberacao.label_itens_nao_conformes.clear()
        relatos_liberacao.lineEdit_descricao.clear()

        self.hoje = date.today()
        self.hoje_formatado = self.hoje.strftime("%d/%m/%Y")
        self.now = datetime.now()
        self.horario_liberacao = self.now.strftime("%H:%M")

        relatos_liberacao.label_nome.setText(f"NOME: {standby.colaborador2[0]} {standby.colaborador2[-1]}")
        relatos_liberacao.label_data.setText(self.hoje_formatado)
        relatos_liberacao.label_periodo.setText(self.horario_liberacao)
        relatos_liberacao.lineEdit_descricao.setFocus()
        liberacao_seguranca.string_da_lista = " ".join(liberacao_seguranca.inconformidades)
        relatos_liberacao.label_itens_nao_conformes.setText(liberacao_seguranca.string_da_lista)

        relatos_liberacao.show()
        aviso_liberacao.hide()

################################ TELA DE RELATO DE INCONFORMIDADES DA LIBERAÇÃO ################################
class Relatos_liberacao(QMainWindow, Ui_Relatos_liberacao): #Tela que mostra todas as inconformidades encontradas durante o processo de liberação e disponibiliza um campo para o usuário digitar algum comentário caso necessário.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_cancelar.clicked.connect(self.voltar)
        self.botao_finalizar.clicked.connect(self.salvar)
        #self.lineEdit_descricao.returnPressed.connect(self.digita)

        # ******************************* VARIÁVEIS *******************************

        self.voltar_registros_ou_liberacao = False

        # ******************************* CONFIGURAÇÕES *******************************

        self.lineEdit_descricao.clear()
        self.lineEdit_descricao.setPlaceholderText("Digite aqui uma breve descrição sobre o incidente ou anomalia encontrada.")

    # Função que quebra a linha da line_edit_descrição. (teste)
    """def digita(self):
        self.value = self.lineEdit_descricao.text()

        self.wrapper = textwrap.TextWrapper(width=10)
        self.string = self.wrapper.fill(text=self.value)
        self.lineEdit_descricao.setText(self.string)
        self.teste = self.string.split()


        for i in self.teste:
            self.teste.insert(1, '\n')
        print(self.teste)
        print(self.string)"""

    def salvar(self): # Função que salva o registro digitado pelo usuário e as inconformidades no banco de dados.
        self.inconformidades = self.label_itens_nao_conformes.text()
        self.descricao = self.lineEdit_descricao.text()

        try:
            self.colaborador = f"{standby.colaborador2[0]} {standby.colaborador2[-1]}"
            self.hoje = date.today()
            self.hoje_formatado = self.hoje.strftime("%d/%m/%Y")
            self.now = datetime.now()
            self.horario_liberacao = self.now.strftime("%H:%M")
            self.exames = "A,B"
            self.edv = str(banco_dados.pesquisar_colaborador(standby.tag_cartao)[-1])
            self.resultado = "NÃO OK"
            banco_dados.salvar_relato_liberacao(self.colaborador, self.hoje_formatado, self.horario_liberacao,self.exames, self.edv, self.resultado, self.descricao, self.inconformidades)
            banco_dados.estado_manutencao(True, serra_de_perfil)
            Menu02.clear_checkboxes()
            manutencao.maquina_em_manutencao()

        except Exception as erro:
            print(erro)

        Menu01.show()
        relatos_liberacao.hide()
        self.label_itens_nao_conformes.clear()
        self.lineEdit_descricao.clear()

    def voltar(self): # Função de voltar.
        self.label_itens_nao_conformes.clear()
        liberacao_seguranca.string_da_lista = " "
        liberacao_seguranca.inconformidades.clear()
        liberacao_seguranca.lista_erros = []

        if self.voltar_registros_ou_liberacao == False:
            liberacao_seguranca.show()
            relatos_liberacao.hide()

        else:
            registro_historico_utilizacao.show()
            relatos_liberacao.hide()


################################ TELA MENU DE INTERFACE DIDÁTICA ################################
class Interface_didatica_menu(QMainWindow, Ui_interface_didatica_menu): # Tela que fornece um suporte didático sobre a utilização da máquina para os colaboradores.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_botoes.clicked.connect(self.botoes)
        self.botao_finalidades.clicked.connect(self.finalidade)
        self.botao_home.clicked.connect(self.home)

        # ******************************* FUNÇÕES DA CLASSE *******************************

    def finalidade(self): # Função que chama a tela de Finalidade da Máquina.
        interface_menu_finalidade.show()
        interface_menu.hide()

    def botoes(self): # Função que chama a tela que explica os botões existentes na máquina.
        interface_menu_botoes.show()
        interface_menu.hide()

    def home(self): # Função que volta para o Menu.
        Menu01.show()
        interface_menu.hide()


################################ TELA DE BOTÕES DA MÁQUINA ################################
class Interface_botoes(QMainWindow, Ui_interface_didatica_menu_botoes): # Tela que Explica a funcionalidade de cada botão existente na sera de perfil.
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

    def botao_01(self): # Função que configura e descreve a função do Botão Liga.
        self.label_indicacao.setText("1")
        self.label_titulo.setStyleSheet(self.estilo_fonte)
        self.label_titulo.setText("<html><head/><body><p align=\"center\"><span style=\" color:#FFC000;\">BOTÃO LIGA A SERRA</span></p></body></html>")
        self.label_caixa_de_texto.setText("             Botão responsável por iniciar o processo de \ncorte do perfil se a porta estiver trancada e a peça \ntravada. \n")

    def botao_02(self): # Função que configura e descreve a função da Chave Seletora.
        self.label_titulo.setStyleSheet(self.estilo_fonte)
        self.label_indicacao.setText("2")
        self.label_titulo.setText("<html><head/><body><p align=\"center\"><span style=\" color:#FFC000;\">CHAVE SELETORA DE PERFIL 30/45</span></p></body></html>")
        self.label_caixa_de_texto.setText("             Chave seletora responsável por definir se o \nperfil a ser cortado é de 30 ou 45 para estabelecer a \ndistância que a serra deverá cortar para ultrapassar o \nperfil de 30/45 completamente.")

    def botao_03(self): # Função que configura e descreve a função do Botão Liga.
        self.label_indicacao.setText("3")
        self.label_titulo.setStyleSheet(self.estilo_fonte)
        self.label_titulo.setText("<html><head/><body><p align=\"center\"><span style=\" color:#FFC000;\">CHAVE SELETORA DE PORTA TRANCADA</span></p></body></html>")
        self.label_caixa_de_texto.setText("             Chave seletora responsável por garantir o \ntravamento da porta.\n\n")

    def botao_04(self): # Função que configura e descreve a função do Botão de Travar a Peça.
        self.label_indicacao.setText("4")
        self.label_titulo.setStyleSheet(self.estilo_fonte)
        self.label_titulo.setText("<html><head/><body><p align=\"center\"><span style=\" color:#FFC000;\">BOTÃO PARA TRAVAR PEÇA</span></p></body></html>")
        self.label_caixa_de_texto.setText("             Ao pressionar o botão, dois pistões pneumáticos \ntravam a peça na posição estabelecida pelo usuário.\n\n")

    def botao_05(self): # Função que configura e descreve a função do Botão Reset.
        self.label_indicacao.setText("5")
        self.label_titulo.setStyleSheet(self.estilo_fonte)
        self.label_titulo.setText("<html><head/><body><p align=\"center\"><span style=\" color:#FFC000;\">BOTÃO RESET</span></p></body></html>")
        self.label_caixa_de_texto.setText("             Botão necessário para reiniciar os processos da \nmáquina caso ocorra alguma falha, como a tentativa de \nabrir as portas de segurança durante a operação, ou ao \npressionar o botão de emergência.")

    def botao_emergencia(self): # Função que chama a tela de explicação do Botão de Emergência.
        interface_menu_botao_emergencia.show()
        interface_menu_botoes.hide()

    def home(self): # Função que volta para o menu interface.
        interface_menu.show()
        interface_menu_botoes.hide()


################################ TELA DE BOTÃO DE EMERGÊNCIA ################################
class Interface_botao_emergencia(QMainWindow, Ui_interface_didatica_menu_botao_emergencia): # Tela que explica a funcionalidade do botão de emergência.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_home.clicked.connect(self.home)
        self.botao_seta_esquerda.clicked.connect(self.botoeira)

        # ******************************* FUNÇÕES DA CLASSE *******************************

    def home(self): # Função que volta para o menu interface.
        interface_menu.show()
        interface_menu_botao_emergencia.hide()

    def botoeira(self): # Função que chama a tela de Botões da Máquina.
        interface_menu_botoes.show()
        interface_menu_botao_emergencia.hide()


################################ TELA DE FINALIDADE DE MÁQUINA ################################
class Interface_finalidade(QMainWindow, Ui_interface_didatica_finalidade): # Tela de explicação sobre a finalidade da serra de perfil.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_home.clicked.connect(self.home)

        # ******************************* FUNÇÕES DA CLASSE *******************************

    def home(self): # Função que volta para o menu interface.
        interface_menu.show()
        interface_menu_finalidade.hide()


################################ TELA DE MENU DE DOCUMENTOS E DESENHOS ################################
class Documentos_menu(QMainWindow, Ui_documentos_menu): # Tela de menu de documentos que contém as peças a serem desenvolvidas, o diagrama elétrico da máquina e o mapa de riscos e danos.
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

    def home(self): # Função que volta para o menu documentos.
        Menu01.show()
        documentos_menu.hide()

    def documentos_de_pecas(self): # Função que abre o menu de documentos de perfis (desenhos técnicos e especificações).
        documentos_de_pecas_menu.show()
        documentos_menu.hide()

    def diagrama_eletrico(self): # Função que abre o diagrama elétrico.
        diagrama_eletrico.show()
        documentos_menu.hide()

    def mapa_de_riscos(self): # Função que abre o mapa de riscos e danos.
        mapa_de_riscos.show()
        documentos_menu.hide()


################################ TELA DE MENU DE DESENHOS DE PEÇAS ################################
class Documentos_documentos_de_pecas_menu(QMainWindow, Ui_documentos_documentos_de_pecas_menu): # Tela que possui os desenhos mecânicos sobre as peças a serem desenvolvidas durante as aulas.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_home.clicked.connect(self.home)
        self.botao_peca01_1.clicked.connect(self.perfil_de_aluminio_30)
        self.botao_peca01_2.clicked.connect(self.perfil_de_aluminio_30)
        self.botao_peca02_1.clicked.connect(self.perfil_de_aluminio_45)
        self.botao_peca02_2.clicked.connect(self.perfil_de_aluminio_45)
        self.botao_peca03_1.clicked.connect(self.perfil_de_aluminio_60)
        self.botao_peca03_2.clicked.connect(self.perfil_de_aluminio_60)

        # ******************************* VARIÁVEIS *******************************

        self.perfil_30 = QPixmap("imagens/Perfil_30.png")
        self.perfil_30_2 = QPixmap("imagens/Perfil_30_2.png")
        self.perfil_45 = QPixmap("imagens/Perfil_45_certo.png")
        self.perfil_45_2 = QPixmap("imagens/Perfil_45_2.png")
        self.perfil_60 = QPixmap("imagens/Perfil_60.png")
        self.perfil_60L = QPixmap("imagens/Perfil_60L.png")

    # ******************************* FUNÇÕES DA CLASSE *******************************

    def home(self): # Função que volta para o menu documentos.
        documentos_menu.show()
        documentos_de_pecas_menu.hide()

    def perfil_de_aluminio_30(self): # Função que abre o as informações do perfil de alumínio de 30x30.
        perfil_de_aluminio.troca_pagina = 1
        perfil_de_aluminio.label_titulo.setText("PERFIL DE ALUMÍNIO DE 30x30")
        perfil_de_aluminio.label_imagem.move(110,110)
        perfil_de_aluminio.label_imagem.setPixmap(self.perfil_30)
        perfil_de_aluminio.show()
        documentos_de_pecas_menu.hide()

    def perfil_de_aluminio_45(self): # Função que abre o as informações do perfil de alumínio de 45x45.
        perfil_de_aluminio.troca_pagina = 2
        perfil_de_aluminio.label_titulo.setText("PERFIL DE ALUMÍNIO DE 45x45")
        perfil_de_aluminio.label_imagem.move(110, 110)
        perfil_de_aluminio.label_imagem.setPixmap(self.perfil_45)
        perfil_de_aluminio.show()
        documentos_de_pecas_menu.hide()

    def perfil_de_aluminio_60(self): # Função que abre o as informações do perfil de alumínio de 60x60.
        perfil_de_aluminio.troca_pagina = 3
        perfil_de_aluminio.label_titulo.setText("PERFIL DE ALUMÍNIO DE 60x60")
        perfil_de_aluminio.label_imagem.move(110, 110)
        perfil_de_aluminio.label_imagem.setPixmap(self.perfil_60)
        perfil_de_aluminio.show()
        documentos_de_pecas_menu.hide()


################################ TELA PERFIL DE ALUMÍNIO ################################
class Documentos_de_peca_perfil_de_aluminio(QMainWindow, Ui_peca01): # Tela que mostra as informações doos perfis de alumínio.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_home.clicked.connect(self.home)
        self.botao_seta.clicked.connect(self.troca_imagem)

        # ******************************* VARIÁVEIS *******************************

        self.troca_pagina = 0

    # ******************************* FUNÇÕES DA CLASSE *******************************

    def home(self): # Função que volta para o menu documentos.
        documentos_de_pecas_menu.show()
        perfil_de_aluminio.hide()

    def troca_imagem(self): # Função que troca as imagens dos perfis.
        if self.troca_pagina == 1:
            self.label_imagem.move(230,90)
            self.label_imagem.setPixmap(documentos_de_pecas_menu.perfil_30_2)
            self.troca_pagina = 11

        elif self.troca_pagina == 11:
            self.label_imagem.move(110,110)
            self.label_imagem.setPixmap(documentos_de_pecas_menu.perfil_30)
            self.troca_pagina = 1

        if self.troca_pagina == 2:
            self.label_imagem.move(230,90)
            self.label_titulo.setText("PERFIS DE ALUMÍNIO DE 40, 45 E 50")
            self.label_imagem.setPixmap(documentos_de_pecas_menu.perfil_45_2)
            self.troca_pagina = 22

        elif self.troca_pagina == 22:
            self.label_imagem.move(110,110)
            self.label_titulo.setText("PERFIL DE ALUMÍNIO DE 45x45")
            self.label_imagem.setPixmap(documentos_de_pecas_menu.perfil_45)
            self.troca_pagina = 2

        if self.troca_pagina == 3:
            self.label_imagem.move(110,90)
            self.label_titulo.setText("PERFIS DE ALUMÍNIO DE 60x60")
            self.label_imagem.setPixmap(documentos_de_pecas_menu.perfil_60)
            self.troca_pagina = 33

        elif self.troca_pagina == 33:
            self.label_imagem.move(110,90)
            self.label_titulo.setText("PERFIL DE ALUMÍNIO DE 60x60 L")
            self.label_imagem.setPixmap(documentos_de_pecas_menu.perfil_60L)
            self.troca_pagina = 3


################################ TELA DE DIAGRAMA ELÉTRICO ################################
class Diagrama_eletrico(QMainWindow, Ui_documentos_diagrama_eletrico): # Tela que contém o diagrama elétrico da máquina.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_home.clicked.connect(self.home)
        self.botao_seta_direita.clicked.connect(self.proxima_pagina)
        self.botao_seta_esquerda.clicked.connect(self.pagina_anterior)

        # ******************************* VARIÁVEIS *******************************

        self.contador = 1  # Contador que representa o número da página
        self.pagina1 = QPixmap("imagens/Diagrama_eletrico_01.png")
        self.pagina2 = QPixmap("imagens/Diagrama_eletrico_02.png")
        self.pagina3 = QPixmap("imagens/Diagrama_eletrico_03.png")

        # ******************************* CONFIGURAÇÕES *******************************

        self.label_imagem.setPixmap(self.pagina1)

        # ******************************* FUNÇÕES DA CLASSE *******************************

    def home(self): # Função que volta para o menu documentos.
        documentos_menu.show()
        diagrama_eletrico.hide()

    def proxima_pagina(self): # Função que muda a imagem do diagrama e o número da página (Próxima Página).
        if self.contador < 3:
            self.contador += 1

        if self.contador == 2:
            self.label_imagem.setPixmap(self.pagina2)
            self.label_paginas.setText("PÁGINA 02/03")

        if self.contador == 3:
            self.label_imagem.setPixmap(self.pagina3)
            self.label_paginas.setText("PÁGINA 03/03")

    def pagina_anterior(self): # Função que muda a imagem do diagrama e o número da página (Página Anterior).
        if self.contador > 1:
            self.contador -= 1

        if self.contador == 1:
            self.label_imagem.setPixmap(self.pagina1)
            self.label_paginas.setText("PÁGINA 01/03")

        if self.contador == 2:
            self.label_imagem.setPixmap(self.pagina2)
            self.label_paginas.setText("PÁGINA 02/03")


################################ TELA DE MAPA DE PERIGOS E RISCOS ################################
class Mapa_de_riscos(QMainWindow, Ui_mapa_de_riscos): # Tela que contém o mapa de perigos e riscos e as assinaturas dos responsáveis pelo setor.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_home.clicked.connect(self.home)
        self.botao_seta.clicked.connect(self.muda_pagina)

        # ******************************* VARIÁVEIS *******************************

        self.mapa_de_riscos_01 = QPixmap("imagens/Mapa_de_riscos_01.png")
        self.mapa_de_riscos_02 = QPixmap("imagens/Mapa_de_riscos_02.png")
        self.mapa_de_riscos_03 = QPixmap("imagens/Mapa_de_riscos_03.png")
        self.pagina = 2

    # ******************************* FUNÇÕES DA CLASSE *******************************

    def home(self): # Função que volta para o menu documentos.
        documentos_menu.show()
        mapa_de_riscos.hide()

    def muda_pagina(self): # Função que muda a página.
        if self.pagina == 1:
            self.label_imagem.setPixmap(self.mapa_de_riscos_01)
            self.pagina = 2

        elif self.pagina == 2:
            self.label_imagem.setPixmap(self.mapa_de_riscos_02)
            self.pagina = 3

        elif self.pagina == 3:
            self.label_imagem.setPixmap(self.mapa_de_riscos_03)
            self.pagina = 1


################################ TELA DE MENU DE REGISTROS ################################
class Registros_menu(QMainWindow, Ui_Registros_menu): # Tela que contém todos as liberações realizadas.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************
        self.botao_home.clicked.connect(self.home)
        self.botao_historico_utilizacao_01.clicked.connect(self.resgistros_de_uso)
        self.botao_historico_utilizacao_02.clicked.connect(self.resgistros_de_uso)
        self.botao_relatorio_defeitos_01.clicked.connect(self.registros_defeitos)
        self.botao_relatorio_defeitos_02.clicked.connect(self.registros_defeitos)

        # ******************************* VARIÁVEIS *******************************

        self.defeitos = False

        # ******************************* FUNÇÕES DA CLASSE *******************************

    def home(self): # Função que volta para o menu 01.
        Menu01.show()
        registros_menu.hide()

    def resgistros_de_uso(self): # Função que lista todos os registros.
        self.defeitos = False
        registro_historico_utilizacao.load_registros()
        registro_historico_utilizacao.show()
        registros_menu.hide()

    def registros_defeitos(self): # Função que lista apenas as liberações que deram "NÃO OK".
        self.defeitos = True
        registro_historico_utilizacao.load_registros()
        registro_historico_utilizacao.show()
        registros_menu.hide()


################################ TELA DE HISTÓRICO DE UTILIZAÇÃO  ################################
class Registro_historico_utilizacao(QMainWindow, Ui_cadastros_historico_utilizacao): # Tela que mostra o histórico de quem e quando foi utilizada a máquina.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_voltar.clicked.connect(self.voltar)
        self.botao_analisar.clicked.connect(self.analisar)

        # ******************************* CONFIGURAÇÕES *******************************

        self.load_registros()

        # ******************************* FUNÇÕES DA CLASSE *******************************
    def analisar(self): # Função responsável por abrir a ficha da liberação selecionada pelo usuário.
        self.load_registros() # Carrega os registros

        try: # Pega os dados da linha selecionada.
            index = (self.tabela_utilizacao.selectionModel().currentIndex())
            row = self.tabela_utilizacao.currentItem().row()
            self.nome = index.sibling(row, 0).data()
            self.edv = index.sibling(row, 1).data()
            self.data = index.sibling(row, 2).data()
            self.horario = index.sibling(row, 3).data()
            self.resultado = index.sibling(row, 5).data()

        except Exception as erro:
            print(erro)

        if self.resultado == "NÃO OK": # Se a linha selecionada for um registro "NÃO OK":
            try:
                self.informacoes = banco_dados.retorna_descricao_registro(self.edv,self.horario,self.data,self.resultado) # Retorna os dados sobre a liberação selecionada (Data, Hora, Descrição...)

            except Exception as erro:
                print(erro)

            relatos_liberacao.label_nome.setText(f"NOME: {self.nome}")
            relatos_liberacao.label_data.setText(self.data)
            relatos_liberacao.label_periodo.setText(self.horario)

            try:
                relatos_liberacao.label_itens_nao_conformes.setText(self.informacoes[1])
                relatos_liberacao.lineEdit_descricao.setText(self.informacoes[0])

            except Exception as erro:
                print(erro)

            relatos_liberacao.voltar_registros_ou_liberacao = True
            relatos_liberacao.botao_finalizar.setDisabled(True)
            relatos_liberacao.show()
            registro_historico_utilizacao.hide()

        else:
            pass

    def load_registros(self): # Função que carrega as configurações e dados da tabela de utilização.
        self.tabela_utilizacao.setColumnCount(6)
        self.tabela_utilizacao.setColumnWidth(0, 395)
        self.tabela_utilizacao.setColumnWidth(1, 150)
        self.tabela_utilizacao.setColumnWidth(2, 170)
        self.tabela_utilizacao.setColumnWidth(3, 180)
        self.tabela_utilizacao.setColumnWidth(4, 120)
        self.tabela_utilizacao.setColumnWidth(5, 180)
        self.tabela_utilizacao.setHorizontalHeaderLabels(["NOME", "EDV", "DATA", "HORA", "EXAME", "RESULTADO"])
        self.tabela_utilizacao.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Se o botão de historico de utilização for pressionado, chama todos os registros.
        if registros_menu.defeitos == False:
            try:
                self.registros = banco_dados.chama_registros()
                print(self.registros)

            except Exception as erro:
                print(erro)

        # Se o botão de historico de defeitos for pressionado, chama apenas os registros "NÃO OK".
        else:
            try:
                self.registros = banco_dados.chama_resgistros_nao_conformes()

            except Exception as erro:
                print(erro)

        self.tabela_utilizacao.setRowCount(len(self.registros))
        row = 0

        for x in self.registros:
            self.tabela_utilizacao.setItem(row, 0, QTableWidgetItem(str((x[1]))))
            self.tabela_utilizacao.setItem(row, 1, QTableWidgetItem(str((x[2]))))
            self.tabela_utilizacao.setItem(row, 2, QTableWidgetItem(str((x[3]))))
            self.tabela_utilizacao.setItem(row, 3, QTableWidgetItem((x[4])))
            self.tabela_utilizacao.setItem(row, 4, QTableWidgetItem((x[5])))
            self.tabela_utilizacao.setItem(row, 5, QTableWidgetItem((x[6])))
            row = row + 1

    def voltar(self): # Função que volta para o menu registros.
        self.load_registros()
        registros_menu.show()
        registro_historico_utilizacao.hide()


################################ TELA DE HISTÓRICO DE UTILIZAÇÃO  ################################
class Segundo_Menu(QMainWindow, Ui_Menu02):  # Tela do segundo menu, que contém manutenção e cadastros.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.Botao_Seta_Esquerda.clicked.connect(self.tela_anterior)
        self.Botao_Cadastros.clicked.connect(self.cadastros)
        self.Botao_Sair.clicked.connect(self.sair)
        self.Botao_Manutencao.clicked.connect(self.manutencao)

        # ******************************* VARIÁVEIS *******************************

        self.cadeado_fechado = QIcon("imagens/CADEADO_FECHADO.png")

        # ******************************* FUNÇÕES DA CLASSE *******************************

    def tela_anterior(self): # Função que volta para o menu 01.
        print(colaborador)
        Menu01.show()
        Menu02.hide()

    def cadastros(self): # Função que abre o menu de cadastros.
        cadastros_menu.load_tabela()
        cadastros_menu.show()
        Menu02.hide()

    def manutencao(self):  # Função que abre a tela de manutenção.
        manutencao.show()
        Menu02.hide()

    def sair(self): # Função de sair e que reconfigura todas as funções e telas para seu estado original.
        interface_menu_botoes.label_titulo.setText("<html><head/><body><p align=\"center\"><span style=\" color:#ffffff;\">BOTOEIRA</span></p></body></html>")
        interface_menu_botoes.label_caixa_de_texto.setText("             Clique nos números para verificar a respectiva \nfunção do botão ou chave seletora. \n")

        if Menu01.maquina_liberada == True: # Se a máquina foi liberada, escreve o horário que o colaborador terminou de utilizar a máquina.
            self.now = datetime.now()
            self.horario_saida = self.now.strftime("%H:%M")
            self.horario_saida = f"{liberacao_meio_ambiente.horario_liberacao} - {self.horario_saida}"

            try:
                self.ID_liberacao = str(liberacao_meio_ambiente.ID_Liberacao)

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
        #GPIO.output(Alimentacao_maquina, False)
        standby.show()
        Menu01.hide()
        Menu02.hide()

    def clear_checkboxes(self): # Desmarca todos os check_boxes para a próxima liberação.
        Menu01.maquina_liberada = False
        self.checkboxes = [liberacao_seguranca.checkBox_1, liberacao_seguranca.checkBox_2, liberacao_seguranca.checkBox_3, liberacao_seguranca.checkBox_4, liberacao_seguranca.checkBox_5,
                           liberacao_seguranca.checkBox_6, liberacao_seguranca.checkBox_7, liberacao_seguranca.checkBox_8, liberacao_seguranca.checkBox_9, liberacao_meio_ambiente.checkBox_1]
        for i in self.checkboxes:
            i.setChecked(False)
        Menu01.Botao_Liberar_Maquina.setIcon(self.cadeado_fechado)


################################ TELA DE MENU CADASTROS ################################
class Cadastros_menu(QMainWindow, Ui_cadastros_menu): # Tela de gerenciamento dos cadastros dos usuários, na qual é possível adicionar, editar e excluir.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_voltar.clicked.connect(self.home)
        self.botao_adicionar.clicked.connect(self.adicionar_usuario)
        self.botao_editar.clicked.connect(self.editar)

        # ******************************* VARIÁVEIS *******************************

        self.imagem_aprendiz2 = QPixmap("imagens\Aprendiz_03.png")
        self.imagem_meio_oficial2 = QPixmap("imagens\Meio_oficial_03.png")
        self.imagem_manutentor2 = QPixmap("imagens\Manutentor_03.png")
        self.imagem_responsavel2 = QPixmap("imagens\Responsavel_03.png")

        # ******************************* CONFIGURAÇÕES *******************************
        self.load_tabela()

    # ******************************* FUNÇÕES DA CLASSE *******************************

    def editar(self): # Função que abre e configura a tela de edição de usuário a partir da linha da tabela selecionada.
        self.load_tabela()

        try: # Coleta os dados da linha selecionada.
            index = (self.tabela.selectionModel().currentIndex())
            row = self.tabela.currentItem().row()
            self.nome = index.sibling(row, 0).data()
            self.edv = index.sibling(row, 1).data()
            self.classe = index.sibling(row, 2).data()
            self.ID = str(banco_dados.ID_User(self.edv))
            self.Data_Nasciento = banco_dados.Data_nascimento(self.ID)
            cadastros_menu_escolher_classe.alterar_classe = True
            self.ficha()

        except Exception as erro:
            print(erro)

    def ficha(self): # Configura a tela e as lineEdits com os dados do usuário.
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

    def load_tabela(self): # Carrega e configura a tabela de usuários com os dados do Banco de Dados.
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

    def adicionar_usuario(self): # Função de inicia o processo de adicionar usuário.
        cadastros_menu_leitor.adicionar = True
        cadastros_menu_escolher_classe.alterar_classe = False
        cadastros_menu_escolher_classe.show()
        cadastros_menu.hide()

    def home(self): # Função que volta para o Menu 02.
        Menu02.show()
        cadastros_menu.hide()


################################ TELA DE EDIÇÃO DE USUÁRIO  ################################
class Cadastros_menu_editar(QMainWindow, Ui_Editar_cadastro): # Tela na qual os dados do usuário podem ser alterados ou excluir o cadastro.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_cancelar.clicked.connect(self.home)
        self.botao_alterar_tag_cartao.clicked.connect(self.leitor)
        self.botao_atualizar.clicked.connect(self.atualizar)
        self.botao_alterar_classe.clicked.connect(self.mudar_classe)
        self.botao_excluir.clicked.connect(self.excluir_usuario)

        # ******************************* CONFIGURAÇÕES *******************************

        self.lineEdit_nome.setText("")
        self.lineEdit_data_nascimento.setText("")
        self.lineEdit_edv.setText("")
        self.lineEdit_nome.setPlaceholderText("NOME COMPLETO")
        self.lineEdit_edv.setPlaceholderText("EDV")
        self.lineEdit_data_nascimento.setPlaceholderText("DATA DE NASCIMENTO")

        # ******************************* FUNÇÕES DA CLASSE *******************************

    def leitor(self): # Função que abre a tela para alterar a tag do crachá.
        cadastros_menu_leitor.adicionar = False # Variável que é utilizada para adicionar ou alterar a tag do usuário.
        cadastros_menu.ficha()
        cadastros_menu_leitor.opcao = False
        cadastros_menu_leitor.show()
        cadastros_menu_editar.hide()

    def mudar_classe(self): # Função que inicia o processo de mudar a classe do usuário.
        cadastros_menu_escolher_classe.alterar_classe = True # Variável utilizada para alterar ou adicionar a a classe do usuário.
        cadastros_menu_escolher_classe.show()
        cadastros_menu_editar.hide()

    def home(self): # Função que volta para o menu de cadastros.
        cadastros_menu.show()
        cadastros_menu_editar.hide()

    def atualizar(self): # Função que atualiza os novos dados cadastrados nas lineEdits.
        self.nome = self.lineEdit_nome.text()
        self.data_nascimento = self.lineEdit_data_nascimento.text()
        self.data_nascimento = f"'{self.data_nascimento}'"
        self.edv = self.lineEdit_edv.text()

        try:
            banco_dados.atualizar_cadastro(self.nome, self.data_nascimento, self.edv, cadastros_menu.ID)
            self.colaborador = banco_dados.pesquisar_colaborador(standby.tag_cartao)[0]
            self.colaborador2 = self.colaborador.split(" ")
            self.classe = banco_dados.verifica_classe(standby.tag_cartao)
            Menu01.Label_Colaborador.setText(f'COLABORADOR: {self.colaborador2[0]} {self.colaborador2[-1]}')
            Menu01.Label_EDV.setText(f"EDV: {banco_dados.pesquisar_colaborador(standby.tag_cartao)[-1]}")
            Menu02.Label_Colaborador.setText(f'COLABORADOR: {self.colaborador2[0]} {self.colaborador2[-1]}')
            Menu02.Label_EDV.setText(f"EDV: {banco_dados.pesquisar_colaborador(standby.tag_cartao)[-1]}")
            cadastros_menu.show()
            cadastros_menu_editar.hide()
            cadastros_menu.edv = self.edv
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

    def excluir_usuario(self): # Função de excluir o cadastro de usuário.
        banco_dados.deleta_usuario(cadastros_menu.edv)
        cadastros_menu_editar.hide()
        cadastros_menu.show()
        cadastros_menu.load_tabela()


################################ TELA DE HISTÓRICO DE UTILIZAÇÃO  ################################
class Cadastros_menu_leitor(QMainWindow, Ui_Aproxime_cartao): # Tela de alterar ou adicionar a tag do cartão.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_cancelar.clicked.connect(self.cancelar)
        self.botao_registrar.clicked.connect(self.registrar)

        # ******************************* VARIÁVEIS *******************************

        self.adicionar = bool

        # ******************************* CONFIGURAÇÕES *******************************

        self.lineEdit_tag_cartao.setText("")
        self.lineEdit_tag_cartao.setFocus()

        # ******************************* FUNÇÕES DA CLASSE *******************************

    def cancelar(self): # Função de voltar.
        self.lineEdit_tag_cartao.clear()

        if self.adicionar == True: # Se for o processo de adicionar volta para a tela de adicionar.
            cadastros_menu_adicionar_usuario.show()
            cadastros_menu_leitor.hide()

        else: # Se for o processo de editar volta para a tela de editar usuario.
            cadastros_menu_editar.show()
            cadastros_menu_leitor.hide()

    def registrar(self): # Termina o processo de adicionar usuário ou apenas altera a tag do cartão se for o processo de editar.
        try:
            self.tag_cartao = self.lineEdit_tag_cartao.text()

            if not self.tag_cartao == "":

                if self.adicionar == True: # Adicionar usuário.
                    banco_dados.adicionar_cadastro(self.tag_cartao, cadastros_menu_adicionar_usuario.nome, cadastros_menu_adicionar_usuario.edv, cadastros_menu_adicionar_usuario.classe, cadastros_menu_adicionar_usuario.data_nascimento)

                    self.lineEdit_tag_cartao.setText("")
                    cadastros_menu_adicionar_usuario.lineEdit_edv.setText("")
                    cadastros_menu_adicionar_usuario.lineEdit_nome.setText("")
                    cadastros_menu_adicionar_usuario.lineEdit_data_nascimento.setText("")
                    self.lineEdit_tag_cartao.clear()
                    self.lineEdit_tag_cartao.setFocus()

                    usuario_registrado.show()
                    # AQUI FALTA O DELAY ENTRE AS TELAS
                    cadastros_menu.show()
                    usuario_registrado.hide()
                    cadastros_menu_leitor.hide()

                    cadastros_menu.load_tabela()

                else: # Alterar tag do cartão
                    self.lineEdit_tag_cartao.setFocus()
                    banco_dados.update_tag(self.tag_cartao, cadastros_menu_editar.lineEdit_edv.text())
                    self.lineEdit_tag_cartao.clear()
                    cadastros_menu.show()
                    cadastros_menu_leitor.hide()

            else:
                print("Tente novamente")

        except Exception as erro:
            print(erro)


################################ TELA DE ADICIONAR CADASTRO  ################################
class Cadastros_menu_escolher_classe(QMainWindow, Ui_cadastros_classes): # Tela de selecionar a classe do colaborador.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_voltar.clicked.connect(self.home)
        self.botao_aprendiz.clicked.connect(self.aprendiz)
        self.botao_meio_oficial.clicked.connect(self.meio_oficial)
        self.botao_manutentor.clicked.connect(self.manutentor)
        self.botao_responsavel.clicked.connect(self.responsavel)

        # ******************************* VARIÁVEIS *******************************

        self.imagem_aprendiz = QPixmap("imagens\Aprendiz_02.png")
        self.imagem_meio_oficial = QPixmap("imagens\Meio_oficial_02.png")
        self.imagem_manutentor = QPixmap("imagens\Manutentor_02.png")
        self.imagem_responsavel = QPixmap("imagens\Responsavel_02.png")
        self.alterar_classe = bool

        # ******************************* FUNÇÕES DA CLASSE *******************************

    def aprendiz(self): # Função de adicionar aprendiz.
        if self.alterar_classe == False:
            cadastros_menu_adicionar_usuario.classe = "Aprendiz"
            cadastros_menu_adicionar_usuario.label_imagem_classe.setPixmap(self.imagem_aprendiz)
            cadastros_menu_adicionar_usuario.show()
            cadastros_menu_escolher_classe.hide()

        else:
            try:
                banco_dados.alterar_classe("Aprendiz", cadastros_menu_editar.lineEdit_edv.text())
                cadastros_menu_editar.label_imagem_patente.setPixmap(cadastros_menu.imagem_aprendiz2)
                cadastros_menu_editar.show()
                cadastros_menu_escolher_classe.hide()
                cadastros_menu.load_tabela()

            except Exception as erro:
                print(erro)

    def meio_oficial(self): # Função de adicionar meio oficial.
        if self.alterar_classe == False:
            cadastros_menu_adicionar_usuario.classe = "Meio-Oficial"
            cadastros_menu_adicionar_usuario.label_imagem_classe.setPixmap(self.imagem_meio_oficial)
            cadastros_menu_adicionar_usuario.show()
            cadastros_menu_escolher_classe.hide()

        else:
            try:
                banco_dados.alterar_classe("Meio Oficial", cadastros_menu_editar.lineEdit_edv.text())
                cadastros_menu_editar.label_imagem_patente.setPixmap(cadastros_menu.imagem_meio_oficial2)
                cadastros_menu_editar.show()
                cadastros_menu_escolher_classe.hide()
                cadastros_menu.load_tabela()

            except Exception as erro:
                print(erro)

    def manutentor(self): # Função de adicionar manutentor.
        if self.alterar_classe == False:
            cadastros_menu_adicionar_usuario.classe = "Manutentor"
            cadastros_menu_adicionar_usuario.label_imagem_classe.setPixmap(self.imagem_manutentor)
            cadastros_menu_adicionar_usuario.show()
            cadastros_menu_escolher_classe.hide()

        else:
            try:
                banco_dados.alterar_classe("Manutentor", cadastros_menu_editar.lineEdit_edv.text())
                cadastros_menu_editar.label_imagem_patente.setPixmap(cadastros_menu.imagem_manutentor2)
                cadastros_menu_editar.show()
                cadastros_menu_escolher_classe.hide()
                cadastros_menu.load_tabela()

            except Exception as erro:
                print(erro)

    def responsavel(self): # Função de adicionar responsável.
        if self.alterar_classe == False:
            cadastros_menu_adicionar_usuario.classe = "Responsável"
            cadastros_menu_adicionar_usuario.label_imagem_classe.setPixmap(self.imagem_responsavel)
            cadastros_menu_adicionar_usuario.show()
            cadastros_menu_escolher_classe.hide()

        else:
            try:
                banco_dados.alterar_classe("Responsável", cadastros_menu_editar.lineEdit_edv.text())
                cadastros_menu_editar.label_imagem_patente.setPixmap(cadastros_menu.imagem_responsavel2)
                cadastros_menu_editar.show()
                cadastros_menu_adicionar_usuario.hide()
                cadastros_menu.load_tabela()

            except Exception as erro:
                print(erro)

    def home(self): # Função de voltar para menu de cadastros.
        cadastros_menu.show()
        cadastros_menu_escolher_classe.hide()


################################ TELA DE ADICIONAR OS DADOS DO NOVO USUÁRIO ################################
class Cadastros_menu_adicionar_usuario(QMainWindow, Ui_cadastros_adicionar_ficha01): # Tela de preencher os dados do novo usuário, Nome, Edv e Data de nascimento.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_cancelar.clicked.connect(self.home)
        self.botao_avancar.clicked.connect(self.cadastro)

        # ******************************* CONFIGURAÇÕES *******************************

        self.lineEdit_nome.setText("")
        self.lineEdit_data_nascimento.setText("")
        self.lineEdit_edv.setText("")
        self.lineEdit_nome.setPlaceholderText("NOME COMPLETO")
        self.lineEdit_edv.setPlaceholderText("EDV")
        self.lineEdit_data_nascimento.setPlaceholderText("DATA DE NASCIMENTO (XX/YY/ZZZZ)")

        # ******************************* FUNÇÕES DA CLASSE *******************************

    def cadastro(self): # Função que valida os dados escritos para passar para a tela do leitor.
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
            cadastros_menu_adicionar_usuario.hide()

    def home(self): #Função de voltar para a tela de escolher classes.
        cadastros_menu_escolher_classe.show()
        cadastros_menu_adicionar_usuario.hide()

################################ TELA DE USUÁRIO CADASTRADO ################################
class Usuario_registrado(QMainWindow, Ui_Usuario_registrado): # Tela que retorna que o usuário foi adicionado no banco. (Ainda não estamos usando, falta a thread)
    def __init__(self):
        super().__init__()
        super().setupUi(self)


################################ TELA DE MANUTENÇÃO ################################
class Manutencao(QMainWindow, Ui_Manutencao): # Tela de manutenção, na qual é possível fazer testes com os componentes eletrônicos e controlar o estado de manutenção da máquina.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_home.clicked.connect(self.home)
        self.botao_energizar_contator_1.clicked.connect(self.energizar_maquina)
        self.botao_energizar_contator_2.clicked.connect(self.energizar_maquina)
        self.botao_liberar_trava1.clicked.connect(self.liberar_trava)
        self.botao_liberar_trava2.clicked.connect(self.liberar_trava)
        self.botao_maquina_manutencao.clicked.connect(self.maquina_em_manutencao)

        # ******************************* VARIÁVEIS *******************************

        self.cadeado_normal = QIcon("imagens/CADEADO_FECHADO.png")
        self.cadeado_manutencao = QIcon("imagens/Cadeado_manutencao.png")

        # ******************************* CONFIGURAÇÕES *******************************

        self.painel_liberado = False
        self.painel_energizado = False

        if banco_dados.verifica_estado_de_manutencao(serra_de_perfil) == True:
            self.estado_manutencao = True

        else:
            self.estado_manutencao = False

        self.maquina_em_manutencao()

        # ******************************* FUNÇÕES DA CLASSE *******************************

    def energizar_maquina(self): # Função para energizar o contatorl, dessa forma, liberando a alimentação da máquina.
        if self.painel_energizado == False:
            self.painel_energizado = True
            self.label_raio.setStyleSheet("border-style: outset;\n" "color: rgb(0, 0, 0);\n" "border-color: rgb(0, 0, 0);\n" "border-width:6px;\n" "font: 75 34pt \"Bosch Sans Bold\";\n" "background-color: rgb(255,207,0);")
            self.botao_energizar_contator_2.setStyleSheet("border-style: outset;\n" "border-color: rgb(0, 0, 0);\n" "border-width:7px;\n" "border-radius: 0px;\n" "background-color: rgb(237, 0, 7);")
            #GPIO.output(Alimentacao_maquina, True)
        else:
            self.painel_energizado = False
            self.label_raio.setStyleSheet("border-style: outset;\n" "color: rgb(0, 0, 0);\n" "border-color: rgb(0, 0, 0);\n" "border-width:6px;\n" "font: 75 34pt \"Bosch Sans Bold\";\n" "background-color: rgb(255,255,255);")
            self.botao_energizar_contator_2.setStyleSheet("border-style: outset;\n" "border-color: rgb(0, 0, 0);\n" "border-width:7px;\n" "border-radius: 0px;\n" "background-color: rgb(255, 255, 255);")
            #GPIO.output(Alimentacao_maquina, False)

    def liberar_trava(self): # Função de liberar a trava do painel elétrico da máquina.
        if self.painel_liberado == False:
            self.painel_liberado = True
            self.botao_liberar_trava2.setStyleSheet("border-style: outset;\n" "border-color: rgb(0, 0, 0);\n" "border-width:7px;\n" "border-radius: 0px;\n" "background-color: rgb(237, 0, 7);")
            self.label_trava_solenoide.move(330, 565)
            #GPIO.output(trava_do_painel, True)
        else:
            self.painel_liberado = False
            self.botao_liberar_trava2.setStyleSheet("border-style: outset;\n" "border-color: rgb(0, 0, 0);\n" "border-width:7px;\n" "border-radius: 0px;\n" "background-color: rgb(255, 255, 255);")
            self.label_trava_solenoide.move(370, 565)
            #GPIO.output(trava_do_painel, False)

    def maquina_em_manutencao(self): # Função alterar o estado de manutenção da máquina.
        if self.estado_manutencao == False:
            banco_dados.estado_manutencao(self.estado_manutencao, serra_de_perfil)
            self.estado_manutencao = True # Variável estado de manutenção.

            Menu01.Botao_Liberar_Maquina.setIcon(self.cadeado_normal) #Configurações do botão de manutenção:
            Menu01.Botao_Liberar_Maquina.setIconSize(QtCore.QSize(220, 220))
            self.label_sim_nao.move(580, 500)
            self.botao_maquina_manutencao.move(790, 500)
            self.label_sim_nao.setText("NÃO")
            self.label_sim_nao.setStyleSheet("border-style: outset;\n" "color: rgb(0, 0, 0);\n" "border-color: rgb(0, 0, 0);\n" "border-width:6px;\n" "border-radius: 0px;\n" "\n" "font: 75 55pt \"Bosch Sans Bold\";\n" "background-color: rgb(0, 136, 74);")
            self.label_painel_eletrico.setStyleSheet("\n" "color: rgb(0, 0, 0);\n" "border-color: rgb(0, 0, 0);\n" "border-radius: 90px;\n" "font: 75 28pt \"Bosch Sans Bold\";\n" "background-color: rgb(138, 144, 151);")
            self.label_fundo_painel.setStyleSheet( "border-style: outset;\n" "color: rgb(0, 0, 0);\n" "border-color: rgb(0, 0, 0);\n" "border-width:6px;\n" "border-radius: 90px;\n" "font: 75 34pt \"Bosch Sans Bold\";\n" "background-color: rgb(138, 144, 151);")
            #GPIO.output(led_manutencao, False)

        else:
            banco_dados.estado_manutencao(self.estado_manutencao, serra_de_perfil)
            self.estado_manutencao = False # Variável estado de manutenção.

            Menu01.Botao_Liberar_Maquina.setIcon(self.cadeado_manutencao) #Configurações do botão de manutenção:
            Menu01.Botao_Liberar_Maquina.setIconSize(QtCore.QSize(231, 231))
            self.label_sim_nao.move(970, 500)
            self.botao_maquina_manutencao.move(580, 500)
            self.label_sim_nao.setText("SIM")
            self.label_sim_nao.setStyleSheet("border-style: outset;\n" "color: rgb(0, 0, 0);\n" "border-color: rgb(0, 0, 0);\n" "border-width:6px;\n" "border-radius: 0px;\n" "\n" "font: 75 55pt \"Bosch Sans Bold\";\n" "background-color: rgb(237, 0, 7);")
            self.label_painel_eletrico.setStyleSheet("\n" "color: rgb(0, 0, 0);\n" "border-color: rgb(0, 0, 0);\n" "border-radius: 90px;\n" "font: 75 28pt \"Bosch Sans Bold\";\n" "background-color: rgb(237, 0, 7);")
            self.label_fundo_painel.setStyleSheet("border-style: outset;\n" "color: rgb(0, 0, 0);\n" "border-color: rgb(0, 0, 0);\n" "border-width:6px;\n" "border-radius: 90px;\n" "font: 75 34pt \"Bosch Sans Bold\";\n" "background-color: rgb(237, 0, 7);")
            #GPIO.output(led_manutencao, True)

    def home(self): # Função que volta para o Menu 02.
        Menu02.show()
        manutencao.hide()


################################ TELA DE HISTÓRICO DE UTILIZAÇÃO  ################################
class Feliz_aniversario(QMainWindow, Ui_Feliz_aniversario): # Tela de aniversário caso seja aniversário do colaborador.
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        # ******************************* AÇÕES *******************************

        self.botao_obrigado.clicked.connect(self.sair)

        # ******************************* VARIÁVEIS *******************************

        self.patinho = QMovie("imagens/patinho.gif")
        self.confete = QMovie("imagens/confetti-10.gif")

        # ******************************* CONFIGURAÇÕES *******************************

        self.label_patinho.setMovie(self.patinho)
        self.label_gif.setMovie(self.confete)
        self.label_gif_2.setMovie(self.confete)
        self.patinho.start()
        self.confete.start()

        # ******************************* FUNÇÕES DA CLASSE *******************************

    def sair (self): # Função que fecha a tela de aniversário.
        Menu01.show()
        aniversario.hide()

# CONFIGURAÇÕES:
ap = QApplication(sys.argv)
ap.setStyle("Fusion")
banco_dados = Connection("Banco.db")
Menu01 = Primeiro_Menu()

# DECLARAÇÃO DOS NOMES DAS TELAS:
liberacao_seguranca = Liberacao_seguranca()
Menu02 = Segundo_Menu()
liberacao_atencao = Liberacao_atencao()
liberacao_meio_ambiente = Liberacao_meio_ambiente()
documentos_menu = Documentos_menu()
documentos_de_pecas_menu = Documentos_documentos_de_pecas_menu()
perfil_de_aluminio = Documentos_de_peca_perfil_de_aluminio()
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
cadastros_menu_escolher_classe = Cadastros_menu_escolher_classe()
cadastros_menu_adicionar_usuario = Cadastros_menu_adicionar_usuario()
usuario_registrado = Usuario_registrado()
registro_historico_utilizacao = Registro_historico_utilizacao()
manutencao = Manutencao()
standby = Standby()
relatos_liberacao = Relatos_liberacao()
aniversario = Feliz_aniversario()

standby.show() # Primeira tela que aparecerá.
sys.exit(ap.exec())