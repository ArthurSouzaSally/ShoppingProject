
import socket, pickle, threading, time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(5)

ip = input("IP do Tracker: ")
port = 15000

# Enviar mensagens para o Servidor
def enviar(info):
	global s, ip, port
	s.sendto(pickle.dumps(info),(ip,port))
	while True:
		data = s.recvfrom(15000)
		if data[1][0] == ip and data[1][1] == port:
			return pickle.loads(data[0])
			break

# Atualizando informações de Peers da rede P2P
print("Atualizando informações...")
eu = ""
peers = ""
limite = 0
total = 0
while eu == "" and peers == "" and limite == 0:
	try:
		eu = enviar("oi")["ip"]
		try:
			peers = enviar("list")["list"]
			try:
				limite = enviar("limit")["limite"]
			except:
				limite = 0
		except:
			peers = ""
	except:
		eu = ""

# Verificando Login e Senha
while True:
	try:
		login = input("Informe o Login: ")
		senha = input("Informe a Senha: ")
		if enviar("@"+login+";"+senha)["login"]:
			break
		else:
			print("Login ou Senha Incorretas")
	except:
		print("Erro na Comunicação, Tente novamente")

# Variaveis para Determinar quem eu sou no Shopping
sou = ""
estou = 0
while sou != "s" and sou != "l" and sou != "a":
	try:
		print("s - Shopping")
		print("a - andar")
		print("l - Loja")
		sou = input("").lower()
	except:
		sou = ""
if sou == "a" or sou == "l":
	estou = 0
	while estou <= 0:
		print("Qual andar eu estou?")
		try:
			estou = int(input(""))
			break
		except:
			estou = 0

# Receber Pacotes e processar informações
def receber():
	global s, eu, peers, ip, port, limite, total, sou, estou
	while True:
		try:
			data = s.recvfrom(15000)
			# confirmar a entrega do pacote
			s.sendto(pickle.dumps("OK"),data[1])
			# mensagem do servidor:
			if data[1][0] == ip and data[1][1] == port:
				try:
					for x in pickle.loads(data[0]):
						if x == "ip":
							eu = pickle.loads(data[0])["ip"]
						if x == "list":
							peers = pickle.loads(data[0])["list"]
				except:
					pass
			# mensagem própria:
			elif data[1][0] == eu[0] and data[1][1] == eu[1]:
				pass
			# mensagem de outro peer:
			else:
				# verificar autenticidade
				n = 0
				for x in peers:
					if data[1][0] == pickle.loads(x)[0] and data[1][1] == pickle.loads(x)[1]:
						n = 1
				if n == 1:
					data = pickle.loads(data[0])
					try:
						d = data["saiu"]
						if d >= 0 and d <= limite:
							# analisar o data['sou'] para saber o que fazer
							total = d
					except:
						pass
					try:
						d = data["entrou"]
						if d >= 0 and d <= limite:
							# analisar o data['sou'] para saber o que fazer
							total = d
					except:
						pass
					print("Dados Atualizados")
		except:
			pass

threading.Thread(target=receber, args=()).start()

# Enviar mensagens para outros peers
def falar(info,tipo):
	global s, peers, estou, sou
	for x in peers:
		while True:
			try:
				s.sendto(pickle.dumps({tipo:info,"sou":str(estou)+sou}),pickle.loads(x))
				d = s.recvfrom(10000)
				if d[1][0] == pickle.loads(x)[0] and d[1][1] == pickle.loads(x)[1]:
					if pickle.loads(d[0]) == "OK":
						break
			except:
				pass

# Loop de Comandos
while True:
	i = input("")
	if i == "mPeer":
		print("Meu Peer: "+str(eu))
	elif i == "mPeers":
		print("Lista de Peers: ")
		for x in peers:
			print(pickle.loads(x))
	elif i == "status":
		print("Limite:      "+str(limite))
		print("Atualmente:  "+str(total))
		if sou == "s":
			print("Eu sou:      Shopping")
		elif sou == "a":
			print("Eu sou:      "+str(estou)+"º andar")
		elif sou == "l":
			print("Eu sou:      loja no "+str(estou)+"º andar")
	elif i == "help":
		print("Lista de Comandos:")
		print("mPeer -> Ver o meu Peer")
		print("mPeers -> Ver lista de Peers")
		print("status -> Ver Estado do Shopping")
		print("saiu -> Informar saída de pessoas")
		print("entrou -> Informar entrada de pessoas")
	elif i == "saiu":
		n = 0
		while n <= 0:
			try:
				n = int(input(">> "))
			except:
				n = 0
		# comparador
		if total >= n:
			total-=n
			falar(total,"saiu")
	elif i == "entrou":
		n = 0
		while n <= 0:
			try:
				n = int(input(">> "))
			except:
				n = 0
		# comparador
		if total+n <=limite:
			total+=n
			falar(total,"entrou")
	else:
		print("Comando não Reconhecido")

print("FIM")

"""
O que falta:
- Entradas para Funcionarios
- Hierarquia entre Andares, Lojas e Shopping
"""
