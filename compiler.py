import os
import json

os.system('cls')

automatas = {
    "0-9": {"start": ['$'+str(i) for i in range(6)]},
    "A-Z": {"start": ['$'+chr(i+65) for i in range(6)]},
    "a-z": {"start": ['$'+chr(i+97) for i in range(6)]},
    "sign": {"start": ["$+", "$-"]},
    "op": {"start": ["$+", "$-", "$*", "$/"]},
    
    "id": {
        "start": ["*a-z", "*A-Z"],
        "a-z": ["*a-z", "*A-Z", "*int", "$"],
        "A-Z": ["*A-Z", "*a-z", "*int", "$"],
        "int": ["*int", "*A-Z", "*a-z", "$"]
    },
    "int": {
        "start": ["*0-9"],
        "0-9": ["*0-9", '$']
    },
    "float": {
        "start": ["$.#0", "*int#0"],
        ".#0": ["*int#1"],
        ".#1": ["*int#1", "$"],
        "int#0": ["*int#0", "$.#1", "$"],
        "int#1": ["*int#1", "$"]
    },
    "op_int": {
        "start": ["*int"],
        "int": ["*op", "$"],
        "op": ["*int"],
    },
    "op_float": {
        "start": ["*float"],
        "float": ["*op", "$"],
        "op": ["*float"],
    },
    "mat_f": {
        "start": ["*sign"],
        "sign": ["*op_int", "*op_float"],
        "op_int": ["*sign", "$"],
        "op_float": ["*sign", "$"],
    },
    "teste": {
        "start": ["*sign"],
        "sign": ["*int", "$"],
        "int": ["*teste"]
    },
}

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
                    else:
                        return 1
        else:
            if '$' in states:
                log(f"{spaces(depth)}{'🔸'*3} FIM {automata} {'🔸'*3}")
                #log('')
                return 1
            log(f"{spaces(depth)}❌ {state=}")

            return 0
        
        if depth == 1:
            log('\n')


string = 'if numero_int * numero_real != numero_real then ident := ident '

pos = 0
string=list(string.split()+['$'])

with open('lalg.json') as j: algol = json.load(j)
automatas |= algol

#dball= ['🟡', '🟢', '🔵', '🟠', '🔴', '🟣','🟤', '⚫']*2

spaces = lambda x: ''.join([f'|{s}|' if s==x-1 else '|   ' for s in range(x)])
format_ = lambda x: x.split('#')[0][1:]
log = lambda x: print(x) if True else ...

sm_result = state_machine('comandos')

print(f"\n{'#'*12}\n{bool(sm_result)}, [{pos}:{len(string)-1}]\n{'#'*12}")
#print((len(string) == pos+1) and bool(sm_result))




    

