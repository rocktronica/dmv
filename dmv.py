import json
import sys
from random import randint
import argparse

# fix: questions_asked/questions_to_ask, avoid duplicates
# ideas: keep a list of problem questions, reprint failed questions!

questions = json.load(open("questions.json"))

def get_random_question():
    return questions[randint(0, len(questions)) - 1]

def prompt_question(question):
    print question.get("label")

    correct_answer_letter = None
    for i, option in enumerate(question.get("options")):
        option_letter = chr(i + 65)
        print "  " + option_letter + ": " + option.get("text")
        if option.get("isAnswer"):
            correct_answer_letter = option_letter

    got_correct = True

    user_answer_letter = raw_input("  ?: ").upper()
    while (not user_answer_letter == "Q" and not user_answer_letter == correct_answer_letter):
        user_answer_letter = raw_input("  X: ").upper()
        got_correct = False

    # maybe this could return a (correct: false, continue: true, etc)
    if user_answer_letter == "Q":
        return None
    else:
        print "That's right: " + user_answer_letter + "! \n"
        return got_correct

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--questions", help="number of questions to ask", type=int)
    args = parser.parse_args()

    questions_total = 0
    questions_to_ask = args.questions or 5
    questions_correct = 0

    keep_going = True

    print

    while (keep_going and questions_total < questions_to_ask):
        got_answer_correct = prompt_question(get_random_question())
        if got_answer_correct:
            questions_correct += 1
        keep_going = not got_answer_correct == None
        if keep_going:
            questions_total += 1

    print "Your score: " + str(questions_correct) + "/" + str(questions_total) + " - " + str(int(float(questions_correct) / float(questions_total) * 100)) + "%"