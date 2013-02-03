import json
import sys
from random import randint
import argparse

# ideas: answer as sentence, keep a list of problem questions, avoid duplicates, reprint failed questions!

questions = json.load(open("questions.json"))

def get_random_question():
    return questions[randint(0, len(questions)) - 1]

def get_correct_letter(question):
    for i, option in enumerate(question.get("options")):
        if option.get("isAnswer"):
            return index_to_letter(i)

def print_question(question):
    print question.get("label")
    for i, option in enumerate(question.get("options")):
        print "  " + index_to_letter(i) + ": " + option.get("text")

def prompt_for_answer(question):
    correct_letter = get_correct_letter(question)

    user_answer_letter = raw_input("  ?: ").upper()

    return {
        'letter': user_answer_letter,
        'correct': user_answer_letter == correct_letter
    }

def index_to_letter(index):
    return chr(index + 65)

def percent_score(correct, total):
    return str(int(float(questions_correct) / float(questions_total) * 100)) + "%"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--questions", help="number of questions to ask", type=int)
    args = parser.parse_args()

    questions_total = 0
    questions_to_ask = args.questions or 5
    questions_correct = 0

    continue_questions = True

    print

    while (continue_questions and questions_total < questions_to_ask):
        question = get_random_question()
        asking = True
        answered = True
        correct = True

        print_question(question)

        while (asking):
            user_answer = prompt_for_answer(question)
            if (user_answer.get("letter") == "Q"):
                asking = False
                answered = False
                continue_questions = False
            elif (user_answer.get("correct")):
                asking = False
            elif (not user_answer.get("correct")):
                correct = False

        print

        if answered:
            questions_total += 1
            print "  That's right! \n"
            if correct:
                questions_correct += 1

    if (questions_total > 0):
        print "Correct: " + str(questions_correct) + "/" + str(questions_total)
        print "Score:   " + percent_score(questions_correct, questions_total)