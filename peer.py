import socket, pickle, threading

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Cogitando uma Falha no Tracker
s.settimeout(5)

h = input("IP do Tracker: ")

# Função para Falar com o Servidor
def Tracker(data):
	try:
		s.sendto(pickle.dumps(data),(h,15000))
		d = s.recvfrom(1024)
		if d[1][0] == h and d[1][1] == 15000:
			return pickle.loads(d[0])
	except:
		return False

# Login e Senha
login = input("Login : ")
senha = input("Senha : ")
while Tracker(login+"@"+senha) != True:
	print("Login ou Senha Incorretos!")
	login = input("Login : ")
	senha = input("Senha : ")
print("Acesso Concedido!")

# Atualização de Dados
print("Atualizando Dados...")
peer = ""
list = ""
# Atualizar quem eu sou
while True:
	try:
		peer = Tracker("me")["me"]
		break
	except:
		pass
# Atualizar lista de Peers
while True:
	try:
		list = Tracker("list")["list"]
		break
	except:
		pass
print("Dados Atualizados!")

# Caracteristicas do pedaço do Shopping
sou = "" # Quem eu sou
estou = 0 # Que andar eu estou
id = 0 # Caso seja uma loja
limite = 0 # Limite de pessoas
total = 0 # Quantidade atual
print("O que eu sou?")
print("s - Shopping")
print("a - Andar")
print("l - Loja")
while sou != "s" and sou != "a" and sou != "l":
	sou = input("").lower()
if sou == "a" or sou == "l":
	print("Em qual andar eu estou?")
	while True:
		try:
			estou = int(input(""))
			break
		except:
			estou = 0
if sou == "l":
	print("Qual é o ID da loja?")
	while True:
		try:
			id = int(input(""))
			break
		except:
			id = 0
print("Qual é o seu limite de pessoas?")
while True:
	try:
		limite = int(input(""))
		break
	except:
		limite = 0
print("Peer Rodando!")

def RECEBER():
	global s, h, peer, list, sou, estou, id, limite, total, interrupt
	while True:
		try:
			d = s.recvfrom(1024)
			s.sendto(pickle.dumps("OK"),d[1])
			# Processar caso esteja na rede
			if pickle.dumps(d[1]) in list:
				data = pickle.loads(d[0])
				for x in data:
					if list[pickle.dumps(d[1])] < x:
						list[pickle.dumps(d[1])] = x
						# PROCESSAR MENSAGEM AQUI
						temp2 = ""
						for temp1 in data[x]:
							if temp1 == "entrou":
								temp2 = "entrou"
							if temp1 == "saiu":
								temp2 = "saiu"
						if temp2 == "entrou":
							if sou == "s" and data[x]['de'].split(";")[0] == "f":
								# Caso eu seja o Shopping mas passe do limite de pessoas
								# enviar um pacote informando que pessoas foram barradas
								if total+data[x]['entrou'] > limite:
									ENVIAR({"sou":data[x]['sou'],"saiu":data[x]['entrou'],"para":data[x]['de']})
								# Caso eu seja o Shopping eu Processo
								elif total+data[x]['entrou'] <= limite:
									total = total+data[x]['entrou']
							# Caso eu me identico como o mesmo Peer
							if data[x]['sou'].split(";")[0] == sou and data[x]['sou'].split(";")[1] == str(estou) and data[x]['sou'].split(";")[2] == str(id):
								if total+data[x]['entrou'] > limite:
									ENVIAR({"sou":data[x]['sou'],"saiu":data[x]['entrou'],"para":data[x]['de']}) # Mensagem de pessoas barradas
								elif total+data[x]['entrou'] <= limite:
									total = total+data[x]['entrou']
							# Caso eu seja de onde veio
							if data[x]['de'].split(";")[0] == sou and data[x]['de'].split(";")[1] == str(estou) and data[x].split(";")[2] == str(id):
								if total-data[x]['entrou'] < 0:
									ENVIAR({"sou":data[x]['sou'],"saiu":data[x]['entrou'],"para":data[x]['de']}) # Mensagem de que não é possivel
								elif total-data[x]['entrou'] >= 0:
									total = total-data[x]['entrou']
						elif temp2 == "saiu":
							# Caso eu seja o shopping e elas tenham saido
							if sou == "s" and data[x]['para'].split(";")[0] == "f":
								if total-data[x]['saiu'] < 0:
									ENVIAR({"sou":data[x]['sou'],"entrou":data[x]['saiu'],"de":data[x]['para']})
								elif total-data[x]['saiu'] >= 0:
									total = total-data[x]['saiu']
							# Caso eu seja de onde elas sairam
							if data[x]['sou'].split(";")[0] == sou and data[x]['sou'].split(";")[1] == str(estou) and data[x]['sou'].split(";")[2] == str(id):
								if total-data[x]['saiu'] < 0:
									ENVIAR({"sou":data[x]['sou'],"entrou":data[x]['saiu'],"de":data[x]['para']}) # Mensagem de pessoas barradas
								elif total-data[x]['saiu'] >= 0:
									total = total-data[x]['saiu']
							# Caso eu seja para onde as pessoas foram
							if data[x]['para'].split(";")[0] == sou and data[x]['para'].split(";")[1] == str(estou) and data[x]['para'].split(";")[2] == str(id):
								if total+data[x]['saiu'] > limite:
									ENVIAR({"sou":data[x]['sou'],"entrou":data[x]['saiu'],"de":data[x]['para']}) # Mensagem de pessoas barradas
								elif total+data[x]['saiu'] <= limite:
									total = total+data[x]['saiu']
						elif temp2 == "":
							if data == "OK":
								interrupt = 1
						print(data[x])
					else:
						break
			# Ignorar caso seja um pacote próprio
			elif d[1][0] == peer[0] and d[1][1] == peer[1]:
				pass
			# Caso seja uma atualização do Tracker
			elif d[1][0] == h and d[1][1] == 15000:
				for x in pickle.loads(d[0]):
					if x == "list":
						list = pickle.loads(d[0])["list"]
		except:
			pass

