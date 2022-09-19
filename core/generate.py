import asyncio

from DGT.core.merger import DEFAULT_DCT, LoadData

dds = {
    96:0,

}
class Generator:
    def __init__(self,modules,chainList) -> None:
        self.modules = modules
        self.chainList = chainList
    def run(self):
        asyncio.run(self.main())
    async def generate(self,module,character,lenght):
        match character:
            case 64:#35:'numbers',36:'products',42:
                pass
            case 35:
                pass
            case 36:
                pass
            case 42:
                pass
    async def onCoincidence(self,n):
        st = set(n)
        ms = [ (m,n.count(m)) for m in st ]
        print('ems',n)
        if len(ms) > 1:
            mod = ms[0][1]
            rps = dds.get(mod,None)
            flg = 0
            for x in ms:
                if flg == 0 and rps != None:

                    continue
                else:
                    print('cant',x[1],ms)
            yield ''
        '''
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
    async def checkNuddles(self,lst):
        self.lddata = LoadData([],DEFAULT_DCT)
        idlst = 0
        for n in lst:

            idn = 0
            #print(n)
            
            if isinstance(n,list):
                for q in n:
                    #print('eps',q)
                    async for r in self.onCoincidence(q):
                        ...
                    #print('hello')
                    #print(r,q)
                """
                if idn != id(n):
                    #print(n)
                    async for p in self.onCoincidence(n):
                        print(p,n)
                    #print(module)
                    #print(n)
                    idn = id(n)"""
            else:
                if idlst != id(lst):
                    print(lst)
                    idlst = id(lst)
                    #self.lddata.lst = 
                continue
    async def main(self):
        #print(self.chainList)
        print(self.modules)

        for x in self.chainList:
            if isinstance(x,list):
                idn = 0
                #print(x)
                await self.checkNuddles(x)
                #print(x)
    