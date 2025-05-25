import sys, pathlib, random, json, datetime
from kw_player import Player

global game_on
game_on = True
global game_mode
game_mode = "normal" if input('(N)ormal or (P)ractise?: ').lower() == 'n' else "dev"
class Quiz:
    def __init__(self):
        global game_mode
        self.player = Player(mode=game_mode)
        
        # Load topics with error handling
        self.topics = json.load(open('kw_topics.json', 'r'))
        
        # Select topics based on player level
        try:
            self.topics = self.topics[:self.player.level * 4]
        except IndexError:
            self.topics = self.topics  # Fallback if slicing fails

        self.questions = []
        self.topic = ''
        self.done_topics = []


    def topic_selection(self):
        global game_on, game_mode
        # prompt if no topic exists
        if not self.topics:
            print('No topic exists yet.')
            game_on = False
        # check if enough points to run quiz, with option to change to new topic
        elif self.player.points >= 15:
            self.player.points -= 15
            # first gamble action occurs here
            self.player.gamble()
            while True:
                try:
                    # ensures the same topic will be repeated in next reroll
                    if game_mode == "normal":
                        self.topic = random.choice([x for x in self.topics if x != self.topic and not x in self.done_topics])
                    elif game_mode == "dev":
                        topic = ''
                        while not topic in self.topics:
                            topic = input(f'Out of {self.topics}, which topic? ')
                            if topic in self.topics:
                                self.topic = topic
                            else:
                                print(f'Invalid topic, please select from {self.topics}')


                # exit run when no topic exists that has not been marked as complete (ie at least 10 questions not completed)
                except KeyboardInterrupt:
                    print('\nBye!')
                    sys.exit()
                except:
                    print('No unfinished topic at this moment.')
                    sys.exit()

                # generate available questions from comparing with quesions removed from given topic
                available_questions = []
                for i in json.load(open(f'kw_{self.topic}.json', 'r')):
                    if not i[0] in self.player.removed:
                        available_questions.append(i)
                if len(available_questions) >= 10:
                    print(f'\nYour topic is {self.topic}.')
                    if self.player.points >= 5 and self.player.mode == 'normal':
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
                            self.player.boss_q_a.append(i)
                    self.done_topics.append(self.topic)
        # ends game when topics exist yet not enough points        
        else:
            print(f"Sorry, but you don't have enough points to continue on.")
            game_on = False
    
    def boss(self):
        if self.player.level == 10:
            self.boss_qa(self.player.boss_q_a, True)
        else:
            self.answer_quiz(self.questions)

    def boss_qa(self, qa, qatrue):
        if qa:
            print(f'\n#### Boss QA has started ####')
            while input('Continue with boss QA? Y/N: ').lower() == 'y':
                self.current_boss_qa = random.sample(qa, k=10)
                for question in enumerate(self.current_boss_qa, 1):
                    print(f'BQ{question[0]}: {question[1][0]}')
                answer_list = []
                for i in range(10):
                    player_answer = input(f'Q{i+1}: {qa[i][0]}: ')
                    answer_list.append(player_answer)
                print(f'\n#### Please verify your answers ####')
            for i in range(10):
                self_mark = input(f"{qa[i][1]}, your answer: {answer_list[i]}, Y if correct: ")
                self.player.report.append([qa[i][0], qa[i][1], answer_list[i]])
                # for each correctly xp question
                if self.player.mode == 'normal':
                    if self_mark.lower() == "y":
                        self.player.points += 2
                        # update gamble counter
                        self.player.current_correct += 1
                        self.player.remove_check(qa[i], True)
                        self.player.already_answered.append(qa[i][0])
                        self.player.removed.append(qa[i])
                    else:
                        self.player.remove_check(qa[i], False)


    def question_selection(self):
        # retrieve 10 random questions from topic file, and display them
        if self.player.mode == 'normal':
            self.questions = random.sample(self.questions, k=10) # does sample exceed size traceback still occur?
        for question in enumerate(self.questions, 1):
            print(f'Q{question[0]}: {question[1][0]}')
        # offer chance to randomize the list of questions, if so repeat the whole process
        if self.player.mode == 'normal':
            if self.player.points >= 5:
                if input(f'\nRandomize questions for 5/{self.player.points} points, Y/N?: ').lower() == 'y':
                    self.player.points -= 5
                    self.questions = []
                    self.question_selection() 



    def answer_quiz(self, qa):
        # display each question and save player response 
        start_time = datetime.datetime.now()
        print(f'\n#### Quiz has started at {start_time} ####')
        answer_list = []
        if self.player.mode == 'normal':
            for i in range(10): player_answer = input(f'Q{i+1}: {qa[i][0]}: ') ; answer_list.append(player_answer) # inputting
        # show each question, answer and player input to be self marked, calculate correct xp and points earned, save all the report
            print(f'\n#### Please verify your answers ####')
            for i in range(10):
                self_mark = input(f"{qa[i][1]}, your answer: {answer_list[i]}, Y if correct: ")
                self.player.report.append([qa[i][0], qa[i][1], answer_list[i]])
                # for each correctly xp question
                if self_mark.lower() == "y":
                    self.player.points += 2
                    # update gamble counter
                    self.player.current_correct += 1
                    # already_answered > already_answered, xp > xp
                    if not answer_list[i] in self.player.already_answered:
                        self.player.xp += 1
                    self.player.removed.append(qa[i])
                    self.player.answering[qa[i][0]] = 'removed'
                    self.player.already_answered.append(qa[i][0])

                        
                else:
                    # if incorrect, deduct one for the question
                    self.player.remove_check(qa[i], False)
            print(f"\nYour current points: {self.player.points+(self.player.gamble_amount*2 if self.player.current_correct > 5 else 0)}")
        else:
            for i in enumerate(qa, 1): 
                answer_list.append(input(f'Q{i[0]}: {i[1][0]}: ')) # inputting
            print(f'\n#### Please verify your answers ####')    
            for i in enumerate(qa, 1): 
                if input(f"{i[0]}: {i[1][0]}, your answer: {answer_list[(i[0])-1]}, Y if correct: ").lower() == 'y': 
                    self.player.points += 2 ; self.player.current_correct += 1 ; self.player.already_answered.append(i[1][0])
        # evaluate gamble result at the end of a run
        self.player.gamble_check()
        total_time = datetime.datetime.now()-start_time
        if self.player.mode == 'normal' : self.player.update_stat(total_time)
        else: print(f"Time taken: {total_time}")
        self.player.current_correct = 0

if __name__ == "__main__":
    thequiz = Quiz()
    while True:
        thequiz.topic_selection() # modifies game_on if not enough points
        if game_on == True:
            thequiz.question_selection() 
            thequiz.boss()
        else:
            break
    sys.exit()
