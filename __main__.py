#/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import re
import sys
import warnings
import fileinput
import getopt

try:
    xrange
except NameError:
    xrange = range

def GetUUID():
    UU = uuid.uuid1().__str__();
    UU = re.sub(r"\-", "_", UU)
    return UU

def GetG(matchobj):
    return g[matchobj.group(1)]

def TidyLine(Line):
    Line = re.sub(r"(\S)([ \t]+)($)", r"\1\3", Line, 1)
    Line = re.sub(r"(%s)[ \t]+([%s%s])" % (chr(0x0a), chr(0x0d), chr(0x0a)), r"\1\2", Line)

    return TidyLineNoStripRight(Line)


def SpecialHandlingForSignAtLineBeginning(m):
    if m.group(1) == "":
        return "%s " % m.group(2)
    else:
        return " %s " % m.group(2)
    pass


class Namespace1:
    pass

def TidyLineNoStripRight(Line):
    k1     = Namespace1()
    k1.key = {}
    def ProtectKeyword(m):
        uid         = GetUUID()
        k1.key[uid] = m.group(1)
        return uid
    def UnProtectKeyword(m):
        return k1.key[m.group(1)]

    Line = re.sub(r"^[\t ]+?(\S)", r"\1", Line, 1)
    Line = re.sub(r",[\t ]*", r", ", Line)
    Line = re.sub(r",[\t ]*(%s?%s)" % (chr(0x0d), chr(0x0a)), r",\1", Line)
    for k in Protect.keys():
        Line = re.sub(r"[\t ]*%s[\t ]*" % k, " %s " % Protect[k], Line)
        pass
    for x in["=", "+", "-", "*", "/", "%", "<", ">", ":"]:
        if x == ":":
            if re.search(r":[ \t]*[%s%s]" % (chr(0x0d), chr(0x0a)), Line):
                continue
        k     = re.escape(x)
        Line1 = re.sub(r"(%s)(%s)[\t ]*" % (chr(0x0a), k), r"\1\2 ", Line)
        if Line1 != Line:
            Line = Line1
            continue
        Line = re.sub(r"([\t ]*)(%s)[\t ]*" % (k), r" \2 ", Line)

    for k in RProtect.keys():
        Line = re.sub(r"%s" % k, RProtect[k], Line)
        pass

    k = r"\b(and|del|from|not|while|as|elif|global|or|with|assert|else|if|pass|yield|break|except|import|print|class|exec|in|raise|continue|finally|is|return|def|for|lambda|try)\b"
    #for k in ["and", "del", "from", "not", "while", "as", "elif", "global", "or", "with", "assert", "else", "if", "pass", "yield", "break", "except", "import", "print", "class", "exec", "in", "raise", "continue", "finally", "is", "return", "def", "for", "lambda", "try"]:
    Line = re.sub(r"(%s[\t ]*%s)" % (chr(0x0a), k), ProtectKeyword, Line)


    #Line = re.sub(r"%s" % k, r" \1 ", Line)
    Line = re.sub(r"[\t ]*%s" % k, r" \1", Line)
    #Line = re.sub(r"^%s$" % k, r" \1 ", Line)

    for x in k1.key.keys():
        Line = re.sub(r"(%s)" % x, UnProtectKeyword, Line, 1)
    k1.key.clear()

    Line = re.sub(r"%s[\t ]*([^:])" % (k), r"\1 \2", Line)
    Line = re.sub(r"%s[\t ]*([%s%s])" % (k, chr(0x0d), chr(0x0a)), r"\1\2", Line)

    return Line

def CloseChar(c):
    if c == "(":
        return ")"
    if c == "[":
        return "]"
    if c == "{":
        return "}"

