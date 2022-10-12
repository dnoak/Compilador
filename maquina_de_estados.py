import os
from pprint import pprint

os.system('cls')

class MaquinaDeEstados():
    def __init__(self):
        self.state_dict = {
            '0-9': self.is_int,
            'a-zA-Z': self.is_alpha,
            'A-Z': self.is_upper,
            'a-z': self.is_lower,
            'op': self.is_operator,

            '+': self.is_plus,
            '-': self.is_minus,
            '*': self.is_mult,
            '/': self.is_div,

            '>': self.is_bigger,
            '<': self.is_minor,
            '=': self.is_assign, 

            '.': self.is_dot,
            ',': self.is_comma,
            ':': self.is_colon,            
            ';': self.is_scolon,
            
            ' ': self.is_space,

            'END': self.END,
        }


        self.transitions_dict = {
            'id': {
                'START':   ['a-zA-Z'],
                'a-zA-Z':    ['0-9', 'a-zA-Z', 'END'],
                '0-9':  [ '0-9', 'a-zA-Z', 'END'],
                'END': ['END']
            },

            'int': {
                'START':   ['0-9'],
                '0-9':  ['0-9', 'END'],
                'END': ['END']
            },

            'float': {
                'START':       ['0-9 (ESQ)', '. (1)'],
                '0-9 (ESQ)':  ['0-9 (ESQ)', '. (2)', 'END'],
                '0-9 (DIR)':  ['0-9 (DIR)', 'END'],
                '. (1)':            ['0-9 (DIR)'],
                '. (2)':            ['0-9 (DIR)', 'END'],
                'END': ['END']
            },

            'int operation': {
                'START':       ['-', '+', '0-9'],
                '0-9': ['-', '+', '*', '/', '0-9', 'END'],

                '-': ['0-9',],
                '+': ['0-9',],
                '*': ['0-9',],
                '/': ['0-9',],
                'END': ['END']
            },

            '==': {
                'START': ['= (1)'],
                '= (1)': ['= (2)'],
                '= (2)': ['END'],

                'END': ['END']
            },

            '>=': {
                'START': ['>'],
                '>': ['='],
                '=': ['END'],
                'END': ['END']
            }
        }

    def is_int(self, char): return char.isdigit()
    def is_alpha(self, char): return char.isalpha()
    def is_lower(self, char): return char.islower()
    def is_upper(self, char): return char.isupper()
    def is_operator(self, char): return char in ['+','-', '/','*']
    def is_dot(self, char): return char == '.'
    def is_comma(self, char): return char == ','
    def is_plus(self, char): return char == '+'
    def is_minus(self, char): return char == '-'
    def is_mult(self, char): return char == '*'
    def is_div(self, char): return char == '/'
    def is_space(self, char): return char == ' '
    def is_bigger(self, char): return char == '>'
    def is_minor(self, char): return char == '<'
    def is_assign(self, char): return char == '='
    def is_colon(self, char): return char == ':'
    def is_scolon(self, char): return char == ';'
    def END(self, char): return False

    def state_machine(self, string, key):

        string = list(string)
        transitions = self.transitions_dict[key]

        directions = transitions['START']
        for char in string:
            #print(char)
            for dir in directions:

                if self.state_dict[dir.split()[0]](char):

                    directions = transitions[dir]
                    break
            else: return False

        #print(directions, end=' - ')
        
        if 'END' in directions:
            return True
        else:
            return False

a = MaquinaDeEstados()

print(f"{a.state_machine('=', '==') = }")
print(f"{a.state_machine('==', '==') = }")
print(f"{a.state_machine('===', '==') = }")
print()
print(f"{a.state_machine('>=', '>=') = }")
print(f"{a.state_machine('>==', '>=') = }")
print(f"{a.state_machine('>>=', '>=') = }")
print(f"{a.state_machine('=', '>=') = }")
print(f"{a.state_machine('>', '>=') = }")
print()
print(f"{a.state_machine('238+342/4880-6*4/45', 'int operation') = }")
print(f"{a.state_machine('238++342/4880-6*4/45', 'int operation') = }")
print(f"{a.state_machine('238+3440-6*/4/45', 'int operation') = }")
print()
print(f"{a.state_machine('.', 'float') = }")
print(f"{a.state_machine('1.', 'float') = }")
print(f"{a.state_machine('.1', 'float') = }")
print(f"{a.state_machine('2384.21', 'float') = }")
print()
print(f"{a.state_machine('sd.', 'id') = }")
print(f"{a.state_machine('sdda0032', 'id') = }")
print(f"{a.state_machine('9sd123', 'id') = }")
print(f"{a.state_machine('ad34ssdsad874', 'id') = }")