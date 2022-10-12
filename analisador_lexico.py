from maquina_de_estados import MaquinaDeEstados
from pprint import pprint
import os

os.system('cls')

path = 'codigo.dan'
with open(path, 'r') as f:
    codigo = f.read()

'''replace_list = ['== >= <= <>'.split(), '= > <. , : ; ( ) + - * / { }'.split()]
replace_dict = [ {key: f' {key} ' for key in list_n} for list_n in replace_list ] 
'''
'''for dict in replace_dict:
    for key in dict:
        codigo = codigo.replace(key, dict[key])'''
#print(codigo)

A = MaquinaDeEstados()
A.lexical_analyzer(codigo)
#print(A.state_machine('{ 34xs 55 ssd', 'comment'))