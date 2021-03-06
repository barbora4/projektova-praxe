###################################################################
# Barbora Šmahlíková
# 2020/2021
# Construction of atomic Buchi automata and operations over them.
###################################################################

from copy import copy
from itertools import product
from automaton import Automaton
from optimize import *

def get_all_variables(a):
    """Returns set of all used variables of automaton a."""
    
    alphabet=set()
    for i in a.alphabet:
        for j in set(i.split('|')):
            alphabet.add(j.split(':')[0])

    return alphabet

def add_to_transitions(a1,alphabet1,alphabet2):
    """Adds variables to transitions of a1."""

    old_alphabet=copy(a1.alphabet)
    change=False
    for a in alphabet2:
        if a not in alphabet1:
            change=True
            # add to alphabet
            alphabet1.add(a)
            for b in copy(old_alphabet):
                old_alphabet.add("{}|{}:0".format(b,a))
                old_alphabet.add("{}|{}:1".format(b,a))
                old_alphabet.remove(b)
            # add to all transitions
            for i in range(len(copy(a1.transitions))):
                if a1.transitions[i][1] != "":
                    a1.transitions.append([a1.transitions[i][0], "{}|{}".format(a1.transitions[i][1],"{}:{}".format(a,'1')), a1.transitions[i][2]])
                    a1.transitions[i][1]="{}|{}".format(a1.transitions[i][1],"{}:{}".format(a,'0'))
                else:
                    a1.transitions.append([a1.transitions[i][0], "{}".format("{}:{}".format(a, '1')), a1.transitions[i][2]])
                    a1.transitions[i][1]="{}".format("{}:{}".format(a, '0'))
    
    a1.alphabet=copy(old_alphabet)

def alphabetical_order(a):
    """Sorts input variables in transitions alphabetically."""

    for i in range(len(a.transitions)):
        t=list(a.transitions[i][1].split('|'))
        t.sort()
        first=True
        for j in t:
            if first:
                a.transitions[i][1]=j
                first=False
            else:
                a.transitions[i][1]="{}|{}".format(a.transitions[i][1], j)

    new_alphabet=set()
    for i in a.alphabet:
        t=list(i.split('|'))
        t.sort()
        first=True
        for j in t:
            if first:
                i=j
                first=False
            else:
                i="{}|{}".format(i,j)
        new_alphabet.add(i)
    a.alphabet=copy(new_alphabet)


def cylindrification(a1,a2):
    """Adds variables that are only in one automaton to the second one and sorts input variables alphabetically."""

    alphabet1=get_all_variables(a1)
    alphabet2=get_all_variables(a2)

    add_to_transitions(a1,alphabet1,alphabet2)
    add_to_transitions(a2,alphabet2,alphabet1)

    alphabetical_order(a1)
    alphabetical_order(a2)


def true():
    """Returns automaton for true formula."""

    return Automaton(set("0"), set(), [["0", "", "0"]], set("0"), set("0"))

def false():
    """Returns automaton for false formula."""

    return Automaton(set("0"), set(), list(), set("0"), set())

def exists(X,a):
    """Projection: eliminates X from the input alphabet and transitions of automaton a."""

    # remove X from the input alphabet
    alphabet=list(copy(a.alphabet))
    for i in range(len(alphabet)):
        t=list(alphabet[i].split('|'))
        for j in t:
            if X in j:
                t.remove(j)
        first=True
        alphabet[i] = ''
        for j in t:
            if first:
                alphabet[i]=j
                first=False
            else:
                alphabet[i]="{}|{}".format(alphabet[i],j)
    alphabet=set(alphabet)
    if '' in alphabet:
        alphabet.remove('')

    # remove X from all transitions
    transitions=copy(a.transitions)
    for i in transitions:
        t=list(i[1].split('|'))
        for j in t:
            if X in j:
                t.remove(j)
        first=True
        for j in t:
            if first:
                i[1]=j
                first=False
            else:
                i[1]="{}|{}".format(i[1],j)
        if first:
            i[1]=""

    # remove duplicate transitions
    tran=list()
    for t in transitions:
        if t not in tran:
            tran.append(t)

    b=Automaton(a.states,alphabet,tran,a.start,a.accept)
    
    # empty alphabet
    if len(alphabet)==0:
        # true if it contains at least one accept state, otherwise false
        if len(a.accept)>0:
            return true()
        else:
            return false()

    optimize(b)
    return b


