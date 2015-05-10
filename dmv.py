import json
import sys
import random
import argparse
import re
import os

# ideas: keep a list of problem questions, reprint failed questions!, single character input

questions = json.load(open(os.path.dirname(os.path.realpath(__file__)) + "/questions.json"))

# Randomize possible answers
for i, question in enumerate(questions):
    random.shuffle(questions[i].get("options"))

def get_random_question():
    if (len(questions) >= 1):
        question = questions[random.randint(0, len(questions)) - 1]
        questions.remove(question)
        return question

def get_correct_index(question):
    for i, option in enumerate(question.get("options")):
        if option.get("isAnswer"):
            return i

def get_correct_letter(question):
    return index_to_letter(get_correct_index(question))

def print_question(question):
    wrap_print(question.get("label"))
    for i, option in enumerate(question.get("options")):
        wrap_print(index_to_letter(i) + ": " + option.get("text"), 2, 5)

def prompt_for_answer(question):
    correct_letter = get_correct_letter(question)

    user_answer_letter = raw_input("  ?: ").upper()

    return {
        'letter': user_answer_letter,
        'correct': user_answer_letter == correct_letter
    }

def answer_as_sentence(question):
    label = question.get("label").strip()
    answer = question.get("options")[get_correct_index(question)].get("text")
    sentence = None

    if (label[-1:] == ":"):
        separator = " "
        if (label.lower().find("when") == 0) and (label.find(",") == -1):
            separator = ", "
        sentence = label[:-1] + separator + lowercase_first(answer)
    elif (label.find("__") > -1):
        sentence = re.sub(r'_+', answer, label)
    else:
        sentence = label + " " + answer

    if (not sentence[-1:] == "."):
        sentence += "."

    return sentence

def lowercase_first(str):
    return str[:1].lower() + str[1:]

def index_to_letter(index):
    return chr(index + 65)

def percent_score(correct, total):
    return str(int(float(questions_correct) / float(questions_total) * 100)) + "%"

# First pass at implementation, confident there are more efficient ways!
def wrap_print(string, first_line_indent=0, other_lines_indent=0, line_width=80):
    on_first_line = True
    current_line_length = line_width - first_line_indent

    lines = [string]

    while (len(lines[-1]) > current_line_length):
        old_last_line = lines[-1]

        split_at = old_last_line[0:current_line_length].rindex(" ") + 1
        if (split_at == -1):
            split_at = current_line_length

        second_to_last_line = old_last_line[0:split_at]
        new_last_line = old_last_line[split_at:len(old_last_line)]

        lines[-1] = second_to_last_line
        lines.append(new_last_line)

        if (on_first_line):
            current_line_length = line_width - other_lines_indent
            on_first_line = False

    indent = (" " * first_line_indent)
    for i, line in enumerate(lines):
        lines[i] = indent + line
        indent = (" " * other_lines_indent)

    print "\n".join(lines)

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

        if not question:
            continue_questions = False
        else:
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
                wrap_print("That's right!", 2)
                wrap_print(answer_as_sentence(question), 2, 2)
                print
                if correct:
                    questions_correct += 1

    if (questions_total > 0):
        wrap_print("Correct: " + str(questions_correct) + "/" + str(questions_total))
        wrap_print("Score:   " + percent_score(questions_correct, questions_total))