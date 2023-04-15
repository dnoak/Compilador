import os

os.system('cls')

automatas = {
    # terminais
    "0-9": {"start": ["$"+str(i) for i in range(10)]},
    "A-Z": {"start": ["$"+chr(i+65) for i in range(10)]},
    "a-z": {"start": ["$"+chr(i+97) for i in range(10)]},
    "op_add": {"start": ["$+", "$-"]},
    "op_mul": {"start": ["$*", "$/"]},

    # não terminais
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
    "op_mat": {
        "start": ["*op_add"],
        "op_add": ["*int", "$("],
        "int": ["*int", "*op_mul", "*op_add", "$end"],
        "op_mul": ["*op_add"],
        "(": ["*op_mat"],
        "op_mat": ["$)"],
        ")": ["*op_mat", "$end"],
    },
    "sinal": {"start": ["$+", "$-"]},
    "op": {"start": ["$+", "$-", "$*", "$/"]},
    "int_op": {
        "start": ["*int", "*mat"],
        "int": ["*op#0", "$end"],
        "op#0": ["*int"],
        "mat": ["*op#1", "$end"],
        "op#1": ["*mat"]
    },
    "mat": {
        "start": ["$("],
        "(": ["*sinal"],
        "sinal": ["*int_op"],
        "int_op": ["$)"],
        ")": ["*mat", "$end"],
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
        #print(pos,len(string))

        return_state = None
        states = automatas[automata][next_state]
        log(f"{depth*spaces}❓\"{string[pos]}\" ⏩ {states}")

        for state_pos, state in enumerate(states): #🟢
            if state[0] == '$':
                if (string[pos]) == format(state):
                    log(f"{(depth+1)*spaces}✔️ {string[pos]} {state}")
                    pos += 1
                    if state[1:] in automatas[automata].keys():
                        next_state = state[1:]
                        break
                    else:
                        log(f"{(depth+1)*spaces}🟢 $ {return_state=}, {state=}")
                        return state

            else:
                log(f"{(depth+1)*spaces} ↘️ {state}")
                return_state = state_machine(format(state), depth+1)

                if return_state is not None:
                    next_state = state[1:]
                    log(f"{(depth+1)*spaces}🟢 * {return_state=}, {state=}")
                    break
                    #return state
                else:
                    #print(state_pos, len(states))
                    #if state_pos < len(states):
                       # continue
                    #return None
                    continue

        # else:
        #     if state == '$end':
        #         print(f"{depth*' '*2}✔️ FIM {automata}")
        #         print()
        #         return state
        #     print(f"{depth*' '*2}<< TODOS {return_state=}, {state=}")
        #     return None
        else:
            if '$end' in states:
                log(f"{depth*' '*2}{'✅'*10} FIM {automata} {'✅'*10}")
                log('')
                return '$end'
 
            log(f"{depth*' '*2}❌ {return_state=}, {state=}")
            return None
    #return None

pos = 0
string = '(+1*2+-(+3)+(+4))'
spaces = 4*' '

string=list(string+'$')
sm_result = state_machine('mat')
print(sm_result)
print(pos, len(string))
print(len(string) == pos+1 and sm_result == '$end')




    

