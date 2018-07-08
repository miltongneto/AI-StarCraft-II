import random

import sc2
from sc2 import Race
from sc2.constants import *
from sc2.player import Bot
from sc2.units import Unit
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.ability_id import AbilityId

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

                if (self.units(GATEWAY).ready.exists):
                    for gateway in self.units(GATEWAY).ready:
                        await self.createArmy(gateway)
                    await self.getAgent('Scouter').scouting()    

                if (self.supply_used > 32 and len(self.getAgent('Fighter').getFighters()) >= 12):
                    await self.getAgent('Fighter').attack()

                if (self.units(ROBOTICSFACILITY).ready.exists and self.units(IMMORTAL).amount < 3):
                    roboticsfacility = self.units(ROBOTICSFACILITY)[0]
                    if self.can_afford(IMMORTAL) and roboticsfacility.noqueue:
                        await self.do(roboticsfacility.train(IMMORTAL))
                    
                if self.units(ROBOTICSFACILITY).ready.exists and self.units(OBSERVER).amount == 0:
                    robotfac = self.units(ROBOTICSFACILITY).first
                    if self.can_afford(OBSERVER) and len(robotfac.orders) < 3:
                        await self.do(robotfac.train(OBSERVER))

                if self.units(FORGE).ready.exists:
                    forge = self.units(FORGE).first
                    abilities = await self.get_available_abilities(forge)
                    if AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL1 in abilities and self.can_afford(AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL1): #and AbilityId.FORGERESEARCH_PROTOSSGROUNDARMORLEVEL1 in abilities:
                        print("Melhoramento em armas de unidades térreas")
                        await self.do(forge(AbilityId.FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL1)) #aprimorar armamento
                    if AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL1 in abilities and self.can_afford(AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL1):
                        print("Melhoramento de escudos em unidades térreas")
                        await self.do(forge(AbilityId.FORGERESEARCH_PROTOSSSHIELDSLEVEL1))

                if(self.units(OBSERVER).exists):
                    await self.getAgent("Scouter").scoutObserver()#scout com observadores

                if self.units(CYBERNETICSCORE).ready.exists: #melhoria em armas e armaduras de unidades aéreas
                    cybercore = self.units(CYBERNETICSCORE).first
                    abilities = await self.get_available_abilities(cybercore)
                    if AbilityId.CYBERNETICSCORERESEARCH_PROTOSSAIRWEAPONSLEVEL1 in abilities and self.can_afford(AbilityId.CYBERNETICSCORERESEARCH_PROTOSSAIRWEAPONSLEVEL1):
                        print("Melhoramento em armas de unidades aéreas")
                        await self.do(cybercore(AbilityId.CYBERNETICSCORERESEARCH_PROTOSSAIRWEAPONSLEVEL1))
                    if AbilityId.CYBERNETICSCORERESEARCH_PROTOSSAIRARMORLEVEL1 in abilities and self.can_afford(AbilityId.CYBERNETICSCORERESEARCH_PROTOSSAIRARMORLEVEL1):
                        print("Melhoramento em armadura de unidades aéreas")
                        await self.do(cybercore(AbilityId.CYBERNETICSCORERESEARCH_PROTOSSAIRARMORLEVEL1))

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
        if self.units(ZEALOT).amount < 5 and len(gateway.orders)<2:
            if self.can_afford(ZEALOT):
                await self.do(gateway.train(ZEALOT)) 
        elif self.units(SENTRY).amount < 4 and len(gateway.orders)<2 and self.units(ROBOTICSFACILITY).exists:
            if self.can_afford(SENTRY):
                await self.do(gateway.train(SENTRY))
        elif self.units(STALKER).amount < 6 and len(gateway.orders)<2:
            if self.can_afford(STALKER):
                await self.do(gateway.train(STALKER))
        #usando stargate para unidades aéreas
        if self.units(STARGATE).amount > 0:
            stargate = self.units(STARGATE).first
            if self.can_afford(VOIDRAY) and self.units(VOIDRAY).amount < 3:
                await self.do(stargate.train(VOIDRAY))
                                
        agent = self.getAgent('Fighter')
        if agent == None:
            self.agents.append(('Fighter', FighterAgent(self)))
            

    def getAgent(self, key):
        for (k, v) in self.agents:
            if key == k:
                return v
        return None
