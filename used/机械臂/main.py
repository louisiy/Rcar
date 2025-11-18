# version: Python3
ip="192.168.200.1"
port=6001
err,socket=TCPinit(ip,port)
P1={"joint":[180,0,90,0,-90,0]}
P2={"joint":[140,0,90,0,-90,0]}
h1=15
h2=205
if err == 0:
  while True:
    err1,RecBuf=TCPRead(socket,0,"string")
    if err1 == 0:
      n = int(RecBuf)
      for i in range(n):
        h1 = h1 + 50
        h2 = h2 - 50
        grab(P1,h1,1)
        grab(P2,h2,0)



