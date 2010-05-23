from sys import argv
import aspell
import string

dic = aspell.Speller("lang","en")

def hyphen(word1,word2):
    word1 = word1.strip(string.punctuation)
    word2 = word2.strip(string.punctuation)
    nodash = word1 + word2
    dash = word1 + "-" + word2
    check_nodash = dic.check(nodash)
    check_dash = dic.check(dash)
    if (check_nodash,check_dash) == (1,0): # is hyphen
        return nodash
    if (check_nodash,check_dash) == (0,1): # is dash
        return dash
    # don't know
    prompt = nodash + " () / " + dash + " (-): "
    c = raw_input(prompt)
    if c == "":
        try: dic.addtoSession(nodash)
        except Exception: pass
        return nodash
    else:
        return dash

def cleanHyphen(filename):
    f = file(filename)
    lines = f.readlines()
    f.close()
    for i in xrange(len(lines)):
        st = lines[i].strip()
        if len(st) > 0 and st[-1] == "-" and len(lines) > i+1:
            l_cur = lines[i].strip().split()
            l_next = lines[i+1].strip().split()
            if len(l_next) > 0:
                word1 = l_cur[-1]
                word2 = l_next[0]
                word = hyphen(word1,word2)
                print word
                lines[i] = string.join(l_cur[:-1] + [word]," ") + "\n"
                lines[i+1] = string.join(l_next[1:]," ") + "\n"
    f = file(filename,'w')
    f.writelines(lines)
    f.close()

if __name__ == "__main__":
    files = argv[1:]
    for f in files:
        print f
        cleanHyphen(f)

"""
xenoarcheologists
ther-moregulation
"""
    
