import sc2
from sc2.constants import *
from sc2.units import Unit, Units
from random import randint
import math
import configCounterScout

class ScouterBot(object):
    configCounterScout.counter = 0

    def __init__(self, coordinator):
        self.coordinator = coordinator
    
    async def on_step(self, iteration):
        if(iteration != 0):
            await self.scouting()

    async def scouting(self):
        if self.coordinator.units(PROBE).idle.exists:
            arry_aux = self.coordinator.units(PROBE).idle
            for probe in range(math.ceil(len(arry_aux)/2)):
                #ver se consigo passar qtd por parametro depois   
                if configCounterScout.counter == 0:
                    configCounterScout.counter += 1 
                    print("Scouting na localizacao inicial") 
                    await self.coordinator.do(arry_aux[probe].move(self.coordinator.enemy_start_locations[0]))
