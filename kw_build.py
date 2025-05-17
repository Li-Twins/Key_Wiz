from pathlib import Path
import json


def building_quiz():
    # load up topic lists
    f = open('kw_topics.json', 'r')
    topic_list = json.load(f)
    f.close()
    while True:
        # add new topic if not exising, create topic file as well
        if input(r'(n)ew topic or (e)xisting : ').lower() == 'n':
            f = open('kw_topics.json', 'w')
            while True:
                new_topic = input('New topic: ')
                if not new_topic in topic_list:
                    topic_list.append(new_topic)
                    json.dump(topic_list, f)
                    topic = Path('kw_' + new_topic + '.json')
                    q_a = []
                    f.close()
                    break
                else:
                    print('This topic already exists.')
        # select existing topic and load previous QAs
        else:
            while True:
                topic = input(f'Choose from {topic_list}: ')
                if topic in topic_list:
                    break
                else:
                    print('Invalid topic. Please try again.')
            topic = Path('kw_' + topic + '.json')
            temp_path = open(topic)
            q_a = json.load(temp_path)
        # keep recording new Q and A until exit        
        while True:
            f = open(topic, 'w')
            acounter = len(q_a) + 1
            a = input(f'Q{acounter}: ')
            b = input(f'A{acounter}: ')
            save_exit = input(f'(s)ave or (n)new topic: ')
            if save_exit.lower() == 'n':
                break
            elif save_exit.lower() == 's':
                q_a.append([a, b])
        # this step is reached when new topic is chosen, which safely dumps to json and close the file before reopening
        json.dump(q_a, f)
        f.close()

building_quiz()

