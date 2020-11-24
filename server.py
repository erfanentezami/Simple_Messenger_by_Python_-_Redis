from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import redis

redis_host = '127.0.0.1'
redis_port = 6379
redis_password = ""

m = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
m_list=[]


def register():
    while True:
        client, client_address = SERVER.accept()
        addresses[client] = client_address
        print("%s:%s has connected." % client_address)
        try:
             r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
             
             client.send(bytes("Enter your full name : ", "utf8"))
             full_name = client.recv(BUFSIZ).decode("utf8")
             
             client.send(bytes("Enter your user name : ", "utf8"))
             username = client.recv(BUFSIZ).decode("utf8")

             client.send(bytes("Enter your phone number : ", "utf8"))
             phone = client.recv(BUFSIZ).decode("utf8")
             
             info={
                 "name":full_name,
                 "usernamr":username,
                 "phone_number":phone}
             
             user_ip = str(client_address)
             r.set(user_ip, str(info))
             print("user registered")
             
             
             Thread(target=handle_client, args=(client,username,)).start()
        except Exception as e:
            print(e)


def handle_client(client,name):  # Takes client socket as argument.

    welcome = 'Welcome %s' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
 
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            item = str(name)+" : "+str(msg)
            m_list.append(str(item))
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            m.set("all_messages",str(m_list))
            print(m.get("all_messages"))
            break

def broadcast(msg, prefix=""):  # prefix is for name identification.

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

        
clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=register)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()