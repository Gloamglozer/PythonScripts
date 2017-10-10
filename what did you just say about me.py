# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 19:10:51 2016

@author: Eric
"""
biglist = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q"]
log = open('log.txt','r')
butt = log.read()
log.close()
log = open('log.txt','a')
print(butt.split())
bookmark = len(butt.split())
for i in range(bookmark , bookmark+3):
    log.write(" {}".format(biglist[i]))
log.close()