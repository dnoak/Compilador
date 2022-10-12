import os
from pprint import pprint
import time

#os.system('cls')

class MaquinaDeEstados:
    def __init__(self):
        self.syms_list = ', ; : ( ) + - * / > < ='.split()
        self.syms_special_list = '.'.split()
        self.dsyms_list = '== >= <='.split()
        self.reserved_list = 'program var integer real begin end procedure readd if else while do'.split()

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
            '(': self.is_lbracket,
            ')': self.is_rbracket,
            '{': self.is_lbrace,
            '}': self.is_rbrace,
            
            #'space': self.is_space,
            'ALL': self.ALL,
            'END': self.END,
            #'ERROR': self.error,
        }

        self.automatas_dict_syntactic = {
            'int operation': {
                'START': ['-', '+', '0-9'],
                '0-9': ['-', '+', '*', '/', '0-9', 'END'],
                '-': ['0-9',],
                '+': ['0-9',],
                '*': ['0-9',],
                '/': ['0-9',],
                'END': ['END']
            },
        }

        self.automatas_dict_regex = {
            'id': {
                'START': ['a-zA-Z'],
                'a-zA-Z': ['0-9', 'a-zA-Z', 'END'],
                '0-9':  [ '0-9', 'a-zA-Z', 'END'],
                'END': ['END']
            },

            'int': {
                'START': ['0-9'],
                '0-9': ['0-9', 'END'],
                'END': ['END']
            },

            'float': {
                'START': ['0-9 (ESQ)', '. (1)'],
                '0-9 (ESQ)': ['0-9 (ESQ)', '. (2)'],
                '0-9 (DIR)': ['0-9 (DIR)', 'END'],
                '. (1)': ['0-9 (DIR)'],
                '. (2)': ['0-9 (DIR)', 'END'],
                'END': ['END']
            },

            'comment': {
                'START': ['{'],
                '{': ['}', 'ALL'],
                'ALL': ['}', 'ALL'],
                '}': ['END'],
                'END': ['END']
            },
        }

        self.automatas_dict_dsyms = {
            dsym: {
                'START': [f'{dsym[0]} (1)'],
                f'{dsym[0]} (1)': [f'{dsym[1]} (2)'],
                f'{dsym[1]} (2)': ['END'],
                'END': ['END']
            } for dsym in self.dsyms_list
        }

        self.automatas_dict_syms = {
            sym: {
                'START': [sym],
                sym: ['END'],
                'END': ['END'],
            } for sym in self.syms_list
        }

        self.automatas_dict_syms_special = {
            sym: {
                'START': [sym],
                sym: ['END'],
                'END': ['END'],
            } for sym in self.syms_special_list
        }

        self.automatas_dict = {
            **self.automatas_dict_regex,
            **self.automatas_dict_dsyms,
            **self.automatas_dict_syms,
            **self.automatas_dict_syms_special,
            #**self.automatas_dict_syntactic,
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
    def is_lbracket(self, char): return char == '('
    def is_rbracket(self, char): return char == ')'
    def is_lbrace(self, char): return char == '{'
    def is_rbrace(self, char): return char == '}'
    def ALL(self, char): return True
    def END(self, char): return False

    def state_machine(self, string, key):
        string = list(string)
        transitions = self.automatas_dict[key]
        directions = transitions['START']
        for char in string:
            for dir in directions:
                if self.state_dict[dir.split()[0]](char):
                    directions = transitions[dir]
                    break
            else: return False
        if 'END' in directions: return True
        else: return False

    def lexical_analyzer(self, code):
        code = code.replace('\n', ' ')
        pos = 0
        formated_code = ''
        while pos < len(code):
            if code[pos] == '{':
                jump = 1
                while code[pos + jump] != '}':
                    jump += 1
                pos += jump + 1
                continue

            syms = {**self.automatas_dict_dsyms, **self.automatas_dict_syms}
            if code[pos:pos + 2] in syms:
                formated_code += f' {code[pos:pos+2]} '
                pos += 1
            elif code[pos] in syms:
                formated_code += f' {code[pos]} '
            else:
                formated_code += code[pos]
            pos += 1

        string_list = formated_code.split()

        for string in string_list:
            if string in self.reserved_list:
                print(f'{string} - {string.upper()}')
                continue
            for automata in self.automatas_dict:
                if self.state_machine(string, automata):
                    print(f'{string} - {automata}')
                    break
            else:
                print(f'{string} - ERRO')

def main_test():
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
    print(f"{a.state_machine('1453', 'int') = }")
    print(f"{a.state_machine('2384.21', 'float') = }")
    print()
    print(f"{a.state_machine('sd.', 'id') = }")
    print(f"{a.state_machine('sdda0032', 'id') = }")
    print(f"{a.state_machine('9sd123', 'id') = }")
    print(f"{a.state_machine('ad34ssdsad874', 'id') = }")

if __name__ == '__main__':
    main_test()