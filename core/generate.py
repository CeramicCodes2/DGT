import asyncio
from . import Fore,Style
from tqdm.asyncio import trange
#from inspect import isfunction

from DGT.core.merger import DEFAULT_DCT, LoadData,DataWriter

class Generator(LoadData):
    def __init__(self,modules,chainList,rows) -> None:
        self.modules = modules
        self.rows = rows 
        self.chainList = chainList
        self.hashLists = dict()
        self.controlCharacters = [96,'r',43]
        super().__init__(self,self.modules)
    def run(self):
        asyncio.run(self.main())
        #super().run()
    #async def load(self,)
    async def countCoincidence(self,n):
        '''
        funcion destinada a contar la cantidad de apariciones de cada numero
        en la lista
        '''
        st = set(n)
        ms = [ (m,n.count(m)) for m in st ]
        #print('ems',ms)
        return ms
    async def specialCharacters(self,char,apprs=False) -> str:
        '''
        funcion destinada a
        realizar un procedimiento dado un caracter especial

        recibe como parametros  (caracter especial,cantidad de ocurrencias)
        '''
        match char:
            case 96:
                return self.modules.get(apprs)
            case 'r':
                return self.modules.get(123)
            case _:
                raise NameError(f'caracter desconocido {char}')
        pass
    def checkStr(self,lst) -> bool:
        '''
        checa si todos los items de una lista son caracteres
        '''
        return all([ True if isinstance(x,str) else False for x in set(lst) ])
    def chrInList(self,lst) -> bool:
        '''
        checa si hay un caracter en la lista y si es asi checa si el caracter
        es un caracter especial 
        '''
        return any([ True if (isinstance(x,str)) and (x in self.controlCharacters) else False for x in lst])
    async def checkFourtyOne(self,listApprs,mod,idx=[1,-1],eidx=[1]):
        #print('appp',listApprs)
        if listApprs[-1][0] == 43:
            return ((listApprs[idx[0]],listApprs[idx[1]]),mod)#1,-1
        else:
            return ((listApprs[eidx[0]],(43,1)),mod)# al resultado se le restara un 1 (1)
    async def getModules(self,lst):
        '''
        funcion destinada a obtener el nombre del modulo dependiendo de la lista
        se ingresa una lista simple
        [96,64,64,64,64]
        retorna
        [96,64,64,64,64],'modulo'
        '''
        #print('littt',lst)
        if self.checkStr(lst):
            # seguramente si todos los items de la lista son caracteres es un choice
            #print('choice',lst)
            
            return (lst,self.modules.get(40))
        elif self.chrInList(lst) or self.hashLists.get(hash := self.getHash(lst),None):
            if lst[0] == 'r':
                char = lst[0]
                mod = await self.specialCharacters(char)
                lst.pop(0)# elimnamos por fin 'r'
            else:
                #print('OTHERRR')
                mod = self.modules.get(123)
                #print(mod)
            return (lst,mod)
        listApprs = [n for n in await self.countCoincidence(lst)]
        #print(listApprs,lst)
        #print('apprsCOUNT',listApprs,'LIST',lst)
        if listApprs[0][0] == 96:
            char,apprs = listApprs[0]
            #print('APC LL',listApprs)
            mod = await self.specialCharacters(char,apprs)
            return await self.checkFourtyOne(listApprs,mod)
        elif listApprs[-1][0] == 43:
            #print('OPL',listApprs,lst)
            mod = [self.modules.get(listApprs[0][0])]# se requiere una lista
            # el modulo sera 64 o algun otro codigo al no tener ningun 96 
            #char,apprs = listApprs
            return await self.checkFourtyOne(listApprs,mod,idx=[0,-1],eidx=[0])# seguramente al no haber 96 se escogera el modulo 0
        #elif listApprs[-1][0]:
        #    char,apprs = listApprs[0]
        #    return await self.checkFourtyOne(listApprs,await self.specialCharacters(char,apprs))
        for x in listApprs:
            char,apprs = x
            #print('pre',char)
            md = self.modules.get(char,None)
            if md == None:
                print(f'ALERTA: no se pudo cargar el modulo para el valor {char} insertando valor por defecto')
                md = DEFAULT_DCT.get('default')
                #print(md,x)
            return (x,md)
    async def loadMod(self,character,module):
        #self.lddata = LoadData(module)
        await super().run()
        await super().load()
        
        #await super().run()
        
        
        
    async def generateNotNuddlesData(self,lst):
        #print('not nuddle',lst)
        #await self.load()
        #await self.load('readRowData',self.modules)
        #print('nuddle',await self.getModules(lst))
        yield await self.getModules(lst)
        
    
    async def generateNuddles(self,lst):
        #print('lstt',lst)
        for x in lst:
            
            yield self.getModules(x)
        #apprs = [n for m in lst for n in await self.countCoincidence(m)]
        #print('apprs nuddles',apprs)
    def getHash(self,element,q=101,d=256):
        '''
        funcion destinada a crear un hash nuevo de una lista
        
        para ello usaremos numeros primos y la forma de crear hashes de el algoritmo
        de krap
        
        fuentes:
            https://www.geeksforgeeks.org/rabin-karp-algorithm-for-pattern-searching/
        '''
        p = 0# valor del hash
        #d = 256 numero de caracteres en el alfabeto 
        for item in element:
            p = (d * p + item)%q
        return p 
        
    async def generate(self,lst:iter): #,item,idx):
        '''
        generador de datos
        se suministrara una lista con el caracter,coincidencias y su modulo de ejecucion
        
        '''
        async for element in lst:
            #print(element)
            if not(isinstance(element[0][0],int) or isinstance(element[0][0],str)):
                '''
                solo procesamos datos con modulos o anidados
                ejemplo 
                nt (((64, 4), (43, 3)), ['C:\\Users\\ispi2\\OneDrive\\Documents\\projects\\DGT\\DGT\\dataBase\\names_estados.csv'])
                
                '''
                #96 64 etc 43
                #print('\nnt',element)
                #await asyncio.sleep(3)
                num,cot = element[0][1]
                cot -= 1# restamos uno para que se acceda al modulo
                # especificado ya que se cuenta desde cero
                if num == 43:
                    #print(element[-1])
                    
                    #super().setColumnNumber = cot# colocamos la columna a usar
                    if len(element[-1]) == 2:
                        
                        element[-1].pop(-1)# eliminamos el 64 que esta al final
                    #print(element[-1])
                    #print(cot)
                    rows = await super().getModuleRows(element[-1])
                    
                    #print(rows,cot,element)
                    if rows < cot:
                        raise NameError(f'se esta accediendo a una columna inexistente el archivo {element[-1]} solo tiene {rows + 1} y se quiere acceder a {cot + 1}')
                    self.setColumnNumber = cot# colocamos la columna a usar
                    #print(self.setColumnNumber)
                    #print(await super().randomIndex(element[-1]))
                    #print('IMPORTANT',num,cot,element,await super().randomIndex(element[-1]))
                        
                    yield await super().randomIndex(element[-1],lambda x: len(x) < element[0][0][1])#super().readRowData(element[-1])# el modulo es el ultimo elemento
                #print(element[0][1][0],element[0][1][1])
            else:
                '''
                procesamos datos no anidados
                
                para ello checaremos si su hash es igual a alguno de los que existen en el DEFAULT_DCT
                '''
                #print(element)
                #print(element[-1].__hash__(),DEFAULT_DCT['hashes'].keys(),True)
                if key := DEFAULT_DCT['hashes'].get(element[-1].__hash__(),None):
                    #print(element,key,'ky')
                    function = element[-1]
                    match key:
                        #case 'names': no habra case names por que ya lo procesamos 
                        case 'eage':
                            ...
                        case 'numbers':
                            # mandamos a llamar y retornamos valor
                            yield function(element[0][1])
                        case 'guids':
                            yield function()
                        case 'abso':
                            if len(element[0]) <= 2:
                                # esta condicion solo se ejecutara en la primer iteracion
                                # ya que toda lista de rangos despues de la primer iteracion
                                # sera mayor o igual a 2 
                                #print(True)
                                #await asyncio.sleep(0.5)
                                element[0].append(1)# {10 ~ 300} -> {10 ~ 300 | 1}
                                # la funcion recibe 3 parametros y se le esta dando solo 2 por ello agregamos 
                                # el salto 
                            # creamos un diccionario que enlazara cada hash de una lista con
                            # un rango
                            #print(self.createNewHash(element[0]),'ELEMEEEENT')

                            if not(self.hashLists.get(hash:=self.getHash(element[0]),None)):
                                #await asyncio.sleep(3)
                                #print(element)
                                # nos cercioramos que no exista el hash en la lista
                                # ya que esta funcion se mandara a llamar cada
                                # vez que se procesen los datos 
                                # si none es true entonces crearemos el hash
                                self.hashLists.update({
                                    hash:iter(function(*element[0]))# a;adimos el rango y convertimos en un iterador
                                })
                                #print('nx',hash)
                                #await asyncio.sleep(3)
                                #element[0].insert(0,'r')
                                """                                
                                try:
                                    res = next(self.hashLists.get(hash))
                                except StopIteration:
                                    res = 0
                                yield res# devolveremos el primer valor
                                """
                            try:
                                res = next(self.hashLists.get(self.getHash(element[0]),None))# obtenemos el siguiente valor
                            except StopIteration:
                                res = 0
                            yield res
                            #yield ''
                        case 'characters':
                            yield function(element[0])
                        case _:
                            # default
                            pass
                        
                    pass
                
                #yield element
                #print('ops',element)
                # usaremos los metodos magicos __hash__ en caso de que sea una funcion para
                
                
                # comprobar si no es un rango
                '''
                if isfunction(element[-1]) and (len(element) -1 < 2) and not(isinstance(element[0][0],str)):
                    #return element[-1]
                    print(element)
                #    print(element)#(element[0][-1]))
                else:
                    print(element)
                #    print(element)
                #    #print(element[-1](*element[::-1]))'''
    def concatData(self,lst):
        pass     
    async def checkNuddles(self,lst):
        '''
        funcion destinada a buscar datos  anidados y no anidados
        dependiendo de ello llamara funciones destinadas a generar los datos
        esta funcion retornara un solo valor dependiendo de la lista parseada ejemplo
        [96,64,64,64] o lo que seria
        '`@@@' -> (se cargo el modulo names_jordan) -> hello
        
        '''
        #self.lddata = LoadData([],DEFAULT_DCT)
        #cnudle = 0
        idlst = 0
        #print('er',rlist)
        for idx,n in enumerate(lst):
            
            idn = 0
            #print(n)
            
            if isinstance(n,list):
                # detectamos si es un dato anidado
                if idn != id(n):
                    #print('nuddles',n)
                    idn = id(n)
                    self.nuddleElement = True
                    async for element in self.generate((await sx async for sx in self.generateNuddles(n))):
                        yield element# aqui juntaremos el elemento generado para despues concatenar todo

            else:

                if idlst != id(lst):
                    #print('not nuddles',lst)
                    idlst = id(lst)
                    #print(await self.generate(self.generateNotNuddlesData(lst)))
                    nod =  self.generateNotNuddlesData(lst)
                    #print(lst)
                    async for k in self.generate(nod):
                        #print(k)
                        yield k
                    #print([w async for w in self.generate(self.generateNotNuddlesData(lst),n,idx)])
                    #await self.generate(self.generateNotNuddlesData(lst),item=n,idx=idx)
                    #self.lddata.lst = 
                    #cnudle += 1
                continue
        # se termino de llenar la lista
        # ahora podremos generar los datos
    async def main(self):
        print(f'{Fore.GREEN} starting to generate data {Style.RESET_ALL}'.center(70,'='))
        print(Fore.CYAN)
        gen = 0
        self.nuddleElement = False
        # nuddle element sera una bandera que se activara cada que se tenga un valor anidado
        # esta se desactivara por cada elemento por lo que el meotod
        # check nuddles se encargara de activarla cada que sea necesario
        #iterRows = 0:
        #print('iteration',iterRows)
        writter = DataWriter('test.txt','sql',self.rows)
        writter.setTableName = 'NOMBRES_ESTADOS'
        writter.enableCalculateRows
        writter.enableCalculateRows = ['NOMBRE','ID']
        #ops = open('tests.txt','w+')
        for itm in trange(0,self.rows):
            for x in self.chainList:
                #print(x)
                self.resps = []# por cada item se vuelve a resetear la lista
                self.nuddleElement = False
                # desactibamos nuddleFlag
                if isinstance(x,list):
                    #await asyncio.sleep(0.5)
                    idn = 0
                    #print(x)
                    async for res in self.checkNuddles(x):
                        #print(res)
                        if self.nuddleElement:
                            #print(True)
                            self.resps.append(res)
                            #print('res',res)
                        else:
                            await writter.toSql(res,itm)
                            #ops.write(str(res) + ' ')
                    smstr = ''
                    for concat in self.resps:
                        #print('con',concat)
                        smstr += str(concat)
                        smstr += ''
                    #print('concat',smstr,self.resps)
                    
                    if smstr != '':
                        await writter.toSql(smstr,itm,convert2Str=True)
            await writter.toSql('',itm,insertNewFile=True)# insertamos una nueva
                    #ops.write('\n')
                    
        """_summary_
        EL RESULTADO DE ESTE CODIGO ARROJA
            [43, 43, 43, 64, 64, 64, 64]
            OPL [(64, 4), (43, 3)] [43, 43, 43, 64, 64, 64, 64]
            []
            [[[64, 64, 64, 64, 64, 64, 64, 64], [35, 35, 35], [42, 42, 42, 42]]]
            [2, UUID('ea1ae6da-25ce-4652-8c21-a1f3e77d3741')]
            [42, 42, 42, 42, 42, 42]
            []
            [35, 35, 35, 35, 35, 35]
            []
            [[[43, 64, 64, 64], [42, 42, 42, 42]]]
            OPL [(64, 3), (43, 1)] [43, 64, 64, 64]
            ['Chiapas', UUID('fb926f8d-8e01-4dca-b539-6a318bef99da')]
            ['r', 112, 333, 3]
            []
            [35, 35, 35]
            []
            [[['chardet', 'cyna'], [42, 42, 42, 42]]]
            ['cyna', UUID('9aa3d105-fedd-491a-8b39-a25fcb86c95b')]
            [[['cypher', 'control']]]
            ['cypher']
            [[['r', 3, 100]]]
            [range(3, 101)]
            [[['r', 20, 200, 2]]]
            [range(20, 201, 2)]
        POR LO QUE SERA NECESARIO 
        EN EL CASO DE LOS RANGOS ESTRAERLOS Y CUANDO LLEGE EL MOMENTO DE INSERTAR UN NUEVO
        VALOR SALTAR A LA CORRUTINA QUE DEVOLVERA EL SIGUIENTE VALOR DEL RANGO
        
        MODO DE SOLUCION PROPUESTO:
        
            QUE SE USE EL HASH DE LA LISTA Y SE CREE DINAMICAMENTE UN DICCIONARIO DE LA FORMA
            
            HASH: [RANGE(X,Y,N)]
            
            ASI SE RELACIONARA EL HASH CON EL RANGO Y POR CADA OCURRENCIA DEL RANGO
            SE GENERARA UNA ITERACION NUEVA 
            
            TAMBIEN ES NECESARIO A;ADIR UNA EXCEPCION EN CASO DE QUE EL RANGO SEA MENOR
            A LA CANTIDAD DE DATOS ITERADOS ESPERADOS
            """
                #print(self.resps)
                #print('fill list',self.resps)
                
        
    