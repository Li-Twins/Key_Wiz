import sys, pathlib, random, json, datetime
from kw_player import Player

global game_on
game_on = True
class Quiz:
    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.topics = json.load(open('kw_topics.json', 'r'))
        self.player = Player(self.topics)
        
        # Load topics with error handling
        # Select topics based on player level
        try:
            self.topics = self.topics[:self.player.level * 4]
        except IndexError:
            self.topics = self.topics  # Fallback if slicing fails

        self.questions = []
        self.topic = ''
        self.done_topics = []


    def topic_selection(self):
        global game_on
        # prompt if no topic exists
        if not self.topics:
            print('\nNo topic exists yet.')
            game_on = False
        # check if enough points to run quiz, with option to change to new topic
        elif self.player.points >= 15:
            self.player.points -= 15
            # first gamble action occurs here
            self.player.gamble()
            while True:
                try:
                    # ensures the same topic will be repeated in next reroll
                    self.topic = random.choice([x for x in self.topics if x != self.topic and not x in self.done_topics])
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
                            self.questions = available_questions
                            break
                        self.player.points -= 5 
                    else:
                        self.questions = available_questions
                        break
                else:
                    # topics with less than 10 incompleted quesions are removed for the run, this behaviour needs to be reworked
                    print(f'You have finished {self.topic}.')
                    for i in available_questions:
                        if not i[0] in list(self.player.answering.keys()):
                            self.player.boss_questions.append(i)
                    self.done_topics.append(self.topic)
        # ends game when topics exist yet not enough points        
        else:
            print(f"Sorry, but you don't have enough points to continue on.")
            game_on = False
    
    def boss(self):
        if self.player.level == 10:
            self.boss_qa(self.player.boss_questions)
        else:
            self.answer_quiz(self.questions)

    def boss_qa(self, qa):
        if qa:
            print(f'\n#### Boss QA has started ####')
            while input('Continue boss QA? Y/N: ').lower() == 'y' and len(self.player.boss_questions) >= 10:
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
        # retrieve 10 random questions from topic file, and display them
        self.questions = random.sample(self.questions, k=10) # does sample exceed size traceback still occur?
        for question in enumerate(self.questions, 1):
            print(f'Q{question[0]}: {question[1][0]}')
        # offer chance to randomize the list of questions, if so repeat the whole process
        if self.player.points >= 5:
            if input(f'\nRandomize questions for 5/{self.player.points} points, Y/N?: ').lower() == 'y':
                self.player.points -= 5
                self.questions = []
                self.question_selection() 



    def answer_quiz(self, qa):
        # display each question and save player response 
        answer_list = []
        self.start_time = datetime.datetime.now()
        print(f'\n#### Quiz has started at {self.start_time} ####')
        for i in range(10): 
            player_answer = input(f'\nQ{i+1}: {qa[i][0]}: ') 
            answer_list.append(player_answer) # inputting
            self_mark = input(f"Answer:{qa[i][1]}, (C)orrect?: ")


        # show each question, answer and player input to be self marked, calculate correct xp and points earned, save all the report
        for i in range(10):
            self.player.report.append([qa[i][0], answer_list[i]])
            # for each correctly xp question
            if self_mark.lower() == "c":
                self.player.points += 2
                # update gamble counter
                self.player.current_correct += 1
                # already_answered > already_answered, xp > xp
                if not qa[i][0] in self.player.already_answered:
                    self.player.xp += 1
                self.player.remove_check(qa[i], True)
                self.player.answering[qa[i][0]] = 'removed'
                self.player.already_answered.append(qa[i][0])
            else:
                # if incorrect, deduct one for the question
                self.player.remove_check(qa[i], False)
            
        # evaluate gamble result at the end of a run
        self.player.gamble_check()
        print(f"\nPoints remaining: {self.player.points}")
        self.player.current_correct = 0

        
if __name__ == "__main__":
    thequiz = Quiz()
    while True:
        thequiz.topic_selection() # modifies game_on if not enough points
        if game_on == True:
            thequiz.question_selection() 
            thequiz.boss()
            thequiz.player.update_stat(datetime.datetime(1, 1, 1, 0, 0, 0, 0)+(datetime.datetime.now()-thequiz.start_time), False)
        else:
            thequiz.player.update_stat(datetime.datetime(1, 1, 1, 0, 0, 0, 0)+(datetime.datetime.now()-thequiz.start_time), True)
            if input('Another run? Y/N? ').lower() == 'y':
                game_on = True
                thequiz = Quiz()
                continue
            print('Bye!')
            break
            

