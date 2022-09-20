import asyncio
from inspect import isfunction

from DGT.core.merger import DEFAULT_DCT, LoadData

dds = {
    96:0,
    'r':1

}
class Generator:
    def __init__(self,modules,chainList) -> None:
        self.modules = modules
        self.chainList = chainList
        self.controlCharacters = [96,'r']
    def run(self):
        asyncio.run(self.main())
    async def countCoincidence(self,n):
        '''
        funcion destinada a contar la cantidad de apariciones de cada numero
        en la lista
        '''
        st = set(n)
        ms = [ (m,n.count(m)) for m in st ]
        #print('ems',ms)
        return ms
        '''
        if len(ms) > 1:
            mod = ms[0][1]
            moduleName = dds.get(mod,None)
            flg = 0
            print(moduleName)
            for x in ms:
                if flg == 0 and moduleName != None:
                    print(moduleName)
                    continue
                else:
                    print('cant',x[1],ms)
            yield ''
        else:
            yield ms
        
        if len(ms) > 1:
            print('mm',ms)
            #print(ms[0][1])
            #module = self.modules.get(ms[0][1])#96
            #print(ms,module)
            # obtendremos el modulo y lo generamos los datos

            #lddata.lst = [module[0]]
            #lddata.run()
            #lddata.filter(lambda x: x if len(x) > ms[1][1] else None,module)
            #yield module
        else:
            print('mos',ms)
            # de listas normales tambien obtenemos el modulo y procesamos
            #print(x)
            for x in ms:
                # generacion de datos
                #print(self.modules)
                yield self.modules.get(x[0])'''
    async def generate(self,character,lenght):
        '''
        funcion destinada a generar datos dependiendo del
        tipo de dato que se requiera

        ejemplo  si hay un 96 en character
        entonces 
        '''
        match character:
            case 96:
                pass
            case 35:
                pass
            case 36:
                pass
            case 42:
                pass
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
                raise NameError(f'caracter desconosido {char}')
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
            return (listApprs[1],mod)
        for x in listApprs:
            char,apprs = x
            #print('pre',char)
            md = self.modules.get(char,None)
            if md == None:
                print(f'ALERTA: no se pudo cargar el modulo para el valor {char} insertando valor por defecto')
                md = DEFAULT_DCT.get('default')
            return (x,md)
            #print(char,self.modules.get(char,None))
        '''
        for x in lst:
            print(x)
            #listApprs = [n for m in lst for n in await self.countCoincidence(lst)]
            #if (rs:=dds.get(x,None)) != None:
            #    print('edrsss',rs,listApprs)'''
    async def LoadMod(self,character,module):
        self.lddata = LoadData(module)
        pass


        
    async def generateNotNuddlesData(self,lst):
        #print('not nuddle',lst)
        print('apprs',await self.getModules(lst))
    
    async def generateNuddles(self,lst):
        #print('lstt',lst)
        for x in lst:
            ...
            print('nnudle',await self.getModules(x))
        #apprs = [n for m in lst for n in await self.countCoincidence(m)]
        #print('apprs nuddles',apprs)
    async def checkNuddles(self,lst):
        '''
        funcion destinada a buscar datos  anidados y no anidados
        dependiendo de ello llamara funciones destinadas a generar los datos
        '''
        self.lddata = LoadData([],DEFAULT_DCT)
        idlst = 0
        for n in lst:

            idn = 0
            #print(n)
            
            if isinstance(n,list):
                # detectamos si es un dato anidado
                if idn != id(n):
                    #print('nuddles',n)
                    await self.generateNuddles(n)
                    idn = id(n)
                #print('nuddle',lst)

            else:

                if idlst != id(lst):
                    await self.generateNotNuddlesData(lst)
                    idlst = id(lst)
                    #self.lddata.lst = 
                continue
    async def main(self):
        print('starting to generate data'.center(70,'='))
        print(self.chainList)
        #print(self.modules)

        for x in self.chainList:
            if isinstance(x,list):
                idn = 0
                #print(x)
                await self.checkNuddles(x)
                #print(x)
    