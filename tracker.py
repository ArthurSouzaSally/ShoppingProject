
import socket, pickle, threading, json

dados = json.loads(open('data.txt','r').read())
print("Iniciando Servidor...")
h = socket.gethostbyname(socket.gethostname())
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((h,15000))
print("Criando Tracker em: "+h+":15000")

limite = 0
while limite <= 0:
	try:
		limite = int(input("Limite de Pessoas no Shopping: "))
	except:
		pass

peers = []

def receber():
	global s, peers, dados
	while True:
		try:
			a = s.recvfrom(10000)
			# Atualizar lista de peers
			try:
				if peers.index(pickle.dumps(a[1])):
					pass
			except:
				peers+=[pickle.dumps(a[1])]
				print("Novo Peer: "+a[1][0]+":"+str(a[1][1]))
			# Informar sua Posição
			if pickle.loads(a[0]) == "oi":
				s.sendto(pickle.dumps({"ip":a[1]}),a[1])
			# Informar outros peers
			elif pickle.loads(a[0]) == "list":
				print("Atualizando Peers")
				for x in peers:
					s.sendto(pickle.dumps({"list":peers}),pickle.loads(x))
			# Informar limite de pessoas
			elif pickle.loads(a[0]) == "limit":
				s.sendto(pickle.dumps({"limite":limite}),a[1])
			# Verificar Login e Senha
			elif pickle.loads(a[0])[0] == "@":
				data = pickle.loads(a[0])[1:len(pickle.loads(a[0]))].split(";")
				try:
					if dados[data[0]] == data[1]:
						s.sendto(pickle.dumps({"login":True}),a[1])
					else:
						s.sendto(pickle.dumps({"login":False}),a[1])
				except:
					s.sendto(pickle.dumps({"login":False}),a[1])
		except:
			pass
	print("FIM")

threading.Thread(target=receber, args=()).start()







