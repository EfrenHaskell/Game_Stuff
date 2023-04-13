'''
Efren Haskell
Prototype Sudoku Solver

Notes:
 - Currently only capable of solving easy, medium and some hard difficulty puzzles
 - Lacks more complex logic when comparing practical values

Sample data:
 - Easy:
 - 000560019900000630008003000009830400504706000600000001230609148870000005490285760
 - Med:
 - 009030005300070000280040000003284109008000700040150020005003490090400080700000506
 - 500800920027000000190050000000407568080000302052003007000002600001000034830004200
 - Hard:
 - 007400030936200700804003096000500080050020003000609007005000000000074560600000009
 - 

'''
class game:
    def __init__(self):
        # for numerical data
        self.tiles = []
        # for placement of unknown vals
        self.data = dict()

    # fill tile set based on data set values
    def fill(self):
        for i in range(81):
            if len(self.data[i]) == 1:
                self.tiles[int(i/9)][i%9] = self.data[i].pop()

    # modify data set based on horizontal analysis
    def horizontal(self):
        for i in range(9):
            for j in range(9):
                dataVals = self.data[i*9+j]
                for k in range(9):
                    val = self.tiles[i][k]
                    if val != 0 and val in dataVals:
                        dataVals.remove(val)

    # modify data set based on vertical analysis
    def vertical(self):
        # find possible values on verticals
        count = 0
        for i in range(81):
            if i % 9 == 0 and i != 0:
                count += 1
            dataVals = self.data[i % 9 * 9 + count]
            for j in range(9):
                val = self.tiles[j][int(i/9)]
                if val != 0 and val in dataVals:
                    dataVals.remove(val)

    # modify data set based on in-square analysis of missing values
    def missingSet(self):
        count = 0
        for i in range(81):
            dataVals = self.data[count]
            if i % 9 == 0:
                countv = count
            for j in dataVals:
                found = False
                tempv = countv
                for k in range(9):
                    val = self.data[tempv]
                    if j in val and count != tempv:
                        found = True
                    tempv += 1
                    if tempv % 3 == 0:
                        tempv += 6
                    if found:
                        break
                if not found:
                    self.data[count] = {j}
            count += 1
            if count % 3 == 0:
                count+=6
            if count >= 81:
                count = (count-6) % 9

    # modify data set based on in-square comparison (3x3)
    def squareSet(self):
        # find possible values in square sets
        count = 0
        for i in range(81):
            dataVals = self.data[count]
            if i % 9 == 0:
                countv = count
            tempv = countv
            for k in range(9):
                val = self.tiles[int(tempv/9)][tempv%9]
                if val != 0 and val in dataVals:
                    dataVals.remove(val)
                tempv += 1
                if tempv % 3 == 0:
                    tempv += 6
            count += 1
            if count % 3 == 0:
                count+=6
            if count >= 81:
                count = (count-6) % 9

    # unintrusive modifying method with tile set
    def set_tiles_basic(self):
        inp_len = 0
        # accept tile vals (0's represent unset vals)
        while inp_len != 81:
            tilevals = input("Set Tile data: ")
            inp_len = len(tilevals)
        # convert tilevals to 2d array
        for i in range(9):
            temp = []
            avlb = {1,2,3,4,5,6,7,8,9}
            for j in range(9):
                val = int(tilevals[i*9+j])
                temp.append(val)
                if val != 0:
                    # find possible values on horizontals
                    avlb.remove(val)
            self.tiles.append(temp)
            for j in range(9):
                # initialize data dict
                if self.tiles[i][j] == 0:
                    self.data[i*9+j] = avlb.copy()
                else:
                    self.data[i*9+j] = set()

    # includes a single run-through of tile simulation
    # -- has increased testing efficiency --
    # can be subbed for set_tiles_basic
    # FOR BASIC USE ONLY
    def set_tiles_mod(self): 
        inp_len = 0
        # accept tile vals (0's represent unset vals)
        while inp_len != 81:
            tilevals = input("Set Tile data: ")
            inp_len = len(tilevals)
        # convert tilevals to 2d array
        for i in range(9):
            temp = []
            avlb = {1,2,3,4,5,6,7,8,9}
            for j in range(9):
                val = int(tilevals[i*9+j])
                temp.append(val)
                if val != 0:
                    # find possible values on horizontals
                    avlb.remove(val)
            self.tiles.append(temp)
            for j in range(9):
                # initialize data dict
                if self.tiles[i][j] == 0:
                    self.data[i*9+j] = avlb.copy()
                else:
                    self.data[i*9+j] = set()
        game.fill(self)
        game.vertical(self)
        game.squareSet(self)

    # print tiles
    def disp_tiles(self):
        if len(self.tiles) >= 0:
            counti = 0
            countj = 0
            # iteration of tilevals array
            for i in range(9):
                for j in range(9):
                    print(self.tiles[i][j], end = "")
                    countj += 1
                    # formatting (horizontal) element: places a space between sets of 3
                    if countj >= 3:
                        print(" ", end = "")
                        countj = 0
                counti += 1
                # formatting (vertical) element: places a space between sets of 3
                if counti >=  3:
                    print()
                    counti = 0
                print()
                
        else:
            # edge-case: set_tiles must be called before tiles can be displayed
            print("----Tiles not set----\n")

    # print tile data values
    def disp_data(self):
        for i in range(81):
            print(self.data[i])

    # get tile data values
    def get_data(self) -> str:
        res = ""
        for i in range(81):
            res += self.data[i] + "|"
        return res

    # display value at specific tile index (tiles index vertically)
    '''
    tile structure:
    
        0  1  2  3  ...  8
        9  10 11 12 ...  17
        19 20 21 22 ...  26
        27
        ...
    '''
    def disp_index(self,index):
        print(self.data[index])

    # get value at specific tile index
    def get_index(self, index) -> int:
        return self.data[index]

    # tests if values have been fully set
    def test_set(self) -> bool:
        for i in self.data.values():
            if len(i) > 0:
                return False
        return True

    # runs simulation of sudoku game
    def config_data(self):
        tilesSet = False
        count = 0
        while not tilesSet and count <= 1000:
            tilesSet = game.test_set(self)
            game.horizontal(self)
            game.vertical(self)
            game.squareSet(self)
            game.missingSet(self)
            game.fill(self)
            count += 1

# code testing    
if __name__ == '__main__':
    # init client
    new_game = game()
    new_game.set_tiles_mod()
    #new_game.disp_tiles()
    new_game.config_data()
    new_game.disp_tiles()
