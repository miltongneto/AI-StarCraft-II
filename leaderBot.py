import random

import sc2
from sc2 import Race
from sc2.constants import *
from sc2.player import Bot
from sc2.units import Unit


from builderBot import BuilderAgent
from fighterBot import FighterAgent
from collectorBot import CollectorAgent
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

                if (self.units(GATEWAY).ready.exists):
                    await self.createArmy(self.units(GATEWAY).first)

                if (self.supply_used - self.workers.amount >= 20):
                    await self.getAgent('Fighter').attack()

                if (self.units(ROBOTICSFACILITY).ready.exists and self.units(ZEALOT).amount < 3):
                    roboticsfacility = self.units(ROBOTICSFACILITY)[0]
                    if self.can_afford(IMMORTAL) and roboticsfacility.noqueue:
                        await self.do(roboticsfacility.train(IMMORTAL)) 
                
                if (self.units(GATEWAY).amount >= 2 and self.units(GATEWAY)[1].is_ready):
                    await self.createArmy(self.units(GATEWAY)[1])                

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
        #agent = filter(lambda k,v: k == key, self.agents)
        #return agent