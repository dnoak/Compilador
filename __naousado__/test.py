import os
from collections import defaultdict
from pprint import pprint
import json

os.system('cls')

lalgol = \
'''\
1. <programa> ::= program ident ; <corpo> .
2. <corpo> ::= <dc> begin <comandos> end
3. <dc> ::= <dc_v> <dc_p>
4. <dc_v> ::= var <variaveis> : <tipo_var> ; <dc_v> | λ
5. <tipo_var> ::= real | integer
6. <variaveis> ::= ident <mais_var>
7. <mais_var> ::= , <variaveis> | λ
8. <dc_p> ::= procedure ident <parametros> ; <corpo_p> <dc_p> | λ
9. <parametros> ::= ( <lista_par> ) | λ
10. <lista_par> ::= <variaveis> : <tipo_var> <mais_par>
11. <mais_par> ::= ; <lista_par> | λ
12. <corpo_p> ::= <dc_loc> begin <comandos> end ;
13. <dc_loc> ::= <dc_v>
14. <lista_arg> ::= ( <argumentos> ) | λ
15. <argumentos> ::= ident <mais_ident>
16. <mais_ident> ::= ; <argumentos> | λ
17. <pfalsa> ::= else <cmd> | λ
18. <comandos> ::= <cmd> ; <comandos> | λ
19. <cmd> ::=\
    read ( <variaveis> ) |\
    write ( <variaveis> ) |\
    while <condicao> do <cmd> |\
    if <condicao> then <cmd> <pfalsa> |\
    ident := <expressao> |\
    ident <lista_arg> |\
    begin <comandos> end
20. <condicao> ::= <expressao> <relacao> <expressao>
21. <relacao> ::= = | <> | >= | <= | > | <
22. <expressao> ::= <termo> <outros_termos>
23. <op_un> ::= + | - | λ
24. <outros_termos> ::= <op_ad> <termo> <outros_termos> | λ
25. <op_ad> ::= + | -
26. <termo> ::= <op_un> <fator> <mais_fatores>
27. <mais_fatores> ::= <op_mul> <fator> <mais_fatores> | λ
28. <op_mul> ::= * | /
29. <fator> ::= ident | numero_int | numero_real | ( <expressao> ) \
'''

def format(state, sym=True):
    if state[0] == '<' and state[-1] == '>':
        return sym*'*'+state[1:-1]
    else:
        return sym*'$'+state

automatas = defaultdict(lambda: defaultdict())
for line in lalgol.split('\n'):
    automata = line.split('::=')[0].split()[1][1:-1]
    branch_states = line.split('::=')[1].split('|')
    automatas[automata]['start'] = []
    for states in branch_states:
        next_state = 'start'
        for state in states.split():
            if next_state == 'start':
                automatas[automata][next_state].append(format(state))
            else:
                automatas[automata][next_state] = [format(state)]
            next_state = format(state, sym=False)
        #automatas[automata][next_state] = ['$']
    print(branch_states)

    pprint(json.loads(json.dumps(automatas)), indent=2, sort_dicts=False)
    #print(json.dumps(automatas, indent=4))
    #input()


with open('jahhahaha.json', 'w') as j:
    j.write(json.dumps(automatas, indent=2))