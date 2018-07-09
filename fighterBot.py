import sc2
from sc2.constants import *
from sc2.units import Unit
from random import randint
from priorityConstants import Priority
import math

class FighterAgent(object):
    
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self.attacking = False

    async def on_step(self, iteration):
        if iteration == 0:
            print("first action of Fighter Agent")
        else:
            if self.attacking and (iteration % 2) == 0:
                self.need_help()
                    

    async def attack(self):
        self.attacking = True
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

    async def defend(self, nexus, enemies):
        fighters = self.getFighters()
        
        for fighter in fighters:
            if fighter.position.to2.distance_to(nexus) < 50:
                await self.coordinator.do(fighter.attack(enemies.closest_to(fighter))) 

    def get_fighters_attacking(self):
        fighters = self.getFighters()
        fighters_attacking = []
        
        for fighter in fighters:
            if not fighter.is_idle:
                fighters_attacking.append(fighter)

        return fighters_attacking

    def need_help(self):
        enemies = len([enemy for enemy in self.coordinator.known_enemy_units if enemy not in self.coordinator.known_enemy_structures])
        fighters = len(self.get_fighters_attacking())

        diff = fighters - enemies
        if diff <= 2:
            self.attacking = False
        elif diff >= 5 and diff <= 10:
            self.coordinator.messagesQueue.append(('Fighter', Priority.WARNING, enemies, fighters))


