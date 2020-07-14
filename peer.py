
# As bibliotecas são:
  # socket - para fazer comunicação na rede
  # pickle - para transformar variaveis em bytes
  # threading - para executar funções em paralelo
  # time - para controle temporal
import socket, pickle, threading, time

# Criar um socket UDP usando IPv4
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Limitando o tempo de resposta do envio de pacotes UDP
s.settimeout(5)

# Receber o IP do Tracker
ip = input("IP do Tracker: ")
# Porta Padrão do Tracker
port = 15000

# Função que Envia informações para o Tracker e recebe uma resposta
def enviar(info):
	global s, ip, port
	while True:
		s.sendto(pickle.dumps(info),(ip,port))
		data = s.recvfrom(15000)
		if data[1][0] == ip and data[1][1] == port:
			return pickle.loads(data[0])
			break

# Informando ao Publico que as Informações estão sendo atualizadas
print("Atualizando informações...")
# Variavel 'eu' que guarda quem você é na rede
eu = ""
# Variavel 'peers' que guarda a lista dos peers atual
peers = ""
# Variavel 'limite' que guarda o limite de pessoas no shopping
limite = 0
# Variavel 'total' que guarda a quantidade atual de pessoas no shopping
total = 0
# Estrutura de Repetição para entrar em contato com o Servidor com a
# função anterior e só sai quando todas as informações estão atualizadas
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

# Verificando Login e Senha, quando as informações são confirmadas
# pelo Tracker com uma variavel boleana "True" então o peer pode
# prosseguir com o código
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

# Variavel para Determinar quem eu sou no Shopping
# "l" - Loja
# "a" - Andares
# "s" - Entrada do Shopping
sou = ""
# Variavel que determina o tipo de entrada no Shopping:
# "f" - Entrada do Shopping para Funcionarios
# "c" - Entrada para Clientes
de = ""
# Variavel que guarda em qual andar eu estou
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
de = ""
while de != "f" and de != "c":
	try:
		print("f - Funcionarios")
		print("c - Clientes")
		de = input("").lower()
	except:
		de = ""

# Função que entra em loop infinito, para receber pacotes da rede
# independente de onde venha o pacote, este é processado e avaliado
# para 3 casos: se o pacote é um que o próprio peer enviou, se foi
# enviado por outro peer, ou se foi enviado pelo tracker
def receber():
	global s, eu, peers, ip, port, limite, total, sou, estou
	while True:
		try:
			data = s.recvfrom(15000)
			# confirmar a entrega do pacote
			s.sendto(pickle.dumps("OK"),data[1])
			# Caso a mensagem seja enviada pelo servidor, devemos
			# avaliar qual é o tipo de informação que ele recebeu
			# poís um novo peer pode ter entrado e o tracker pode
			# estar atualizando a variavel 'peers' para que este
			# nó saíba quem enviou a mensagem.
			if data[1][0] == ip and data[1][1] == port:
				try:
					for x in pickle.loads(data[0]):
						if x == "ip":
							eu = pickle.loads(data[0])["ip"]
						if x == "list":
							peers = pickle.loads(data[0])["list"]
				except:
					pass
			# Caso este peer envie um pacote e ele acabe interceptando
			# o próprio pacote, não há a necessidade de se fazer nada,
			# mas o caso deve ser tratado para que não ocorram erros na
			# ultima parte.
			elif data[1][0] == eu[0] and data[1][1] == eu[1]:
				pass
			# Caso a mensagem seja diferente das duas anteriores, então
			# provavelmente ela foi enviada de outro peer presente na
			# rede, para isso:
			else:
				# Primeiramente precisamos verificar na variavel peers
				# se a mensagem veio de um peer existente na rede, quase
				# como se fosse uma autenticação de usuario.
				n = 0
				for x in peers:
					if data[1][0] == pickle.loads(x)[0] and data[1][1] == pickle.loads(x)[1]:
						n = 1
				# No caso do Usuario ter sido autenticado, ou seja a 
				# variavel 'n' é igual a 1 pois a mensagem veio de um
				# peer na rede, ele processa a informação.
				if n == 1:
					data = pickle.loads(data[0])
					try:
						d = data["saiu"]
						if d >= 0 and d <= limite:
							# analisar o data['sou'] para saber o que fazer
							# analisar o data['para'] para saber onde a pessoa foi
							total = d
					except:
						pass
					try:
						d = data["entrou"]
						if d >= 0 and d <= limite:
							# analisar o data['sou'] para saber o que fazer
							# analisar o data['para'] para saber onde a pessoa foi
							total = d
					except:
						pass
					print("Dados Atualizados")
		except:
			pass

