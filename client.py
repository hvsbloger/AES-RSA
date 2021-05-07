import RSA
import AES
import socket

msg=0b1101011100101000
key=0b0100101011110101
p=13
q=17

publick,privatek=RSA.generate_keypair(p,q)
ckey,n=publick

ciphertext= AES.encrypt(msg,key)


message='please send server public key'
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 9999))

try:
    clientsocket.send(bytes(message, 'utf-8'))
    skey=int((clientsocket.recv(2048)).decode('utf-8'))
    n=int((clientsocket.recv(2048)).decode('utf-8'))
    
except:
    pass
sk=(skey,n)

ekey=RSA.encrypt(sk,str(key))
hashval=RSA.hashFunction(str(msg))
signature=RSA.encrypt(privatek, hashval)
print(len(signature)) 
print(ekey)
print(signature)
clientsocket.send(bytes(str(ckey), 'utf-8'))
clientsocket.send(bytes(str(n), 'utf-8'))

clientsocket.send(bytes(str(signature),'utf-8'))
clientsocket.send(bytes(str(ekey),'utf-8'))
clientsocket.send(bytes(str(ciphertext),'utf-8'))
print("client pub key :", publick )
print("clinet private key :", privatek)
print("enc sec key: " , ekey )
print("cihper text: ", ciphertext )
print("digest is " , hashval )
print("digital sign : " , signature)
clientsocket.close()
