#encoding:utf8
import libxml2
from sys import argv
import numpy 

# parse le document
doc = libxml2.parseFile('processed.xml')

def text(page):
    req = '/pdf2xml/page[@number=%d]/text[(@size="22" or @size="16" or @size="12" or @size="7") and (@color="#231f20" or @color="#007c97")]' %(page)
    return doc.xpathEval(req)

def bluenote(page):
    req = '/pdf2xml/page[@number=%d]/text[(@size="16" or @size="7") and @color="#ffffff"]' %(page)
    return doc.xpathEval(req)

def content(nodes):
    return [n.content for n in nodes]

def columns(nodes,number=2):
    if nodes == []: return None
    pos = numpy.bincount([n.prop('left') for n in nodes])
    return numpy.sort(numpy.argsort(pos)[-number:] - 5)

def parsecolumn(nodes,pos):
    text = ""
    for n in nodes:
        size = int(n.prop('size'))
        left = int(n.prop('left'))
        if pos < left < pos+20:
            if  size == 22:
                text += "\n\\section{%s}\n\n" %(n.content.title()) # new section
            elif size == 16:
                text += "\n\\subsection{%s}\n\n" %(n.content.title()) # new subsection
            elif size == 12:
                text += "\n\\subsubsection{%s}\n\n" %(n.content.title()) # new subsubsection
            elif pos+10 < left:
                text += "\n%s\n" %(n.content) # new paragraph
            else:
                text += "%s\n" %(n.content) # new line
    return text

def parsepage(nodes,number=2):
    cols = columns(nodes,number)
    if cols == None:
        return "\n"
    text = ""
    for c in cols:
        text += parsecolumn(nodes,c)
    return text

def chap(start,end,title):
    f = file(title+".tex","w")    
    for p in xrange(start,end):
        print p
        f.write("%%% " + "%03d\n" %(p))
        f.write(parsepage(text(p)))
    f.close()

if __name__ == "__main__":
    chap(20,32,"02 - enter the singularity")
    chap(34,114,"03 - a time of eclipse")
    chap(116,130,"04 - game mechanics")
    chap(132,156,"05 - character creation")
    chap(174,189,"06 - skills")
    chap(190,218,"07 - action and combat")
    chap(220,236,"08 - mind hacks")
    chap(238,268,"09 - the mesh")
    chap(270,294,"10 - accelerated future")
    chap(296,352,"11 - gear")
    chap(354,390,"12 - game information")
    chap(392,396,"13 - tables")
    chap(396,397,"14 - references")
