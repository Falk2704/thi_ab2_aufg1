#!/usr/bin/python
import io, re

from coloredoutput import fcolors, print_colorized


class Grammar:
    v, t, p, s, productions, words = [], [], [], [], {}, []

    @staticmethod
    def read_file(fname):
        try:
            with io.open(fname, encoding="utf-8") as f:
                lines = [x.replace("\n", "") for x in f.readlines()]
            return lines
        except:
            raise Exception("Unable to load file!")

    @staticmethod
    def parse_file(lines):
        v, t, p, s = [], [], [], []
        for line in lines:
            vname, data = Grammar.parse_line(line)
            if vname == "V":
                v = Grammar.parse_data(data)
            elif vname == "T":
                t = Grammar.parse_data(data)
            elif vname == "P":
                p = Grammar.parse_data(data)
            elif vname == "S":
                s = Grammar.parse_data(data)
        return v, t, p, s

    @staticmethod
    def parse_line(line):
        matches = re.match("(.*) = {(.*)}", line)
        if matches is None:
            raise Exception("Invalid grammar file!")
        return matches.group(1), matches.group(2)

    @staticmethod
    def parse_data(var):
        return [x.strip() for x in var.split(",")]

    def parse_productions(self):
        for production in self.p:
            current = []
            matches = re.search("([^->]{1}) -> (.*)", production)
            if len(matches.groups()) == 2:
                self.productions[matches.group(1)] = matches.group(2).split("|")
            else:
                raise Exception("Invalid production found!")

    def __init__(self, file, depth):
        self.depth = depth
        self.v, self.t, self.p, self.s = Grammar.parse_file(Grammar.read_file(file))
        self.parse_productions()
        #erg = self.produce_words("S", 0)
        erg = self.gen_words("S")
        erg = [x.replace("D", "") for x in erg]
        erg = [int(x) for x in erg]
        print_colorized(sorted(erg), fcolors.OKGREEN)


    def gen_words(self, start):
        retval = []
        if len(start) <= 4:
            for char in start:  # Durchlaufe jedes Zeichen
                if char in self.v:  # Wenn Zeichen = Variable dann
                    for prod in self.productions[char]:  # Erstelle instanzen für alle möglichkeiten
                            retval.append(start.replace(char, prod))
                            retval = retval + self.gen_words(retval[-1])

        return retval

    def produce_words(self, start, counter):
        retval = []
        for zeichen in start:
            if zeichen in self.v:
                for rechteseite in self.productions[zeichen]:
                    s = start.replace(zeichen, rechteseite)
                    retval.append(s)
                    if(counter < 5):
                        counter += 1
                        retval = retval + self.produce_words(s, counter)
                    else:
                        break
        return retval

if __name__ == "__main__":
    options = {
        "depth": 4,
        "file": "grammar.txt"
    }
    print_colorized("[Program started!]", fcolors.OKGREEN)

    try:
        g = Grammar(file=options["file"], depth=options["depth"])
    except Exception as e:
        raise
        #print_colorized("[Error: {}]".format(str(e)), fcolors.FAIL)
    except:
        raise
