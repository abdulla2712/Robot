from random import random 
import mesa
from mesa.datacollection import DataCollector
from Explore_Robot import *
from FirstAid_Robot import *
from Mountain import *
from Person import *
import matplotlib.pyplot as plt
import numpy as np

def compute_gini(model):
    agent_health = [agent.bettary for agent in model.schedule.agents]
    x = sorted(agent_health)
    N =len(agent_health)
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1 / N) - 2 * B 
#create the Model -Grid
class Model(mesa.Model):
    #A model with some number of agents.

    def __init__(self, ex,fa,p, width, height):
        self.num_explore_robot = ex
        self.num_firstaid_robot = fa
        self.num_person=p
        self.grid = mesa.space.MultiGrid(width, height, True)        
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        self.Type=""
        self.droneList = [] #list of Drones
        self.firstAidList = [] #list of FirstAid
        self.personList = []  #list of Persons
        posX=1
        posY=13
        # Create agents and place them into the grid
        for i in range(self.num_explore_robot):
            a = ExploreAgent("Drone_"+str(i+1), self)
            a.Num=i+1
            self.set_position(a,i)
            self.droneList.append(a)
            self.Type="Drone"
        for j in range(self.num_firstaid_robot):
            b = FirstAidAgent("FirstAid_"+str(j+1), self)
            b.Num=j+1
            self.set_position(b,j)
            self.firstAidList.append(b)
            self.Type="First Aid"
        for k in range(self.num_person):
            c = PersonAgent("Person_"+str(k+1), self)        
            c.Num = k+1
            self.set_position(c,k)
            self.personList.append(c)
            self.Type="Person"            
        for t in range(25): #Print the Green Area
            d = MountainAgent("Mountain_"+ str(t+1), self)
            self.Type="Mountain"
            self.schedule.add(d)           
            if(posX >= 6):
                posX = 1
                posY -= 1          
            self.grid.place_agent(d, (posX, posY)) 
            posX += 1
        self.data_collector = mesa.DataCollector(
            model_reporters={"Gini": compute_gini}, agent_reporters={"Bettary": "bettary"} 
        )
    def step(self):
        #Advance the model by one step.
        self.data_collector.collect(self)
        self.schedule.step() 
        
    def set_position(self,d,num):
        self.schedule.add(d)
        width = self.grid.width
        if(d.Type=="Drone"):
            x = width - (num +1)
            y = 1 
        elif(d.Type=="First Aid"):
            x = width - (num + 1)
            y = 13              
        if(d.Type=="Person"):
             min_w,max_w,min_h,max_h=1,5,10, 13
             x = self.random.randrange(min_w,max_w)
             y = self.random.randrange(min_h,max_h)          
        # Add the agent to a random grid cell            
        self.grid.place_agent(d, (x, y)) 
     
            
########## Visualizing Object #############
def agent_portrayal(agent):
    portrayal = {"Filled": "true",
                 "r": 0.6}
    if agent.Type =="Mountain":
        portrayal["Color"] = "lightgreen"
        portrayal["Layer"] = 0
        portrayal["Shape"]="rect"
        portrayal["w"] = 1
        portrayal["h"] = 1
    if agent.Type =="Drone":
        portrayal["Shape"]="circle"
        portrayal["Color"] = "yellow"
        portrayal["Layer"] = 1
        portrayal["text"] = agent.bettary
        portrayal["text_color"] = "black"
    elif agent.Type =="First Aid":
        portrayal["Shape"]="circle"
        portrayal["Color"] = "red"
        portrayal["Layer"] =2
        portrayal["text"] = agent.bettary
        portrayal["text_color"] = "black"
    elif agent.Type =="Person":
        portrayal["Shape"]="circle"
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 3
        portrayal["text"] = agent.Num
        portrayal["text_color"] = "black"
        
    return portrayal
########## End visualization ##############

def main():
    #####create visualization#####

    grid = mesa.visualization.CanvasGrid(agent_portrayal,15, 15, 500, 500)

    server = mesa.visualization.ModularServer(
        Model, [grid], "Model", {"ex": 2,"fa": 3,"p":3, "width": 15, "height": 15}
    )
    server.port = 8521  # The default
    server.launch()
    
    #end visualization
   

if __name__ == "__main__":
    main()