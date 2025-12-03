import json

class STATE:
    def __init__(self,path):
        # 0 idle 1 running
        self.state = 0
        self.task = ""
        self.tasks = []
        self.index = 0
        self.load(path)
        self.cb = None
        self.go = False
        self.over = False

    def load(self,path):
        with open(path,"r",encoding="utf-8") as f:
            data = json.load(f)
        self.tasks = data
        self.index = 0
        self.state = 0
        self.task = ""
        self.over = False
        print(f"[TASK] 加载任务序列，共{len(self.tasks)}条")

    def done(self):
        print(f"[TASK] {self.task}完成")
        self.state = 0
        self.task = ""

    def next(self):
        if self.index >= len(self.tasks):
            return None

        self.task = self.tasks[self.index]
        self.index +=1
        self.state = 1
        print(f"[TASK] {self.task}开始")
        return self.task

    def update(self):
        if self.state == 0:
            task = self.next()
            if task is not None:
                if self.cb:
                    self.cb("TASK", task)
            else:
                self.over = True