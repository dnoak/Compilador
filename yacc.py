import os
import json
import glob

os.system('cls')

def recursive_state_machine(automata, code, depth=1, next_state='start'):
    global pos
    while pos < len(code):
        states = automatas[automata][next_state]
        log_syntatic(f"{spaces(depth)}❓\"{code[pos]}\" ⏩ {states}")
        for state in states:
            if state[0] == '$':
                if (code[pos]) == format_state(state):
                    log_syntatic(f"{spaces(depth+1)}🟢 \"{code[pos]}\" {state}", 'green')
                    pos += 1
                    if state[1:] in automatas[automata].keys():
                        next_state = state[1:]
                        break
                    else:
                        log_syntatic(f"{spaces(depth)} ✔️ $ {state=}")
                        return True
            else:
                log_syntatic(f"{spaces(depth+1)}{'🔹'} ↘️ INICIO {state}")
                return_state = recursive_state_machine(format_state(state), code, depth+1)
                if return_state:
                    if state[1:] in automatas[automata].keys():
                        next_state = state[1:]
                        log_syntatic(f"{spaces(depth)} * {state=}")
                        break
                    else: return True
        else:
            if '$' in states:
                log_syntatic(f"{spaces(depth)}{'🔸'} FIM {automata}")
                return True
            log_syntatic(f"{spaces(depth)}❌ {state=}", 'red')
            return False
        if depth == 1: log_syntatic('\n')

def read_automatas(folder):
    with open(f'{folder}/types.json') as j: types_fsm = json.load(j)
    with open(f'{folder}/lalg.json') as j: lalg_fsm = json.load(j)
    with open(f'{folder}/lexical.json') as j: lexical_fsm = json.load(j)
    return types_fsm, lalg_fsm, lexical_fsm

def remove_coments(code):
    for pos, char in enumerate(code):
        if char == '{':
            code[pos] = ''
            while code[pos] != '}':
                code[pos] = ''
                pos += 1
            code[pos] = ''
    return ''.join(code)

def format_code(code, lexical_fsm):
    code = remove_coments(list(code))
    lexical_order = list(lexical_fsm.keys())[0:2]
    for order in lexical_order:
        for symbol in lexical_fsm[order]['start']:
            code = code.split(' ')
            for i in range(len(code)):
                if '$' in code[i]: 
                    continue
                if symbol[1:] in code[i].strip():
                    code[i] = code[i].replace(symbol[1:], f' {symbol} ')
            code = ' '.join(code)
    code = code.replace('end.', 'end .')
    return (code.replace('$', '').replace('  ', ' ')+' $').split()

def tokenization(code):
    global pos
    lex_keys = ['reserved_symbols_2char', 'reserved_symbols_1char', 'reserved_words']
    lex_tokens = sum([automatas[lex_key]['start'] for lex_key in lex_keys], [])
    types_tokens = {'id': 'ident', 'int': 'numero_int', 'float': 'numero_real', '.': '.'}
    tokenized_code = []
    lexical_error = 0
    log(f" ______Análise léxica______", 'yellow')
    for token_pos, token in enumerate(code[:-1]):
        if ('$'+token) in lex_tokens:
            tokenized_code.append(token)
            continue
        else:
            for ttoken_key, ttoken_value in types_tokens.items():
                pos = 0
                result = recursive_state_machine(ttoken_key, list(token+'$'))
                if result:
                    if pos == len(token):
                        tokenized_code.append(ttoken_value)
                        break
            else:
                log(f"| Erro: \"{token}\", posição: {token_pos}", 'red')
                lexical_error += 1
    result_color = 'green' if len(code)-lexical_error == len(code) else 'red'
    log(f"| tokens corretos: {len(code)-lexical_error}/{len(code)}", result_color)
    return tokenized_code + ['$']

spaces = lambda x: ''.join([f'|{s}|' if s==x-1 else '|   ' for s in range(x)])
format_state = lambda x: x.split('#')[0][1:]
log_syntatic = lambda x, color=False, enable=False: log(x, color) if enable else ...
log = lambda x, color=False: print(f"{colors[color]}{x}\033[0m") if color else print(x)

colors = {'green': '\033[92m', 'red': '\033[91m', 'yellow': '\033[93m', 'blue': '\033[96m'}

codes = []
for file in glob.glob('codes/*.lalg'):
    with open(file) as f:
        codes.append((f.read(), file))

for i, (code, file_name) in enumerate(codes):
    log(f'Código: {os.path.split(file_name)[1]}', 'blue')
    automata = 'programa'

    types_fsm, lalg_fsm, lexical_fsm = read_automatas('automatas')
    automatas = types_fsm | lalg_fsm | lexical_fsm

    pos = 0
    formated_code = format_code(code, lexical_fsm)
    tokenized_code = tokenization(formated_code)

    pos = 0
    recursive_state_machine_result = recursive_state_machine(automata, tokenized_code)

    color_end = 'green' if recursive_state_machine_result else 'red'
    color_read = 'green' if pos == len(formated_code)-1 else 'red'
    color_last = 'green' if tokenized_code[pos] == '$' else 'red'
    log(f" _____Análise sintática_____", 'yellow')
    log(f"| Chegou ao fim: {bool(recursive_state_machine_result)}", color_end)
    log(f"| Tokens lidos: {pos}/{len(formated_code)-1}", color_read)
    log(f"| Último token lido: {tokenized_code[pos]} ({formated_code[pos]})", color_last)
    print('\n\n')
