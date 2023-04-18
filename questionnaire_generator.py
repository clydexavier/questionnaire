import random
import json
import os
import glob
import concurrent.futures as futures
import time

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

    difficulty = difficultySelection()
    time_alloted = difficulty * (num/len(existing_question_and_answer)) # Time with respect to number of questions
    time_alloted = time_alloted + ((difficulty * num) / 60) # (difficulty + num)/60 is typing time offset bonus time

    os.system('cls')
    print(f'You are attempting to answer {num} {"question" if num == 1 else "questions"} under {time.strftime("%M minute(s) and %S second(s)", time.gmtime(int(time_alloted))) } minutes')
    print('Once entered, you cannot exit 🥰, CTRL + C to Exit but will take quite a while since functions cannot be stopped 🥰')
    print('\n-- Pres ENTER to continute --')
    input()
    score = quiz(num, questions, time_alloted)

    os.system("cls")
    print(f'Quiz statistics\nScore: {score} out of {num} questions\n')
    check()

def difficultySelection():
    print('Select a time difficulty: ')
    diff = None

    while not diff:
        diff = input('[E]asy\n[M]edium\n[H]ard\n\nAnswer: ').lower().strip()
        if diff not in ['e', 'm', 'h']:
            diff = None
            print('Choice not in selection')

    return {'e': 15, 'm' : 10, 'h' : 7}[diff] * 60 # In minutes

def quiz(items_total, questions, time_limit):
    global incorrect_question_and_answer
    global incorrect_question_num
    score = 0
    os.system("cls")

    with futures.ThreadPoolExecutor() as executor:
        timer = executor.submit(time.sleep, time_limit)
        start_time = time.monotonic()

        j = 1
        for i in questions:
            answer: str = ''

            try:
                answering = executor.submit(input, "Question "+ str(j) + "\n\t"+ i + "\nAnswer: ")

                done, not_done = futures.wait([answering, timer], return_when=futures.FIRST_COMPLETED)

                if timer in done and answering in not_done:
                    raise Exception
                elif answering in done:
                    answer = answering.result()
                    answer = answer.strip()

            except Exception as e:
                print('\n\n-- Time is up! Answer entered will not be counted --')
                incorrect_question_num.append(j)
                incorrect_question_and_answer[i] = answer.lower()
                print("\nCorrect answer is: " + existing_question_and_answer[i] + '\n')
                print('Press any key to continue. . .')
                executor.shutdown(wait=False)
                return score

            if(answer.lower() == existing_question_and_answer[i].lower()):
                print("Your answer is correct.\n\n")
                score += 1
            else:
                incorrect_question_and_answer[i] = answer
                print("Your answer is incorrect.\nCorrect answer is: " + existing_question_and_answer[i]+ "\n\n")
                incorrect_question_and_answer[i] = answer.lower()
                incorrect_question_num.append(j)

            j += 1
            items_total -= 1
            if(items_total == 0):
                break

        if timer.running():
            print(f'Time took to complete quiz: {round(time.monotonic() - start_time, 2)}\nTime left: {time_limit - (round(time.monotonic() - start_time, 2))}\n')

            timer.cancel()
            executor.shutdown(wait=False, cancel_futures=True)

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
