import csv
from inspect import isfunction
from os import getcwd,walk,remove
from os.path import join,isfile
from random import randint,choice
from secrets import randbits
from . import Style,Fore
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
        self.tempName = join(getcwd(),'DGT','temp',str(uuid4()))
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
            yield function(x[self.setColumnNumber]),x[self.setColumnNumber]
    async def randomTemporal(self,modules):
        totalRows = len([ x for x in open(modules,'r').readlines()])
        rind = randint(0,totalRows)
        return await self.readIndex([modules],rind)
        
    async def temporalTable(self,function,modules):
        '''
        funcion destinada a crear un archivo temporal
        con una serie de registros que cumplan un criterio
        para ser usada en randomIndex
        
        
        el archivo se eliminara al llamarse el recolector de basura
        
        '''
        tmp = self.tempName
        if not(isfile(tmp)):
            with open(tmp,'w+') as tempOpen:
                dataCounter = 0# si se encontro una coincidencia se aumentara
                # si es cero quiere decir que no se encontro coincidencia y por tanto
                # no se devolvera ningun valor
                async for x,item in self.filter(function,modules):
                    if x:
                        tempOpen.write(item + '\n')
                        dataCounter += 1
                if dataCounter == 0:
                    return 'none'# no se encontraron coincidencias
            return await self.temporalTable(function,modules)
        else:
            return await self.randomTemporal(tmp)
        """
        campidx = randint(0,await self.getModuleRows(tmp))
        # obtenemos un indice aleatoreo
        await self.readIndex(tmp,campidx)"""
            
    async def randomIndex(self,module:list,filt=None):
        campidx = randint(1,await self.getModuleRows(module))# leemos una fila aleatoria que no sean los encabezados
        # filtrer sera una funcion que se encargara de filtrar el valor si esta correcto
        if filt:
            # leeremos las columnas que si cumplan el criterio y 
            # de ellas escogemos una aleatoriamente
            
            return await self.temporalTable(filt,module)
            
            #return await self.readIndex(module,)
            
        else:
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
    def __init__(self,filename,outputFormat,maxIteration) -> None:
        self.filename = open(filename,'w+')
        self.__tableName = 'DEFAULT'
        self.__dataList = []
        self.__calculateRows = False
        self.maxIteration = maxIteration# el numero maximo de iteraciones
        self.loadFilename()
        #return (headers,data)
    def loadFilename(self):
        '''
        checa si el archivo confiene algo y arroja una advertencia si es a si
        '''
        if self.filename.read():
            print(f'{Fore.YELLOW} ALERTA: {Fore.RED} el archivo contiene informacion')
            pod = input(f'{Fore.LIGHTRED_EX} desea proceder (y/n) \n {Fore.LIGHTYELLOW_EX}$>')[0]# obtenemos solo el primer caracter
            if pod == 'y':
                self.filename.seek(0)
            else:
                opod = input(f"{Fore.LIGHTGREEN_EX} ingrese otro archivo de salida: {Fore.CYAN}")
                self.filename = open(opod,'w+')
                return self.loadFilename()# recursivo
        

    @property
    def setTableName(self):
        '''
        propiedad destinada a fijar el nombre de la tabla en la cual se insertaran los datos
        '''
        return self.__tableName
    @setTableName.setter
    def setTableName(self,name:str):
        self.__tableName = name
    @property
    def enableCalculateRows(self) -> bool:
        '''
        propiedad de una cnstante se usara para habilitar 
        si se quiere usar la sintaxis para campos calculados
                
                insert into hello(campoNoCalculado, ...) values (any, ...);

            recordemos que en una tabla con campos calculados como:

                create table hello(
                    precio number(3),
                    iva (number * 0.16)
                );

                no se puede llenar con la sintaxis:

                insert into hello values (1000,22);

                ya que los campos calculados se llenan solos apartir de los datos que se van insertando por ello se usara esta constante
                para habilitar la segunda forma de llenado de datos en la funcion
                toSql 

                al habilitar esta forma de llenar los datos sera necesario suministrar una lista con el nombre de los campos

                la lista tiene que tener un largo total a los datos pasados en el string de parseado es decir:


                @@@ {1 ~ 30|1} (casado | divorciado) -> ['nombre','id','estado_civil']

                si esto no es asi se producira una excepcion llamada

                exceso de campos 
        '''
        self.__calculateRows = True
        return True
        # se tendra un getter que al ser llamado se activara
        # se comprobara en el cuerpo de la funcion si esta vareable esta activa
    @enableCalculateRows.setter
    def enableCalculateRows(self,dataList:list) -> None:
        '''
        dataList -> la lista de valores discutida en el metodo getter
        '''
        self.__dataList = dataList
    async def insertorType(self,typeInsertion:bool,data,iteration,insertNewFile:bool):
        '''
        esta funcion realizara ambos tipos de inserts 
        si la bandera typeInsertion es true se hara el insert con valores
        si no es asi se hara el insert normal 
        '''
        insertion = ''
        if typeInsertion:
            # si es true se hara la forma con campos calculados
            insertion = f'INSERT INTO {self.__tableName}({",".join(self.__dataList)}) VALUES ('
        else:
            insertion = f'INSERT INTO {self.__tableName} VALUES ('
        if insertNewFile:
            pos = self.filename.tell()
            if pos != 0:
                self.filename.seek(pos - 1)
                #restamos uno para eliminar un caracter coma que se coloca siempre
            self.filename.write(f');\n')# se insertara un cierre 
            if iteration <= self.maxIteration -2:# como contamos desde el 0 quitamos 1
                # 
                self.filename.write(insertion)
        else:
            if self.filename.tell() == 0:
                self.filename.write(insertion)
                # si es la posicion 0 colocamos un insertion ya que 
                # los insertion se colocan por cada insertNewFile
            self.filename.write(f'{data},')
    def convert2str(self,data,flag:bool):
        if flag:
            return f"'{str(data)}'"
        else:
            return data
    async def toSql(self,data,iteration:int,convert2Str:bool=False,insertNewFile:bool=False):
        '''
        esta funcion se llamara por cada dato que se procesara ejemplo:

        'ivan',11 etc se habra llamado 2 veces

        data -> el dato a almacenar
        iteration -> el numero de la iteracion
        tableName -> nombre de la tabla
        convert2str -> es una bandera que se pasara por cada dato con ella nos aseguraremos de que si no es necesario convertir a string
        entonces no se hara y se respetara el hecho de que es un entero
        ademas si es un string se colocaran ""
        insertNewFile -> cada que sea true se insertara una nueva linea en el archivo es decir un \\n \n

        '''
        if self.__calculateRows and len(self.__dataList) != 0:
            # checamos si se activo calculate rows
            # si es asi usaremos la sintaxis de  insersion de datos con nombre de campos
            await self.insertorType(True,self.convert2str(data,convert2Str),iteration,insertNewFile)
            # inicio de la escritura de datos
        else:
            # insercion clasica

            await self.insertorType(False,self.convert2str(data,convert2Str),iteration,insertNewFile)
"""dw = DataWriter('tests.txt','sql',6)
dw.setTableName = 'HELLO_WORLD'
dw.enableCalculateRows
dw.enableCalculateRows = ['id','nombre','estado_civil']
sqd = ['','carlos','soltero',1,'ivan','soltero',3,'ipsops','electrasss',22]
async def rg(dw,sqd):
    for n,x in enumerate(sqd):
        ins = False
        if n%3 == 0:
            ins = True
        #print(n,ins)
        await dw.toSql(x,n,len(sqd) -1 ,insertNewFile=ins)
async def main():
    await asyncio.gather(
        rg(dw,sqd)
    )
asyncio.run(main())"""



#print(DEFAULT_DCT.get('names')[0])
#test = LoadData(lst=[DEFAULT_DCT.get('names')[0]])
#test.getFilter = lambda x: x if len(x) <= 6 else False
#test.setColumnNumber = 0
#test.run()