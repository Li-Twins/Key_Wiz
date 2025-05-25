from pathlib import Path
import json, datetime, sys

class Player:
    def __init__(self, mode):
        self.player_data = json.load(open('kw_players.json', 'r'))
        self.name = input('Player name: ')
        self.start = datetime.datetime.now()
        self.current_correct = 0
        self.gamble_amount = 0
        self.gambling = False
        self.mode = mode
        self.points = 20
        # load existing player 
        if self.name in list(self.player_data.keys()):
            print('Welcome back, ', self.name)
            self.level = self.player_data[self.name]['level']
            self.xp = self.player_data[self.name]['xp']
            self.removed = self.player_data[self.name]['removed']
            self.already_answered = self.player_data[self.name]['already_answered']
            self.answering = self.player_data[self.name]['answering']
            self.boss_q_a = self.player_data[self.name]['boss_q_a']
            self.last_played = self.player_data[self.name]['last_played']
            target = datetime.datetime.strptime(self.last_played, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=8)
            if datetime.datetime.now() > target:
                current = datetime.datetime.strptime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
                extra = round(((datetime.datetime.strptime(current-target, "%Y-%m-%d %H:%M:%S")).hour)%8)
                if extra > 1:
                    extra *= 5
                    if extra > 50:
                        extra = 50
                self.points += extra
            else:
                if self.mode == 'normal':
                    current = datetime.datetime.now()
                    hours_left = (target - current).total_seconds() / 3600
                    print(f'You have to wait another {round(hours_left)} hours.') # printing remaining hours till replay
                    sys.exit()

        # create new player with default values, save to list of players    
        else:
            print(f'Welcome to Key-wiz, {self.name},  your Key to become a Wiz!')            
            self.player_data[self.name] = {
                'level': 1,
                'xp': 0,
                'removed': [],
                'already_answered': [],
                'answering': {},
                'boss_q_a': [],
                'last_played': datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
            }
            self.level = 1
            self.xp = 0
            self.removed = []
            self.already_answered = []
            self.answering = {}
            self.boss_q_a = []
            self.last_played = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
            # Save to file
            with open('kw_players.json', 'w') as f:
                json.dump(self.player_data, f)

        # all players get assigned points and fresh new report    
        if self.mode == 'dev':
            self.points = 99999999999999999999999
        self.report = []
    
    def gamble(self):
        self.gambling = input('Gamble y/n? ').lower() == 'y'
        if self.gambling:
            while True:
                try:
                    self.gamble_amount = int(input(f'How much({self.points})? '))
                    if self.gamble_amount <= self.points:
                        self.points -= self.gamble_amount
                        break
                    else:
                        print("You don't have that many points.")
                except:
                    print('Number please.')

    def gamble_check(self):
        if self.gambling:
            if self.current_correct > 5:
                print(f'You won {self.gamble_amount} points!')
                self.points += self.gamble_amount*2
            else:
                print(f'You lost {self.gamble_amount} points.')
            self.gamble_amount = 0

    def update_stat(self, time):
        # this is called after a round of quiz is completed, to check level update
        if self.mode == 'normal':
            if self.xp >= 60:
                self.xp -= 60
                self.level += 1
                print(f'Level up! You are now level {self.level}! Congrats!')
            if self.level >= 10:
                print('BOSS QA HOMING IN (maybe again)')

            # save all relevant info for the player/current session
            self.player_data[self.name] = {'level':self.level, 'xp':self.xp, 'removed':self.removed, 'already_answered':self.already_answered, 'answering':self.answering, 'boss_q_a':self.boss_q_a, 'last_played':datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")}
            json.dump(self.player_data, open('kw_players.json', 'w'))
            try:
                contents = json.load(open(f'kw_{self.name}_report.json', 'r'))
                contents[str(time)] = self.report
                json.dump(contents, open(f'kw_{self.name}_report.json', 'w'))
            except:
                json.dump({str(time):self.report}, open(f'kw_{self.name}_report.json', 'w'))
            self.report = []


    def nogain(self, question):
        self.already_answered.append(question)
    

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
