import socket
import select
import time

#importing libraries
bufferSpace  = 1024

#creating socket connections
recieverIPaddress = "10.0.0.2"
recieverPortnumber   = 20002
senderAddressPortnumber = ("10.0.0.1", 20001)
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socket_send = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
socket_udp.bind((recieverIPaddress, recieverPortnumber))

print("Socket created successfully -------------------")


#recieving file:
# path, addr = socket_udp.recvfrom(bufferSpace)
# print("path of the file recieved %s:" %path)

#creating file 
file = open(b'/home/p4/Assignment2/testFile.jpg','wb')
print("image file created successfully___")

#important variables 
flag = 0 # to close the connection
pointer1 = 0
pointer2 = 0#to keep track of packets recieved


while not flag:
    #recieveing data packets
    packets, addr = socket_udp.recvfrom(bufferSize)

    #seperating image data from other
    flag = packets[-1]
    pointer2 = int.from_bytes(packets[:2],'big')
    image = packets[2:1023]

    if flag == 0:
        if(pointer1 < pointer2):
            file.write(image)
            #sending acknowledgement
            acknowledgement = b"True"
            socket_send.sendto(acknowledgement, senderAddressPortnumber)
            pointer1 = pointer2
        ## incase acknowledgement missed
        elif(pointer2 == pointer1):
            #sending acknowledgement
            socket_send.sendto(acknowledgement,senderAddressPortnumber)

    else:
        if(pointer1 < pointer2):
            file.write(image)
            #sending acknowledgement
            acknowledgement = b"True"
            socket_send.sendto(acknowledgement, senderAddressPortnumber)
            pointer1 = pointer2
            print("complete image recieved succesfully :-)")
            print("image stored at location: %s", f)
            #closing the file
            file.close()
        ## incase acknowledgement missed
        elif(pointer2 == pointer1):
            #sending acknowledgement
            socket_send.sendto(acknowledgement,senderAddressPortnumber)



#closing the connection
socket_send.close()
socket_udp.close()



    # #split the recieved tuple into variables
    # recievedMessage = bytesAddressPair[0]
    # senderAddress = bytesAddressPair[1]

    # #print them just for understanding
    # msgString = "Message from Client:{}".format(recievedMessage)
    # detailString  = "Client IP Address:{}".format(senderAddress)
    # print(msgString)
    # print(detailString)

    # # Sending a reply to client
    # message = str.encode("This is a reply message from the server")
    # socket_udp.sendto(message, senderAddress)
