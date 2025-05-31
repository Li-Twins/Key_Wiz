import sys, pathlib, random, json, datetime
from kw_player import Player

class Quiz:
    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.topics = json.load(open('kw_topics.json', 'r'))
        self.player = Player()
        # Load topics with error handling, Select topics based on player level
        try:
            self.topics = self.topics[:self.player.level * 4]
        except IndexError:
            self.topics = self.topics  # Fallback if slicing fails
        self.questions = []
        self.topic = ''
        self.done_topics = []
        self.rolled = []
        self.current_correct = 0


    def topic_selection(self):
        while True:
            try:
                # ensures the same topic won't be repeated in next reroll
                self.topic = random.choice([x for x in self.topics if x != self.topic and not (x in self.done_topics) and not (x in self.rolled)])
            except:
                # exit run when no topic exists that has not been marked as complete (ie at least 10 questions not completed)
                print('\nNo unfinished topic at this moment.')
                sys.exit()
            # generate available questions from comparing with quesions removed from given topic
            available_questions = []
            for i in json.load(open(f'kw_{self.topic}.json', 'r')):
                if not i[0] in self.player.removed:
                    available_questions.append(i)
            if len(available_questions) >= 10:
                print(f'\nYour topic is {self.topic}.')
                if self.player.points >= 5:
                    if not input(f'\nRandomize topic for 5/{self.player.points} points, Y/N?: ').lower() == 'y':
                        break
                    self.player.points -= 5 
                    self.rolled.append(self.topic)
                else:
                    break
            else:
                # topics with less than 10 incompleted quesions are removed for the run, this behaviour needs to be reworked
                print(f'You have finished {self.topic}.')
                for i in available_questions:
                    if not i[0] in list(self.player.answering.keys()):
                        self.player.boss_questions.append(i)
                self.done_topics.append(self.topic)


    def level_boss_check(self):
        # needs extensive testing, not sure how or if it works, 
        if self.player.level >= 10:
            qa = self.player.boss_questions
            if qa:
                print(f'\n#### Boss QA has started ####')
                while True:
                    x = input('Ready for ten questions? (Y)es or (Q)uit: ')
                    if x.lower() == "q":
                        self.player.update_stat(datetime.datetime(1, 1, 1, 0, 0, 0, 0)+(datetime.datetime.now()-self.start_time), True)
                        sys.exit()
                    if x == 'y' and len(self.player.boss_questions) >= 10:
                        self.current_boss_qa = random.sample(qa, k=10)
                        while self.points >= 5:
                            if input('Randomize questions? Y/N? ').lower() == 'y':
                                self.points -= 5
                                self.current_boss_qa = random.sample(qa, k=10)
                            else:
                                break
                        for question in enumerate(self.current_boss_qa, 1):
                            player_answer = input(f'\nQ{question[0]}: {question[1][1]}: ') 
                            if input(f"Answer:{question[1][1]}, (C)orrect?: ").lower() == 'c':
                                self.player.points += 2
                            self.player.report.append([question[1][0], player_answer])
            

    def question_selection(self):
        # load the questions from selected topic, get 10 samples
        self.questions = json.load(open(f'kw_{self.topic}.json', 'r'))
        self.questions = random.sample(self.questions, k=10) # does sample exceed size traceback still occur?
        for i in enumerate(self.questions, 1):
            print(f'Q{i[0]}: {i[1][0]} ')
        # offer chance to randomize the list of questions, if so repeat the whole process
        if self.player.points >= 5:
            if input(f'\nRandomize questions for 5/{self.player.points} points, Y/N?: ').lower() == 'y':
                self.player.points -= 5
                self.question_selection() 


    def answer_quiz(self, qa):
        # display each question and save player response 
        self.start_time = datetime.datetime.now()
        print(f'\n#### Quiz has started at {self.start_time} ####')
        for i in range(10): 
            player_answer = input(f'\nQ{i+1}: {qa[i][0]}: ') 
            self_mark = input(f"Answer: {qa[i][1]} - (C)orrect?: ")
        # show each question, answer and player input to be self marked, calculate correct xp and points earned, save all the report
            self.player.report.append([qa[i][0], player_answer])
            # for each correctly xp question
            if self_mark.lower() == "c":
                self.player.points += 2
                # update gamble counter
                self.current_correct += 1
                # already_answered > already_answered, xp > xp
                if not qa[i][0] in self.player.already_answered:
                    self.player.xp += 1
                self.player.remove_check(qa[i])
                self.player.already_answered.append(qa[i][0])

        # evaluate gamble result at the end of a run
        self.gamble_check()
        print(f"Points remaining: {self.player.points}\n")
        self.current_correct = 0


    def pt_check(self):
        # checks and deduct if enough points to play a quiz
        if self.player.points >= 15:
            self.player.points -= 15
            return True
        else:
            print ("Not enough points for another quiz, bye\n")
            return False


    def gamble(self):
        while True:
            gambling = input(f'\nHow much to gamble (out of {self.player.points})? ')
            try:
                gambling = int(gambling)
                if gambling <= self.player.points:
                    self.gamble_amount = gambling
                    self.player.points -= gambling
                    break
                else:
                    print('Not enough points.')
            except: 
                print('Number please.')


    def gamble_check(self):
        if self.current_correct > 5 and self.gamble_amount > 0:
            print(f'\nYou gambled and you won {self.gamble_amount} pt!')
            self.player.points += self.gamble_amount*2
        elif self.current_correct <= 5 and self.gamble_amount > 0:
            print(f'\nYou gambled and you lost {self.gamble_amount} pt.')
        self.gamble_amount = 0


    def run_quiz(self):
        # the main flow
        while True:
            # run the boss fight if sufficient level, quits the program without progressing the flow
            self.level_boss_check()
            # run the quiz when enough points
            if self.pt_check():
                print("\nStarting Quiz..\n")
                self.gamble()
                self.topic_selection()
                self.question_selection()
                self.answer_quiz(self.questions)
                # record the last played time at the end of a run
                self.player.update_stat(datetime.datetime(1, 1, 1, 0, 0, 0, 0)+(datetime.datetime.now()-self.start_time), True)
            # without enough points, return to root
            else:
                break


def mode():
    # allows the options of Normal (enter player name), Dev (access with code) or Quit program
    while True:
        # this is the root level where end of normal run returns to
        x = input("\nChoose mode - (N)ormal (D)ev (Q)uit : ")
        # dev mode calls dev function if correct code entered
        if x.lower() == "d":
            if input("Enter code: ") == "781023":
                dev()
            else:
                print("code incorrect")
        # quit
        if x.lower() == "q":
            sys.exit()
        # normal mode, the bulk of the script
        if x.lower() == "n":
            thequiz = Quiz()
            if not thequiz.topics:
                print('\nNo uncompleted topics.')
                break
            else:
                thequiz.run_quiz()


def dev():
    # choose topic, displays all questions within
    topics = json.load(open('kw_topics.json', 'r'))
    while True:
        topic = input(f'\nChoose topic or (q)uit: \n{topics}: ')
        if topic in topics:
            qa = json.load(open(f'kw_{topic}.json', 'r'))
            random.shuffle(qa)
            print('\n(Q)uit anytime.')
            for i in enumerate(qa, 1): 
                if input(f'\nQ{i[0]}: {i[1][0]}: ').lower() != 'q':
                    print(f'Answer: {i[1][1]}')
                else:
                    break
        elif topic.lower() == 'q':
            break
        else:
            print('Invalid topic.')

        
if __name__ == "__main__":
    mode()


