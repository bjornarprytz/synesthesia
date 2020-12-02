from __future__ import print_function, unicode_literals
from PyInquirer import prompt
from pprint import pprint

from music import *

m = Music()


while(True):
    questions = [
        {
            'type': 'input',
            'name': 'args',
            'message': 'Type a sound',
        }
    ]
    answers = prompt(questions)

    args = answers['args']
    
    if (args == ''):
        pass
    if (args == 'exit'):
        break
    m.interpret(answers['args'])


m.close()