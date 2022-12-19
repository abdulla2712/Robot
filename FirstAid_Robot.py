import mesa
import math
import threading
import time
from Person import *
####### Start MESA #########
class Aid:
    water=100 #initial value
    blanket=100 #initial value
    painkillers=500 #initial value
class FirstAidAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.max_speed=500 #initial value 
        self.name=""   
        self.aid=Aid()
        self.bettary=100 #initial value
        self.Type="First Aid"
        self.isServing=False        
        self.Num=0
    def move(self,x,y):
        if(self.bettary > 0):
            self.x,self.y=self.pos
            self.model.grid.move_agent(self, (x,y))
            distance= math.sqrt(math.pow((self.x - x),2) + math.pow((self.y - y),2) )
            if(self.bettary < 0):
                self.bettary=0
        else:
            width = self.model.grid.width
            originX = width - self.Num
            originY = 13 
            self.model.grid.move_agent(self, (originX,originY))            
            t1 = threading.Thread(target=self.charging)
            t1.start()
    def charging(self):
        time.sleep(10)
        self.bettary=100
    def find_nearest(self):
        nearest=[]
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for item in cellmates:
                if isinstance(item, PersonAgent):
                    nearest.append(item)
        if len(nearest) > 1:
            other = self.random.choice(cellmates)
            self.isServing=True
            print('Found Person Number: '+other.unique_id)
            return other
        self.isServing=False
        return None
