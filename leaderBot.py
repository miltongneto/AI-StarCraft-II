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
            self.agents = {'Builder' : BuilderAgent(self), 'Collector' : CollectorAgent(self), 'Scouter' : ScouterBot(self), 'Fighter' : FighterAgent(self) }
        else:
            await self.read_messages()
            
            if self.units(NEXUS).exists:
                for nexus in self.units(NEXUS).ready:
                    await self.verify_attack(nexus)
                    await self.trainProbe(nexus)
                
                if (self.supply_used > 10):
                    await self.agents['Builder'].newNexusAndBase()
                    await self.agents['Scouter'].scouting()


                if (self.units(GATEWAY).ready.exists):
                    for gateway in self.units(GATEWAY).ready:
                        await self.createArmy(gateway)

                if (len(self.agents['Fighter'].getFighters()) >= 25):
                    await self.agents['Fighter'].attack()

                if (self.units(ROBOTICSFACILITY).ready.exists): ##  and self.units(IMMORTAL).amount < 3
                    roboticsfacility = self.units(ROBOTICSFACILITY)[0]
                    if self.can_afford(IMMORTAL) and roboticsfacility.noqueue:
                        await self.do(roboticsfacility.train(IMMORTAL)) 
                
                for agent in self.agents:
                    await self.agents[agent].on_step(iteration)
                
            else:
                print("Without nexus")       


    async def trainProbe(self, nexus):
        if not self.can_afford(PROBE):
            return
        if self.workers.amount < (16 * self.units(NEXUS).ready.amount) and nexus.noqueue:
            print("Training PROBE")
            await self.do(nexus.train(PROBE))
        elif self.units(PYLON).amount >= 2 and self.units(PROBE).amount < 22 and nexus.noqueue:
            print("Training PROBE")
            await self.do(nexus.train(PROBE))
            

    async def createArmy(self, gateway):
        if gateway.noqueue:
            if self.units(ZEALOT).amount < 5 or not self.units(CYBERNETICSCORE).ready.exists:
                if self.can_afford(ZEALOT):
                    await self.do(gateway.train(ZEALOT)) 
            elif self.units(SENTRY).amount < 5:
                if self.can_afford(SENTRY):
                    await self.do(gateway.train(SENTRY))
            ##elif self.units(STALKER).amount < 6 and gateway.noqueue:
            else:
                if self.can_afford(STALKER):
                    await self.do(gateway.train(STALKER))

    async def verify_attack(self, nexus):
        enemies = self.known_enemy_units.closer_than(20.0, nexus)
        if (enemies.exists and enemies.amount > 1):
            await self.agents['Fighter'].defend(nexus, enemies)

    async def read_messages(self):
        for message in self.messagesQueue:
            if (message[0] == 'Fighter'):
                fighters = self.agents['Fighter'].getFighters()
                
                fighters_idle = []
                for f in fighters:
                    if f.is_idle:
                        fighters_idle.append(f)
                
                if len(fighters_idle) >= 5:
                    await self.agents['Fighter'].attack()

        self.messagesQueue = []
