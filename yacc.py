import os
import json

os.system('cls')

def state_machine(automata, depth=1):
    global pos
    next_state = 'start'
    while pos < len(string):
        states = automatas[automata][next_state]
        log(f"{spaces(depth)}❓\"{string[pos]}\" ⏩ {states}")
        for state in states:
            if state[0] == '$':
                if (string[pos]) == format_(state):
                    log(f"{spaces(depth+1)}🟢 \"{string[pos]}\" {state}", 'green')
                    pos += 1
                    if state[1:] in automatas[automata].keys():
                        next_state = state[1:]
                        break
                    else:
                        log(f"{spaces(depth)} ✔️ $ {state=}")
                        return True
            else:
                log(f"{spaces(depth+1)}{'🔹'} ↘️ INICIO {state}")
                return_state = state_machine(format_(state), depth+1)
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

string = '''
program ident ;
var ident : real ;
var ident : integer ;
var ident , ident : integer ;

procedure ident ( ident : real ) ;
begin
    read ( ident , ident ) ;
    if ident < ident + ident then
    begin
        ident := ident + ident ;
        write ( ident ) ;
    end
    else ident := ident + ident ; 
end ;

begin 
  read ( ident ) ;
  ident ( ident ) ;
end .
'''
automata = 'programa'

# string = " ( ident ; ident ; ident ) "
# automata = "lista_arg"

pos = 0
string = list(string.split()+['$']) if len(string.split()) > 1 else list(string+"$")

automatas = {}
with open('lalg.json') as j: automatas |= json.load(j)
with open('automatas.json') as j: automatas |= json.load(j)

spaces = lambda x: ''.join([f'|{s}|' if s==x-1 else '|   ' for s in range(x)])
format_ = lambda x: x.split('#')[0][1:]
log = lambda x, color=False: print(f"{colors[color]}{x}{colors['end']}") if color else print(x)


colors = [f"\x1b[5;30;4{i}m" for i in range(8)]
colors = {'green': '\033[42m', 'red': '\033[41m', 'yellow': '\033[93m', 'end': '\033[0m'}

state_machine_result = state_machine(automata)
print(f"\n {'_'*22}\n| Chegou ao fim: {bool(state_machine_result)}")
print(f"| Tokens lidos: {pos}/{len(string)-1}")
print(f"| Último token: {string[pos]}\n {'‾'*22}")
