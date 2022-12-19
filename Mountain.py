import mesa
import random
####### Start MESA #########
high_list=["K1","K2","K3"]
class MountainAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.location=[0,0]
        self.high=self.random.choice(high_list)
        self.Type="Mountain"
        self.bettary=0

####### END MESA ##########