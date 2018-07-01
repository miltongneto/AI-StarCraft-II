import sc2
from sc2.constants import *
from sc2.units import Unit, Units
from random import randint

class ScouterBot(object):
    global counter = 0

    def __init__(self, coordinator):
        self.coordinator = coordinator
    
    async def on_step(self, iteration):
        if(iteration != 0):
            await self.scouting()

    async def scouting(self,qtd):
        if self.coordinator.units(PROBE).idle.exists:
            for probe in self.coordinator.units(PROBE).idle:
                if counter <= qtd:
                    #for possible_enemy_base in self.coordinator.enemy_start_locations:
                    possivel_base_aleatoria_indice = randint(0,len(self.coordinator.enemy_start_locations)-1)
                    counter = counter+1
                    print("Scouting na localizacao",possivel_base_aleatoria_indice) 
                    await self.coordinator.do(probe.move(self.coordinator.enemy_start_locations[possivel_base_aleatoria_indice]))
