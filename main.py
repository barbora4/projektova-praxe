#! /usr/bin/python3

###################################################################
# Barbora Šmahlíková
# 2020/2021
# Translation of S1S formula to Büchi automaton
###################################################################

from sys import stdin, exit
from automaton import *
from parser import *
from optimize import *
from graph import *
import os

file_text=stdin.read()
a = parse(file_text, analyse_predicates(file_text))

write_to_file(a, 'a.ba')
write_to_gv(a, 'graph.gv')

# show automaton
#os.popen('dot -Tpdf graph.gv -o graph.pdf')
#os.popen('xdg-open graph.pdf')

exit(len(a.states))
