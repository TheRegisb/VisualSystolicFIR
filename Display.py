#!/ust/bin/env python3

# =============================================================

# Copyright 2019 Régis Berthelot

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at

#   http:#www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# =============================================================


import curses # Native on UNIX, required curses-windows for Win32.

stdscr = None # Screen handle. To be initialized when required.

# Function
#   startCurses
# Description
#   Initialize the Curses environment
def startCurses():
    global stdscr

    stdscr = curses.initscr()
    curses.noecho()
    stdscr.keypad(True)
    curses.cbreak()

# Function
#   updateCurses
# Description
#   Refresh the Curses display using the given parameters
# Params
#   cells  : Unidir List : Cells of the systolic array, in logical order
#   inputs : Integer List: Remaining inputs in the inputs list
#   outputs: List        : Current outputs aquired by the calculations
def updateCurses(cells, inputs, outputs):
    global stdscr

    xOffset = 0

    stdscr.clear()
    stdscr.addstr(0, 0, "Inputs: " + str(inputs))
    stdscr.addstr(8, 0, "Outputs: " + str(outputs))
    for cell in cells:
        # Defining per-cells content length
        inputStrSize = ((len(str(cell.x))) if len(str(cell.x)) > len(str(cell.y)) else len(str(cell.y))) + 1
        coefSize = len(str(cell.coef))

        # Displaying inputs
        stdscr.addstr(3, xOffset, str.format("% *d" % (inputStrSize, cell.y)))
        stdscr.addstr(5, xOffset, str.format("% *d" % (inputStrSize, cell.x)))
        xOffset += inputStrSize
        
        # Displaying cells
        stdscr.addstr(2, xOffset, "+" + ("-" * (coefSize + 2)) + "+")
        stdscr.addstr(3, xOffset, "|" + (" " * (coefSize + 2)) + "|")
        stdscr.addstr(4, xOffset, "|" + str.format(" %d " % (cell.coef)) + "|")
        stdscr.addstr(5, xOffset, "|" + (" " * (coefSize + 2)) + "|")
        stdscr.addstr(6, xOffset, "+" + ("-" * (coefSize + 2)) + "+")
        xOffset += coefSize + 4
        
        # Displaying output
        stdscr.addstr(3, xOffset, str.format("--%d--" % (cell.delayY)) if cell.slowOutput else ("-" * (len(str(cell.delayX)) + 4)))
        stdscr.addstr(5, xOffset, str.format("--%d--" % (cell.delayX)) if cell.slowInput  else ("-" * (len(str(cell.delayY)) + 4)))
        xOffset += (len(str(cell.delayX)) if cell.slowInput else len(str(cell.delayY))) + 4

    stdscr.refresh()

# Function
#   waitEnterCurses
# Description
#   Pause the Curses display until a key is pressed
# Returns
#   True : 'q' key pressed
#   False: Any key but 'q' was pressed
def waitEnterCurses():
    global stdscr

    return (stdscr.getkey() == 'q')
    

# Function
#   stopCurses
# Description
#   Terminates properly the started Curses environment.
def stopCurses():
    global stdscr

    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
