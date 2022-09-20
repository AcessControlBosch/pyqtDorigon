import sqlite3

banco = sqlite3.connect("Banco.db")

cursor = banco.cursor()

nome01 = "Will"
classe = "Aprendiz"
edv = 92895606
id_cartao = "009"



#cursor.execute("INSERT INTO Dados (ID_Cartao, Nome, Classe, EDV)  VALUES(004,'Gaby','Aprendiz',92896209)") #inserir Dados
#cursor.execute("INSERT INTO Dados (ID_Cartao, Nome, Classe, EDV)  VALUES ('"+id_cartao+"','"+nome01+"','"+classe+"',"+str(edv)+")") #inserir Dados
#cursor.execute(("DELETE FROM Dados WHERE ID = 4 "))
#cursor.execute("UPDATE Dados Set ID_Cartao = '003' WHERE ID = 3") #atualizar Dados

banco.commit()
#jaburu = cursor.fetchone("SELECT Nome FROM Dados WHERE ID = 2")

cursor.execute("SELECT Nome FROM Dados WHERE ID = 1")
 #cursor.execute("SELECT * FROM Dados")
nome = cursor.fetchone()
cursor.close()
print(nome[0])

#print(jaburu)

class funcoes_banco:
    def adicionar(self, ):