def DoPreParse(ExitChar, LeftSpace):
    global Text
    global Pos
    global NewLine
    Line  = ""
    LfPos = 0
    while(Pos + 1 < len(Text)):
        Pos  = Pos + 1
        Char = Text[Pos]
        if Char == chr(0x0a):
            LfPos = Pos
        if re.match(r"\{", Char):
            gg    = GetUUID()
            Line  = Line + "$%s$" % gg
            g[gg] = Char + DoPreParse("}", Pos - LfPos)
        elif re.match(r"\}", Char):
            if ExitChar == Char:
                Line = Line + Char
                if re.search(r":", Line):
                    Line  = re.sub(r"[%s%s]" % (chr(0x0a), chr(0x0d)), "", Line)
                    Lines = []
                    Lines = re.findall(r"[^,]+,?", Line)
                    if Lines == []:
                        Lines = [Line]
                    Lines.insert(0, "")
                    for i in xrange(len(Lines)):
                        Lines[i] = re.sub(r"^[ \t]*", " " * LeftSpace, Lines[i])
                    Lines[0] = re.sub("[ \t]*", "", Lines[0])
                    #TODO: Fix Line ending
                    Line = NewLine.join(Lines)
                Line = re.sub(RUUID, GetG, Line)
                return Line
        elif(re.match(r"['\"]", Char)):
            ReminingText = Text[Pos : len(Text)]
            if re.match(r"^%s%s%s" % (Char, Char, Char), ReminingText):
                Char = "%s%s%s" % (Char, Char, Char)
            regex = r"^(%s%s|%s.*?[^\\\\]%s)" % (Char, Char, Char, Char)
            m     = re.search(re.compile(regex, re.DOTALL), ReminingText)
            if m:
                Pos  = Pos + len(m.group(1)) - 1
                Line = Line + m.group(1)
        elif(re.match(r"#", Char)):
            ReminingText = Text[Pos : len(Text)]
            m            = re.search(re.compile(r"^(#.*$)", re.MULTILINE), ReminingText)
            if m:
                Pos  = Pos + len(m.group(1)) - 1
                Line = Line + m.group(1)
        elif(re.match(r"([^#\(\)\[\]\{\}\"'])", Char)):
            ReminingText = Text[Pos : len(Text)]
            m            = re.search(r"^([^#\(\)\[\]\{\}\"']+)", ReminingText)
            if m:
                Tmp = m.group(1)
                mm  = re.search(re.compile(r"(.*%s)[^%s]*$" % (chr(0x0a), chr(0x0a)), re.DOTALL), Tmp)
                if mm:
                    LfPos = Pos + len(mm.group(1)) - 2
                Pos  = Pos + len(m.group(1)) - 1
                Line = Line + Tmp
        else:
            Line = Line + Char
    return Line

class Namespace:
    pass
def DoParse(ExitChar):
    global Text
    global Pos
    ns        = Namespace()
    Line      = ""
    Line2     = ""
    DirtyLine = ""
    ns.Buff   = []
    ns.Tab    = - 1
    def MoreTidyLine(LL, Flush):
        uid      = GetUUID()
        SubLines = re.findall(r"[^%s]*%s?" % (chr(0x0a), chr(0x0a)), LL)
        if SubLines == []:
            SubLines = [LL]
        x = ""
        for i in SubLines:
            m = re.search(r"^( *)", i)
            t = len(m.group(1))
            if ns.Tab != t:
                Max    = 0
                Buff2  = []
                ns.Tab = t
                Sign   = ""
                while len(ns.Buff) > 0:
                    S = []
                    S = ns.Buff.pop(0)
                    if len(S) >= 2 and re.match(r"[:=]", S[1]) and(Sign == "" or Sign == S[1]):
                        Sign = S[1]
                        Buff2.append(S)
                        Max = Max if Max > len(S[0]) else len(S[0])
                        continue
                    while len(Buff2) > 0:
                        S2 = []
                        S2 = Buff2.pop(0)
                        H  = S2.pop(0)
                        L  = "%-*s" % (Max, H) + "".join(S2)
                        x  = x + L
                    Sign = ""
                    Max  = 0
                    L    = "".join(S)
                    x    = x + L
                while len(Buff2) > 0:
                    S2 = []
                    S2 = Buff2.pop(0)
                    H  = S2.pop(0)
                    L  = "%-*s" % (Max, H) + "".join(S2)
                    x  = x + L
            for k in Protect.keys():
                i = re.sub(r"[\t ]*%s[\t ]*" % k, " %s " % Protect[k], i)
                #i = re.sub(r"%s" % k, Protect[k], i)
            Z = []
            Z = re.split(r"([:=])", i)
            for i in xrange(len(Z)):
                Z[i] = re.sub(RUUID, GetG, Z[i])
            for m in Z:
                for k in RProtect.keys():
                    m = re.sub(r"%s" % k, RProtect[k], m)
            ns.Buff.append(Z)
        if Flush:
            Max   = 0
            Buff2 = []
            Sign  = ""
            while len(ns.Buff) > 0:
                S = []
                S = ns.Buff.pop(0)
                if len(S) >= 2 and re.match(r"[:=]", S[1]) and(Sign == "" or Sign == S[1]):
                    Sign = S[1]
                    Buff2.append(S)
                    Max = Max if Max > len(S[0]) else len(S[0])
                    continue
                while len(Buff2) > 0:
                    S2 = []
                    S2 = Buff2.pop(0)
                    H  = S2.pop(0)
                    L  = "%-*s" % (Max, H) + "".join(S2)
                    x  = x + L
                Sign = ""
                Max  = 0
                L    = "".join(S)
                x    = x + L
            while len(Buff2) > 0:
                S2 = []
                S2 = Buff2.pop(0)
                H  = S2.pop(0)
                L  = "%-*s" % (Max, H) + "".join(S2)
                x  = x + L
        return x
    while(Pos + 1 < len(Text)):
        Pos  = Pos + 1
        Char = Text[Pos]
        if re.match(r"[\{\[\(]", Char):
            Line      = Line + TidyLine(DirtyLine)
            DirtyLine = ""
            gg        = GetUUID()
            Line      = Line + "$%s$" % gg
            g[gg]     = Char
            Tmp       = DoParse(CloseChar(Char))
            g[gg]     = g[gg] + Tmp
        elif(re.match(r"[\}\]\)]", Char)):
            Line      = Line + TidyLine(DirtyLine)
            DirtyLine = ""
            Line      = Line + Char
            Line2     = Line2 + MoreTidyLine(Line , 1)
            return Line2
        elif(re.match(r"['\"]", Char)):
            ReminingText = Text[Pos : len(Text)]
            if re.match(r"^%s%s%s" % (Char, Char, Char), ReminingText):
                Char = "%s%s%s" % (Char, Char, Char)
            regex = r"^(%s%s|%s.*?[^\\\\]%s)" % (Char, Char, Char, Char)
            m     = re.search(re.compile(regex, re.DOTALL), ReminingText)
            if m:
                Pos       = Pos + len(m.group(1)) - 1
                Line      = Line + TidyLine(DirtyLine)
                DirtyLine = ""
                if re.search(r"[^\(\)\[\]'\"ru \$\t]$", Line):
                    RChar = Line[ - 1]
                    if RChar != chr(0x0d) and RChar != chr(0x0a):
                        Line = Line + " "
                gg    = GetUUID()
                Line  = Line + "$%s$" % gg
                g[gg] = ""
                g[gg] = g[gg] + m.group(1)
        elif(re.match(r"#", Char)):
            ReminingText = Text[Pos : len(Text)]
            m            = re.search(re.compile(r"^(#.*$)", re.MULTILINE), ReminingText)
            if m:
                Pos       = Pos + len(m.group(1)) - 1
                Line      = Line + TidyLineNoStripRight(DirtyLine)
                DirtyLine = ""
                gg        = GetUUID()
                Line      = Line + "$%s$" % gg
                g[gg]     = ""
                g[gg]     = g[gg] + m.group(1)
        elif(re.match(r"([^#\(\)\[\]\{\}\"'])", Char)):
            ReminingText = Text[Pos : len(Text)]
            m            = re.search(r"^([^#\(\)\[\]\{\}\"']+)", ReminingText)
            if m:
                Pos       = Pos + len(m.group(1)) - 1
                DirtyLine = DirtyLine + m.group(1)
        else:
            DirtyLine = DirtyLine + Char
    Line  = Line + TidyLine(DirtyLine)
    Line2 = Line2 + MoreTidyLine(Line, 1)
    return Line2

