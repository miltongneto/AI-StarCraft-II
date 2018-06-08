import sc2
from sc2.constants import *
from sc2.units import Unit

class FighterAgent(object):
    
    def __init__(self, coordinator):
        self.coordinator = coordinator

    async def on_step(self, iteration):
        if iteration == 0:
            print("first action of Fighter Agent")

    async def attack(self):
        fighters = self.getFighters()
        for fighter in fighters:
            await self.coordinator.do(fighter.attack(self.coordinator.enemy_start_locations[0]))

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