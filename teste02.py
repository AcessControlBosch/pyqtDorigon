import sqlite3
from datetime import datetime, date
from locale import setlocale, LC_ALL
class Connection:

    # Construtor da class faz a conexão
    def __init__(self, db):
        self.banco = sqlite3.connect(db)

    # Veriica se o usuario esta no banco de dados
    def pesquisar_colaborador(self, idcard):
        cursor = self.banco.cursor()
        # função do SQL de seleção de dados
        consulta = f"SELECT Nome, ID_Usuario, EDV FROM Usuarios WHERE ID_Card ='{int(idcard)}'"
        cursor.execute(consulta)
        dados = cursor.fetchall()

        cursor.close()
        print(dados)
        print(dados[0])
        return dados[0]

    def coleta_dados(self): #Retorna o Nome, EDV e a Classe para criar a tabela da tela cadastros_menu
        cursor = self.banco.cursor()
        consulta = ("SELECT Nome, EDV, Classe FROM Usuarios")
        cursor.execute(consulta)
        lista = cursor.fetchall()
        cursor.close()
        print("lista:", lista)
        return lista

    def edv(self, idcard): #Não estou usando essa função por enquanto
        cursor = self.banco.cursor()
        consulta = f"SELECT EDV FROM Usuarios WHERE ID_Card ='{int(idcard)}'"
        cursor.execute(consulta)
        edv = cursor.fetchone()
        cursor.close()
        print(edv)
        return edv[0]

    def adicionar_cadastro(self, tag_cartao, nome, edv, classe, data_nascimento):
        cursor = self.banco.cursor()
        adicionar = ("INSERT INTO Usuarios (ID_Card, Nome, EDV, Classe, Data_Nascimento)  VALUES ('" + tag_cartao + "','" + nome + "','" + classe + "','" + edv + "','" + data_nascimento +"')")  # inserir Dados
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

    def Data_nascimento(self, ID): #Estou usando essa função por enquanto
        cursor = self.banco.cursor()
        consulta = f"SELECT Data_Nascimento FROM Usuarios WHERE ID_Usuario ='{ID}'"
        cursor.execute(consulta)
        Data_Nascimento = cursor.fetchone()
        cursor.close()
        print(Data_Nascimento)
        return Data_Nascimento[0]

    def chama_registros(self):  # Retorna o Nome, EDV e a Classe para criar a tabela da tela cadastros_menu
        cursor = self.banco.cursor()
        consulta = ("SELECT * FROM Registros")
        cursor.execute(consulta)
        lista = cursor.fetchall()
        cursor.close()
        print("lista:", lista)
        return lista

    def deleta_usuario (self, EDV):
        cursor = self.banco.cursor()
        deletar = f"DELETE FROM Usuarios WHERE EDV = '{EDV}'"
        cursor.execute(deletar)
        self.banco.commit()
        cursor.close()
        return print("Deletou")



banco_dados = Connection("Banco.db")
ID = "1"
tag = "465240"
nome ="Gabriel Batista Dorigon"
edv = "a"
classe = "Aprendiz"
data_nascimento = "15/11/2002"

#banco_dados.adicionar_cadastro(tag, nome, str(edv), classe, data_nascimento)
#banco_dados.Data_nascimento(ID)

banco_dados.deleta_usuario(edv)





"""
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)

trava_do_painel = 12
Alimentacao_maquina = 16
led_manutencao = 15

GPIO.setup(Alimentacao_maquina, GPIO.OUT)
GPIO.setup(led_manutencao, GPIO.OUT)
GPIO.setup(trava_do_painel, GPIO.OUT)

GPIO.output(Alimentacao_maquina, False)
GPIO.output(led_manutencao, False)


GPIO.output(trava_do_painel, True)
sleep(10)
GPIO.output(trava_do_painel, False)"""


