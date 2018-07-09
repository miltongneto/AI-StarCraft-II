import sc2
from sc2.constants import *
from sc2.units import Unit
from sc2.ids.unit_typeid import UnitTypeId
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
        for fighter in fighters:
            if fighter.is_idle and self.coordinator.known_enemy_structures.exists:
                await self.coordinator.do(fighter.attack(self.coordinator.known_enemy_structures.random))
                abilities = await self.coordinator.get_available_abilities(fighter)
                if fighter.type_id == UnitTypeId.SENTRY:
                    if AbilityId.GUARDIANSHIELD_GUARDIANSHIELD in abilities:
                        await self.coordinator.do(fighter(AbilityId.GUARDIANSHIELD_GUARDIANSHIELD))
                elif fighter.type_id == UnitTypeId.VOIDRAY:
                    if AbilityId.EFFECT_VOIDRAYPRISMATICALIGNMENT in abilities:
                        await self.coordinator.do(fighter(AbilityId.EFFECT_VOIDRAYPRISMATICALIGNMENT))

    async def defendBase(self, nexus):
        fighters = self.getFighters()
        for fighter in fighters:
            await self.coordinator.do(fighter.move(nexus.position))
            if self.coordinator.known_enemy_units.closest_to(nexus):    
                await self.coordinator.do(fighter.attack(self.coordinator.known_enemy_units.closest_to(nexus)))

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
        self.addUnits(units, self.coordinator.units(VOIDRAY))
        return units

    async def defend(self, nexus, enemies):
        fighters = self.getFighters()
        
        for fighter in fighters:
            if fighter.position.to2.distance_to(nexus) < 50:
                await self.coordinator.do(fighter.attack(enemies.closest_to(fighter))) 
