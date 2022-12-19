import mesa
import math
from FirstAid_Robot import *
#from RobotAssignment import *
from Person import *
import threading
import time
####### Start MESA #########
class ExploreAgent(mesa.Agent):
    """An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.max_speed=500 #initial value    
        self.name=""  #initial value  
        self.move_direction="front" #initial value  
        self.bettary=100 #initial value
        self.isServing=False #initial value
        self.nearest=-1
        self.Type="Drone"
        self.Num=0
    def step(self):
        if(self.isServing==False):
            self.move()
    def move(self):
        if(self.bettary > 0 and self.isServing==False):
            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore=True,
                include_center=False)       
            new_position = self.random.choice(possible_steps)
            newX,newY=new_position #Get New Position moved to
            self.x,self.y=self.pos #Get Old position
            self.model.grid.move_agent(self, new_position) #move to Position
            person=self.find_nearest()
            if person != None:
                firstAid=self.random.choice(self.model.firstAidList)
                if firstAid != None and firstAid.bettary >=50 :
                    x,y=person.pos
                    firstAid.move(x,y)
                    print('Get to Person')
            distance= math.sqrt(math.pow((self.x - newX),2) + math.pow((self.y - newY),2))
            self.bettary -= math.floor(distance)
            if(self.bettary < 0):
                self.bettary=0
        else:
            width = self.model.grid.width
            x = width - self.Num
            y = 1 
            self.model.grid.move_agent(self, (x,y))            
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
            self.isServing = True
            print('Found Person Number: '+other.unique_id)
            return other
        self.isServing=False
        return None

