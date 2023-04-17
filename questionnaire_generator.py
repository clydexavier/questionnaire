import random
import json
import os
import glob

existing_question_and_answer = {}
user_question_and_answer = {}
new_question_and_answer = {}
incorrect_question_and_answer = {}
incorrect_question_num = []

filename =  ""
extension = ".qs"
files = glob.glob(f"*{extension}")

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

    score = 0
    total_score = num
    question_num = 1
    os.system("cls")
    for i in questions:
        answer = input("Question "+ str(question_num)+    ".\n\t" + i + "\nAnswer: ")
        answer = answer.strip()
        if(answer.lower() == existing_question_and_answer[i].lower()):
            print("Your answer is correct.\n\n")
            score += 1
        else:
            incorrect_question_and_answer[i] = answer
            incorrect_question_num.append(question_num)
            print("Your answer is incorrect.\nCorrect answer is: " + existing_question_and_answer[i]+ "\n\n")

        num -= 1
        question_num += 1
        if(num == 0):
            break
        
    print("Tolal score: " + str(score) + "/" + str(min(total_score, len(existing_question_and_answer))))      
    
    check()

def check():
    print("\n\nQuestions where your answer is incorrect.")
    global incorrect_question_and_answer
    score = 0
    i = 0
    for key in incorrect_question_and_answer:
        print("\n\nQuestion "+ str(incorrect_question_num[i]) +"\n\t" + key + "\nYour answer: " + incorrect_question_and_answer[key] + "\nCorrect answer: " + existing_question_and_answer[key])
        i+=1
    incorrect_question_and_answer.clear()
    print("\n\n")
    

def main_prompt():
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
    os.system("cls")
    while True:
        main_prompt()
    






