import csv
from email.policy import default
from json import loads
from inspect import isfunction
from os import getcwd,walk
from os.path import join,isfile
from random import randint,choice
from secrets import randbits
from itertools import zip_longest
from uuid import uuid4
import asyncio
DEFAULT_DCT = {
    'names':
        [ join(x,name) for x,y,z in walk(join(getcwd(),'DGT','dataBase')) for name in z if name.startswith('names')],
    'eage':  lambda startEage,endEage: randint([startEage,endEage]),
    'numbers': lambda lenght: randbits(lenght),
    'guid':lambda : uuid4(),
    'abso':lambda x,y,n: range(x,y+1,n),
    'characters':lambda characters: choice(characters),
    'default':'',
}
(lambda : DEFAULT_DCT.update({'hashes':dict((item.__hash__(),key) for key,item in DEFAULT_DCT.items() if isfunction(item))}))()



 


 

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
        self.__separator = ','
        self.lst = lst
        # lista con nombres de las claves de
        # los ficheros de datos a cargar
        self.dct = dct
        self.idx = 0
        self.__columnNumber = 0# columna usada para obtener datos
        self.__functionFiltrer = ''
        # dct es un diccionario en el que se indican las claves que se usaran para 
        # cargar los datos por defecto se suministra DEFAULT_DCT
        #self.load()
        # generateCoords son los datos que usara el generador para generar
        # las cadenas
    @property
    def setSeparator(self):
        return self.__separator
    @setSeparator.setter
    def setSeparator(self,sep):
        if sep == '':
            raise NameError('EL SEPARADOR NO PUEDE SER UNA CADENA SIN CARACTERES')
        self.__separator = sep
    @property 
    def setColumnNumber(self) -> int:
        return self.__columnNumber
    @setColumnNumber.setter
    def setColumnNumber(self,number:int):
        self.__columnNumber = number
    @property
    def getFilter(self) -> 'function':
        return self.__functionFiltrer
    @getFilter.setter
    def getFilter(self,function):
        self.__functionFiltrer = function
    def run(self):
        asyncio.run(self.load())
    async def load(self):
        loop = asyncio.get_running_loop()
        #self.dataLoad = [join('DGT','dataBase',y) for y in self.lst for n in self.dct.keys() if( y.startswith(n))]
        #self.taskPool = [ x for x in self.dataLoad]
        self.filesPool = []
        self.filesPool.append(await loop.run_in_executor(None, self.loadder,self.lst))
        # cargamos los modulos 
        #async for x in self.filter(self.__functionFiltrer,self.lst): print(x)
        #await self.readRowData(self.lst)
    async def filter(self,function,modules):
        '''
        permite colocar de forma perzonalisada una funcion de filtrado
        ejemplo:
        
        test = LoadData(lst=[DEFAULT_DCT.get('names')[0]])
        test.getFilter = lambda x: x if len(x[0]) <= 6 else False
        test.run()
        
        
        '''
        async for x in self.readder(modules=modules,filter=True):
            yield function(x)
    async def randomIndex(self,module:list):
        campidx = randint(0,await self.getModuleRows(module))# leemos una fila aleatoria
        return await self.readIndex(module,campidx)
        
        
    async def readIndex(self,module:list,campidx):
        '''
        funcion destinada a leer un indice en especifico del archivo
        se puede especificar la columna a leer 
        '''
        async for mod in self.loadder(module):
            md = csv.reader(mod,delimiter=self.setSeparator,quotechar='\n')
            for n,x in enumerate(md):
                if n == campidx:
                    #print(x)
                    return x[self.setColumnNumber]# devolvemos el indice
            
        
    async def readRowData(self,modules):
        #print('cols')
        #async for x in self.readder(modules=modules,rows=self.setColumnNumber):
        #    yield x
        #    ...#print(x)
        yield self.readder(modules=modules,rows=self.setColumnNumber)
    async def getModuleRows(self,module:list) -> int:
        '''
        devielve el numero de filas de uno o mas modulos
        '''
        async for x in self.loadder(module):
            mod = csv.reader(x)
            return len(next(mod)) - 1
            
    async def readder(self,modules,filter=False,rows=None):
        #print('rows',rows)
        async for x in self.loadder(modules):
            mod = csv.reader(x)
            line_counter = 0
            headers = ''
            for x in mod:
                if line_counter == 0:
                    if filter:
                        line_counter += 1
                        continue
                    #print('headers',x)
                    headers = ''
                    if isinstance(rows,int):
                        headers = x[rows]
                    else:
                        headers = x
                    line_counter += 1
                    yield headers
                else:
                    line_counter += 1
                    if isinstance(rows,int):
                        yield x[rows]
                    else:
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
            
class DataWriter:
    '''
    clase destinada a escribir los datos en stream en un formato especifico
    los formatos que soprotara son 
        * -> csv
        * -> json
        * -> sql

    '''
    def __init__(self,filename,outputFormat) -> None:
        pass
        #return (headers,data)
    async def toSql(self,tableName:str,convert2Str:bool=False,insertNewFile:bool=False):
        '''
        esta funcion se llamara por cada dato que se procesara ejemplo

        'ivan',11 etc se habra llamado 2 veces

        tableName -> nombre de la tabla
        convert2str -> es una bandera que se pasara por cada dato con ella nos aseguraremos de que si no es necesario convertir a string
        entonces no se hara y se respetara el hecho de que es un entero
        ademas si es un string se colocaran ""
        insertNewFile -> cada que sea true se insertara una nueva linea en el archivo es decir un \\n \n

        '''
        pass
#print(DEFAULT_DCT.get('names')[0])
#test = LoadData(lst=[DEFAULT_DCT.get('names')[0]])
#test.getFilter = lambda x: x if len(x) <= 6 else False
#test.setColumnNumber = 0
#test.run()