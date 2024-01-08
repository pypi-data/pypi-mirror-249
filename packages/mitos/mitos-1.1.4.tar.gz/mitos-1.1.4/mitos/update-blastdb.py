'''
@author: M. Bernt

Generate the files needed for blasting
'''

import argparse

from mitos.update import prepareFiles

usage = "generate blast data bases from the genbank files in a directory"

parser = argparse.ArgumentParser(description=usage)

parser.add_argument("--dir", action="store", required=True, metavar="DIR", help="output directory")
args = parser.parse_args()

prepareFiles(args.dir)
