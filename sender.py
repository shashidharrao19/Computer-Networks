import socket
import sys
import time


file_location = b"/home/p4/Assignment2/testFile.jpg"
bufferspace = 1021

#creating socket connections
senderIPaddress = "10.0.0.1"
senderPortnumber   = 20001
recieverAddressPortnumber = ("10.0.0.2", 20002)
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
socket_send = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socket_send.bind((senderIPaddress , senderPortnumber))
#print("<<<<<<<<<< Succesfully Connection Established Between Sender and Reciever >>>>>>>>>>>> ")
file = open(file_location , "rb")

#declaring important variables
bufferspace = 1021
seq_num = 0 #variable to update latest fpacket sent
img_size = 1175552 # variable to store the space of iage
flag = 0 #to close the sender function
retransmissions = 0

while not flag:
	img_size = img_size - bufferspace 
	seq_num = seq_num + 1
	#loading data into packet
	packets = seq_num.to_bytes(2, 'big') + file.read(bufferspace)
	if img_size <= 0:
		packets = packets + bytes([1])
		flag = 1
	else:
		packets = packets + bytes([0])

	#sending packet

	acknow = False
	while not acknow:
		try:
			socket_send.settimeout(0.05)
			msg, addr = socket_send.recvfrom(1024)
			print(msg)
			acknow = True
		except socket.timeout:
			#resending the packet i case of timeout
			socket_udp.sendto(packets, recieverAddressPortnumber)
			retransmissions = retransmissions + 1


#printing total retransmissions
print("---------------------------------------------------------------------")
print("image succesfully sent")
print("number of retransmissions are : ")
print(retransmissions)



# closing the file
file.close()
print("closed the file!!")
#closing the sockets
socket_udp.close()
socket_send.close()





















