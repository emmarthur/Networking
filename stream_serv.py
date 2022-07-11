# -*- coding: utf-8 -*-
"""
Created on Thu May 12 15:47:56 2022

@author: earthur
"""

# Below is the code to send video frames over UDP

import cv2, imutils, socket
import numpy as npy
import time
import base64  #used for converting video data into text

BUFF_SIZE = 65536 #maximum size of a datagram to be sent over UDP connection

#Create UDP server socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE) #enable program to work cross platform

host_name = socket.gethostname() #Gets hostname of computer
host_addr = '134.10.127.36' #My computer's ip address
print(host_addr)
port = 4569
socket_address = (host_addr,port) #socket address is a size two tuple of host_addr and port
server_socket.bind(socket_address) #bind socket address
print('Listening at:',socket_address)

vid = cv2.VideoCapture("video.mp4") #passing 0 as argument enables webcam  
fps,start,frames_bound,count = (0,0,30,0) #initialize variables for finding the frame rate
#receive datagram from any client at socket address
while True:   
    msg,client_addr = server_socket.recvfrom(BUFF_SIZE) 
    print('Connected to ',client_addr) #testing if UDP connection works.
    WIDTH = 500  #set width of an image frame to 400
    while(vid.isOpened()):
        pic,frame = vid.read() # read and extract frames
        frame = imutils.resize(frame,width=WIDTH) #resize image frame to given width size
        #convert image format to streaming data
        encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,90]) 
        #convert binary data format to text format
        message = base64.b64encode(buffer)
        #send message to client address
        server_socket.sendto(message,client_addr)
        #modify image frame to have text showing frame rate at any given point
        frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        #display transmitted frame
        cv2.imshow('SENDING VIDEO',frame)
        #code makes sure pressing q ends the stream connection
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            server_socket.close()
            break
        #calculate dynamic framerate after receiving frames_bound frames 
        if count == frames_bound:
            try:
                fps =round(frames_bound/(time.time()-start))
                start=time.time()
                count=0
            except:
                pass
        count+=1