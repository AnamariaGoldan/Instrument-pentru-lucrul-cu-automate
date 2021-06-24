class Nodes():
    def __init__(self,x,y,id,type,size):
        super(Nodes, self).__init__()
        self.x = x
        self.y = y
        self.id = id
        self.type = type
        self.size = size

    def changeSize(self,new_size):
        self.size = new_size

    def changeId(self,new_id):
        self.id = new_id

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getType(self):
        return self.type

    def getSize(self):
        return self.size

    def getId(self):
        return self.id

    def getCenter(self):
        return (self.x,self.y)

    def get_all_info(self):
        return (self.getX(),self.getY(),self.getType(),self.getSize(),self.getId())

class Transition():
    def __init__(self,node_from,node_to,value):
        super(Transition, self).__init__()
        self.node_from = node_from
        self.node_to = node_to
        self.value = []
        self.value.append(value)

    def getNodeFrom(self):
        return self.node_from

    def getNodeTo(self):
        return self.node_to

    def getValues(self):
        return self.value

    def changeNodeFrom(self,node_from_new_id):
        self.node_from = node_from_new_id

    def changeNodeTo(self,node_to_new_id):
        self.node_to = node_to_new_id

    def updateValues(self,new_value):
        if new_value not in self.value:
            self.value.append(new_value)

    def get_all_info(self):
        return (self.getNodeFrom(),self.getNodeTo(),self.getValues())
