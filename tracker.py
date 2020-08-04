
import socket, pickle, json

print("Iniciando Servidor...")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
h = socket.gethostbyname(socket.gethostname())
s.bind((h,15000))
print("Tracker Rodando em "+str(h)+":15000")

peers = {}
banco = json.loads(open("data.txt","r").read())

while True:
	try:
		while True:
			data = s.recvfrom(1024)
			if pickle.dumps(data[1]) in peers:
				# Solicitando Atualização de Peers
				print("Solicitação de Peer "+data[1][0]+":"+str(data[1][1]))
				if pickle.loads(data[0]) == "me":
					s.sendto(pickle.dumps({"me":data[1]}),data[1])
				if pickle.loads(data[0]) == "list":
					s.sendto(pickle.dumps({"list":peers}),data[1])
			else:
				# Comandos para Login e Senha
				if "@" in pickle.loads(data[0]):
					login = pickle.loads(data[0]).split("@")[0]
					senha = pickle.loads(data[0]).split("@")[1]
					if login in banco:
						if banco[login] == senha:
							peers[pickle.dumps(data[1])] = 0
							print("Novo Peer Processado: "+data[1][0]+":"+str(data[1][1]))
							s.sendto(pickle.dumps(True),data[1])
							for x in peers:
								s.sendto(pickle.dumps({"list":peers}),pickle.loads(x))
						else:
							s.sendto(pickle.dumps(False),data[1])
					else:
						s.sendto(pickle.dumps(False),data[1])
	except:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		h = socket.gethostbyname(socket.gethostname())
		s.bind((h,15000))
