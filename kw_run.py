import sys, pathlib, random, json, datetime
from kw_player import Player

global game_on
game_on = True
global exception
exception = False

class Quiz: # TESTING DAD
    def __init__(self):
        self.player = Player()
        # select four existing topics for each player level, or all exisiting topics if less than 5 
        try:
            self.topics = json.load(open('kw_topics.json', 'r'))[:(self.player.level*4)]
        except IndexError:
            self.topics = json.load(open('kw_topics.json', 'r'))
        self.questions = []
        self.topic = ''


    def topic_selection(self):
        global game_on
        # prompt if no topic exists
        if not self.topics:
            print('No topic exists yet.')
            game_on = False

        # check if enough points to run quiz, with option to change to new topic
        elif self.player.points >= 15:
            self.player.points -= 15
            while True:
                try:
                    # ensures the same topic will be repeated in next reroll
                    self.topic = random.choice(list(x for x in self.topics if x != self.topic))
                # exit run when no topic exists that has not been marked as complete (ie at least 10 questions not completed)
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
                    if self.player.points >= 5:
                        if not input(f'\nRandomize topic for 5/{self.player.points} points, Y/N?: ').lower() == 'y':
                            self.questions = available_questions
                            break
                        self.player.points -= 5
                    else:
                        self.questions = available_questions
                        break
                else:
                    print(f'You have finished {self.topic}.')
                    del self.topics[self.topics.index(self.topic)]


        # ends game when topics exist yet not enough points        
        else:
            print(f"Sorry, but you don't have enough points to continue on.")
            game_on = False

        

    def question_selection(self):
        # retrieve 10 random questions from topic file, and display them
        global exception
        try:
            self.questions = random.sample(self.questions, k=10)
            for question in enumerate(self.questions, 1):
                print(f'Q{question[0]}: {question[1][0]}')

            # offer chance to randomize the list of questions, if so repeat the whole process
            if self.player.points >= 5:
                if input(f'\nRandomize questions for 5/{self.player.points} points, Y/N?: ').lower() == 'y':
                    self.player.points -= 5
                    self.questions = []
                    self.question_selection() 
        except:
            print(f'You have finished {self.topic}.')
            self.player.points += 15
            exception = True


    
    def answer_quiz(self):
        # display each question and save player response 
        start_time = datetime.datetime.now()
        print(f'\n#### Quiz has started at {start_time} ####')
        answer_list = []
        for i in range(10):
            player_answer = input(f'Q{i+1}: {self.questions[i][0]}: ')
            answer_list.append(player_answer)

        # show each question, answer and player input to be self marked, calculate correct answered and points earned, save all the report
        print(f'\n#### Please verify your answers ####')
        for i in range(10):
            self_mark = input(f"{self.questions[i][1]}, your answer: {answer_list[i]}, Y if correct: ")
            self.player.report.append([self.questions[i][0], self.questions[i][1], answer_list[i]])
            if self_mark.lower() == "y":
                self.player.points += 2
                if not answer_list[i] in self.player.nogainqa:
                    self.player.answered += 1
                self.player.remove_check(self.questions[i], True)
                self.player.nogain(self.questions[i][0])
            else:
                self.player.remove_check(self.questions[i], False)
        print(f"\nYour current points: {self.player.points}")
        total_time = datetime.datetime.now()-start_time
        self.player.update_stat(total_time)

if __name__ == "__main__":
    thequiz = Quiz()
    while True:
        thequiz.topic_selection() # modifies game_on if not enough points
        if game_on == True:
            thequiz.question_selection() 

            thequiz.answer_quiz()
        else:
            break
    sys.exit()
