from world import World

if __name__ == '__main__':
    while(True):
        world = World(width=500, height=400, blockSize=1,
                      transmitRange=120, agentCount=12, anchorCount=6, errDist=60)
        world.run()
