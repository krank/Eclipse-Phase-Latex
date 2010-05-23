#encoding:utf8
import libxml2
import numpy
import scipy.cluster.vq

print 'load the file'
doc = libxml2.parseFile('CAT21000_EclipsePhase.xml')

print 'extract all the fontspecs'
fontnodes = doc.xpathEval('/pdf2xml/page/fontspec')

specs = {}
for fs in fontnodes:
    i = int(fs.prop('id'))
    s = fs.prop('size')
    c = fs.prop('color')
    specs[i] = (s,c)

print 'get all the text nodes'
textnodes = doc.xpathEval('/pdf2xml/page/text')

print 'modify each text node'
for t in textnodes:
    i = int(t.prop('font'))
    s,c = specs[i]
    t.unsetProp('font')
    t.setProp('size',s)
    t.setProp('color',c)

print 'remove the fontspec nodes'
for f in fontnodes:
    f.unlinkNode()
    f.freeNode()

print 'replace all <i> by textit'
for n in doc.xpathEval('//i'):
    content = '\\textit{%s}' %(n.content)
    new = libxml2.newText(content)
    n.replaceNode(new)
    n.freeNode()

print 'replace all <b> by textbf'
for n in doc.xpathEval('//b'):
    content = '\\textbf{%s}' %(n.content)
    new = libxml2.newText(content)
    n.replaceNode(new)
    n.freeNode()

### parsing pages

def gettext(page):
    """get a page node, return a list of text nodes from this page"""
    req ='./text[ (@size="22" and (@color="#231f20" or @color="#007c97" or @color="#b01016")) or (@color="#231f20" and (@size="16" or @size="12" or @size="7"))]'
    return  page.xpathEval(req)

def display(text):
    for t in text: print t.content

def cluster(text):
    """get a list of text nodes, sort out the columns"""
    obs = numpy.array([int(t.prop('left')) for t in text])
    if obs.var() < 200:
        nb = 1
    else:
        nb = 2
    code_book,_ = scipy.cluster.vq.kmeans(obs,nb)
    code_book.sort()
    grouping,_ = scipy.cluster.vq.vq(obs,code_book)
    cols = dict([(k,[]) for k in code_book])
    for i in xrange(len(text)):
        c = code_book[grouping[i]]
        cols[c].append(text[i])
    return cols

def cleantext(text):
    text = text.replace(u"ﬁ ", "fi")
    text = text.replace(u"fl ", "fl")
    text = text.replace(u"…", "...")
    text = text.replace(u"’", "'")
    text = text.replace(u"“","``")
    text = text.replace(u"”","''")
    return text

def parsecolumn(position,column):
    text = ""
    for n in column:
        size = int(n.prop('size'))
        left = int(n.prop('left'))
        content = cleantext(n.content)
        if  size == 22:
            text += "\n\\section{%s}\n\n" %(content.title()) # new section
        elif size == 16:
            text += "\n\\subsection{%s}\n\n" %(content.title()) # new subsection
        elif size == 12:
            text += "\n\\subsubsection{%s}\n\n" %(content.title()) # new subsubsection
        elif left > position+5:
            text += "\n%s\n" %(content) # new paragraph
        else:
            text += "%s\n" %(content) # new line
    return text
    
def parsepage(page):
    pagenumber = int(page.prop('number'))
    print "page=%03d" %(pagenumber)
    text = gettext(page)
    ret = "%%% " + "%03d\n" %(pagenumber)
    if len(text) != 0:
        cols = cluster(text)
        keys = cols.keys()
        keys.sort()
        for pos in keys:
            ret += parsecolumn(pos,cols[pos])
    return ret

def chapter(pages,title):
    f = file(title+".tex","w")    
    for p in pages:
        f.write(parsepage(p))
    f.close()

pages = doc.xpathEval('/pdf2xml/page')

chapter(pages[17:31],"02 - enter the singularity")
chapter(pages[31:113],"03 - a time of eclipse")
chapter(pages[113:129],"04 - game mechanics")
chapter(pages[129:155],"05 - character creation")
chapter(pages[171:188],"06 - skills")
chapter(pages[188:217],"07 - action and combat")
chapter(pages[217:235],"08 - mind hacks")
chapter(pages[235:267],"09 - the mesh")
chapter(pages[267:295],"10 - accelerated future")
chapter(pages[295:351],"11 - gear")
chapter(pages[351:391],"12 - game information")
chapter(pages[391:395],"13 - tables")
chapter(pages[396:400],"14 - references")
