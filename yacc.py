import os
import json

os.system('cls')

def recursive_state_machine(automata, code, depth=1, next_state='start'):
    global pos
    while pos < len(code):
        states = automatas[automata][next_state]
        log(f"{spaces(depth)}❓\"{code[pos]}\" ⏩ {states}")
        for state in states:
            if state[0] == '$':
                if (code[pos]) == format_state(state):
                    log(f"{spaces(depth+1)}🟢 \"{code[pos]}\" {state}", 'green')
                    pos += 1
                    if state[1:] in automatas[automata].keys():
                        next_state = state[1:]
                        break
                    else:
                        log(f"{spaces(depth)} ✔️ $ {state=}")
                        return True
            else:
                log(f"{spaces(depth+1)}{'🔹'} ↘️ INICIO {state}")
                return_state = recursive_state_machine(format_state(state), code, depth+1)
                if return_state:
                    if state[1:] in automatas[automata].keys():
                        next_state = state[1:]
                        log(f"{spaces(depth)} * {state=}")
                        break
                    else: return True
        else:
            if '$' in states:
                log(f"{spaces(depth)}{'🔸'} FIM {automata}")
                return True
            log(f"{spaces(depth)}❌ {state=}", 'red')
            return False
        if depth == 1: log('\n')

def read_automatas(folder):
    with open(f'{folder}/types.json') as j: types_fsm = json.load(j)
    with open(f'{folder}/lalg.json') as j: lalg_fsm = json.load(j)
    with open(f'{folder}/lexical.json') as j: lexical_fsm = json.load(j)
    return types_fsm, lalg_fsm, lexical_fsm

def format_code(code, lexical_fsm):
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
    return (code.replace('$', '').replace('  ', ' ')+' $').split()

def tokenization(code):
    global pos
    lex_keys = ['reserved_symbols_2char', 'reserved_symbols_1char', 'reserved_words']
    lex_tokens = sum([automatas[lex_key]['start'] for lex_key in lex_keys], [])
    types_tokens = {'id': 'ident', 'int': 'numero_int', 'float': 'numero_real'}
    tokenized_code = []
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
                print(f"Erro no token \"{token}\", posição {token_pos}")
    return tokenized_code + ['$']

spaces = lambda x: ''.join([f'|{s}|' if s==x-1 else '|   ' for s in range(x)])
format_state = lambda x: x.split('#')[0][1:]
log = lambda x, color=False: ...#print(f"{colors[color]}{x}{colors['end']}") if color else print(x)
colors = {'green': '\033[92m', 'red': '\033[91m', 'yellow': '\033[93m', 'end': '\033[0m'}

code = '''
program ident;
var teste : real;
var id3 : real ;
var id2, id42 : integer;

procedure sdusu2282j2(ident: integer);
begin
    ident := ident + ident;
    begin
        while ident <= ident+ident do
        read(ident);
    end;
end;

procedure ident(ident:real);
begin
    read(ident, ident );
    if ident <=ident +ident then
    begin
        ident := ident + 123;
        write ( ident ) ;
        write (ident);
    end
    else ident := ident + 123.321 ; 
end ;

begin 
    read(   ident);
    ident( ident);
end 
'''

automata = 'programa'
pos = 0

types_fsm, lalg_fsm, lexical_fsm = read_automatas('automatas')
automatas = types_fsm | lalg_fsm | lexical_fsm

formated_code = format_code(code, lexical_fsm)

tokenized_code = tokenization(formated_code)
#print(tokenized_code)

pos = 0
recursive_state_machine_result = recursive_state_machine(automata, tokenized_code)
print(f"\n {'_'*22}\n| Chegou ao fim: {bool(recursive_state_machine_result)}")
print(f"| Tokens lidos: {pos}/{len(formated_code)-1}")
print(f"| Último token: {tokenized_code[pos]} ({formated_code[pos]})\n {'‾'*22}")

