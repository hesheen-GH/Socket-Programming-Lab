# Socket-Programming-Lab

CEG3185 Lab 3 Socket Programming

Group #31: 

Yaseen Naas, 8755563
Nabil Ali, 300067998

# Libraries

Please install latest version of Python 3.X and add python to PATH. 

Make sure you install the following libraries if not present:

pip install socket
pip install getopt 


# How to run 

## Running client.py

python client.py -s SERVER_IP -c CLIENT_IP -p SERVER_PORT

ex. python client.py -s 192.168.0.13 -c 192.168.0.16 -p 8888

## Running server.py 

python server.py -s SERVER_IP -p SERVER_PORT

ex. python client.py -s 192.168.0.13 -p 8888

## Sending a message

Once the client is able to establish a connection, the client would be prompted to write a message on a terminal

ex. Please enter message:

COLOMBIA 2 - MESSI 0 

Then information regarding total packet length, message length, and checksum validation would be displayed

Multiple messages can be sent. Feel free to send as many messages as you please. 

## Disconnect the client from server

Enter the messsage "!DISCONNECT" (No quotes) on input. 
 

