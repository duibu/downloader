import inquirer
import sys


def text_input(param, message,default=None,validate=True):
    try:
        questions = [inquirer.Text(param, message=message, default=default, validate=validate, show_default=False)]
        answer = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        return answer[param]
    except TypeError:
        sys.exit()

def confirm_input(param, message,default=None,validate=True):
    try:
        questions = [inquirer.Confirm(param, message=message, default=default, validate=validate)]
        answer = inquirer.prompt(questions, raise_keyboard_interrupt=True)
        return answer[param]
    except TypeError as e:
        pass
        sys.exit()