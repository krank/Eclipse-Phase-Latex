#encoding:utf8
import libxml2

"""
this script aims to change some stuff in the XML source file.

In the original file, two nodes are important :
- <text> contains one line of text and a font id
- <fontspec> associates fonts sizes and colors to ids

But it's not very convenient. So the id is to remove the <fontspec> nodes and
write down the size and color directly in the <text> nodes.
"""

print "load the file"
doc = libxml2.parseFile('CAT21000_EclipsePhase.xml')

print "extract all the fontspecs"
fontnodes = doc.xpathEval('/pdf2xml/page/fontspec')

specs = {}
for fs in fontnodes:
    i = int(fs.prop('id'))
    s = fs.prop('size')
    c = fs.prop('color')
    specs[i] = (s,c)

print "get all the text nodes"
textnodes = doc.xpathEval('/pdf2xml/page/text')

print "modify each text node"
for t in textnodes:
    i = int(t.prop('font'))
    s,c = specs[i]
    t.unsetProp('font')
    t.setProp('size',s)
    t.setProp('color',c)

### THIS IS CAUSING A SEGFAULT
#print "remove the fontspec nodes"
#for f in fontnodes:
#    f.freeNode()

print "save the result"
doc.saveFile("output.xml")
