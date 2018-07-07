import sc2
from sc2.constants import *
from sc2.units import Unit
from random import randint
import math

class FighterAgent(object):
    
    def __init__(self, coordinator):
        self.coordinator = coordinator

    async def on_step(self, iteration):
        if iteration == 0:
            print("first action of Fighter Agent")

    async def attack(self):
        fighters = self.getFighters()
        aux_metade = math.ceil(len(fighters)/2)
        for fighter in range(aux_metade):
            await self.coordinator.do(fighters[fighter].attack(self.coordinator.enemy_start_locations[0]))
        if len(self.coordinator.known_enemy_structures) > 0:
            for fighter in range(aux_metade,len(fighters)-1):
                estrut_aleatoria = randint(0,len(self.coordinator.known_enemy_structures)-1)
                print("Atacando estrutura aleatória")
                await self.coordinator.do(fighters[fighter].attack(self.coordinator.known_enemy_structures[estrut_aleatoria]))

    def addUnits(self, units, unitsAux):
        for unit in unitsAux:
            units.append(unit)
        return units

    def getFighters(self):
        units = []
        self.addUnits(units, self.coordinator.units(ZEALOT))
        self.addUnits(units, self.coordinator.units(SENTRY))
        self.addUnits(units, self.coordinator.units(STALKER))
        self.addUnits(units, self.coordinator.units(IMMORTAL))
        return units