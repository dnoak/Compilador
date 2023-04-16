import os

os.system('cls')

automatas = {
    "0-9": {"start": ['$'+str(i) for i in range(6)]},
    "A-Z": {"start": ['$'+chr(i+65) for i in range(6)]},
    "a-z": {"start": ['$'+chr(i+97) for i in range(6)]},
    "sign": {"start": ["$+", "$-"]},
    "op": {"start": ["$+", "$-", "$*", "$/"]},
    
    "id": {
        "start": ["*a-z", "*A-Z"],
        "a-z": ["*a-z", "*A-Z", "*int", "$end"],
        "A-Z": ["*A-Z", "*a-z", "*int", "$end"],
        "int": ["*int", "*A-Z", "*a-z", "$end"]
    },
    "int": {
        "start": ["*0-9"],
        "0-9": ["*0-9", '$end']
    },
    "float": {
        "start": ["$.#0", "*int#0"],
        ".#0": ["*int#1"],
        ".#1": ["*int#1", "$end"],
        "int#0": ["*int#0", "$.#1", "$end"],
        "int#1": ["*int#1", "$end"]
    },
    "op_int": {
        "start": ["*int"],
        "int": ["*op", "$end"],
        "op": ["*int"],
    },
    "op_float": {
        "start": ["*float"],
        "float": ["*op", "$end"],
        "op": ["*float"],
    },
    "mat_f": {
        "start": ["*sign"],
        "sign": ["*op_int", "*op_float"],
        "op_int": ["*sign", "$end"],
        "op_float": ["*sign", "$end"],
    },
    "teste": {
        "start": ["*sign"],
        "sign": ["*int", "$end"],
        "int": ["*teste"]
    },

    "programa": {
        "start": ["$program"],
        "program": ["$ident"],
        "ident": ["$;"],
        ";": ["*corpo"],
        "corpo": ["$."],
        ".": ["$end"],
    },
    "corpo": {
        "start": ["*dc"],
        "dc": ["$begin"],
        "begin": ["*comandos"],
        "comandos": ["$end"],
    },
    "dc": {
        "start": ["*dc_v", "*dc_p"],
    },
    "dc_v": {
        "start": ["$var", "$end"],
        "var": ["$variaveis"],
        "variaveis": ["$:"],
        ":": ["*tipo_var"],
        "tipo_var": ["$;"],
        ";": ["*dc_v"],
    },
    "tipo_var": {
        "start": ["$tipo_var"]
    },
    "dc_p": {
        "start": ["$dc_p"]
    },
    "comandos": {
        "start": ["$comandos"]
    },
    
    "condicao": {
        "start": ["*expressao"],
        "expressao": ["*relacao", "$end"],
        "relacao": ["*expressao"],
    },
    "relacao": {
        "start": ["$!=", "$>=", "$<=", "$>", "$<" ]
    },
    "expressao": {
        "start": ["*termo"],
        #"termo": []
    },
    "termo": {
        "start": ["$x", "$y", "$z"]
    }
}

format_ = lambda x: x.split('#')[0][1:]
log = lambda x: print(x) if 1 else ...

def state_machine(automata, depth=1):
    global pos
    next_state = 'start'
    return_state = 0
    while pos < len(string):
        states = automatas[automata][next_state]
        log(f"{spaces(depth)}{dball[depth]}❓\"{string[pos]}\" ⏩ {states}")

        for state_pos, state in enumerate(states): #🟢
            if state[0] == '$':
                if (string[pos]) == format_(state):
                    log(f"{spaces(depth+1)}✔️ {string[pos]} {state}")
                    pos += 1
                    if state[1:] in automatas[automata].keys():
                        next_state = state[1:]
                        break
                    else:
                        log(f"{spaces(depth)}{dball[depth]} ✔️ $ {return_state=}, {state=}")
                        return 1

            else:
                log(f"{spaces(depth+1)}{'🔹'*5} ↘️ INICIO {state} {'🔹'*5}")
                return_state = state_machine(format_(state), depth+1)

                if return_state:
                    # if e else adicionados (testando ainda)
                    if state[1:] in automatas[automata].keys():
                        next_state = state[1:]
                        log(f"{spaces(depth)}{dball[depth]}✔️ * {return_state=}, {state=}")
                        break
                    else:
                        return 1
        else:
            if '$end' in states:
                log(f"{spaces(depth)}{'🔸'*5} FIM {automata} {'🔸'*5}")
                #log('')
                return 1
            log(f"{spaces(depth)}❌ {return_state=}, {state=}")
            return 0
        
        if depth == 1:
            log('\n')

dball= ['🟡', '🟢', '🔵', '🟠', '🔴', '🟣','🟤', '⚫']
pos = 0
string = ['x', '>=', 'y', '<', 'z', '!=', "x"]
spaces = lambda x: ''.join([f'|{s}|' if s==x-1 else ' '*4 for s in range(x)])

string=list(string+['$'])
sm_result = state_machine('condicao')
print(sm_result)
print(pos, len(string))
print(len(string) == pos+1)




    

