#!/usr/bin/env python3

"""Main."""

import sys
import datetime
from cpu import *

cpu = CPU()

if len(sys.argv) < 2:
    print("Error: Please load the Program")
else:
    program_file = sys.argv[1]
    cpu.load(program_file)
    cpu.run()


