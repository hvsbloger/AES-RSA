import RSA
import AES
import socket




p=13
q=17
publick,privatek =RSA.generate_keypair(p,q)
skey,n=publick
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 9999))
serversocket.listen(5)

try:
    clientsocket, address = serversocket.accept()
    print(f"Connection to {address} has been established!!")
    print()
    #clientsocket.send(bytes(message, 'utf-8'))
    msg=clientsocket.recv(4096)
    print(msg.decode('utf-8'))
    #print("Received Ciphertext: ",ciphertext)
    clientsocket.send(bytes(str(skey), 'utf-8'))
    clientsocket.send(bytes(str(n), 'utf-8'))    
except OSError:
    pass

ckey=int((clientsocket.recv(4096)).decode('utf-8'))
n=int((clientsocket.recv(4096)).decode('utf-8'))
pkey=(ckey,n)

signature=clientsocket.recv(4096).decode('utf-8')
print(type(signature)) #ext


ekey=clientsocket.recv(4096).decode('utf-8')
print(ekey)#ext


ciphertext=clientsocket.recv(4096)
print(ciphertext)



signature=signature.replace('[', '').replace(']', '')
signature=signature.split(',')
signa=[]
for i in range(len(signature)):
    signa.append(int(signature[i]))
print(signa) #ext
print(type(signa)) #ext
ekey=ekey.replace('[', '').replace(']', '')
ekey=ekey.split(',')
enkey=[]
for i in range(len(ekey)):
    enkey.append(int(ekey[i]))
print(enkey) #ext
akey=RSA.decrypt(privatek,enkey)
print(type(akey)) # ext
plaintext=AES.decrypt(int(ciphertext.decode('utf-8')),int(akey))
print(plaintext)
sign = RSA.decrypt(pkey, signa)
print("333333333")
print("public key" , publick )
print("private key" , privatek )
print("dec sec key " , akey)
print("dec message" , plaintext )
print("message digest")


RSA.verify(sign,str(plaintext))

clientsocket.close()