if __name__ == "__main__":

    warnings.simplefilter('always')
    warn = warnings.warn

    global Tabsize
    global Text
    global Pos
    global RUUID
    global NewLine

    Tabsize = 4
    try:
        opts, args = getopt.getopt(sys.argv[1 : ], "ht:")
    except getopt.GetoptError:
        sys.stdout.write('python -m pythontidy2 [-t expandtabsize] ')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            sys.stdout.write('python -m pythontidy2 [-t expandtabsize] ')
            sys.exit()
        elif opt in("-t"):
            Tabsize = int(arg)

    if sys.platform == "win32":
        import os, msvcrt
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)


    Protect  = {}
    RProtect = {}
    g        = {}
    for x in["==", "<=", ">=", "+=", "-=", "*=", "/=", "%=", "->", "!=", "**"]:
        RProtect[GetUUID()] = x
    for x in RProtect.keys():
        Protect[re.escape(RProtect[x])] = x




    RUUID = r"\$(\w{8}_\w{4}_\w{4}_\w{4}_\w{12})\$"
    #with open(argv[1], 'r') as f:
    #    Text = f.read()
    #f.closed
    Text = chr(0x0a)
    for L in fileinput.input(args, mode = 'rb'):
        Text = Text + L.decode("utf-8")
    Text    = Text.expandtabs(Tabsize)
    NewLine = "%s" % chr(0x0a)
    if re.search(r"%s%s" % (chr(0x0d), chr(0x0a)), Text):
        NewLine = "%s%s" % (chr(0x0d), chr(0x0a))
    while(True):
        g    = {}
        Pos  = - 1
        Text = DoPreParse("", 0)
        Text = re.sub(RUUID, GetG, Text)
        g    = {}
        Pos  = - 1
        Text = DoParse('')
        for k in RProtect.keys():
            Text = re.sub(r"%s" % k, RProtect[k], Text)
        Text1 = Text
        g     = {}
        Pos   = - 1
        Text  = DoPreParse("", 0)
        Text  = re.sub(RUUID, GetG, Text)
        if Text == Text1:
            break
    Text = Text[1 : ]
    sys.stdout.write(Text)
