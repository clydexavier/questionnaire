import random
import json
import os
import glob
import time
import threading as th

existing_question_and_answer = {}
user_question_and_answer = {}
new_question_and_answer = {}
incorrect_question_and_answer = {}
incorrect_question_num = []

filename =  ""
extension = ".qs"
files = glob.glob(f"*{extension}")

with open("appdevenum.qs", 'w') as f:
    json.dump(new_question_and_answer , f)

def print_files():
    if(len(files) == 0):
        return 0

    else:
        print("Questionnaires in current directory.")
        for file in files:
            print(file)

def open_file(filename):
    with open (filename, 'r') as f:
       global existing_question_and_answer
       existing_question_and_answer = json.load(f)

def save_questions():
    if len(new_question_and_answer) == 0:
        print("No questions to save.")
        return

    global filename
    print_files()
    filename = input("Where to save questions?\nAnswer: ")
    open_file(filename)
    existing_question_and_answer.update(new_question_and_answer)
    new_question_and_answer.clear()
    with open(filename, 'w') as f:
        json.dump(existing_question_and_answer, f)


def add_question():
    global new_question_and_answer
    question = input("Enter question: ")
    question = question.lower()
    answer = input("Enter answer to the question: ")
    answer = answer.lower()
    new_question_and_answer[question] = answer


def open_questionnaire():
    if print_files() == 0:
        print("No questionnaire in current directory.")

    questionnaire = input("What file to open?\nAnswer: ")
    global filename
    global incorrect_question_and_answer
    global incorrect_question_num
    filename = questionnaire
    open_file(questionnaire)

    questions = existing_question_and_answer.keys()
    questions = list(questions)
    random.shuffle(questions)
    os.system("cls")

    num = int(input("How man questions to generate out of " + str(len(existing_question_and_answer)) + "?\nAnswer: "))
    if(num < 0):
        raise ValueError("Input must be a positive number")

    difficulty = difficultySelection()
    
    os.system('cls')
    print(f'You are attempting to answer {num} {"question" if num == 1 else "questions"}. You can answer each question in under {difficulty} {"second" if difficulty == 1 else "seconds."} ')
    print('\n-- Pres ENTER to continute --')
    input()
    score = quiz(num, questions, difficulty)

    os.system("cls")
    print(f'Quiz statistics\nScore: {score} out of {num} questions\n')
    check()

def difficultySelection():
    print('Select a time difficulty')
    print('Answer each question in: ')
    diff = None

    while not diff:
        easy = 45
        med = 20
        difficult = 10
        diff = input('[E]asy - '+str(easy)+ ' seconds. \n[M]edium - '+str(med)+' seconds\n[H]ard - '+ str(difficult)+' seconds\n\nAnswer: ').lower().strip()
        if diff not in ['e', 'm', 'h']:
            diff = None
            print('Choice not in selection')

    return {'e': 45, 'm' : 20, 'h' : 10}[diff] # In minutes

def foo():
    pass

def quiz(items_total, questions, time_limit):
    global incorrect_question_and_answer
    global incorrect_question_num
    score = 0
    os.system("cls")

    question_num = 1
    answered = 0
    for i in questions:
        S = th.Timer(time_limit, foo)
        S.start()
        
        answer = input("Question "+ str(question_num)+    ".\n\t" + i + "\nAnswer: ")
        answer = answer.strip()
        if answer.lower() == existing_question_and_answer[i].lower() and S.is_alive():
            print("Your answer is correct.\n\n")
            score += 1

        elif answer.lower() != existing_question_and_answer[i].lower() and S.is_alive(): 
            incorrect_question_and_answer[i] = answer
            incorrect_question_num.append(question_num)
            print("Your answer is incorrect.\nCorrect answer is: " + existing_question_and_answer[i]+ "\n\n")

        else:
            incorrect_question_and_answer[i] = "Time's up."
            incorrect_question_num.append(question_num)
            print("Time's up.\n\n")

        S.cancel()
            
    
        question_num += 1
        items_total -= 1

        if items_total == 0:
            break
        

        
    return score

def check():
    global incorrect_question_and_answer

    if not incorrect_question_and_answer:
        return

    print("Questions where your answer is incorrect.\n")

    i = 0
    for key in incorrect_question_and_answer:
        print("Question "+ str(incorrect_question_num[i]) +"\n\t" + key + "\nYour answer: " + incorrect_question_and_answer[key] + "\nCorrect answer: " + existing_question_and_answer[key])
        print("\n")
        i += 1

    incorrect_question_and_answer.clear()

    print("Press any key to continue. . .")
    input()


def main_prompt():
    os.system("cls")
    ans = input("[A]. Add Question \n[B]. Open Questionnaire \n[C]. Save Questions\n[D]. Exit\nAnswer: ")
    ans = ans.upper()
    if ans == 'A':
        add_question()
    elif ans == 'B':
        open_questionnaire()
    elif ans == 'C':
        save_questions()
    elif ans == 'D':
        exit()
    else:
        print("Invalid answer.")

if __name__ == "__main__":
    while True:
        main_prompt()
