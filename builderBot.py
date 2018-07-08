import random
import sc2
from sc2.constants import *
from sc2.units import Unit, Units

class BuilderAgent(object):
    
    def __init__(self, bot):
        self.bot = bot
        self.phase = 1

    async def on_step(self, iteration):
        if iteration != 0:
            if self.bot.units(NEXUS).exists:
                nexus = self.bot.units(NEXUS).first
                if self.phase == 1:
                    await self.createSimpleUnits(nexus)
                elif self.phase == 2:
                    await self.expandBase(nexus)

            else:
                print("Without nexus")

    async def buildAssimilators(self, nexus):
        if self.bot.units(ASSIMILATOR).amount < 2 and not self.bot.already_pending(ASSIMILATOR):
            for vespeno_gas in self.bot.state.vespene_geyser.closer_than(20.0, nexus):
                if self.bot.can_afford(ASSIMILATOR):
                    proble = self.bot.units(PROBE).closest_to(vespeno_gas)
                    print("Build ASSIMILATOR")
                    await self.bot.do(proble.build(ASSIMILATOR, vespeno_gas))

    async def buildSothingIfNotExist(self, building, pos):
        if ((not self.bot.units(building).exists) and (self.bot.already_pending(building) == False)):
            if self.bot.can_afford(building):
                print("Build", building)
                await self.bot.build(building, near=pos)
    
    async def buildSothing(self, building, pos, n):
        if ((self.bot.units(building).amount < n) and (self.bot.already_pending(building) == False)):
            if self.bot.can_afford(building):
                print("Build", building)
                await self.bot.build(building, near=pos)

    async def createSimpleUnits(self, nexus):
        await self.buildSothingIfNotExist(PYLON, nexus)
                        
        if self.bot.units(PYLON).exists:
            pylon = self.bot.units(PYLON).first
            
            await self.buildSothingIfNotExist(GATEWAY, pylon)
            await self.buildAssimilators(nexus)
        
        if (self.bot.units(PYLON).exists and self.bot.units(GATEWAY).ready.exists):
            await self.buildSothingIfNotExist(CYBERNETICSCORE, pylon)
            self.phase = 2

    async def buildPhotonCannon(self, nexus):
        if not self.bot.units(PHOTONCANNON).exists and self.bot.can_afford(PHOTONCANNON):
            pylon = self.bot.units(PYLON).closest_to(self.bot.enemy_start_locations[0])
            await self.bot.build(PHOTONCANNON, pylon)

    async def buildPylon(self, nexus):
        if self.bot.supply_left < 2 and not self.bot.already_pending(PYLON) and self.bot.can_afford(PYLON):
            await self.bot.build(PYLON, nexus)
    
    async def expandBase(self, nexus):    
        await self.buildSothing(PYLON, nexus, 4)
        await self.buildSothing(FORGE, nexus, 1)
        await self.buildPhotonCannon(nexus)

        await self.buildPylon(nexus)

        if self.bot.units(PYLON).amount >= 2:
            pylon = self.bot.units(PYLON)[1]
            await self.buildSothing(GATEWAY, pylon, 2)

        if self.bot.units(CYBERNETICSCORE).ready.exists:
            cyberneticscore = self.bot.units(CYBERNETICSCORE)[0]
            await self.buildSothingIfNotExist(ROBOTICSFACILITY, cyberneticscore)
            await self.buildSothingIfNotExist(STARGATE,cyberneticscore)

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
                await self.bot.build(NEXUS, mineral_field, max_distance=10, unit=worker)
        elif self.bot.units(NEXUS).ready.amount > 1:
            await self.createSimpleUnits(self.bot.units(NEXUS)[1])

    def removeMinerals(self, minerals_next_nexus, minerals):
        return [mineral for mineral in minerals if mineral not in minerals_next_nexus]
    
        
        