# 

import threading
import socket
import pygame
import tello
import math

RC_VAL_MIN = 364
RC_VAL_MID = 1024
RC_VAL_MAX = 1684

IDX_ROLL = 0
IDX_PITCH = 1
IDX_THR = 2
IDX_YAW = 3

class PS4DroneController(object):

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        
        self.maxSpeed = 5
        self.mRCVal = [1024, 1024, 1024, 1024]
        self.drone = tello.Tello()
        self.grounded = True

    def listen(self):
        
        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == 0:
                        if event.value < -0.2 or event.value > 0.2:
                            self.mRCVal[IDX_ROLL] = round(RC_VAL_MID + event.value * 660)
                        else:
                            self.mRCVal[IDX_ROLL] = RC_VAL_MID
                    if event.axis == 1:
                        if event.value < -0.2 or event.value > 0.2:
                            self.mRCVal[IDX_PITCH] = round(RC_VAL_MID - event.value * 660)
                        else:
                            self.mRCVal[IDX_PITCH] = RC_VAL_MID
                    if event.axis == 2:
                        if event.value < -0.2 or event.value > 0.2:
                            self.mRCVal[IDX_YAW] = round(RC_VAL_MID + event.value * 660)
                        else:
                            self.mRCVal[IDX_YAW] = RC_VAL_MID
                    if event.axis == 5:
                        if event.value < -0.2 or event.value > 0.2:
                            self.mRCVal[IDX_THR] = round(RC_VAL_MID - event.value * 660)
                        else:
                            self.mRCVal[IDX_THR] = RC_VAL_MID
                    
                        
                elif event.type == pygame.JOYBUTTONUP:
                    if event.button == 0:
                        self.drone._sendCmd(0x68, 92, bytearray([0x01]))
                        print("Doing left flip")
                    if event.button == 1:
                        self.drone._sendCmd(0x68, 92, bytearray([0x02]))
                        print("Doing back flip")
                    if event.button == 2:
                        self.drone._sendCmd(0x68, 92, bytearray([0x03]))
                        print("Doing right flip")
                    if event.button == 3:
                        self.drone._sendCmd(0x68, 92, bytearray([0x00]))
                        print("Doing front flip")
                elif event.type == pygame.JOYHATMOTION:
                    if event.hat == 0:
                        if event.value == (1, 0):
                            print("hright")
                        if event.value == (-1, 0):
                            print("hleft")
                        if event.value == (0, 1):
                            print("hup")
                        if event.value == (0, -1):
                            if self.grounded:
                                print("Started takeoff")
                                self.drone.takeOff()
                                self.grounded = False
                            else:
                                print("Started landing")
                                self.drone.land()
                                self.grounded = True

            # print("lrSpeed: {} fbSpeed: {}".format(self.mRCVal[IDX_ROLL], self.mRCVal[IDX_PITCH]))
            self.drone.setStickData(0, self.mRCVal[IDX_ROLL], self.mRCVal[IDX_PITCH], self.mRCVal[IDX_THR], self.mRCVal[IDX_YAW])
            # sendCmd(0x60, 80, None)


host = ''
port = 8888
locaddr = (host, port)

sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

tello_addr = ('192.168.10.1', 8889)

sckt.bind(locaddr)

if __name__ == "__main__":
    ps4 = PS4DroneController()
    ps4.init()
    ps4.listen()
    
