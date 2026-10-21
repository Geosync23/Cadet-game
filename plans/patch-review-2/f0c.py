from pp import *
g = start('?nosave&debug'); g.step(5)
print(g.ev("({ from: SHIP.evFrom, plan: evCalPlan(), skipFor20: evSkippedFor(20, [], null), due: evCalDue(), d12: eventDay(12), d13: eventDay(13), band: eventBandOf('ionStorm'), n: eventJobsCount('ionStorm') })"))
print(g.errors[:3]); g.close()