interrupt = 0

def ENVIAR(data):
	global s, h, peer, list, interrupt
	# Atualizando o pacote atual
	list[pickle.dumps(peer)]+=1
	for x in list:
		s.sendto(pickle.dumps({list[pickle.dumps(peer)]:data}),pickle.loads(x))
		d = s.recvfrom(1024)
		while True:
			if interrupt == 1:
				interrupt = 0
				break
			if pickle.loads(d[0]) == "OK" and d[1][0] == pickle.loads(x)[0] and d[1][1] == pickle.loads(x)[1]:
				break
			else:
				s.sendto(pickle.dumps({list[pickle.dumps(peer)]:data}),pickle.loads(x))
				d = s.recvfrom(1024)

threading.Thread(target=RECEBER, args=()).start()

while True:
	nova = input("")
	if nova == "help" or nova == "ajuda" or nova == "h":
		print("Lista de Comandos")
		print("help - para exibir lista de comandos")
		print("status - para visualizar quem eu sou na rede")
		print("saiu - para indicar que um numero de pessoas saiu")
		print("entrou - para indicar que um numero de pessoas entrou")
		print("peer - para ver qual peer eu sou")
		print("peers - para ver lista de peers")
	if nova == "status":
		if sou == "s":
			print("Eu sou o Shopping")
		if sou == "a":
			print("Eu sou o "+str(estou)+"º andar")
		if sou == "l":
			print("Eu sou a loja "+str(id)+" localizada no "+str(estou)+"º andar")
		print("Temos "+str(total)+"/"+str(limite)+" pessoas")
	if nova == "peer":
		print("Eu sou o Peer: "+str(peer[0])+":"+str(peer[1]))
	if nova == "peers":
		print("Lista de Peers:")
		for x in list:
			print(pickle.loads(x))
	if nova == "entrou":
		temp1 = 0
		while temp1 <= 0:
			try:
				temp1 = int(input(">>"))
			except:
				pass
		print("De onde?")
		print("f - Fora")
		print("a - Andar")
		print("l - Loja")
		temp2 = ""
		while temp2 != "f" and temp2 != "a" and temp2 != "l":
			try:
				temp2 = input("").lower()
			except:
				pass
		temp3 = 0
		if temp2 == "a" or temp2 == "l":
			print("De qual andar?")
			while temp3 <= 0:
				try:
					temp3 = int(input(""))
				except:
					pass
		temp4 = 0
		if temp2 == "l":
			print("Qual id da loja?")
			while temp4 <= 0:
				try:
					temp4 = int(input(""))
				except:
					pass
		if total+temp1 > limite:
			print("Passou do Limite")
		else:
			total = total+temp1
			ENVIAR({"sou":sou+";"+str(estou)+";"+str(id),"entrou":temp1,"de":temp2+";"+str(temp3)+";"+str(temp4)})
	if nova == "saiu":
		temp1 = 0
		while temp1 <= 0:
			temp1 = int(input(">>"))
		print("Para onde?")
		print("f - Fora")
		print("a - Andar")
		print("l - Loja")
		temp2 = ""
		while temp2 != "f" and temp2 != "a" and temp2 != "l":
			try:
				temp2 = input("").lower()
			except:
				pass
		temp3 = 0
		if temp2 == "a" or temp2 == "l":
			print("De qual andar?")
			while temp3 <= 0:
				try:
					temp3 = int(input(""))
				except:
					pass
		temp4 = 0
		if temp2 == "l":
			print("Qual id da loja?")
			while temp4 <= 0:
				try:
					temp4 = int(input(""))
				except:
					pass
		if total-temp1 < 0:
			print("Não temos esse numero de pessoas")
		else:
			total = total-temp1
			ENVIAR({"sou":sou+";"+str(estou)+";"+str(id),"saiu":temp1,"para":temp2+";"+str(temp3)+";"+str(temp4)})

# A variavel list é uma biblioteca, onde a informação primeira é a localização do peer
# e a informação que ela guarda é a quantidade de pacotes que ela já enviou pela rede,
# assim se torna possivel saber qual pacote ela está enviando atualmente, e diferenciar
# de pacotes que já foram enviados anteriormente.

"""
ERROS:
- Não modifique informações pelo peer Shopping! Outros Peers não processam mensagens dele
- Andares podem não processar quando uma loja modifica informações dele próprio
FAZER:
- Barramento por parte de shopping, lojas e andares
"""