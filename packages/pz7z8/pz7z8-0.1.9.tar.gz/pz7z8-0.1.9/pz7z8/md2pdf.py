#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#把md用pandoc转成pdf

import os,sys,re,difflib,pathlib

def filemtime(wj):
    if not os.path.isfile(wj):
        return 0
    return os.stat(wj).st_mtime

def pandoc(md):
    pdf=md[:-3]+".pdf"
    if filemtime(md)>filemtime(pdf):
        配置文件=pathlib.Path.joinpath(pathlib.Path(__file__).parent,"datafile","md2pdf.yaml")
        cmd="pandoc -s --pdf-engine=xelatex -o %s %s %s" %(pdf,配置文件,md)
        print(cmd)
        os.system(cmd)

def main():
    for i in range(1,len(sys.argv)):
        pandoc(sys.argv[i])

if __name__ == "__main__":
    main()
