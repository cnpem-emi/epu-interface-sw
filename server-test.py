import socket
import struct

IP_BBB = "10.0.6.52"
PORT_BBB = 5050

command = {"R": "Leitura", "W": "Escrita"}

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp.connect((IP_BBB, PORT_BBB))

def sendVariable(variableID, size, function, valueToWrite = 0):
    
    if (function == "R"):
        send_message = [0x00, 0x10] + [c for c in struct.pack("!h",size+1)] + [variableID]
        
    elif (func == "W" and (com in [32, 33, 34, 35])):
        send_message = [0x00, 0x20] + [c for c in struct.pack("!h", size + 1)] + [variableID]

    else:
        send_message = [0x00, 0x20] + [c for c in struct.pack("!h",size+1)] + [variableID] + [valueToWrite]
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
    func = input("Digite o tipo de comando - R: Reads - W: Writes \n").upper()
    com = int(input(f"Digite o comando de {command[func]}: \n"), 16)
    
    if(func == "R"):
        tcp.send(sendVariable(com, size = 1, function = func).encode()) 
       
    elif(func == "W" and (com not in [32, 33, 34, 35])):
        value = int(input("Digite o valor: \n"), 16)
        tcp.send(sendVariable(com, size = 2, function = func, valueToWrite = value).encode())
    
    else: 
        tcp.send(sendVariable(com, size=1, function=func).encode())
        
    print([ord(i) for i in tcp.recv(128).decode("latin-1")])
    
        
