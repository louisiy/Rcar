def test():
  ######  移液工作站  ######
  P0={"joint":[0,0,-90,-90,-90,0]}
  #MovJ(P0,{"a":30,"v":30,"cp":50})  为方便测试先注释掉
  #小车运动到移液工作站
  ###### 放置容器  ######
  #S_DROPCONTAINER_LEFT=READ(LEFT)
  MovJ({"joint":[90,0,-90,-90,-90,0]},{"a":30,"v":30,"cp":50})
  #Send(CAM:OK)
  #S_DROPCONTAINER_ATAG=READ(A,B,C)
  S_DROPCONTAINER_ATAG='30,20,20'
  #约定摄像头右、上分别为正，同时为X,Z的正方向；即ABC分别对应XZY
  DROPCONTAINER_ATAG=S_DROPCONTAINER_ATAG.split(',')
  X_ATAG=float(DROPCONTAINER_ATAG[0])
  Z_ATAG=float(DROPCONTAINER_ATAG[1])
  Y_ATAG=float(DROPCONTAINER_ATAG[2])
  DY_ATAG=10
  RelMovLTool([X_ATAG, Z_ATAG, Y_ATAG-DY_ATAG, 0, 0, 0],{"a":30,"v":30,"r":5}) #根据atag距离对准atag码
  #Send(CAM:OK)
  #S_DROPCONTAINER_ATAGCHECK=READ(AA,BB,CC)
  S_DROPCONTAINER_ATAGCHECK='-30,-20,20'
  DROPCONTAINER_ATAGCHECK=S_DROPCONTAINER_ATAGCHECK.split(',')
  X_ATAGCHECK=float(DROPCONTAINER_ATAGCHECK[0])
  Z_ATAGCHECK=float(DROPCONTAINER_ATAGCHECK[1])
  Y_ATAGCHECK=float(DROPCONTAINER_ATAGCHECK[2])
  RelMovLTool([X_ATAGCHECK, Z_ATAGCHECK, Y_ATAGCHECK-DY_ATAG, 0, 0, 0],{"a":30,"v":30,"r":5}) #根据atag距离对准atag码
  P_ATAG = GetPose()  #获得当前位置
  #Send(CAM:OK)
  #S_DROPCONTAINER_DOWN=READ(DOWN)
  DZ_DROPCONTAINER=70
  RelMovLTool([0, -DZ_DROPCONTAINER, 0, 0, 0, 0],{"a":20,"v":20,"r":5})
  SetParallelGripper(70)  #松开夹爪
  RelMovLTool([0, 0, -10, 0, 0, 0],{"a":20,"v":20,"r":5})
  RelMovLTool([0, 20, 0, 0, 0, 0],{"a":20,"v":20,"r":5})
  MovJ(P_ATAG,{"a":20,"v":20,"cp":50})
  #Send(CAM:OK)
  ###### 夹取移液枪  ######
  #S_PIPETTE_MOVE=READ(MOVE)
  RelMovLTool([80, 0, 0, 0, 0, 0],{"a":30,"v":30,"r":5}) #此处X方向移动参数需结合ATAG码位置调整
  #Send(CAM:OK)
  #S_PIPETTE_ATAG=READ(A,B,C)
  S_PIPETTE_ATAG='-30,-20,-10'
  PIPETTE_ATAG=S_PIPETTE_ATAG.split(',')
  X_ATAG=float(PIPETTE_ATAG[0])
  Z_ATAG=float(PIPETTE_ATAG[1])
  Y_ATAG=float(PIPETTE_ATAG[2])
  RelMovLTool([X_ATAG, Z_ATAG, Y_ATAG-DY_ATAG, 0, 0, 0],{"a":30,"v":30,"r":5}) #根据atag距离对准atag码
  #Send(CAM:OK)
  #S_DROPCONTAINER_ATAGCHECK=READ(AA,BB,CC)
  S_PIPETTE_ATAGCHECK='30,20,10'
  PIPETTE_ATAGCHECK=S_PIPETTE_ATAGCHECK.split(',')
  X_ATAGCHECK=float(PIPETTE_ATAGCHECK[0])
  Z_ATAGCHECK=float(PIPETTE_ATAGCHECK[1])
  Y_ATAGCHECK=float(PIPETTE_ATAGCHECK[2])
  RelMovLTool([X_ATAGCHECK, Z_ATAGCHECK, Y_ATAGCHECK-DY_ATAG, 0, 0, 0],{"a":30,"v":30,"r":5}) #根据atag距离对准atag码
  P_PIPETTE_ATAG = GetPose()  #获得当前位置
  #Send(CAM:OK)
  #S_PIPETTE_GRAB=READ(GRAB)
  DY_PIPETTE=50
  RelMovLTool([0, 0, DY_PIPETTE, 0, 0, 0],{"a":30,"v":30,"r":5}) #前伸
  SetParallelGripper(10)
  RelMovLTool([0, 50, 0, 0, 0, 0],{"a":30,"v":30,"r":5})
  RelMovLTool([0, 0, -DY_PIPETTE, 0, 0, 0],{"a":30,"v":30,"r":5})
  MovL(P_PIPETTE_ATAG,{"a":20,"v":20,"cp":50})
  #Send(CAM:OK)
  ###### 吸取溶液  ######
  #S_SOLUTION_MOVE=READ(MOVE)
  MovL(P_ATAG,{"a":20,"v":20,"cp":50})
  RelMovLTool([-80, 0, 0, 0, 0, 0],{"a":30,"v":30,"r":5}) #此处X方向移动参数需结合ATAG码与容器的相对位置调整
  #Send(CAM:OK)
  #S_SOLUTION_DOWN=READ(DOWN)
  DZ_SOLUTION=70
  RelMovLTool([0, -DZ_SOLUTION, 0, 0, 0, 0],{"a":30,"v":30,"r":5})
  #Send(CAM:OK)
  #S_SOLUTION_UP=READ(UP)
  RelMovLTool([0, DZ_SOLUTION, 0, 0, 0, 0],{"a":30,"v":30,"r":5})
  #Send(CAM:OK)
  ###### 加液  ######
  #S_ADD_MOVE=READ(MOVE)
  MovL(P_ATAG,{"a":20,"v":20,"cp":50})
  #Send(CAM:OK)
  #S_ADD_DOWN=READ(DOWN)
  DZ_INJECT=70
  RelMovLTool([0, -DZ_INJECT, 0, 0, 0, 0],{"a":30,"v":30,"r":5})
  #Send(CAM:OK)
  #S_ADD_UP=READ(UP)
  RelMovLTool([0, DZ_INJECT, 0, 0, 0, 0],{"a":30,"v":30,"r":5})
  #Send(CAM:OK)
  #收到传回的距离atag码的x_atag,y_atag,z_atag，单位毫米；此处取(30,30,30)
  #将当前机械臂位置存为P0，此处取P1={"joint":[0,0,-90,-60,-120,0]}
  ###### 放下移液枪  ######
  #S_DROPPIPETTE_MOVE=READ(MOVE)
  MovL(P_PIPETTE_ATAG,{"a":20,"v":20,"cp":50})
  RelMovLTool([0, 20, 0, 0, 0, 0],{"a":30,"v":30,"r":5}) #留出余量，具体需要调
  RelMovLTool([0, 0, DY_PIPETTE, 0, 0, 0],{"a":30,"v":30,"r":5})
  RelMovLTool([0, -15, 0, 0, 0, 0],{"a":30,"v":30,"r":5})
  SetParallelGripper(70)
  RelMovLTool([0, 0, -DY_PIPETTE, 0, 0, 0],{"a":30,"v":30,"r":5})
  RelMovLTool([0, 15, 0, 0, 0, 0],{"a":30,"v":30,"r":5})
  MovL(P_PIPETTE_ATAG,{"a":20,"v":20,"cp":50})
  #Send(CAM:OK)
  ###### 夹取容器  ######
  #S_GRABCONTAINER_MOVE=READ(MOVE)
  MovL(P_ATAG,{"a":20,"v":20,"cp":50})
  RelMovLTool([0, -10, 0, 0, 0, 0],{"a":30,"v":30,"r":5})
  RelMovLTool([0, 0, -DY_ATAG, 0, 0, 0],{"a":30,"v":30,"r":5})
  RelMovLTool([0, 10, 0, 0, 0, 0],{"a":30,"v":30,"r":5})
  SetParallelGripper(20)
  MovJ(P0,{"a":30,"v":30,"cp":50})
  #Send(CAM:OK)
  #小车运动到分液工作站
  ###### 放置容器  ######
  #S_EXTRACTION_LEFT=READ(LEFT) 
  MovJ({"joint":[90,0,-90,-90,-90,0]},{"a":30,"v":30,"cp":50})
  #Send(CAM:OK)
  #S_EXTRACTION_ATAG=READ(A,B,C) 
  S_EXTRACTION_ATAG='30,20,20'
  EXTRACTION_ATAG=S_EXTRACTION_ATAG.split(',')
  X_ATAG=float(EXTRACTION_ATAG[0])
  Z_ATAG=float(EXTRACTION_ATAG[1])
  Y_ATAG=float(EXTRACTION_ATAG[2])
  DY_ATAG=10
  RelMovLTool([X_ATAG, Z_ATAG, Y_ATAG-DY_ATAG, 0, 0, 0],{"a":30,"v":30,"r":5}) #根据atag距离对准atag码
  #Send(CAM:OK)
  #S_EXTRACTION_ATAGCHECK=READ(AA,BB,CC) 
  S_EXTRACTION_ATAGCHECK='-30,-20,20'
  EXTRACTION_ATAGCHECK=S_EXTRACTION_ATAGCHECK.split(',')
  X_ATAGCHECK=float(EXTRACTION_ATAGCHECK[0])
  Z_ATAGCHECK=float(EXTRACTION_ATAGCHECK[1])
  Y_ATAGCHECK=float(EXTRACTION_ATAGCHECK[2])
  RelMovLTool([X_ATAGCHECK, Z_ATAGCHECK, Y_ATAGCHECK-DY_ATAG, 0, 0, 0],{"a":30,"v":30,"r":5}) #根据atag距离对准atag码
  P_EXTRACTION = GetPose()  #获得当前位置
  RelMovLTool([0, 0, -20, 0, 0, 0],{"a":30,"v":30,"r":5}) 
  RelMovLTool([0, 30, 0, 0, 0, 0],{"a":30,"v":30,"r":5}) 
  print(P_EXTRACTION)
  X_EXTRACTION=P_EXTRACTION["pose"][0]  
  Y_EXTRACTION=P_EXTRACTION["pose"][2]   #Y方向需结合针头微调
  #Send(CAM:OK)
  #S_EXTRACTION_DOWN=READ(DOWN)
  DY_EXTRACTION=70
  RelMovLTool([0, -DY_EXTRACTION, 0, 0, 0, 0],{"a":20,"v":20,"r":5})
  SetParallelGripper(70)  #松开夹爪
  RelMovLTool([0, 0, -10, 0, 0, 0],{"a":20,"v":20,"r":5})
  #Send(CAM:OK)
  ###### 确定相界面  ######
  #S_INTERFACE_FINE=READ(MOVE) 
  RelMovLTool([0, -30, 0, 0, 0, 0],{"a":20,"v":20,"r":5})
  #Send(CAM:OK)
  #S_INTERFACE=READ(A,B,C) 
  S_INTERFACE='30,20,20'
  k=1  #比例系数，需要调整
  INTERFACE=S_INTERFACE.split(',')
  Z_INTERFACE=k*float(INTERFACE[1])
  RelMovLTool([0, Z_INTERFACE, 0, 0, 0, 0],{"a":30,"v":30,"r":5}) #根据atag距离对准atag码
  #Send(CAM:OK)
  #S_INTERFACE_CHECK=READ(A,B,C) 
  S_INTERFACE_CHECK='30,20,20'
  INTERFACE_CHECK=S_INTERFACE_CHECK.split(',')
  Z_INTERFACE_CHECK=k*float(INTERFACE_CHECK[1])
  RelMovLTool([0, Z_INTERFACE_CHECK, 0, 0, 0, 0],{"a":30,"v":30,"r":5}) #根据atag距离对准atag码
  P_INTERFACE=GetPose()
  print(P_INTERFACE["pose"][1])
  Z_EXTRACTION=P_INTERFACE["pose"][1]
  #Send(CAM:OK)
  ###### 夹取针头  ######
  #S_NEEDLE_MOVE=READ(MOVE) 
  RelMovLTool([80, 0, 0, 0, 0, 0],{"a":30,"v":30,"r":5}) #此处X方向移动参数需结合ATAG码位置调整
  #Send(CAM:OK)
  #S_NEEDLE_ATAG=READ(A,B,C) 
  S_NEEDLE_ATAG='-30,-20,-20'
  NEEDLE_ATAG=S_NEEDLE_ATAG.split(',')
  X_ATAG=float(NEEDLE_ATAG[0])
  Z_ATAG=float(NEEDLE_ATAG[1])
  Y_ATAG=float(NEEDLE_ATAG[2])
  RelMovLTool([X_ATAG, Z_ATAG, Y_ATAG-DY_ATAG, 0, 0, 0],{"a":30,"v":30,"r":5}) #根据atag距离对准atag码
  #Send(CAM:OK)
  #S_NEEDLE_ATAGCHECK=READ(AA,BB,CC) 
  S_NEEDLE_ATAGCHECK='30,20,20'
  NEEDLE_ATAGCHECK=S_NEEDLE_ATAGCHECK.split(',')
  X_ATAGCHECK=float(NEEDLE_ATAGCHECK[0])
  Z_ATAGCHECK=float(NEEDLE_ATAGCHECK[1])
  Y_ATAGCHECK=float(NEEDLE_ATAGCHECK[2])
  RelMovLTool([X_ATAGCHECK, Z_ATAGCHECK, Y_ATAGCHECK-DY_ATAG, 0, 0, 0],{"a":30,"v":30,"r":5}) #根据atag距离对准atag码
  P_NEEDLE_ATAG = GetPose()  #获得当前位置
  #Send(CAM:OK)
  #S_NEEDLE_GRAB=READ(GRAB)
  DY_NEEDLE=50
  RelMovLTool([0, 0, DY_NEEDLE, 0, 0, 0],{"a":30,"v":30,"r":5}) #前伸
  SetParallelGripper(10)
  RelMovLTool([0, 0, -DY_NEEDLE, 0, 0, 0],{"a":30,"v":30,"r":5}) 
  RelMovLTool([0, 50, 0, 0, 0, 0],{"a":30,"v":30,"r":5}) 
  MovL(P_NEEDLE_ATAG,{"a":20,"v":20,"cp":50})
  #Send(CAM:OK)
  ###### 分液  ######
  #S_PUMP_MOVE=READ(MOVE) 
  MovL({"pose":[0, Z_EXTRACTION+80, 0, 90, 0, 180]},{"a":30,"v":30,"r":5}) 
  MovL({"pose":[X_EXTRACTION, Z_EXTRACTION+80, Y_EXTRACTION, 90, 0, 180]},{"a":30,"v":30,"r":5}) 
  MovL({"pose":[X_EXTRACTION, Z_EXTRACTION, Y_EXTRACTION, 90, 0, 180]},{"a":30,"v":30,"r":5}) 
  #Send(CAM:OK)
  #S_PUMP_UP=READ(UP)
  DZ_PUMP=70
  RelMovLTool([0, DZ_PUMP, 0, 0, 0, 0],{"a":30,"v":30,"r":5})
  #Send(CAM:OK)
  ###### 放回枪头  ######
  #S_DROPNEEDLE_MOVE=READ(MOVE) 
  MovL(P_NEEDLE_ATAG,{"a":20,"v":20,"cp":50})
  DY_NEEDLE=50
  RelMovLTool([0, 0, DY_NEEDLE, 0, 0, 0],{"a":30,"v":30,"r":5}) #前伸
  SetParallelGripper(70)
  RelMovLTool([0, 0, -DY_NEEDLE, 0, 0, 0],{"a":30,"v":30,"r":5}) 
  RelMovLTool([0, 50, 0, 0, 0, 0],{"a":30,"v":30,"r":5}) 
  MovL(P_NEEDLE_ATAG,{"a":20,"v":20,"cp":50})
  #Send(CAM:OK)
  ###### 夹取容器  ######
  #S_GRABEXTRACTION_MOVE=READ(MOVE)
  MovL(P_EXTRACTION,{"a":20,"v":20,"cp":50})
  RelMovLTool([0, 0, -10, 0, 0, 0],{"a":20,"v":20,"r":5})
  RelMovLTool([0, -DY_EXTRACTION, 0, 0, 0, 0],{"a":20,"v":20,"r":5})
  RelMovLTool([0, 0, 10, 0, 0, 0],{"a":20,"v":20,"r":5})
  SetParallelGripper(10)  
  MovJ(P0,{"a":30,"v":30,"cp":50})
  #Send(CAM:OK)

class SIGNAL:
  def __init__(self):
    self.exit = False

_cmd = {}

def reg(name):
    def deco(fn):
        _cmd[name] = fn
        return fn
    return deco

@reg("XIQU")
def xiqu(socket):
  # 具体的吸取代码
  TCPWrite(socket,"ARM:XQOK")

# 测试用信号
#@reg("CLOSE")
#def close(socket):
#  global exit
#  exit = True
#  TCPDestroy(socket)

def main():
  is_server=True
  #ip="192.168.5.1"
  ip="192.168.200.1"
  port=5200
  timeout=0
  err, socket = TCPCreate(is_server, ip, port)
  TCPStart(socket, timeout)
  while not s.exit:
    err, data = TCPRead(socket)
    if not data:
      continue
    raw = data.decode().strip()
    if not raw:
      continue
    print("[TCP] 收到:",raw)
    fn = _cmd.get(raw)
    if fn:
      fn(socket)
    else:
      print("[ARM] 未知命令:", raw)

s = SIGNAL()
main()

