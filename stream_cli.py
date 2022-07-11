# -*- coding: utf-8 -*-
"""
Created on Thu May 12 15:48:50 2022

@author: earthur
"""
# Below is the client code to receive video frames over UDP
import cv2, imutils, socket
import numpy as npy
import time
import base64

BUFFER_SIZE = 65536
#Create UDP client socket 
client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFFER_SIZE)

host_name = socket.gethostname()
host_addr = '134.10.127.36'

print(host_addr)
port = 4569
#Test to make sure client socket works
message = b'Hello world'
client_socket.sendto(message,(host_addr,port))
#Initialize frame rate variables 
fps,start,frames_bound,count = (0,0,30,0)

#Start receiving frame data from server
while True:
    #receive datagram
	packet,pic = client_socket.recvfrom(BUFFER_SIZE)
    #decode received datagram
	data = base64.b64decode(packet,' /')
    #interpret buffer as 1d array
	npdata = npy.frombuffer(data,dtype=npy.uint8) 
    #convert data from 1d array into an image
	frame = cv2.imdecode(npdata,1)
    # add text to image showing the frame rate
	frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
	cv2.imshow("RECEIVING VIDEO",frame)
    #code below makes sure pressing q ends connection
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		client_socket.close()
		break
    #calculate dynamic framerate after receiving frames_bound frames
	if count == frames_bound:
		try:
			fps = round(frames_bound/(time.time()-start))
			start=time.time()
			count=0
		except:
			pass
	count+=1
