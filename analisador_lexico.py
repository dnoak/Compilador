from maquina_de_estados import MaquinaDeEstados
from pprint import pprint
import os

os.system('cls')

path = 'codigo.dan'
with open(path, 'r') as f:
    codigo = f.read()

codigo = '''
program lalg;
var a: integer;
2323.23
{asd} {s dasds s  s  s }
332==1;
3 == a * 3 /56.8;
var a3: -1;
var sss: 3 >= 3 <= 4
34 < 3
3 > 32
if (bal120ss== 1 ) begin
axxx3 = 123.;
end

begin
readd(a,@,1);
read(B);
end .
'''

A = MaquinaDeEstados()
A.lexical_analyzer(codigo)
