import argparse
from ..core.data import fileTypes
from .Ozis import Oasis
from colorama import Fore
class parser:
    '''_summary_
    interfaz de usuario base cli para DGT
    '''
    def __init__(self) -> None:
        self.__default_subparsers = ['conf','sql']
        self.parser = argparse.ArgumentParser()
        self.mainParser()
        self.subparser = self.parser.add_subparsers()
        self.toSqlParser()
        self.configurationsDataBases()
        self.args = self.parser.parse_args()
        self.processParser()
        #self.args.func(self.args)
        #print(self.args)
        #self.args.conf(self.args)
    def callSubparsers(self,dct_args:dict):
        for x in dct_args:
            if x in self.__default_subparsers:
                dct_args[x](self.args)#mandamos a llamar
    def processParser(self):
        '''
        para procesar los argumentos parseados primero que nada vamos a
        mandar a llamar a los subparsers si hay alguno para ello se tendra
        una lista de los default subparsers
        '''
        dct_args = vars(self.args)
        self.callSubparsers(dct_args)
        call_Ozis = dict()# en este diccionario colocaremos todos los parametros
        # comprobaremos ahora los argumentos de mainParser
        # obviamos argumentos posicionales por que es seguro que deben estar para este punto
        
        call_Ozis.update('')
        for x in dct_args.keys():
            match x:
                case 'fileType':
                    ...
                case 'output':
                    ...
                case 'noBanner':
                    ...
                    
                
        
    def mainParser(self):
        self.parser.add_argument('rows',help='cantidad de columnas a escribir',type=int)
        self.parser.add_argument('stringChain',help='la cadena de caracteres que se usara para generar los datos')
        self.parser.add_argument('-f','--fileType',help='especificar el tipo de archivo',choices=fileTypes)
        self.parser.add_argument('-o','--output',help='especificar el nombre del archivo de salida')
        self.parser.add_argument('-nb','--noBanner',help='no imprimir el banner')
    def toSqlParser(self):
        self.sqlParser = self.subparser.add_parser('sql')
        self.sqlParser.add_argument('-i2str','--intToString',help='convertir numeros enteros a strings',action='store_true')# bandera
        self.sqlParser.set_defaults(sql=parser.sql)
    @classmethod
    def sql(*args): pass
    @classmethod
    def configure(*args):
        '''
        debemos definir los subcomandos que se ejecutaran como metodos estaticos
        o de clase ya que argparse no reconoce como metodos de contexto dinamico

        '''
        print('the args: ',args)
    def configurationsDataBases(self):
        self.subparser.dest='configure'
        self.configure = self.subparser.add_parser('configure')
        self.configure.add_argument('-regen','--regenerate',help='regenerar archivo de configuraciones',action='store_true')
        self.configure.add_argument('-del','--delimitator',help='establecer un delimitador de un archivo csv ejemplo "file:\'delimitator\'" ')
        self.configure.add_argument('-down','--download_data',help='descargar datos desde un servidor')
        self.configure.add_argument('-form','--format_databases',help='establecer todas las bases de datos con un delimitador especifico')
        self.configure.set_defaults(conf=parser.configure)
        #print(dir(self.configure))
        #self.configure.set_defaults()
    def callModules(self):
        self.banner = open('banner.txt','r')
        print(f'{Fore.GREEN}' + self.banner.read())
        ...
        #cli = Oasis(self.args.stringChain,rows=self.args.rows)

        
if __name__ == '__main__':
    s = parser()