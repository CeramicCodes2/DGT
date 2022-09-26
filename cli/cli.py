import argparse
from ..core.data import fileTypes
from .cli import Oasis
class parser:
    """_summary_
    interfaz de usuario base cli para DGT
    """
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser()
        self.mainParser()
        self.toSqlParser()
        self.args = self.parser.parse_args()
    def mainParser(self):
        self.parser.add_argument('rows',help='cantidad de columnas a escribir')
        self.parser.add_argument('stringChain',help='la cadena de caracteres que se usara para generar los datos')
        self.parser.add_argument('-f','--fileType',help='especificar el tipo de archivo',choices=fileTypes)
        self.parser.add_argument('-o','--output',help='especificar el nombre del archivo de salida')
        self.parser.add_argument('-nb','--noBanner',help='no imprimir el banner')
        
    def toSqlParser(self):
        self.sqlSubParser = self.parser.add_subparsers()
        self.sqlParser = self.sqlSubParser.add_parser('sql')
        self.sqlParser.add_argument('-i2str','--intToString',help='convertir numeros enteros a strings',action='store_true')# bandera
        #self.sqlParser.set_defaults(func=lambda e,s,q: print(e))
        #print(self.sqlParser.parse_args())
    def callModules(self):
        cli = Oasis(self.args.stringChain,rows=self.args.rows)
        
if __name__ == '__main__':
    s = parser()