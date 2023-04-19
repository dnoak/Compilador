from lixo.maquina_de_estados import MaquinaDeEstados
from pprint import pprint
import os

os.system('cls')

path = 'codigo.dan'
with open(path, 'r') as f:
    codigo = f.read()

A = MaquinaDeEstados()
A.lexical_analyzer(codigo)
