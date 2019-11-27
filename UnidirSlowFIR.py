#!/usr/bin/env python3

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

import argparse
from Cells import UnidirCell # Local file
import Display # Local file

def main():
    # Definition of command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", action = "store", dest = "input", help = "List of comma separated numbers to process.")
    parser.add_argument("-c", "--coef", action = "store", dest = "coef", help = "List of comma separated numbers to process the input list with.")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--slowInput", action = "store_true", dest = "slowInput", help = "Activate slow input convolution method.")
    group.add_argument("--slowOutput", action = "store_true", dest = "slowOutput", help = "Activate slow output convolution method.")

    options = parser.parse_args()
    if not (options.slowOutput or options.slowInput):
        parser.error("One of --slowInput or --slowOutput must be selected")

    # Generating inputs and cells list from given -i, -c and --slowMODE arguments
    inputs = [int(x) for x in options.input.split(',')]
    cells = [UnidirCell(int(x), slowInput = options.slowInput, slowOutput = options.slowOutput) for x in options.coef.split(',')]

    origInputSize = len(inputs)
    outputs = []

    if (options.slowOutput): # Reverse inputs on slow output mode to preserve original convolution
        inputs.reverse()

    Display.startCurses()
    while len(outputs) != origInputSize + (len(cells) * 2) - 1: # Loop until the systolic array have been emptied (with skewing)
        inputx = 0 # Default fallback value for empty input list
        if (len(inputs) != 0):
            inputx = inputs[0]
            inputs = inputs[1:] # Pops the first element of the list

        cells[0].feed(inputx, 0)
        for i in range(1, len(cells)):
            cells[i].feed(cells[i - 1].getPartial()[0], cells[i - 1].getPartial()[1])

        Display.updateCurses(cells, inputs, outputs)
        if (Display.waitEnterCurses()): # 'q' key pressed -- leaving early
            Display.stopCurses()
            break

        for cell in cells:
            cell.calc()
        outputs.append(cells[-1].getPartial()[1])
    else: # While loop wasn't broken
        Display.stopCurses()
        print(list(filter(lambda x : x != 0, outputs))) # Remove 0 values due to skewing

if __name__=="__main__":
    main()
        
