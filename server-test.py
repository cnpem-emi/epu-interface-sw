import socket
import struct

IP_BBB = "10.0.6.52"
PORT_BBB = 5050

command = {"R": "Leitura", "W": "Escrita"}

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp.connect((IP_BBB, PORT_BBB))

def sendVariable(variableID, size, function):
    
    if (function == "R"):
        send_message = [0x00, 0x10] + [c for c in struct.pack("!h",size+1)] + [variableID]
    else:
        send_message = [0x00, 0x20] + [c for c in struct.pack("!h",size+1)] + [variableID]
    return("".join(map(chr,includeChecksum(send_message))))

def includeChecksum(list_values):
    counter = 0
    i = 0
    while (i < len(list_values)):
        counter += list_values[i]
        i += 1
    counter = (counter & 0xFF)
    counter = (256 - counter) & 0xFF
    return(list_values + [counter])

while(True):
    func = input("Digite o tipo de comando - R: Reads - W: Writes \n")
    tcp.send(sendVariable(int(input(f"Digite o comando de {command[func]}: \n"), 16), size = 1, function = func).encode())
    
    if(func == "R"):
        print([ord(i) for i in tcp.recv(128).decode()]) 
