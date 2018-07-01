import random

import sc2
from sc2 import Race
from sc2.constants import *
from sc2.player import Bot
from sc2.units import Unit


from builderBot import BuilderAgent
from fighterBot import FighterAgent
from collectorBot import CollectorAgent
from scouterBot import ScouterBot
from sc2.player import Bot

class LeaderBot(sc2.BotAI):
    messagesQueue = []

    async def on_step(self, iteration):
        if iteration == 0:
            print("First action")
            self.agents = [('Builder', BuilderAgent(self)), ('Collector', CollectorAgent(self))]
        else:
            if self.units(NEXUS).exists:
                nexus = self.units(NEXUS).first
                
                await self.trainProbe(nexus)

                scouters = self.getAgent('Scouter')
                if scouters == None:
                    self.agents.append(('Scouter', ScouterBot(self)))
                
                if (self.supply_used > 10):
                    await self.getAgent('Builder').newNexusAndBase()
                    await self.getAgent('Scouter').scouting(2)


                if (self.units(GATEWAY).ready.exists):
                    for gateway in self.units(GATEWAY).ready:
                        await self.createArmy(gateway)

                if (self.supply_used > 32 and len(self.getAgent('Fighter').getFighters()) >= 15):
                    await self.getAgent('Fighter').attack()

                if (self.units(ROBOTICSFACILITY).ready.exists and self.units(IMMORTAL).amount < 3):
                    roboticsfacility = self.units(ROBOTICSFACILITY)[0]
                    if self.can_afford(IMMORTAL) and roboticsfacility.noqueue:
                        await self.do(roboticsfacility.train(IMMORTAL)) 
                
                for (_,agent) in self.agents:
                    await agent.on_step(iteration)
                
            else:
                print("Without nexus")       


    async def trainProbe(self, nexus):
        if not self.can_afford(PROBE):
            return
        if self.workers.amount < 16 and nexus.noqueue:
            print("Training PROBE")
            await self.do(nexus.train(PROBE))
        elif self.units(PYLON).amount >= 2 and self.units(PROBE).amount < 22 and nexus.noqueue:
            print("Training PROBE")
            await self.do(nexus.train(PROBE))
            

    async def createArmy(self, gateway):
        if self.units(ZEALOT).amount < 5 and gateway.noqueue:
            if self.can_afford(ZEALOT):
                await self.do(gateway.train(ZEALOT)) 
        elif self.units(SENTRY).amount < 4 and gateway.noqueue:
            if self.can_afford(SENTRY):
                await self.do(gateway.train(SENTRY))
        elif self.units(STALKER).amount < 6 and gateway.noqueue:
            if self.can_afford(STALKER):
                await self.do(gateway.train(STALKER))
                                
        agent = self.getAgent('Fighter')
        if agent == None:
            self.agents.append(('Fighter', FighterAgent(self)))
            

    def getAgent(self, key):
        for (k, v) in self.agents:
            if key == k:
                return v
        return None
