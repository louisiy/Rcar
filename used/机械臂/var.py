# version: Python3
def grab(point,height,mode):
  #MovJ(point,{"user":1,"tool":1,"a":20,"v":20,"cp":50})
  MovJ(point)
  if mode == 1:
    SetParallelGripper(70)
    p=RelPointUser(point,[0,0,-height,0,0,0])
    #MovL(p,{"user":1,"tool":1,"a":20,"v":20,"r":5})
    MovL(p)
    SetParallelGripper(53)
    #MovL(point,{"user":1,"tool":1,"a":20,"v":20,"r":5})
    MovL(point)
    
  elif mode == 0:
    #SetParallelGripper(60)
    p=RelPointUser(point,[0,0,-height,0,0,0])
    #MovL(p,{"user":1,"tool":1,"a":20,"v":20,"r":5})
    MovL(p)
    SetParallelGripper(70)
    SetParallelGripper(53)
    SetParallelGripper(70)
    RelMovJTool([0,0,-20,0,0,0])
    RelMovJTool([0,0,0,0,0,90])
    RelMovJTool([0,0,20,0,0,0])
    SetParallelGripper(53)
    SetParallelGripper(70)
    #MovL(point,{"user":1,"tool":1,"a":20,"v":20,"r":5})
    MovL(point)

def TCPinit(ip,port):
  err=0
  socket=0
  err,socket=TCPCreate(True,ip,port)
  if err == 0:
    print("TCPCreate successful")
  err1=TCPStart(socket,0)
  if err1 == 0:
    print("TCPStart successful")
  return err,socket
  

  