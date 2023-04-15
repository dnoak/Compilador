import os

os.system('cls')

automatas = {
    "0-9": {"start": ["$"+str(i) for i in range(10)]},
    "A-Z": {"start": ["$"+chr(i+65) for i in range(10)]},
    "a-z": {"start": ["$"+chr(i+97) for i in range(10)]},
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
        "sign": ["*op_float"],
        "op_int": ["*sign", "$end"],
        "op_float": ["*sign", "$end"],
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
    }
}

def format(state):
    return state.split('#')[0][1:]

def log(message, t=True):
    if t: print(message)

def state_machine(automata, depth=0):
    global pos
    next_state = 'start'
    while pos < len(string):
        return_state = None
        states = automatas[automata][next_state]
        for state_pos, state in enumerate(states): #🟢
            if state[0] == '$':
                if (string[pos]) == format(state):
                    pos += 1
                    if state[1:] in automatas[automata].keys():
                        next_state = state[1:]
                        break
                    else: return state
            else:
                return_state = state_machine(format(state), depth+1)
                if return_state is not None:
                    if next_state in states:
                        next_state = state[1:]
                        break
                    else: return state
        else:
            if '$end' in states: return '$end'
            return None

pos = 0
string = ['program', 'ident', ';', 'dc', 'begin', 'comandos', '.', '$']#'+43.8*.4737/4385'
spaces = 4*' '

#string=list(string+'$')
sm_result = state_machine('programa')
print(sm_result)
print(pos, len(string))
print(len(string) == pos+1 and sm_result == '$end')




    

