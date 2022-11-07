# cause we gotta do the GUIs my dude
from tkinter import *

# author: Efren Haskell
# attempt at a tic-tac-toe bot

class game():
    def __init__(self):
        # init game window size 400x400
        self.hub = Tk()
        self.hub.geometry("400x400")
        # init game data
        self.selectable = list()
        self.game_data = list()
        self.comp_data = list()
        self.comp_playable = [0,1,2,3,4,5,6,7,8]
        # init game constant data
        self.t_cases = {
            0: [[1,2],[3,6],[4,8],[2,1],[6,3],[8,4]],
            1: [[0,2],[4,7],[2,0],[7,4]],
            2: [[0,1],[5,8],[4,6],[1,0],[8,5],[6,4]],
            3: [[0,6],[4,5],[6,0],[5,4]],
            4: [[0,8],[1,7],[2,6],[3,5],[8,0],[7,1],[6,2],[5,3]],
            5: [[3,4],[2,8],[4,3],[8,2]],
            6: [[0,3],[2,4],[7,8],[3,0],[4,2],[8,7]],
            7: [[1,4],[6,8],[4,1],[8,6]],
            8: [[0,4],[2,5],[6,7],[4,0],[5,2],[7,6]]
        }
        self.trunc_t_case = {
            0: [1,2,3,6,4,8],
            1: [0,2,4,7],
            2: [0,1,5,8,4,6],
            3: [0,6,4,5],
            4: [0,8,1,7,2,6,3,5],
            5: [3,4,2,8],
            6: [0,3,2,4,7,8],
            7: [1,4,6,8],
            8: [0,4,2,5,6,7]
        }
    def start_game(self):
        self.comp_playable = [0,1,2,3,4,5,6,7,8]
        # set_play displays client play checking that it is a viable play option
        def set_play(selected):
            if selected not in self.game_data and selected not in self.comp_data:
                # set tile to "x"
                self.selectable[selected].config(text = "X")
                # add selected val to game_data
                self.game_data.append(selected)
                # remove playable options for computer
                # necessary for comp_play to choose only available vals
                self.comp_playable.remove(selected)
                # call computer play while game is active
                if len(self.comp_playable) > 0:
                    comp_play()

        def config_play():
            # clear weights
            weights = {
                0: 0,
                1: 0,
                2: 0,
                3: 0,
                4: 0,
                5: 0,
                6: 0,
                7: 0,
                8: 0
            }
            for i in self.game_data:
                for j in self.trunc_t_case.get(i):
                    if j in self.comp_playable:
                        # incr. weights based on play patterns
                        weights[j] += 1

            choice = 0
            choice_weight = 0
            
            for i in weights.keys():
                if weights.get(i) > choice_weight:
                    # set choice based on weight comparison
                    choice = i
                    choice_weight = weights.get(i)
                # ineffective implementation
                '''
                elif (weights.get(i) == choice_weight) and (len(game_data) > 1):
                    for j in range(len(game_data)-1):
                        temp = [game_data[j],game_data[j+1]]
                        if temp in t_cases.get(i):
                            choice = i
                            choice_weight = weights.get(i)
                            '''
            # produce temporary list 
            temp_lst = list()
            for i in range(len(self.game_data)):
                temp_lst.append([self.game_data[i],self.game_data[(i+1) % len(self.game_data)]])
            for i in self.comp_playable:
                for j in temp_lst:
                    if j in self.t_cases.get(i):
                        # compare with nontruncated game patterns
                        choice = i
                        choice_weight = weights.get(i)
            
            if len(self.comp_data) > 1:
                # clear temp_lst
                temp_lst = []
                for i in range(len(self.comp_data)):
                    temp_lst.append([self.comp_data[i],self.comp_data[(i+1) % len(self.comp_data)]])
                for i in temp_lst:
                    for j in self.t_cases.keys():
                        if (i in self.t_cases.get(j)) and (j not in self.game_data):
                            # weight override
                            choice = j
            # return final choice
            return choice

        def comp_play():
            # initalize computer turn
            # choose play with config above
            play = config_play()
            #set tile to "o"
            self.selectable[play].config(text = "O")
            # update comp_data
            self.comp_data.append(play)
            # update playable data
            self.comp_playable.remove(play)
            
        # initialize tiles creating a 3x3 grid
        for i in range(3):
            for j in range(3):
                select = Button(self.hub, text = " ", command = lambda selected = 3 * i + j: set_play(selected),width = "10",height = "5")
                select.grid(row = i, column = j)
                self.selectable.append(select)
        def reset():
            # recall game
            self.hub.destroy()
            new_game = game()
            new_game.start_game()
        # init restart button
        re_button = Button(self.hub, text = "RESTART", command = reset)
        re_button.grid(row = 1,column = 4)

# main at bottom cause C++ supremacy
def main():
    # begin game client
    new_game = game()
    new_game.start_game()
main()

