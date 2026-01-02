import time
exit = False
is_server=True
ip="192.168.5.1"
#ip="192.168.200.1"
port=5200
timeout=0
err, socket = TCPCreate(is_server, ip, port)
TCPStart(socket, timeout)
TCPWrite(socket,"ARM:NIHAO")
#SetParallelGripper(40)
SetParallelGripper(18)
while not exit:
  err, data = TCPRead(socket)
  if not data:
    continue
  raw = data.decode().strip()
  if not raw:
    continue
  print("[TCP] 收到:",raw)
  if raw.startswith("ATAG="):
    buf = raw[5:]
    fn = _cmd.get("ATAG=")
    fn(socket,buf)
    continue
  if raw.startswith("PHASE="):
    buf = raw[6:]
    fn = _cmd.get("PHASE=")
    fn(socket,buf)
    continue
  fn = _cmd.get(raw)
  if fn:
    fn(socket)
  else:
    print("[ARM] 未知命令:", raw)
