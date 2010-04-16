#!/usr/bin/python

from sys import argv

debut  = int(argv[1])
fin    = int(argv[2])
sortie = open(argv[3],'w')

for i in xrange(debut,fin+1):
    a = "%03d.txt" %(i)
    b = "%03d_full.txt" %(i)
    fa = open(a,'r')
    fb = open(b,'r')
    ca = fa.readlines()
    cb = fb.readlines()
    fa.close()
    fb.close()
    print ""
    print "==========================================================="
    print ""
    for line in ca:
        print line,
    i = raw_input("?")
    if i == "":
        sortie.write("%%% " + a + " %%%\n")
        sortie.writelines(ca)
    else:
        sortie.write("%%% " + a + " %%%\n")
        sortie.writelines(cb)

sortie.close()
