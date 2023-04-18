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
    automatas = {}
    #for file in os.listdir(folder):
    with open(f'{folder}/types.json') as j: types_fsm = json.load(j)
    with open(f'{folder}/lalg.json') as j: lalg_fsm = json.load(j)
    with open(f'{folder}/lexical.json') as j: lexical_fsm = json.load(j)
    return types_fsm, lalg_fsm, lexical_fsm

def format_code(code, lexical_fsm):
    lexical_order = list(lexical_fsm.keys())[0:2]
    code = code.strip().replace('end.', 'end .')
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

def tokenization(code, lexical_fsm, types_fsm):
    global pos
    lex_tokens = sum([lexical_fsm[a]['start'] for a in lexical_fsm], [])
    types_tokens = ['id', 'int', 'float']
    for token in code:
        print(token, end=' -> ')
        if ('$'+token) in lex_tokens:
            print()
            continue
        else:
            for type_token in types_tokens:
                pos = 0
                #print(type_token)
                if recursive_state_machine(type_token, list(token+'$')):
                    continue
            else:
                print('erro')
        input()
         

spaces = lambda x: ''.join([f'|{s}|' if s==x-1 else '|   ' for s in range(x)])
format_state = lambda x: x.split('#')[0][1:]
log = lambda x, color=False: ...#print(f"{colors[color]}{x}{colors['end']}") if color else print(x)
colors = {'green': '\033[92m', 'red': '\033[91m', 'yellow': '\033[93m', 'end': '\033[0m'}

code = '''
program ident;
var testeee6: real;
var ident: integer;
var ident, ident: integer;

procedure ident(ident: integer);
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
        ident := ident + numero_int;
        write ( ident ) ;
        write (ident);
    end
    else ident := ident + numero_real ; 
end ;

begin
    read(   ident);
    ident( ident);
end .
'''

automata = 'programa'

pos = 0

types_fsm, lalg_fsm, lexical_fsm = read_automatas('automatas')
automatas = types_fsm | lalg_fsm | lexical_fsm
code = format_code(code, lexical_fsm)

tokenization(code, lexical_fsm, types_fsm)
input()

recursive_state_machine_result = recursive_state_machine(automata, code)
print(f"\n {'_'*22}\n| Chegou ao fim: {bool(recursive_state_machine_result)}")
print(f"| Tokens lidos: {pos}/{len(code)-1}")
print(f"| Último token: {code[pos]}\n {'‾'*22}")

