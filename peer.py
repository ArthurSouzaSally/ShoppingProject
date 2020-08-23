
import socket, pickle, threading, time, random

h = input("Informe o IP do Tracker: ")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(5)

def Tracker(data):
	global s, h
	s.sendto(pickle.dumps(data),(h,15000))
	data = s.recvfrom(1024)
	while data[1][0] != h or data[1][1] != 15000:
		s.sendto(pickle.dumps(data),(h,15000))
		data = s.recvfrom(1024)
	return pickle.loads(data[0])

print("Conectando ao Servidor...")
login = input("Login: ")
senha = input("Senha: ")
while Tracker(login+"@"+senha) == False:
	print("Login ou Senha Incorretos")
	login = input("Login: ")
	senha = input("Senha: ")
print("Login Confirmado!")

print("Atualizando Informações...")
peer = "",0
while peer[0] == "" and peer[1] == 0:
	try:
		peer = Tracker("peer")["peer"]
	except:
		peer = "",0
peers = {}
while len(peers) == 0:
	try:
		peers = Tracker("list")["list"]
	except:
		peers = {}
print("Informações Atualizadas!")

print("Quem eu Sou?")
print("s - Shopping")
print("a - Andar")
print("l - Loja")
sou = input("").lower()
while sou != "s" and sou != "l" and sou != "a":
	print("Valor incorreto!")
	sou = input("").lower()
estou = 0
if sou == "l" or sou == "a":
	print("Em qual andar eu estou?")
	while True:
		try:
			estou = int(input(""))
			while estou < 0:
				print("Numero Possitivo, por favor")
				estou = int(input(""))
			break
		except:
			pass
id = 0
if sou == "l":
	print("Qual o ID da loja?")
	while True:
		try:
			id = int(input(""))
			while id < 0:
				print("Numero Possitivo, por favor")
				id = int(input(""))
			break
		except:
			pass
atual = 0
limite = 0
print("Qual o limite de pessoas da area?")
while True:
	try:
		limite = int(input(""))
		while limite < 0:
			print("Não pode existir um limite negativo")
			limite = int(input(""))
		break
	except:
		pass

# FAZER AQUI UM MODO SIMULADOR
sim = ""
print("Ativar modo Simulador?(y/s - sim , n - não)")
while sim != "s" and sim != "y" and sim != "n":
	try:
		sim = input("").lower()
	except:
		sim = ""

print("Peer Rodando!")
# Mensagem enviada do Peer
pEnviar = ""

