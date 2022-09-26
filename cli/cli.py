import argparse
from ..core.data import fileTypes
from .Ozis import Oasis
class parser:
    """_summary_
    interfaz de usuario base cli para DGT
    """
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser()
        self.mainParser()
        self.toSqlParser()
        self.configurationsDataBases()
        self.args = self.parser.parse_args()
    def mainParser(self):
        self.parser.add_argument('-r','--rows',help='cantidad de columnas a escribir')
        self.parser.add_argument('-str','--stringChain',help='la cadena de caracteres que se usara para generar los datos')
        self.parser.add_argument('-f','--fileType',help='especificar el tipo de archivo',choices=fileTypes)
        self.parser.add_argument('-o','--output',help='especificar el nombre del archivo de salida')
        self.parser.add_argument('-nb','--noBanner',help='no imprimir el banner')
    def toSqlParser(self):
        self.subparser = self.parser.add_subparsers()
        self.sqlParser = self.subparser.add_parser('sql')
        self.sqlParser.add_argument('-i2str','--intToString',help='convertir numeros enteros a strings',action='store_true')# bandera
        #self.sqlParser.set_defaults(func=lambda e,s,q: print(e))
        #print(self.sqlParser.parse_args())
    def configure(*args):
        print(args)
    def configurationsDataBases(self):
        self.configure = self.subparser.add_parser('configure')
        self.configure.add_argument('-regen','--regenerate',help='regenerar archivo de configuraciones')
        self.configure.add_argument('-del','--delimitator',help='establecer un delimitador de un archivo csv ejemplo "file:delimitator" ')
        self.configure.add_argument('-down','--download_data',help='descargar datos desde un servidor')
        self.configure.add_argument('-form','--format_databases',help='establecer todas las bases de datos con un delimitador especifico')
        self.configure.set_defaults(func=self.configure)
        #self.configure.set_defaults()
    def callModules(self):
        pass
        #cli = Oasis(self.args.stringChain,rows=self.args.rows)
        
if __name__ == '__main__':
    s = parser()