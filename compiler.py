import os
import json

os.system('cls')

def state_machine(automata, depth=1):
    global pos
    next_state = 'start'
    return_state = 0
    while pos < len(string):
        states = automatas[automata][next_state]
        log(f"{spaces(depth)}❓\"{string[pos]}\" ⏩ {states}")
        for state_pos, state in enumerate(states): #🟢
            if state[0] == '$':
                if (string[pos]) == format_(state):
                    log(f"{spaces(depth+1)}🟢🟢🟢 \"{string[pos]}\" {state} 🟢🟢🟢")
                    pos += 1
                    if state[1:] in automatas[automata].keys():
                        next_state = state[1:]
                        break
                    else:
                        log(f"{spaces(depth)} ✔️ $ {state=}")
                        return 1
            else:
                log(f"{spaces(depth+1)}{'🔹'*3} ↘️ INICIO {state} {'🔹'*3}")
                return_state = state_machine(format_(state), depth+1)

                if return_state:
                    # if e else adicionados (testando ainda)
                    if state[1:] in automatas[automata].keys():
                        next_state = state[1:]
                        log(f"{spaces(depth)} * {state=}")
                        break
                    else: return 1
        else:
            if '$' in states:
                log(f"{spaces(depth)}{'🔸'*3} FIM {automata} {'🔸'*3}")
                return 1
            log(f"{spaces(depth)}❌ {state=}")
            return 0
        if depth == 1: log('\n')


string = 'if numero_int * numero_real != numero_real then ident'
automata = 'comandos'

pos = 0
string=list(string.split()+['$'])

automatas = {}
with open('lalg.json') as j: automatas |= json.load(j)
with open('automatas.json') as j: automatas |= json.load(j)

spaces = lambda x: ''.join([f'|{s}|' if s==x-1 else '|   ' for s in range(x)])
format_ = lambda x: x.split('#')[0][1:]
log = lambda x: print(x) if True else ...

state_machine_result = state_machine(automata)
print(f"\n{'#'*12}\n{bool(state_machine_result)}, [{pos}:{len(string)-1}]\n{'#'*12}")




    

