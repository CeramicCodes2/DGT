from ast import Load
import asyncio
from inspect import isfunction

from DGT.core.merger import DEFAULT_DCT, LoadData

class Generator(LoadData):
    def __init__(self,modules,chainList) -> None:
        self.modules = modules
        self.chainList = chainList
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
        elif self.chrInList(lst):
            char = lst[0]
            mod = await self.specialCharacters(char)
            lst.pop(0)# elimnamos por fin 'r'
            return (lst,mod)
        listApprs = [n for n in await self.countCoincidence(lst)]
        #print('apprsCOUNT',listApprs,'LIST',lst)
        if listApprs[0][0] == 96:
            char,apprs = listApprs[0]
            #print('APC LL',listApprs)
            mod = await self.specialCharacters(char,apprs)
            if listApprs[-1][0] == 43:
                return ((listApprs[1],listApprs[-1]),mod)
            else:
                return ((listApprs[1],1))# al resultado se le restara un 1
        for x in listApprs:
            char,apprs = x
            #print('pre',char)
            md = self.modules.get(char,None)
            if md == None:
                print(f'ALERTA: no se pudo cargar el modulo para el valor {char} insertando valor por defecto')
                md = DEFAULT_DCT.get('default')
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
        return await self.getModules(lst)
        
    
    async def generateNuddles(self,lst):
        #print('lstt',lst)
        for x in lst:
            yield self.getModules(x)
        #apprs = [n for m in lst for n in await self.countCoincidence(m)]
        #print('apprs nuddles',apprs)
    async def generate(self,lst):
        '''
        generador de datos
        se suministrara una lista con el caracter,coincidencias y su modulo de ejecucion
        '''
        for element in lst:
            if isinstance(element,tuple):
                elm = element[0]
                if isinstance(elm,tuple):
                    # concat 64
                    if elm[1][0] == 43:
                        await super().readRowData()
                        elm[1][1]# se seleccionara la columna que se usara de los archivos
                else:
                    pass
    async def checkNuddles(self,lst):
        '''
        funcion destinada a buscar datos  anidados y no anidados
        dependiendo de ello llamara funciones destinadas a generar los datos
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
                    print('nuddles',n)
                    idn = id(n)
                    
                    #self.resps.append([await x async for x in self.generateNuddles(n)])
                    await self.generate([await x async for x in self.generateNuddles(n)])
                    #print('resps',resps)
                    #yield [ emp async for element in self.generateNuddles(n) async for res in element async for emp in res]
                    
                    
                    #print('nuddle',lst)
                    #cnudle += 1

            else:

                if idlst != id(lst):
                    print('not nuddles',lst)
                    idlst = id(lst)
                    #self.resps.append(await self.generateNotNuddlesData(lst))
                    #self.lddata.lst = 
                    #cnudle += 1
                continue
        # se termino de llenar la lista
        # ahora podremos generar los datos
        #await self.generate()
    async def main(self):
        print('starting to generate data'.center(70,'='))
        #print(self.chainList)
        #print(self.modules)
        #pool = []
        for x in self.chainList:
            #self.resps = []# por cada item se vuelve a resetear la lista
            if isinstance(x,list):
                idn = 0
                #print(x)
                await self.checkNuddles(x)
                #pool.append(self.resps)
                #print(self.resps)
                #async for element in self.checkNuddles(x):
        #print(pool)   
        #print([await x for n in self.chainList() async for x in self.checkNuddles(n)])
        
    