# Aqui nós utilizamos a biblioteca threading para executar a 
# função RECEBER em paralelo, permitindo que o código funcione
# com varias coisas ao mesmo tempo.
threading.Thread(target=receber, args=()).start()

# Esta é uma função para enviar mensagens para outros peers,
# nela busca-se enviar mensagens para todos os peers dentro
# da rede, até mesmo para si próprio, evitando ao maximo que
# peers não recebam a mensagem.
def falar(info,tipo,saida):
	global s, peers, estou, sou, de
	# Acontece para todos os peers
	for x in peers:
		# Vai enviar a mensagem infinitas vezes até receber a confirmação de que o pacote foi entregue
		while True:
			# É preciso o try para tratar a possibilidade de uma falha no envio de mensagem
			try:
				s.sendto(pickle.dumps({tipo:info,"sou":str(estou)+sou+de,"para":saida}),pickle.loads(x))
				d = s.recvfrom(10000)
				if d[1][0] == pickle.loads(x)[0] and d[1][1] == pickle.loads(x)[1]:
					if pickle.loads(d[0]) == "OK":
						break
			except:
				pass

# Loop de Comandos, para que seja possivel simular o sensor
# que passa informações de quem entrou ou saiu. Dentro do Loop
# não há variaveis que são modificadas a não ser a variavel
# total que já foi descrita antes, variaveis como 'n' e 'temp1'
# são variaveis temporarias para a solicitação de um valor e
# depois são descartadas
while True:
	# "i" é uma variavel apenas para receber comandos e simular
	# a existencia de um sensor recebendo informações sobre quem
	# entra e quem sai, nesse caso estamos assumindo que todos
	# os sensores funcionam com perfeição e sem erros.
	i = input("")
	if i == "mPeer":
		print("Meu Peer: "+str(eu))
	elif i == "mPeers":
		print("Lista de Peers: ")
		# Um for que serve para varrer a lista de peers e listar eles na tela
		for x in peers:
			print(pickle.loads(x))
	elif i == "status":
		print("Limite:      "+str(limite))
		print("Atualmente:  "+str(total))
		# Falando o que é o peer
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
		# Determinando quantidade de pessoas que sairam
		n = 0
		while n <= 0:
			try:
				n = int(input(">> "))
			except:
				n = 0
		# Determinando localização para onde a pessoa foi
		temp1 = ""
		print("Indo para: ")
		while temp1 != "s" and temp1 != "a" and temp1 != "l":
			try:
				print("s - Saindo do Shopping")
				print("a - Indo para outro Andar")
				print("l - Indo para outra Loja")
				temp1 = input("").lower()
			except:
				temp1 = ""
		# Comparar com o numero total atual
		if total >= n:
			total-=n
			falar(total,"saiu",temp1)
		else:
			print("Não há esse numero de pessoas no Shopping")
	elif i == "entrou":
		# Determinando quantidade de pessoas que entraram
		n = 0
		while n <= 0:
			try:
				n = int(input(">> "))
			except:
				n = 0
		# Determinando localização para onde a pessoa foi
		temp1 = ""
		print("Indo para: ")
		while temp1 != "s" and temp1 != "a" and temp1 != "l":
			try:
				print("s - Saindo do Shopping")
				print("a - Indo para outro Andar")
				print("l - Indo para outra Loja")
				temp1 = input("").lower()
			except:
				temp1 = ""
		# Comparar com o limite maximo de pessoas
		if total+n <=limite:
			total+=n
			falar(total,"entrou",temp1)
		else:
			print("Barradas de Entrar")
	else:
		print("Comando não Reconhecido")

print("FIM")

"""
O que falta:
- Entradas para Funcionarios
- Hierarquia entre Andares, Lojas e Shopping
"""