def RECEBER():
	global s, h, peer, peers, pEnviar, sou, estou, id, atual, limite
	while True:
		# Enviar Pacotes para Outros Peers
		try:
			for x in peers:
				s.sendto(pickle.dumps({peers[pickle.dumps(peer)]:pEnviar}),pickle.loads(x))
		except:
			pass
		# Receber Pacotes
		try:
			d = s.recvfrom(1024)
			data = pickle.loads(d[0])
			if d[1][0] == h and d[1][1] == 15000:
				# Mensagem do Tracker
				try:
					for x in data:
						if x == "peer":
							peer = data["peer"]
						if x == "list":
							# Modificar Atualização de Peers
							novo = data["list"]
							for n in novo:
								if n in peers:
									pass
								else:
									peers[n] = 0
				except:
					pass
			elif d[1][0] == peer[0] and d[1][1] == peer[1]:
				pass # É uma mensagem que eu mesmo enviei
			else:
				# Isso são mensagens vindas de outros peers
				n = 0
				for x in peers:
					if d[1][0] == pickle.loads(x)[0] and d[1][1] == pickle.loads(x)[1]:
						n = 1
				if n == 1:
					for x in data:
						if x > peers[pickle.dumps(d[1])]:
							peers[pickle.dumps(d[1])] = x
							data = data[x]
					for x in data:
						if x == "entrou":
							n = 2
						if x == "saiu":
							n = 3
				if n == 2: # Entrou
					# Caso eu seja o shopping, alguem entrou no shopping
					if sou == "s" and data["de"].split(";")[0] == "f":
						if atual+data["entrou"] <= limite:
							atual = atual+data["entrou"]
						else:
							pEnviar = {"saiu":data["entrou"],"de":data["para"],"para":data["de"]}
							peers[pickle.dumps(peer)]+=1
					# Caso eu seja de onde veio as pessoas, então alguem saiu daqui
					if sou == data["de"].split(";")[0] and estou == int(data["de"].split(";")[1]) and id == int(data["de"].split(";")[2]):
						if atual-data["entrou"] >= 0:
							atual = atual-data["entrou"]
						else:
							pEnviar = {"entrou":data["entrou"],"de":data["para"],"para":data["de"]}
							peers[pickle.dumps(peer)]+=1
					# Caso eu seja para onde foram as pessoas, então alguem entrou aqui
					if sou == data["para"].split(";")[0] and estou == int(data["para"].split(";")[1]) and id == int(data["para"].split(";")[2]):
						if atual+data["entrou"] <= limite:
							atual = atual+data["entrou"]
						else:
							pEnviar = {"saiu":data["entrou"],"de":data["para"],"para":data["de"]}
							peers[pickle.dumps(peer)]+=1
				if n == 3: # Saiu
					# Caso eu seja o shopping e alguem tenha saido para fora
					if sou == "s" and data["para"].split(";")[0] == "f":
						if atual-data["saiu"] >= 0:
							atual = atual - data["saiu"]
						else:
							pEnviar = {"entrou":data["saiu"],"de":data["para"],"para":data["de"]}
							peers[pickle.dumps(peer)]+=1
					# Caso eu seja de onde veio as pessoas, então alguem saiu daqui
					if sou == data["de"].split(";")[0] and estou == int(data["de"].split(";")[1]) and id == int(data["de"].split(";")[2]):
						if atual-data["saiu"] >= 0:
							atual = atual - data["saiu"]
						else:
							pEnviar = {"entrou":data["saiu"],"de":data["para"],"para":data["de"]}
							peers[pickle.dumps(peer)]+=1
					# Caso eu seja para onde foram as pessoas, alguem entrou aqui
					if sou == data["para"].split(";")[0] and estou == int(data["para"].split(";")[1]) and id == int(data["para"].split(";")[2]):
						if atual+data["saiu"] <= limite:
							atual = atual+data["saiu"]
						else:
							pEnviar = {"saiu":data["saiu"],"de":data["para"],"para":data["de"]}
							peers[pickle.dumps(peer)]+=1
		except:
			pass

threading.Thread(target=RECEBER, args=()).start()

