import mysql.connector
import time
import serial
import smtplib
from email.mime.text import MIMEText
from flask import *
import sys




'''
Unica classe do sistema que conversa diretamente com o hardware
'''
class ControladorSensores():
	def __init__(self, serialPort = "/dev/ttyACM0"):
		self.port = serialPort
		self.count = 0
		self.cursor = None
		self.con = None
		self.alertaGas = False
		self.alertaTemp = False
	
	def iniciaConexaoSerial(self):
		comport = None
		try:
			comport = serial.Serial(self.port, 9600)
		except Exception as e:
			print ("A placa nao esta conectada ou esta na porta errada ou o usuario nao tem as permissoes necessairas. Erro: ")
			print (e)
			exit()
		return comport

	def readTemp(self): 
		comport = self.iniciaConexaoSerial()
		
		PARAM_ASCII=str(chr(72)) #equivalente ao caractere H
		time.sleep(1.0)
		comport.write(PARAM_ASCII)
		time.sleep(1.0)

		line = comport.readline()
		# Fechando conexao serial
		comport.close()
		
		print("Foi lido de temp: %sC") % (line.rstrip())

		return line.rstrip()

		
	
	def readGas(self):
		comport = self.iniciaConexaoSerial()	 
		PARAM_CARACTER='G'
		PARAM_ASCII=str(chr(71)) 
		time.sleep(1.0) # nao sei se precisa mesmo
		comport.write(PARAM_ASCII)
		time.sleep(1.0)
		line = comport.readline()
		# Fechando conexao serial
		comport.close()
		print("Foi lido de gas: %s") % (line.rstrip())
		return line.rstrip()


'''
classe que faz as interacoes com o banco de dados
'''
class ControladorBanco():
	def __init__(self, host, user, passwd, database):
	    self.host = host
	    self.user = user
	    self.passwd = passwd
	    self.database = database
	    self.con = None
	    self.cursor = None
	    self.count = 0

	def iniciaConexaoDB(self):
		try:
			self.con = mysql.connector.connect(
		  		host=self.host,
		  		user=self.user,
		  		passwd=self.passwd,
		  		database=self.database
			)
			self.cursor = self.con.cursor()
		except Exception as e:
			print ("Nao foi possivel acessar o banco de dados. ")
			print (e)
	def fechaConexao(self):
		self.cursor.close()
		self.con.close()
	
	def sendLeituras(self, temp, gas):
		self.count+=1
		print(self.count)

		self.iniciaConexaoDB()
		sql = "INSERT INTO leituras  values('%s','%s','%s')" % (self.count, temp, gas)
		self.cursor.execute(sql)
		self.con.commit()
		self.fechaConexao()

	def geraBanco(self):
		self.iniciaConexaoDB()
		sql = "INSERT INTO leituras values()"

	def getLeituras(self):
		#preciso ver quais leituras vou pegar quando tiver muitos dados no banco 
		#pesquisar como selecionar as ultimas 1000 entradas em mysql
		self.iniciaConexaoDB()
		self.cursor.execute("SELECT * FROM leituras ORDER BY id DESC LIMIT 200")
		leituras = self.cursor.fetchall()
		self.fechaConexao()
		return leituras
	#vou precisar dessa funcao para fazer a atualizacao em tempo real da pagina
	def getUltimaLeitura(self):
		self.iniciaConexaoDB()
		self.cursor.execute("SELECT * FROM leituras ORDER BY id DESC LIMIT 1")
		leituras = self.cursor.fetchone()
		self.fechaConexao()
		return leituras



'''
Funcoes utilitarias
'''
def sendEmail():
	user = 'gabrieljsssss@gmail.com'
	pwd = 'Ga92051831'
	recipient = 'gabrieljsss@poli.ufrj.br'
	subject = 'Alerta'
	body = "ALERTA DE INCENDIO. POR FAVOR AGIR RAPIDO E ENTRAR EM CONTATO COM AS AUTORIDADES. ESSA MENSAGEM NAO E UM TREINAMENTO. "
	FROM = user
	TO = recipient if isinstance(recipient, list) else [recipient]
	SUBJECT = subject
	TEXT = body

	message = """From: %s\nTo: %s\nSubject: %s\n\n%s
	""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
	try:
	    server = smtplib.SMTP("smtp.gmail.com", 587)
	    server.ehlo()
	    server.starttls()
	    server.login(user, pwd)
	    server.sendmail(FROM, TO, message)
	    server.close()
	    print('Email enviado')
	except:
		print("Falha ao enviar email")


def run(dbm, cs):
	temperatura = cs.readTemp()
	gas = cs.readGas()

	print ("temperatura: %s C") % (temperatura)
	print ("Niveis de gases: %s") % (gas)
	dbm.sendLeituras(temperatura, gas)

	#fazer assim ou ficar calculando a tangente o tempo todo?
	if int(temperatura) > 50 or int(gas) > 100:
		sendEmail()

def normalizeFile(data):
	c = 0
	xaxis = []
	for i in data:
		xaxis.append(c)
		data[c] = int(i.strip("\n"))
		c+=1
	return data	
def sendLogFilesToDB():
    dbm = ControladorBanco("localhost", "root", "", "sensor")
    file = open("log/log-gas-3.txt", "r")
    file2 = open("log/log-temp-1.txt", "r")
    data = file.readlines()
    data2 = file2.readlines()
    data = normalizeFile(data)
    data2 = normalizeFile(data2)
    count = 0
    for i in data:
    	dbm.sendLeituras(data2[count], i)
    	count+=1



if __name__ == "__main__": 
	sendEmail()
	control = ControladorSensores()
	dbm = ControladorBanco("localhost", "root", "", "sensor")
	while True:
		run(dbm, control)




