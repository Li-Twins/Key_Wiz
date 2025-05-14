import random
a = ['a', 'b', 'c']
b = 'a'
print(random.choice(list(x for x in a if x != b)))