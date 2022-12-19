import mesa
import random
####### Start MESA #########
health_condition=["Very Good","Good","Bad","Very Bad"]
class PersonAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.location=[0,0]
        self.age=random.randrange(15,45) #initial range
        self.health=self.random.choice(health_condition)
        self.Type="Person"
        self.Num=0
        self.bettary=0