def sub(X,Y):
    """Constructs atomic automaton for formula: X is a subset of Y."""

    start={"0"}
    accept=copy(start)
    states=start|accept
   
    alphabet_X={"{}:0".format(X), "{}:1".format(X)}
    alphabet_Y={"{}:0".format(Y), "{}:1".format(Y)}
    alphabet=set()
    for a in alphabet_X:
        for b in alphabet_Y:
            alphabet.add("{}|{}".format(a,b))

    transitions=list()
    for s in start:
        # if an element is in X, it must be also in Y
        transitions.append([s,"{}:0|{}:?".format(X,Y),s])
        transitions.append([s,"{}:1|{}:1".format(X,Y),s])

    a = Automaton(states,alphabet,transitions,start,accept)
    alphabetical_order(a)

    return a

def succ(Y,X):
    """Constructs atomic automaton for formula: Y is a successor of X."""

    start={"0"}
    accept={"0", "1"}
    states={"0", "1"}
   
    alphabet_X={"{}:0".format(X), "{}:1".format(X)}
    alphabet_Y={"{}:0".format(Y), "{}:1".format(Y)}
    alphabet=set()
    for a in alphabet_X:
        for b in alphabet_Y:
            alphabet.add("{}|{}".format(a,b))

    transitions=list()
    transitions.append(["0","{}:0|{}:0".format(X,Y),"0"])
    transitions.append(["0","{}:1|{}:0".format(X,Y),"1"])
    transitions.append(["1","{}:1|{}:1".format(X,Y),"1"])
    transitions.append(["1","{}:0|{}:1".format(X,Y),"0"])
    
    a=Automaton(states,alphabet,transitions,start,accept)
    alphabetical_order(a)

    return a

def zeroin(X):
    """Constructs Buchi automaton for formula: 0 is an element of X."""

    start={"0"}
    accept={"1"}
    alphabet=["{}:0".format(X), "{}:1".format(X)]
    
    transitions=list()
    # first input must be X:1
    transitions.append(["0","{}:1".format(X),"1"])
    transitions.append(["1","{}:?".format(X),"1"])
    
    states=start|accept

    return Automaton(states,set(alphabet),transitions,start,accept)

def is_in(X, Y):
    "x is in Y"

    if isinstance(X, str):
        start={"0"}
        accept={"1"}
        
        alphabet_X={"{}:0".format(X), "{}:1".format(X)}
        alphabet_Y={"{}:0".format(Y), "{}:1".format(Y)}
        alphabet=set()
        for a in alphabet_X:
            for b in alphabet_Y:
                alphabet.add("{}|{}".format(a,b))

        transitions=list()
        transitions.append(["0","{}:0|{}:?".format(X,Y),"0"])
        transitions.append(["0","{}:1|{}:1".format(X,Y),"1"])
        transitions.append(["1","{}:0|{}:?".format(X,Y),"1"])
        
        states=start|accept
        
        a=Automaton(states,alphabet,transitions,start,accept)
        alphabetical_order(a)

        return a
    
    else:
        alphabet = set()
        for c in X.alphabet:
            alphabet.add(c+"|{}:0".format(Y))
            alphabet.add(c+"|{}:1".format(Y))

        transitions=list()
        for t in X.transitions:
            if t[1][2] == "1":
                new = t[1]+"|{}:1".format(Y)
                transitions.append([t[0], new, t[2]])
            elif t[1][2] == "0":
                new = t[1]+"|{}:?".format(Y)
                transitions.append([t[0], new, t[2]])

        a=Automaton(X.states, alphabet, transitions, X.start, X.accept)
        alphabetical_order(a)

        return a


def sing(X):
    """X is a singleton."""

    start={"0"}
    accept={"1"}
    alphabet=["{}:0".format(X), "{}:1".format(X)]
    states = start|accept

    transitions=list()
    transitions.append(["0", "{}:0".format(X), "0"])
    transitions.append(["0", "{}:1".format(X), "1"])
    transitions.append(["1", "{}:0".format(X), "1"])

    return Automaton(states, set(alphabet), transitions, start, accept)

def less(X, Y):
    start={"0"}
    accept={"2"}
    states={"0", "1", "2"}

    alphabet=set()
    alphabet.add("{}:0|{}:0".format(X,Y))
    alphabet.add("{}:0|{}:1".format(X,Y))
    alphabet.add("{}:1|{}:0".format(X,Y))
    alphabet.add("{}:1|{}:1".format(X,Y))

    transitions=list()
    transitions.append(["0", "{}:0|{}:0".format(X,Y), "0"])
    transitions.append(["0", "{}:1|{}:0".format(X,Y), "1"])
    transitions.append(["1", "{}:0|{}:0".format(X,Y), "1"])
    transitions.append(["1", "{}:0|{}:1".format(X,Y), "2"])
    transitions.append(["2", "{}:0|{}:0".format(X,Y), "2"])

    a = Automaton(states, alphabet, transitions, start, accept)
    alphabetical_order(a)

    return a