if sim == "n":
	while True:
		a = input("")
		if a.lower() == "help" or a.lower == "ajuda" or a.lower == "socorro":
			print("Lista de Comandos:")
			print("help -> Para Mostrar essa Lista de Comandos")
			print("peer -> Para Mostrar quem eu sou na Rede")
			print("peers -> Para Mostrar Lista de Peers e quantos pacotes foram enviados por cada")
			print("")
		elif a.lower() == "peer":
			print(peer)
		elif a.lower() == "peers":
			print("Lista de Peers:")
			for x in peers:
				print(str(pickle.loads(x))+" : "+str(peers[x]))
		elif a.lower() == "status":
			if sou == "s":
				print("Eu sou o Shopping")
			if sou == "a":
				print("Eu sou o "+str(estou)+"º Andar")
			if sou == "l":
				print("Sou uma Loja no "+str(estou)+"º Andar, com o ID "+str(id))
			print("Com um total de "+str(atual)+"/"+str(limite)+" pessoas")
		elif a.lower() == "entrou":
			# Informações para outros peers
			temp1 = 0
			while temp1 <= 0:
				try:
					temp1 = int(input(">>"))
				except:
					temp1 = 0
			print("De onde?")
			print("f - de fora")
			print("a - andar")
			print("l - loja")
			temp2 = ""
			while temp2 != "f" and temp2 != "a" and temp2 != "l":
				try:
					temp2 = input("")
				except:
					temp2 = ""
			temp3 = 0
			if temp2 == "a" or temp2 == "l":
				print("De qual andar?")
				while temp3 <= 0:
					try:
						temp3 = int(input(""))
					except:
						temp3 = 0
			temp4 = 0
			if temp2 == "l":
				print("Qual o ID da loja?")
				while temp4 <= 0:
					try:
						temp4 = int(input(""))
					except:
						temp4 = 0
			# Informações Locais
			if atual+temp1 <= limite:
				atual = atual+temp1
				pEnviar = {"entrou":temp1,"de":temp2+";"+str(temp3)+";"+str(temp4),"para":sou+";"+str(estou)+";"+str(id)}
				peers[pickle.dumps(peer)]+=1
			else:
				print("Numero Excede o limite de pessoas")
		elif a.lower() == "saiu":
			# Informações Locais
			# Informações para outros peers
			temp1 = 0
			while temp1 <= 0:
				try:
					temp1 = int(input(">>"))
				except:
					temp1 = 0
			print("Para onde?")
			print("f - para fora")
			print("a - andar")
			print("l - loja")
			temp2 = ""
			while temp2 != "f" and temp2 != "a" and temp2 != "l":
				try:
					temp2 = input("")
				except:
					temp2 = ""
			temp3 = 0
			if temp2 == "a" or temp2 == "l":
				print("Para qual andar?")
				while temp3 <= 0:
					try:
						temp3 = int(input(""))
					except:
						temp3 = 0
			temp4 = 0
			if temp2 == "l":
				print("Qual o ID da loja?")
				while temp4 <= 0:
					try:
						temp4 = int(input(""))
					except:
						temp4 = 0
			if atual-temp1 >= 0:
				atual = atual-temp1
				pEnviar = {"saiu":temp1,"de":sou+";"+str(estou)+";"+str(id),"para":temp2+";"+str(temp3)+";"+str(temp4)}
				peers[pickle.dumps(peer)]+=1
			else:
				print("Numero é menor do que tem presente")
else:
	while True:
		time.sleep(1)
		if random.randint(0,1) == 0: # Entrou
			temp1 = random.randint(1,limite)
			temp2 = random.randint(0,2)
			temp3 = 0
			if temp2 == 1 or temp2 == 2:
				temp3 = random.randint(1,5)
			temp4 = 0
			if temp2 == 2:
				temp4 = random.randint(1,100)
			# Atualizar Informações aqui
			if temp2 == 0:
				temp2 = "f"
			elif temp2 == 1:
				temp2 = "a"
			elif temp2 == 2:
				temp2 = "l"
			if atual+temp1 <= limite:
				atual = atual+temp1
				pEnviar = {"entrou":temp1,"de":temp2+";"+str(temp3)+";"+str(temp4),"para":sou+";"+str(estou)+";"+str(id)}
				peers[pickle.dumps(peer)]+=1
		else: # Saiu
			temp1 = random.randint(1,limite)
			temp2 = random.randint(0,2)
			temp3 = 0
			if temp2 == 1 or temp2 == 2:
				temp3 = random.randint(1,5)
			temp4 = 0
			if temp2 == 2:
				temp4 = random.randint(1,100)
			# Atualizar Informações aqui
			if temp2 == 0:
				temp2 = "f"
			elif temp2 == 1:
				temp2 = "a"
			elif temp2 == 2:
				temp2 = "l"
			if atual-temp1 >= 0:
				atual = atual-temp1
				pEnviar = {"saiu":temp1,"de":sou+";"+str(estou)+";"+str(id),"para":temp2+";"+str(temp3)+";"+str(temp4)}
				peers[pickle.dumps(peer)]+=1
		if sou == "s":
			print("Eu sou o Shopping")
		if sou == "a":
			print("Eu sou o "+str(estou)+"º Andar")
		if sou == "l":
			print("Sou uma Loja no "+str(estou)+"º Andar, com o ID "+str(id))
		print("Com um total de "+str(atual)+"/"+str(limite)+" pessoas")

print("FIM")








