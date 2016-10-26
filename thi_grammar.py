#!/usr/bin/python
import io
import re


class Grammar:
    v, t, p, s, productions = [], [], [], [], {}

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
            matches = re.search("([^->]{1}) -> (.*)", production)
            if len(matches.groups()) == 2:
                self.productions[matches.group(1)] = matches.group(2).split("|")
            else:
                raise Exception("Invalid production found!")

    def __init__(self, file, max_len):
        self.max_len = max_len
        self.v, self.t, self.p, self.s = Grammar.parse_file(Grammar.read_file(file))
        self.parse_productions()
        self.words = self.remove_variables(self.gen_words("S"))

    def remove_variables(self, words):
        temp = []
        for word in words:
            for var in self.v:
                if var in word:
                    temp.append(word)
        for w in temp:
            words.remove(w)
        return words

    def gen_words(self, start):
        retval = []
        if len(start) <= self.max_len:
            for char in start:
                if char in self.v:
                    for prod in self.productions[char]:
                        retval.append(start.replace(char, prod))
                        retval.extend(self.gen_words(retval[-1]))
        return retval

if __name__ == "__main__":
    options = {
        "max_len": 4,
        "file": "grammar.txt"
    }
    print("[Program started!]")

    try:
        g = Grammar(file=options["file"], max_len=options["max_len"])
        words = g.words
        for w in words:
            print(w)

    except Exception as e:
        print("[Error: {}]".format(str(e)))
    except:
        raise
