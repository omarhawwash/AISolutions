class World:
    def __init__(self, size = 2):
        self.TILES = Tile[size]

        for x in range(0,size):
            for y in range(0, size):
                self.TILES[x] = Tile(x, y)

        def setNeighbors(self, world):
            for tile in world.TILES:
                for x in range(0,tile.XPOS):
                    for y in range(0,y):
                        if x != 0:
                            tile.NEIGHBORS[0] = "Left"
                        if x != size:
                            tile.NEIGHBORS[1] = "Right"
                        if y != 0:
                            tile.NEIGHBORS[2] = "Up"
                        if y != size:
                            tile.NEIGHBORS[3] = "Down"




class Tile:
    def __init__(self, X, Y):
        self.XPOS = X
        self.YPOS = Y
        self.STATE = "Dirty"
        self.NEIGHBORS = []

    def cleanTile(self):
        self.STATE = "Clean"




