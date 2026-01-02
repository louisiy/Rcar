P0={"joint":[0,0,-90,-90,-90,0]}
P_TEMP_ATAG={"pose":[78.5128,232.1693,255.673,90,0,180]}
P_TEMP_PHASE={"pose":[78.5128,232.1693,255.673,90,0,180]}
P_PIPETTE_ATAG={"pose":[78.5128,232.1693,255.673,90,0,180]}
P_EXTRACTION_ATAG={"pose":[78.5128,232.1693,255.673,90,0,180]}
Z_EXTRACTION=0
tmp = 0

_cmd = {}

def reg(name):
    def deco(fn):
        _cmd[name] = fn
        return fn
    return deco

###### 主控确认连接 ######
@reg("HELLO")
def hello(socket):
  TCPWrite(socket,"ARM:HELLO")
  print("[ARM] 主控确认连接")

###### 夹取移液枪  ######
@reg("LEFT")
def LEFT(socket):
  MovJ({"joint":[90,0,-90,-90,-90,0]},{"a":30,"v":30,"cp":50})
  TCPWrite(socket,"ARM:LEFT_OK")

@reg("ATAG=")
def ATAG(socket,data):
  ATAG=data.split(',')
  X_ATAG=float(ATAG[0])
  Z_ATAG=float(ATAG[1])
  Y_ATAG=float(ATAG[2])
  DY_ATAG=25
  if abs(X_ATAG) <= 1 and abs(Z_ATAG) <= 1 and abs(Y_ATAG-DY_ATAG) <= 1:
    print(f"X_ATAG: {X_ATAG},Z_ATAG: {Z_ATAG}, Y_ATAG-DY_ATAG: {Y_ATAG-DY_ATAG}")
    global P_ATAG
    P_ATAG=GetPose()
    TCPWrite(socket,"ARM:ATAGOK")

  else:
    print(f"X_ATAG: {X_ATAG},Z_ATAG: {Z_ATAG}, Y_ATAG-DY_ATAG: {Y_ATAG-DY_ATAG}")
    RelMovLTool([X_ATAG, Z_ATAG, Y_ATAG-DY_ATAG, 0, 0, 0],{"a":30,"v":30,"r":5}) #根据atag距离对准atag码
    TCPWrite(socket,"ARM:REATAG")

@reg("PIPETTE_GRAB")
def PIPETTE_GRAB(socket):
  SetParallelGripper(40)
  div=3
  RelMovLUser([-100,0,0,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,105+div,0,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,0,56,0,0,0],{"a":30,"v":30,"r":5})

  SetParallelGripper(20)
  RelMovLUser([0,0,1,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,-(80+div),0,0,0,0],{"a":30,"v":30,"r":5})

  TCPWrite(socket,"ARM:PIPETTE_GRAB_OK")

