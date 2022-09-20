import csv
from json import loads
from os import getcwd,walk
from os.path import join,isfile
from random import randint,choice
from itertools import zip_longest
import asyncio
DEFAULT_DCT = {
    'names':
        [ join(x,name) for x,y,z in walk(join(getcwd(),'DGT','dataBase')) for name in z if name.startswith('names')],
    'eage':  lambda startEage,endEage: randint([startEage,endEage]),
    'numbers': 'hello',
    'guid':'fuck',
    'abso':lambda x,y,n: [n for n in range(x,y+1,n)],
    'characters':lambda characters: choice(characters),
    'default':''
}
"""
https://www.youtube.com/watch?v=MzC19OfZAOo
dct creara un diccionatio en base a los archivos que inicien 
con una nomenclatura determinada:
names -> nombres

$> ls

[ nombres datos almacenados ]
names_apellidos.csv
names_compositores.csv
names_futbolistas.csv
names_estados.csv
u
[ datos generados  ]

numeros
guid
claves 

la forma para acceder a los datos sera mediante la clase LoadData
que tomara como argumentos lst y dct

lst -> lista de los set de datos a cargar
dct -> es un diccionario que se usara para mapear los sets de datos en un directorio dado, 
este diccionario provera de funciones para generar datos

https://youtu.be/x88iTnEl0A4 *****
"""

        
class LoadData:
    """
    clase encargada de 
    cargar unicamente contenido

    """
    def __init__(self,lst:list,dct:dict=DEFAULT_DCT):
        #print(True)
        self.lst = lst
        # lista con nombres de las claves de los ficheros de datos a cargar
        self.dct = dct
        self.idx = 0
        # dct es un diccionario en el que se indican las claves que se usaran para 
        # cargar los datos por defecto se suministra DEFAULT_DCT
        #self.load()
        # generateCoords son los datos que usara el generador para generar
        # las cadenas 
    def run(self):
        asyncio.run(self.load())
    async def load(self):
        loop = asyncio.get_running_loop()
        #self.dataLoad = [join('DGT','dataBase',y) for y in self.lst for n in self.dct.keys() if( y.startswith(n))]
        #self.taskPool = [ x for x in self.dataLoad]
        self.filesPool = []
        self.filesPool.append(await loop.run_in_executor(None, self.loadder,self.lst))
    async def filter(self,function,modules):
        async for x in self.readder(modules=modules):
            yield function(x)
    async def readder(self,modules):
        async for x in self.loadder(modules):
            mod = csv.reader(x)
            line_counter = 0
            headers = ''
            for x in mod:
                if line_counter == 0:
                    headers = x
                    line_counter += 1
                    yield headers
                else:
                    line_counter += 1
                    yield x
    async def loadder(self,modules:list):
        #pool = [csv.reader(open(x,'r')) for x in self.dataLoad]
        """
        for x in pool:
            line_counter = 0
            if line_counter == 0:
                headers = next(x)
            else:
                data = next(x)
            line_counter += 1
        """
        for x in modules:
            yield open(x,'r')

        '''
        mod = csv.reader(mod)
        line_counter = 0
        headers = ''
        data = ''
        for x in mod:
            if line_counter == 0:
                headers = x
            else:
                data = x
            line_counter += 1
            yield (headers,data)'''
        #return (headers,data)
#test = LoadData(lst=[DEFAULT_DCT.get('names')[0]]).run()