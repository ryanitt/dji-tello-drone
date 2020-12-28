import threading
import socket
import sys
import time


host = ''
port = 8888
locaddr = (host, port)

sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

tello_addr = ('192.168.10.1', 8889)

sckt.bind(locaddr)

ready = threading.Condition()


def getResponse():
    print("started response thread")
    while True:
        try:
            data, server = sckt.recvfrom(1024)
            # print("rcv waiting")
            ready.acquire()
            # print("rcv acquired")
            try:
                print(data.decode(encoding="utf-8"))
                ready.notify()
            finally:
                ready.release()
        except Exception:
            print('\nExit . . .\n')
            break


def sendcmd(cmd):
    ready.acquire()
    print("Sending " + cmd + " to Tello...")
    cmd = cmd.encode(encoding="utf-8")
    try:
        sent = sckt.sendto(cmd, tello_addr)
        val = ready.wait(10)
        if val:
            print("Tello ready for next command...")
    finally:
        ready.release()
        


if __name__ == "__main__":
    recvThread = threading.Thread(target=getResponse)
    recvThread.daemon = True
    recvThread.start()
    sendcmd("command")

    while True:
        try:
            cmd = input("[Power " + "%]: ")

            print(cmd)
            if not cmd:
                print("invalid command")
                break

            if 'quit' in cmd:
                print("Tello out...")
                break
            else:
                sendcmd(cmd)
                    
        except (KeyboardInterrupt, AttributeError):
            print("invalid command sent")
            sckt.close()
            break
