
import socket, pickle, json, threading, time
from cryptography.fernet import Fernet

print("Criando chave de Criptografia")
key = Fernet.generate_key()

print("Iniciando Tracker...")
h = socket.gethostbyname(socket.gethostname())
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((h,15000))
print("Rodando Tracker em "+h+":15000")

peers = {}
ant = len(peers)
dados = json.loads(open("data.txt","r").read())

def PRINCIPAL():
	global s, h, peers, dados, key
	while True:
		try:
			d = s.recvfrom(1024)
			data = pickle.loads(d[0])
			if pickle.dumps(d[1]) in peers:
				if data == "eu":
					print("Atualizando peer "+d[1][0]+":"+str(d[1][1])+" sobre Identidade")
					s.sendto(pickle.dumps({"peer":d[1]}),d[1])
				if data == "key":
					print("Atualizando peer "+d[1][0]+":"+str(d[1][1])+" sobre Criptografia")
					s.sendto(pickle.dumps({"chave":key}),d[1])
				if data == "list":
					print("Atualizando peer "+d[1][0]+":"+str(d[1][1])+" sobre Lista de Peers")
					for x in peers:
						s.sendto(pickle.dumps({"list":peers}),pickle.loads(x))
				if "@" in data:
					s.sendto(pickle.dumps(True),d[1])
			else:
				if "@" in data:
					login = data.split("@")[0]
					senha = data.split("@")[1]
					if dados[login] == senha:
						s.sendto(pickle.dumps(True),d[1])
						print("Novo Peer Confirmado: "+d[1][0]+":"+str(d[1][1]))
						s.sendto(pickle.dumps({"peer":d[1]}),d[1])
						peers[pickle.dumps(d[1])] = 0
						# Informar Peers
						for x in peers:
							s.sendto(pickle.dumps({"list":peers}),pickle.loads(x))
					else:
						s.sendto(pickle.dumps(False),d[1])
		except:
			pass

threading.Thread(target=PRINCIPAL, args=()).start()

while True:
	time.sleep(1)
	for x in peers:
		s.sendto(pickle.dumps({"list":peers}),pickle.loads(x))
