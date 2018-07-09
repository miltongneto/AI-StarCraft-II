import random
import sc2
from sc2.constants import *
from sc2.units import Unit, Units
from sc2.position import Point2

class BuilderAgent(object):
    
    def __init__(self, bot):
        self.bot = bot
        self.building_nexus = False
        self.nexus_levels = [(0,1)] ## tuple with nexus index and level

    async def on_step(self, iteration):
        if iteration != 0:
            
            self.update_new_nexus_ready()
            
            for nexus_index in self.nexus_levels:
                if self.bot.units(NEXUS).ready.amount > nexus_index[0]:
                    nexus = self.bot.units(NEXUS)[nexus_index[0]]
                    
                    if nexus_index[1] == 1:
                        await self.createSimpleUnits(nexus, nexus_index)
                    elif nexus_index[1] == 2:
                        await self.expandBase(nexus)

                else: # Fix indexes
                    self.nexus_levels = [(i,1) for i in range(len(self.bot.units(NEXUS).ready.amount))]



    async def buildAssimilators(self, nexus):
        if self.bot.units(ASSIMILATOR).closer_than(12, nexus).amount < 2 and not self.bot.already_pending(ASSIMILATOR):
            for vespeno_gas in self.bot.state.vespene_geyser.closer_than(10.0, nexus):
                if self.bot.can_afford(ASSIMILATOR):
                    proble = self.bot.units(PROBE).closest_to(vespeno_gas)
                    print("Build ASSIMILATOR")
                    await self.bot.do(proble.build(ASSIMILATOR, vespeno_gas))

    async def buildIfNotExist(self, building, pos):
        #pos = self.get_pos_toward_unit(unit_near)
        if ((not self.bot.units(building).closer_than(7, pos).exists) and (self.bot.already_pending(building) == False)):
            if self.bot.can_afford(building):
                print("Build", building)
                await self.bot.build(building, near=pos)
    
    async def build_structure(self, building, pos, n):
        if ((self.bot.units(building).closer_than(15, pos).amount < n) and (self.bot.already_pending(building) == False)):
            if self.bot.can_afford(building):
                print("Build", building)
                await self.bot.build(building, near=pos)

    async def createSimpleUnits(self, nexus, nexus_index):
        pos = self.get_pos_toward_unit(nexus)
        await self.buildIfNotExist(PYLON, pos)

        if self.bot.units(PYLON).closer_than(5, pos).exists:
            pylon = self.bot.units(PYLON).closer_than(5, pos).first
          
            await self.buildIfNotExist(GATEWAY, pylon)
            
            if self.bot.units(ASSIMILATOR).closer_than(10, nexus).amount < 2:
                await self.buildAssimilators(nexus)
        
        if (self.bot.units(PYLON).closer_than(5, pos).ready.exists and self.bot.units(GATEWAY).closer_than(5, pos).ready.exists):
            pylon = self.bot.units(PYLON).closer_than(5, pos).first

            await self.buildIfNotExist(CYBERNETICSCORE, pylon)
        
        if (self.bot.units(CYBERNETICSCORE).closer_than(12, pos).ready.exists):
            self.nexus_levels[nexus_index[0]] = (nexus_index[0], 2)

    async def buildPhotonCannon(self, nexus):
        if not self.bot.units(PHOTONCANNON).exists and self.bot.can_afford(PHOTONCANNON):
            pylon = self.bot.units(PYLON).closest_to(self.bot.enemy_start_locations[0])
            await self.bot.build(PHOTONCANNON, pylon)

    async def buildPylon(self, nexus):
        if self.bot.supply_left < 2 and not self.bot.already_pending(PYLON) and self.bot.can_afford(PYLON):
            await self.bot.build(PYLON, nexus)
    
    async def expandBase(self, nexus):    
        await self.build_structure(PYLON, nexus, 4)
        await self.build_structure(FORGE, nexus, 1)
        await self.buildPhotonCannon(nexus)

        await self.buildPylon(nexus)

        if self.bot.units(PYLON).closer_than(10, nexus).amount >= 2:
            pylon = self.bot.units(PYLON).closer_than(10, nexus)[1]
            await self.build_structure(GATEWAY, pylon, 2)

        if self.bot.units(CYBERNETICSCORE).ready.exists:
            cyberneticscore = self.bot.units(CYBERNETICSCORE)[0]
            await self.buildIfNotExist(ROBOTICSFACILITY, cyberneticscore)


    async def newNexusAndBase(self):
        if self.bot.units(NEXUS).amount < 2 and not self.bot.already_pending(NEXUS) and self.bot.can_afford(NEXUS):
            nexus = self.bot.units(NEXUS).first
            worker = self.bot.workers[0]
            minerals_next_nexus = self.bot.state.mineral_field.closer_than(15, nexus)
            minerals = self.bot.state.mineral_field
            minerals = Units(self.removeMinerals(minerals_next_nexus, minerals), self.bot._game_data)
            mineral_field = minerals.closest_to(nexus)
            
            if not self.bot.units(PYLON).closer_than(20.0, mineral_field).exists and not self.bot.already_pending(PYLON):
                print("Build ", PYLON)
                await self.bot.build(PYLON, mineral_field, max_distance=10, unit=worker)
            
            if self.bot.can_afford(NEXUS):
                print("Build ", NEXUS)
                self.building_nexus = True
                await self.bot.build(NEXUS, mineral_field, max_distance=10, unit=worker)
        #elif self.bot.units(NEXUS).ready.amount > 1:
        #    await self.createSimpleUnits(self.bot.units(NEXUS)[1])

    def update_new_nexus_ready(self):
        if self.building_nexus == True and len(self.nexus_levels) < self.bot.units(NEXUS).ready.amount:
            self.building_nexus = False
            self.nexus_levels.append((len(self.nexus_levels), 1))

    def removeMinerals(self, minerals_next_nexus, minerals):
        return [mineral for mineral in minerals if mineral not in minerals_next_nexus]

    def get_pos_toward_unit(self, unit_pos):
        enemy_towards = unit_pos.position.to2.unit_axes_towards(self.bot.enemy_start_locations[0].position)
        pos = Point2((unit_pos.position[0] + (enemy_towards[0] * 10), unit_pos.position[1] + (enemy_towards[1] * 4)))
        return pos
        
        