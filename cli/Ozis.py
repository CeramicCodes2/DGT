from ast import Load
from itertools import count
from multiprocessing import pool
from typing import final
from ..core.merger import DEFAULT_DCT,LoadData
from ..core.generate import Generator

class Oasis:
    '''
    clase encargada de apartir de los datos que el usuario introduzca llamar a loaddata con datos necesarios
    
    nomenclatura de argumentos 
    * string: 
    @ -> nombre
    # -> numeros
    $ -> productos ('swetter',150000)
    * -> GUID
    = -> 

    la cantidad de veces colocadas un caracter indicaran en el caso de nombres
    la longitud de caracteres de estos nombres por ejemplo:

    @@@@ -> ivan

    operadores especiales como por ejemplo ` se pueden usar para multiples opciones
    
    por ejemplo como el @ se usa para nombres si se colocara el operador `
    se usara con apellidos

        `@@@@@@ -> garcia 
    
    ``@@@@ -> articulo


    el operador ` se modifica dependiendo de los tipos de datos que se manejen
    `$ -> iva

    se puede usar mas de un `
    dependiendo de cuantos se usen sera una opcion a realizar

    en realidad el uso de ` recorera a alguna columna de los datos guardados en csv

    por ejemplo si tenemos los directorios

    nombres_paizes 
    nombres_futbol

    si usamos
    @ estaremos haciendo referencia a la primer columna osea nombres paizes

    si usamos
    `@ estariamos haciendo referencia a que los datos de nombres_futbol

    para crear un nombre y apellido se puede usar
    con los siguientes archivos

    nombres_personas
    apellidos_personas

    @@@@ -> un nombre que tenga 4 caracteres
    juan

    `@@@@@@@ -> un nombre que ttenga 7 caracteres

    mendoza

    quedando como:

    @@@@`@@@@@@@ y esto da como resultado -> 'juan', 'mendoza'

    si queremos que se junte el nombre del apellido y se concatenen usariamos:

    [@@@@`@@@@@@@] -> 'juan mendoza'



    otro ejemplo

    | producto | precio | iva |

    $ -> producto
    `$ -> precio
    ``$ -> iva

    rangos:

    {inicio~final|saltos}

    colocar un caracter o otro

    ( oppus | sierra )

    se eligira aleatoreamente cual 

    https://youtu.be/WCCovrKvAtU
    '''
    def __init__(self,string:str):
        self.string = string
        self.string += ' '
        self.loadModules = []
        self.kwds = {
            64:'names',35:'numbers',36:'products',42:'guid',123:'abso',40:'characters'
        }
        self.procesateString()
        #self.loadMod(data=self.jop)
        
        #print(self.normalMarker,self.markerPersonal)

    @staticmethod
    def findCoincidence(ccNum,number,codecs):
        ps = []
        for x in codecs[ccNum:]:
            if x == number:
                ps.append(x)
            else:
                break
        return ps
    def cutForCoincidence(self,lst:list,char=32):
        oppus = []
        sidx = 0
        for n,x in enumerate(lst):
            if x == char:
                #print(True)
                oppus.append(lst[sidx:n])
                sidx = n + 1
        oppus.append(lst[sidx:])
        return oppus
    def getConcatCodes(self,poolConcat):
        tmp = (lambda idx: self.codecs[idx[0]+1:idx[1]])# remplaza los [] caracteres idx[0]+1
        coincidences = []
        for x in poolConcat:
            coincidences.append([x,self.cutForCoincidence(tmp(x))])# posicion coincidencias sin espacios
        #print(''.join(chr(x) for lst in coincidences for element in lst for x in element))
        return coincidences
    def RangeReplacePop(self,lst,lst2):
        # remplazara un rango de lista
        for x in lst2:
            n,y = x.pop(0)
            mn = min(n,y)
            for n in x:
                lst.insert(mn,n)
    def replaceSpacesInSpecialsCaracters(self,chain:list,pool:list):
        '''
        chain -> la lista de la cadena donde se encuentra el caracter especial
        por ejemplo codecs

        pool -> una lista con 2 items

        [inicio,fin]
        '''
        if (len(chain) -1 < pool[1]):
            raise NameError('El largo de la cadena es mayor a las coordenadas del pool')
        for x in range(pool[0],pool[1]+1):
            # obtenemos posiciones
            if chain[x] == 32:
                chain[x] = ''# colocamos con '' para despues remplazar ya que list.replace no funciona
        return chain
    def convert2Int(self,lst:list)-> int:
        number = ''
        for x in lst:
            number += chr(x)
        return int(number)
    def insRange(self,lst:list)->list:
        '''
        funcion destinada a limpiar y traducir las sentencias de rango

        {123~42|33} ejemplo

        tambien cuenta si hay mas de un caracter de separacion
        y si es asi levanta una excepcion 
        retorna una lista de items varieables

        si se usa el caracter | sera de un largo de 3 items
        el primero seran el inicio del rango 
        el segundo sera el fin del rango
        el tercero sera la cantidad de saltos 
        [[]]
        '''
        
        lst = [x for x in lst if x != '']
        if (lst.count(126)  or lst.count(124)) > 1:
            raise SyntaxError('error se ha insertado mas de un ~ o un | en el rango')
        clear = [d for d in lst if not((d == 123) or (d == 125))]# limpiamos de los {}
        clear = self.cutForCoincidence(clear,char=126)
        clear[1] = self.cutForCoincidence(clear[1],char=124)
        nc = []
        #print('cls',clear)
        for x in clear:
            idn = 0
            for n in x:
                
                if isinstance(n,list):
                    nc.append(self.convert2Int(n))
                else:
                    if idn != id(x):
                        idn = id(x)
                        nc.append(self.convert2Int(x))
                        continue
        #print(nc)
        nc.insert(0,'r')
        return nc
    def insChoice(self,lst):
        pass
    def procesateString(self):
        self.codecs = [ ord(x) for x in self.string]
        #print(self.codecs)
        cc = 0
        nm = []#sin usar ` normal marker
        mp = []#usando ` marquer personal
        parser = False
        #print(codecs)
        #concat = False
        pnc = False
        indexConcat = list()
        poolConcat = list()
        counterParser = 0
        reinterpret = []
        concatCodes = []
        poolNumbers = []
        poolnumConcat = []
        poolCharacters = []
        pchar = []
        globSpecialChr = []
        '''
            if(self.string[cc] ==  '{'):
                poolNumbers = list()
                pnc = True# a;adimos {}
                poolNumbers.append(cc)
            if(self.string[cc] == '}'):
                pnc = False
                poolNumbers.append(cc)
                poolnumConcat.append(poolNumbers)
        '''
        while (cc <= len(self.codecs) - 1):
            match self.codecs[cc]:
                case 40:
                    pchar = []
                    pchar.append(cc)
                case 41:
                    pchar.append(cc)
                    poolCharacters.append(pchar)
                    globSpecialChr.append(pchar)
                case 123:
                    poolNumbers = []
                    poolNumbers.append(cc)
                case 125:
                    poolNumbers.append(cc)
                    poolnumConcat.append(poolNumbers)
                    globSpecialChr.append(poolNumbers)
                case 91:
                    # si esta dentro de un [
                    indexConcat = list()
                    indexConcat.append(cc)
                case 93:
                    indexConcat.append(cc)
                    poolConcat.append(indexConcat)
                    #tmp = (lambda idx: self.codecs[idx[0]:idx[1]+1])
                    #concatCodes.extend([self.cutForCoincidence(tmp(indexConcat))])
            cc += 1
        #print(poolConcat)
        ncodecs = self.codecs

        for n in globSpecialChr:
            #print(n,len(ncodecs))
            self.replaceSpacesInSpecialsCaracters(ncodecs,n)
        print('ncodecs:',ncodecs)
        ps = [ x for x in self.getConcatCodes(poolConcat)]
        #print('pps:',ps)
        #print(ncodecs)
        #print(ncodecs)
        nqd = [ n for x,y in poolConcat for n in range(x,y+1)]# obtenemos las posiciones de los caracteres entre []
        # nqd = [ x for x in range(poolConcat[0],poolConcat[1])]
        #psr = [ n for x,y in ]
        for x in nqd:
            ncodecs[x] = ''
            # eliminamos el valor de la lista 
        ncodecs = [ x for x in ncodecs if x != '']
        #print('ne',ncodecs,ps)
        #ncodecs = [ x for x in self.cutForCoincidence(ncodecs) if not((91 in x) or (93 in x))]# cortamos la lista cada espacio)
        #print('eps',ncodecs,ps)
        # y limpiamos de listas con []
        self.RangeReplacePop(ncodecs,ps)
        #ncodecs = [ x for x in ncodecs if x != []]
        ncodecs = [ x for x in self.cutForCoincidence(ncodecs) if not((91 in x) or (93 in x))]# cortamos la lista cada espacio)
        ncodecs = [ x for x in ncodecs if x != []]# filtramos listas vacias
        #print(ncodecs)
        #print(ps)
        mods = []
        flg = False
        #print('ts',ncodecs)
        for idx,x in enumerate(ncodecs):
            idn = 0
            #print(x)
            for n in x:
                #print(m)
                if isinstance(n,list):
                    #print(n)
                    for subidx,m in enumerate(n):
                        con = 0
                        if m[0] == 96:
                            #print(m)
                            ndx = []
                            for index,s in enumerate(m):
                                if s == 96:
                                    con += 1
                                    ndx.append(index)
                            m = [p for p in m if p != 96]# limpiamos la liasta de esos `

                            m.insert(0,(con,))
                            mods.append(m)
                        if m[0] == 123:
                            m = self.insRange(m)
                            n[subidx] = m 
                            #print(n[subidx])
                            mods.append(m)
                            pass
                            #self.cutForCoincidence(m,)
                        if m[0] == 40:
                            
                            print('cuad',m)
                        else:
                            ...
                            print('emme',m)
                            mods.append(m)
                            continue
                else:
                    if idn != id(x):
                        #print(x)
                        if x[0] == 96:
                            con = x.count(96)
                            x = [ s for s in x if s != 96]
                            x.insert(0,(con,))
                        if x[0] == 123:
                            x = self.insRange(x)
                            ncodecs[idx] = x
                        if x[0] == 40:
                            print('cuad222',x)
                        mods.append(x)
                        #print('mos',mods)
                        idn = id(x)
        #print('ncodecs::',ncodecs)
        #print(mods)
        #print('pnc',poolnumConcat)
        #print(ncodecs)
        #self.loadMod(mods,ncodecs)# cargamos los modulos
        #self.lddata.generateCoords.update({'codecs':ncodecs})
        #self.lddata.run()
    def decode(self,ncodecs):
        chain = ''
        #st = '['
        for x in ncodecs:
            for element in x:
                
                if isinstance(element,list):
                    st = '['
                    for qelement in element:
                        
                        for ielement in qelement:
                            st += chr(ielement)
                            ...
                            #print(ielement)
                    st += ']'
                    chain += st
                else:
                    #print()
                    chain += chr(element)
        print(chain)

    def checkData(self,data):
        for x in data:
            if self.kwds.get(x):
                yield x

    def loadMod(self,data:list,ncodecs:list) -> dict:
        '''
        funcion destinada a cargar los modulos
        esta funcion traducira una lista llamada data
        la cual contendra una serie de codigos de caracteres 
        los cuales se traduciran a nombres de modulos a cargar

        que posterior mente se colocaran dentro de un diccionario
        y con este diccionario y otra lista que contendra todos los caracteres
        que indican el formato en el cual se deben de generar los datos
        se usaran como argumento para invocar al generador de datos
        y posterior el generador de datos invocara a el cargador de datos

        '''
        for x in data:
            if x[0] == 'r':
                print('equs',x)
                x.pop(0)# eliminamos el caracter de rango
                self.loadModules.extend([[DEFAULT_DCT.get(self.kwds.get(123)),123,x]])
                continue# usamos continue para saltar por que si no se generaran mas 
            if isinstance(x[0], tuple):
                #print(DEFAULT_DCT.get('names')[x[1] -  1])s
                try:
                    idx = x.pop(0)[0]
                    #st = set(x,idx)
                    self.loadModules.extend([ [DEFAULT_DCT.get(self.kwds.get(n))[idx],idx,list(set(x))[0]] for n in self.checkData(set(x))])
                except:
                    raise NameError('Fuera de rango de archivos conocidos')
                finally:
                    continue

                #[ DEFAULT_DCT.get(self.kwds.get(n))[x[1]] for n in self.checkData(set(x[2]))])
            else:
                # aqui se usara para datos que no esten dentro de un []
                # si hay un 64 el indice 0 osea el primer archivo sera el que se cargara
                self.loadModules.extend([[DEFAULT_DCT.get(self.kwds.get(n)),n] if n != 64 else [DEFAULT_DCT.get(self.kwds.get(n))[0],n] for n in self.checkData(set(x))])
                continue
        self.loadModules = [x for x in self.loadModules if x[0] != None]
        dct = dict()
        
        for x in self.loadModules:
            if isinstance(x,list):
                if len(x) == 2:
                    print(x)
                    dct[x[1]] = x[0]
                else:
                    dct[x[1]] = [x[0],x[-1]]
        #print(data)
        #print('DCT DISTTT', DEFAULT_DCT.get(self.kwds.get(42)))
        self.lddata = Generator(dct,ncodecs)
        #self.lddata = LoadData(list(self.loadModules))
ps = Oasis('``@@@@ [`@@@ ### ****] {144 ~ 42 | 3} ****** ######   [``@@@ *****] [{ 220 ~ 124 | 800}]  ( oppus | cierra ) [( oppus | cierra )]')
# [ [[96,64, 64, 64, 64, 64],[94,94,94,94,94]],[35,35,35,35,35,35,35,35],[[]]]] [`@@@@@ ^^^^^] ######## [@@@@@@ $$$$$$$]
# [12 ~ 2000]
# [[2,64,64],[12,12,12,12]],[44,4,4,4,4,4],[]
#print(DEFAULT_DCT)