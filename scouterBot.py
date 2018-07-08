import sc2
from sc2.constants import *
from sc2.units import Unit, Units
from random import randint
import math
import configCounterScout

class ScouterBot(object):

    def __init__(self, coordinator):
        self.coordinator = coordinator
    
    async def on_step(self, iteration):
        if iteration != 0:
            await self.scouting()
            await self.scoutObserver()

    async def scouting(self):
        if self.coordinator.units(PROBE).idle.exists:   
            random_scouter = self.coordinator.units(PROBE).idle.random 
            if configCounterScout.counter == 0:
                configCounterScout.counter = configCounterScout.counter+1 
                print("Scouting na localizacao inicial")
                await self.coordinator.do(random_scouter.move(self.coordinator.enemy_start_locations[0], True))
            elif configCounterScout.counter < 3:
                print("Scouting em algum campo de minério...", configCounterScout.counter)
                rand = randint(0,self.coordinator.state.mineral_field.amount-1)
                configCounterScout.counter = configCounterScout.counter+1 
                await self.coordinator.do(random_scouter.move(self.coordinator.state.mineral_field[rand].position, True))
    
    async def scoutObserver(self):
        if self.coordinator.units(OBSERVER).idle.exists:
           observador = self.coordinator.units(OBSERVER).idle.random
           print("Scouting de observador!")
           await self.coordinator.do(observador.move(self.coordinator.state.mineral_field.random.position, True)) 
