from pathlib import Path
import json, datetime

class Player:
    def __init__(self):
        '''initialization'''
        self.player_data = json.load(open('kw_players.json', 'r'))
        self.name = input('Player name: ')
        self.start = datetime.datetime.now()

        # load existing player 
        if self.name in list(self.player_data.keys()):
            print('Welcome back, ', self.name)
            self.level = self.player_data[self.name]['level']
            self.answered = self.player_data[self.name]['answered']
            self.removed = json.load(open(f'kw_players.json', 'r'))[self.name]['removed']
            self.nogainqa = json.load(open(f'kw_players.json', 'r'))[self.name]['nogainqa']
            self.answering = json.load(open(f'kw_players.json', 'r'))[self.name]['answering']

        # create new player with default values, save to list of players    
        else:
            print(f'Welcome to Key-wiz, {self.name},  your Key to become a Wiz!')
            self.level = 1
            self.answered = 0
            self.player_data[self.name] = {'level':1, 'answered':0, 'removed':[], 'nogainqa':[], 'answering':{}}
            json.dump(self.player_data, open('kw_players.json', 'w'))
            self.removed = []
            self.nogainqa = []
            self.answering = {}

        # all players get assigned points and fresh new report    
        self.points = 20
        self.report = []
    

    def update_stat(self, time):
        # this is called after a round of quiz is completed, to check level update
        if self.answered >= 100:
            self.answered = 0
            self.level += 1
            print(f'Level up! You are now level {self.level}! Congrats!')

        # save all relevant info for the player/current session
        self.player_data[self.name] = {'level':self.level, 'answered':self.answered, 'removed':self.removed, 'nogainqa':self.nogainqa, 'answering':self.answering}
        json.dump(self.player_data, open('kw_players.json', 'w'))
        try:
            contents = json.load(open(f'kw_{self.name}_report.json', 'r'))
            contents[str(time)] = self.report
            json.dump(contents, open(f'kw_{self.name}_report.json', 'w'))
        except:
            json.dump({str(time):self.report}, open(f'kw_{self.name}_report.json', 'w'))
        self.report = []


    def nogain(self, question):
        self.nogainqa.append(question)
    

    def remove_check(self, question, true):
        if question[0] in list(self.answering.keys()):
            if true == True:
                if self.answering[question[0]] == 1:
                    self.answering[question[0]] += 1
                elif self.answering[question[0]] == 2:
                    self.removed.append(question)
                    self.answering[question[0]] = 'removed'
            else:
                self.answering[question[0]] -= 1
        else:
            if true == True:
                self.answering[question[0]] = 1
            else:
                self.answering[question[0]] = -1