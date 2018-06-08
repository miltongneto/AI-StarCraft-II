import sc2
from sc2.constants import *
from sc2.units import Unit, Units

class CollectorAgent(object):
    
    def __init__(self, bot):
        self.bot = bot

    async def on_step(self, iteration):
        if iteration != 0:
            await self.gatherVespeneGas()
            await self.useIdleProbles()

    async def useIdleProbles(self):
        if self.bot.units(PROBE).idle.exists:
            for proble in self.bot.units(PROBE).idle:
                mineral_closest = self.bot.state.mineral_field.closest_to(proble)
                await self.bot.do(proble.gather(mineral_closest))

    async def gatherVespeneGas(self):
        for assimilator in self.bot.units(ASSIMILATOR):
            if assimilator.assigned_harvesters < assimilator.ideal_harvesters:
                workers = self.bot.workers.closer_than(20, assimilator)
                if workers.exists:
                    await self.bot.do(workers.random.gather(assimilator)) 
