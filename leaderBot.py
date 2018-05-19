import random

import sc2
from sc2 import Race
from sc2.constants import *
from sc2.player import Bot
from sc2.units import Unit

class LeaderBot(sc2.BotAI):
    async def on_step(self, iteration):
        if iteration == 0:
            print("First action")
        else:
            if self.units(NEXUS).exists:
                nexus = self.units(NEXUS).first
                await self.trainProbe(nexus)
                await self.buildSothingIfNotExist(PYLON, nexus)
                
                if self.units(PYLON).exists:
                    pylon = self.units(PYLON).first
                    await self.buildSothingIfNotExist(GATEWAY, pylon)
                    await self.buildAssimilator(nexus)
                
                if (self.units(PYLON).exists & self.units(GATEWAY).exists):
                    await self.buildSothingIfNotExist(CYBERNETICSCORE, pylon)

                if self.units(PROBE).idle.exists:
                    for proble in self.units(PROBE).idle:
                        mineral_closest = self.state.mineral_field.closest_to(proble)
                        proble.gather(mineral_closest)
            else:
                print("Without nexus")       


    async def trainProbe(self, nexus):
        if self.workers.amount < 16 and nexus.noqueue:
            if self.can_afford(PROBE):
                print("Training PROBE")
                await self.do(nexus.train(PROBE))


    async def buildAssimilator(self, nexus):
        if not self.units(ASSIMILATOR).exists and not self.already_pending(ASSIMILATOR):
            if self.can_afford(ASSIMILATOR):
                vespeno_gas = self.state.vespene_geyser.closest_to(nexus)
                proble = self.units(PROBE).closest_to(vespeno_gas)
                print("Build ASSIMILATOR")
                await self.do(proble.build(ASSIMILATOR, vespeno_gas))

    async def buildSothingIfNotExist(self, building, pos):
        if not self.units(building).exists and not self.already_pending(building):
            if self.can_afford(building):
                print("Build ", building)
                await self.build(building, near=pos)
