###################################################################
# Barbora Šmahlíková
# 2020/2021
# Direct simulation and disconnecting little brother states
###################################################################

from automaton import *
from itertools import product
from optimize import *

def direct_simulation(a):
    """Direct simulation for automaton a."""

    # remove duplicate transitions
    tran=list()
    for t in a.transitions:
        if t not in tran:
            tran.append(t)
    a.transitions = copy(tran)

    # cardinality
    complete = True
    card={}
    for c in a.alphabet:
        dic={}
        for q in a.states:
            dic[q]=0
            for t in a.transitions:
                if t[0]==q and input_equal(c,t[1]):
                    dic[q] += 1
            if dic[q]==0:
                complete=False
        card[c]=dic
    
    if not complete:
        a.states.add(str(len(a.states)))
        for c in a.alphabet:
            card[c][str(len(a.states)-1)]=0
            for q in a.states:
                if card[c][q]==0:
                    a.transitions.append([q, c, str(len(a.states)-1)])
                    card[c][q]+=1

    # matrices - initialize all N(a)s with 0s
    mat = {}
    for c in a.alphabet:
        N = list()
        for i in range(len(a.states)):
            N.append([0]*len(a.states))
        mat[c] = N

    w = set()   # the relation which is the complement of direct simulation at the end
    queue = []
    
    for i in a.accept:
        for j in (a.states-a.accept):
            w.add((i, j))
            queue.append((i, j))

    while len(queue)!=0:
        new = queue.pop(0)    # dequeue
        for c in a.alphabet:
            for t in a.transitions:
                if t[2] == new[1] and input_equal(c, t[1]): # all k for which new[1]c->k
                    mat[c][int(new[0])][int(t[0])] += 1
                    if mat[c][int(new[0])][int(t[0])] == card[c][t[0]]: # there is j: new[0]c->j for which (j,k) in w for all states k 
                        for t2 in a.transitions:
                            if t2[2]==new[0] and input_equal(c, t2[1]): 
                                if (t2[0], t[0]) not in w:
                                    w.add((t2[0], t[0])) 
                                    queue.append((t2[0],t[0])) 

    if not complete:
        a.states.remove(str(len(a.states)-1))
        tran=list()
        for t in a.transitions:
            if not (t[0]==str(len(a.states)) or t[2]==str(len(a.states))):
                tran.append(t)
        a.transitions = copy(tran)
    all_combinations = set(product(a.states, a.states))
    direct = all_combinations - w   # direct simulation
    return direct

def merge(a, q0, q1):
    """Merges two states in automaton a."""

    # merge these two states and update preorder
    # add new state
    a.states.add("new")
    if q0 in a.start or q1 in a.start:
        a.start.add("new")
    if q0 in a.accept or q1 in a.accept:
        a.accept.add("new")
    
    # remove old states
    if q0 in a.states:
        a.states.remove(q0)
    if q1 in a.states:
        a.states.remove(q1)
    if q0 in a.start:
        a.start.remove(q0)
    if q1 in a.start:
        a.start.remove(q1)
    if q0 in a.accept:
        a.accept.remove(q0)
    if q1 in a.accept:
        a.accept.remove(q1)
    
    # adjust transitions
    for i in range(len(a.transitions)):
        if a.transitions[i][0]==q0 or a.transitions[i][0]==q1:
            a.transitions[i][0]="new"
        if a.transitions[i][2]==q0 or a.transitions[i][2]==q1:
            a.transitions[i][2]="new"
    
    # remove duplicate transitions
    tran = list()
    for t in a.transitions:
        if t not in tran:
            tran.append(t)
    a.transitions = copy(tran)
    

def reduction(a):
    """Reduces states in automaton a using direct simulation."""

    change = True
    while change:
        edit_names(a)

        change = False
        skip=False
        direct = direct_simulation(a)

        for d in direct:
            if (d[1],d[0]) in direct and d[0]!=d[1]:
                change=True
                merge(a, d[0], d[1])
                disconnect_little_brothers(a,direct)
                skip=True
                break


def disconnect_little_brothers(a, direct):
    """Disconnects little brother states."""

    count = 0
    change=True
    while change:
        change=False
        skip=False
        if not skip:
            for q in a.states:
                if not skip:
                    for i in range(len(a.transitions)):
                        count=0
                        if not skip:
                            if a.transitions[i][0]==q:
                                for t2 in a.transitions:    
                                    if (a.transitions[i]!=t2 and t2[0]==q and input_equal(a.transitions[i][1],t2[1]) and t2[2]!=a.transitions[i][2] and (a.transitions[i][2],t2[2]) in direct and (t2[2],a.transitions[i][2]) not in direct):
                                        # a.transitions[i][2] is a little brother of t2[2]
                                        change=True
                                        
                                        # all transitions in a.transitions[i]
                                        transitions1=[copy(a.transitions[i][1])]
                                        while any("?" in t for t in transitions1):
                                            for j in range(len(transitions1)):
                                                if "?" in transitions1[j]:
                                                    transitions1.append(transitions1[j].replace('?','0', 1))
                                                    transitions1.append(transitions1[j].replace('?','1', 1))
                                                    transitions1.remove(transitions1[j])
                                        
                                        new=list()
                                        for j in range(len(transitions1)):
                                            if not input_equal(transitions1[j],t2[1]):
                                                # which transitions should be left
                                                new.append(transitions1[j])
                                            else:
                                                count+=1
                                        
                                        for n in new:
                                            a.transitions.append([a.transitions[i][0], n, a.transitions[i][2]])
                                        a.transitions.remove(a.transitions[i])

                                        skip=True
                                        break
