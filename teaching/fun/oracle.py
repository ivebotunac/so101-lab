# Ask a yes or no question: the arm thinks and answers with a gesture.
import random

from gestures import nod, shake, shrug, think
from so101.simple import home

home()
print("Ask me a question that has a yes or no answer. An empty line ends the game.")

questions = 0
while True:
    question = input("Your question: ")
    if question == "":
        break
    questions += 1

    think()
    answer = random.randint(1, 5)
    if answer <= 2:
        print("Yes.")
        nod()
    elif answer <= 4:
        print("No.")
        shake()
    else:
        print("Who knows.")
        shrug()

print(f"I answered {questions} questions.")
home()
