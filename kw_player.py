from pathlib import Path
import json, datetime, sys, random

class Player:
    def __init__(self, topics):
        while True:
            try:
                self.mode = "normal" if input('(N)ormal or (P)ractise?: ').lower() == 'n' else "dev"
            except KeyboardInterrupt:
                print("\nBye!")
                sys.exit()
            if self.mode == 'normal':
                while True:
                    self.player_data = json.load(open('kw_players.json', 'r'))
                    self.name = input('\nPlayer name: ')
                    self.start = datetime.datetime.now()
                    self.current_correct = 0
                    self.gamble_amount = 0
                    self.gambling = False
                    self.points = 20
                    # load existing player 
                    if self.name in list(self.player_data.keys()):
                        if self.last_played != 'interrupted':   
                            target = datetime.datetime.strptime(self.last_played, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=8)
                            if datetime.datetime.now() > target:
                                current = datetime.datetime.strptime(str(datetime.datetime.now()), "%Y-%m-%d %H:%M:%S")
                                extra = round(((datetime.datetime.strptime(current-target, "%Y-%m-%d %H:%M:%S")).hour)%8)
                                if extra > 1:
                                    extra *= 5
                                    if extra > 50:
                                        extra = 50
                                self.points += extra
                            else:
                                current = datetime.datetime.now()
                                hours_left = (target - current).total_seconds() / 3600
                                print(f'You have to wait another {round(hours_left)} hours.') # printing remaining hours till replay
                                continue
                        print('Welcome back, ', self.name)
                        self.level = self.player_data[self.name]['level']
                        self.xp = self.player_data[self.name]['xp']
                        self.removed = self.player_data[self.name]['removed']
                        self.already_answered = self.player_data[self.name]['already_answered']
                        self.answering = self.player_data[self.name]['answering']
                        self.boss_questions = self.player_data[self.name]['boss_questions']
                        self.last_played = self.player_data[self.name]['last_played']
                        break
                    # create new player with default values, save to list of players    
                    else:
                        print(f'Welcome to Key-wiz, {self.name},  your Key to become a Wiz!')            
                        self.player_data[self.name] = {
                            'level': 1,
                            'xp': 0,
                            'removed': [],
                            'already_answered': [],
                            'answering': {},
                            'boss_questions': [],
                            'last_played': datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
                        }
                        self.level = 1
                        self.xp = 0
                        self.removed = []
                        self.already_answered = []
                        self.answering = {}
                        self.boss_questions = []
                        self.last_played = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
                        self.report = []
                        break
                    # all players get assigned points and fresh new report    
            else:
                while True:
                    topic = input(f'\nChoose topic, (q)uit: {topics}: ')
                    if topic in topics:
                        qa = json.load(open(f'kw_{topic}.json', 'r'))
                        random.shuffle(qa)
                        print('(Q)uit anytime.')
                        for i in enumerate(qa, 1): 
                            if input(f'\nQ{i[0]}: {i[1][0]}: ').lower() != 'q':
                                print(f'Answer: {i[1][1]}')
                            else:
                                break
                    elif topic.lower() == 'q':
                        break
                    else:
                        print('Invalid topic.')
                continue
            break
            
            
                    

    def gamble(self):
        while True:
            self.gambling = input(f'\nHow much to gamble (out of {self.points})? ')
            try:
                self.gambling = int(self.gambling)
                if self.gambling <= self.points:
                    break
                else:
                    print('You don\'t have that much.')
            except: 
                print('Number please.')

    def gamble_check(self):
        if self.gambling:
            if self.current_correct > 5:
                print(f'\nYou gambled and you won {self.gamble_amount} pt!')
                self.points += self.gamble_amount*2
            else:
                print(f'\nYou gambled and you lost {self.gamble_amount} pt.')
            self.gamble_amount = 0


    def update_stat(self, time, end):
        # this is called after a round of quiz is completed, to check level update
        if self.xp >= 60:
            self.xp -= 60
            self.level += 1
            print(f'\nLevel up! You are now level {self.level}! Congrats!')
        if self.level >= 10:
            print('BOSS QA HOMING IN (maybe again)')

        # save all relevant info for the player/current session
        last_played = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
        if not end:
            last_played = 'interrupted'
        self.player_data[self.name] = {'level':self.level, 'xp':self.xp, 'removed':self.removed, 'already_answered':self.already_answered, 'answering':self.answering, 'boss_questions':self.boss_questions, 'last_played':last_played}
        json.dump(self.player_data, open('kw_players.json', 'w'))
        try:
            try:
                contents = json.load(open(f'kw_{self.name}_report.json', 'r'))
            except:
                contents = {}
                json.dump({}, open(f'kw_{self.name}_report.json', 'w'))
            self.report.append({'Start': datetime.datetime.strftime(self.start, "%Y-%m-%d %H:%M:%S")})
            contents[datetime.datetime.strftime(datetime.datetime(1, 1, 1, 0, 0, 0, 0)+(datetime.datetime.now()-self.start), '%Y-%m-%d %H:%M:%S')] = self.report
            json.dump(contents, open(f'kw_{self.name}_report.json', 'w'))
        except:
            json.dump({str(time):self.report}, open(f'kw_{self.name}_report.json', 'w'))
        self.report = []


    def nogain(self, question):
        self.already_answered.append(question[0])
    

    def remove_check(self, question, true):
        if question[0] in list(self.answering.keys()):
            if true == True:
                if self.answering[question[0]] == 1:
                    self.answering[question[0]] += 1
                elif self.answering[question[0]] == 2:
                    self.removed.append(question[0])
                    self.answering[question[0]] = 'removed'
            else:
                self.answering[question[0]] -= 1
        else:
            if true == True:
                self.answering[question[0]] = 1
            else:
                self.answering[question[0]] = -1
