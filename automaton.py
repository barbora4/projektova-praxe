"""Class Automaton, loading from .ba files and writing to them."""

import re
import csv
from dataclasses import dataclass

@dataclass
class Automaton:
    """Data class representing an automaton."""

    states: set
    alphabet: set
    transitions: set
    start: set
    accept: set

def load_data(file):
    """Loads data from .ba file to object Automaton"""

    start=set()         # start states
    transitions=set()   # transitions: [input, start, end]
    accept=set()        # accept states
    alphabet=set()      # set of all input symbols
    states=set()        # set of all states

    beginning=True      
    
    for line in file:
        # start states
        if re.search(r"^\[(.)+\]\n$", line) and beginning:
            start.add(line[1:-2])
            states.add(line[1:-2])

        else:
            match=re.search(r"^((.)+),\[((.)+)\]->\[((.)+)\]\n$", line)
            # transitions
            if match:
                beginning=False
                transitions.add((match.group(3), match.group(1), match.group(5)))
                alphabet.add(match.group(1))
                states.add(match.group(3))
                states.add(match.group(5))
        
            # accept states
            elif re.search(r"^\[(.)+\]\n$", line) and not beginning:
                accept.add(line[1:-2])
                states.add(line[1:-2])

            # wrong file format
            else:
                raise FormatError("Wrong format!")

    return Automaton(states,alphabet,transitions,start,accept)


def write_to_file(a,f):
    with open(f, "w") as f:
        for i in a.start:
            print('[%s]'%','.join(map(str, i)), file=f)
        for i in a.transitions:
            t1='[%s]'%','.join(map(str, i[0]))
            t2='[%s]'%','.join(map(str, i[2]))
            inp='%s'%','.join(map(str, i[1]))
            print("{},{}->{}".format(inp,t1,t2), file=f)
        for i in a.accept:
            print('[%s]'%','.join(map(str, i)), file=f)