###### 吸取溶液  ######
@reg("SOLUTION_MOVE")
def SOLUTION_MOVE(socket):
  RelMovLUser([0,0,93,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([105,0,0,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,-14,0,0,0,0],{"a":30,"v":30,"r":5})
  TCPWrite(socket,"ARM:SOLUTION_MOVE_OK")

@reg("SOLUTION_DOWN")
def SOLUTION_DOWN(socket):
  DZ_SOLUTION=75
  RelMovLUser([0,0,-DZ_SOLUTION,0,0,0],{"a":30,"v":30,"r":5})
  TCPWrite(socket,"ARM:SOLUTION_DOWN_OK")

@reg("SOLUTION_UP")
def SOLUTION_UP(socket):
  DZ_SOLUTION=75
  RelMovLUser([0,0,DZ_SOLUTION,0,0,0],{"a":30,"v":30,"r":5})
  TCPWrite(socket,"ARM:SOLUTION_UP_OK")


###### 加液  ######
@reg("ADD_MOVEDOWN")
def ADD_MOVE(socket):
  RelMovLUser([0,0,-15,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([75,0,0,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,0,-28,0,0,0],{"a":30,"v":30,"r":5})
  TCPWrite(socket,"ARM:ADD_MOVEDOWN_OK")

@reg("ADD_UP")
def ADD_UP(socket):
  RelMovLUser([0,0,28,0,0,0],{"a":30,"v":30,"r":5})
  TCPWrite(socket,"ARM:ADD_UP_OK")

###### 放下移液枪  ######
@reg("PIPETTE_DROP")
def PIPETTE_DROP(socket):
  RelMovLUser([-75,0,0,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,0,15,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,18,0,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([-105,0,0,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,0,-93,0,0,0],{"a":30,"v":30,"r":5})

  RelMovLUser([0,0,3,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,80,0,0,0,0],{"a":30,"v":30,"r":5})
  time.sleep(1)
  SetParallelGripper(40)
  time.sleep(1)
  RelMovLUser([0,0,-20,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,-50,0,0,0,0],{"a":30,"v":30,"r":5})
  TCPWrite(socket,"ARM:PIPETTE_DROP_OK")

###### 夹取容器  ######
@reg("CONTAINER_GRAB")
def CONTAINER_GRAB(socket):
  RelMovLUser([85,0,0,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,-46,0,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([100,0,0,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,0,-170,0,0,0],{"a":30,"v":30,"r":5})
  SetParallelGripper(18)
  MovJ({"joint":[0,0,-90,-90,-90,0]},{"a":30,"v":30,"cp":50})
  TCPWrite(socket,"ARM:CONTAINER_GRAB_OK")

###### 放置容器  ######
@reg("EXTRACTION_DROP")
def EXTRACTION_DROP(socket):
  div = 5
  RelMovLUser([0,0,86,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([-85,0,0,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,35+div,0,0,0,0],{"a":30,"v":30,"r":5})
  SetParallelGripper(70)
  RelMovLUser([0,-div,0,0,0,0],{"a":30,"v":30,"r":5})
  TCPWrite(socket,"ARM:EXTRACTION_DROP_OK")
# 截止到这里之前的代码已经完成review
###### 确定相界面  ######
@reg("INTERFACE_MOVE")
def INTERFACE_MOVE(socket):
  RelMovLUser([0,-75,0,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([-70,0,0,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,0,-80,0,0,0],{"a":30,"v":30,"r":5})
  TCPWrite(socket,"ARM:INTERFACE_MOVE_OK")

@reg("PHASE=")
def INTERFACE_FIND(socket,data):
  PHASE=data.split(',')
  k=-0.05
  Z_PHASE=k*float(PHASE[0])
  if abs(Z_PHASE) <= 0.5:
    global P_TEMPT_PHASE
    P_TEMPT_PHASE= GetPose()
    print(P_TEMPT_PHASE["pose"][2])
    global Z_EXTRACTION
    Z_EXTRACTION=P_TEMPT_PHASE["pose"][2]
    TCPWrite(socket,"ARM:PHASEOK")

  else:
    print(f"Z_PHASE: {Z_PHASE}")
    RelMovLTool([0, Z_PHASE, 0, 0, 0, 0],{"a":30,"v":30,"r":5})
    TCPWrite(socket,"ARM:REPHASE")
 
###### 夹取针头  ######
@reg("NEEDLE_GRAB")
def NEEDLE_GRAB(socket):
  SetParallelGripper(30)
#  P_EXTRACTION={"pose":[109.36,315.42,159.1,90,0,-180]}
  div = 4
  Z_NEEDLE=210
  RelMovLUser([0, 0, 50, 0, 0, 0], {"a": 30, "v": 30, "r": 5})
  RelMovLUser([0, 22, 0, 0, 0, 0], {"a": 30, "v": 30, "r": 5})
  RelMovLUser([0, 0, 40, 0, 0, 0], {"a": 30, "v": 30, "r": 5})
  RelMovLUser([240, 0, 0, 0, 0, 0], {"a": 30, "v": 30, "r": 5})
  RelMovLUser([0, 125-div, 0, 0, 0, 0], {"a": 30, "v": 30, "r": 5})
  RelMovLUser([0, 0, Z_NEEDLE-Z_EXTRACTION-85, 0, 0, 0], {"a": 30, "v": 30, "r": 5})
  SetParallelGripper(0)
  RelMovLUser([0, 0, 25, 0, 0, 0], {"a": 30, "v": 30, "r": 5})
  RelMovLUser([0, -(130-div), 0, 0, 0, 0], {"a": 30, "v": 30, "r": 5})
  TCPWrite(socket,"ARM:NEEDLE_GRAB_OK")

###### 移液  ######
@reg("PUMP_MOVE")
def PUMP_MOVE(socket):
  global tmp
#  X_EXTRACTION=84.6021
#  Y_EXTRACTION=205.2678
#  Z_EXTRACTION=37.6071
  SetParallelGripper(0)
  RelMovLUser([-100,0,0,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,0,120,0,0,0],{"a":30,"v":30,"r":5})
  #RelMovLUser([0,0,30,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([-70,0,0,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,50,0,0,0,0],{"a":30,"v":30,"r":5})
  a=GetPose()
  tmp=a["pose"][2]-Z_EXTRACTION-147
  #print(Z_EXTRACTION)
  #print(a["pose"][2])
  print(tmp)
  RelMovLUser([0,0,-tmp,0,0,0],{"a":30,"v":30,"r":5})
#  MovL({"pose": [X_EXTRACTION, Y_EXTRACTION, Z_EXTRACTION, 90, 0, 180]}, {"a": 30, "v": 30, "r": 5})
#  MovL({"pose": [X_EXTRACTION,Y_EXTRACTION , Z_EXTRACTION + 200, 90, 0, 180]}, {"a": 30, "v": 30, "r": 5})
  #MovL({"pose": [X_EXTRACTION,Y_EXTRACTION , Z_EXTRACTION + 200, 90, 0, 180]}, {"a": 30, "v": 30, "r": 5})
  #MovL({"pose": [X_EXTRACTION,Y_EXTRACTION , Z_EXTRACTION + 200, 90, 0, 180]}, {"a": 30, "v": 30, "r": 5})
  #MovL({"pose": [X_EXTRACTION,Y_EXTRACTION , Z_EXTRACTION + 146, 90, 0, 180]})

  TCPWrite(socket,"ARM:PUMP_MOVE_OK")

@reg("PUMP_UP")
def PUMP_UP(socket):
  RelMovLUser([0,0,tmp,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,2,0,0,0,0],{"a":30,"v":30,"r":5})
  TCPWrite(socket,"ARM:PUMP_UP_OK")

###### 放回枪头  ######
@reg("DROPNEEDLE")
def DROPNEEDLE(socket):
  RelMovLUser([50,0,0,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,0,-77,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,-20,0,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([100,0,0,0,0,0],{"a":30,"v":30,"r":5})
  RelJointMovJ([0, 0, 0, 0, 15, 0])
  RelMovLUser([40,0,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,0,-1,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([40,0,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,0,-1,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([40,0,0,0,0],{"a":30,"v":30,"r":5})
  RelMovLUser([0,0,-1,0,0,0],{"a":30,"v":30,"r":5})
  SetParallelGripper(40)
  #RelMovLUser([0,-8,0,0,0,0],{"a":30,"v":30,"r":5})
  #RelMovJUser([0, 0, 0, 0, 0, 35],{"a":30,"v":30,"r":5})
  TCPWrite(socket,"ARM:DROPNEEDLE_OK")