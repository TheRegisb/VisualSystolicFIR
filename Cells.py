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

# Class
#   UnidirCell
# Description
#   Represents a dual inputs/outputs cell that performs a unique preset operation.
#   To be combined with similar cells to form a systolic array.
#   Outputs can be "delay" by one cycle to perform convolution.
class UnidirCell:
    # Variables
    #   coef      : Integer: Intenal coefficient of the cell
    #   x         : Integer: Input from the inputs list
    #   y         : Integer: Previous sums
    #   delayX    : Integer: Retained last value of x, for slow input mode
    #   delayY    : Integer: Retained last value of y, for slow input mode
    #   partialX  : Integer: Result (or output) of the last calculation of x
    #   partialY  : Integer: Result (or output) of the last calculation of y
    #   slowInput : Boolean: Should the cell retains its x value one extra clock cycle
    #   slowOutput: Boolean: Should the cell retains its y value one extra clock cycle

    # Function
    #    __init__
    # Description
    #   Initialize a cell with a coefficient and the definition of its mode
    #   (fast or slow inputs/outputs)
    # Params
    #   coef                : Integer: Coefficient of the cell
    #   slowInput (= False) : Boolean: Enable the slow input (i.e. delay) mode
    #   slowOutput (= False): Boolean: Enable the slow output (i.e. delay) mode
    def __init__(self, coef, slowInput = False, slowOutput = False):
        self.coef = coef
        self.slowInput = slowInput
        self.slowOutput = slowOutput
        self.x = 0
        self.y = 0
        self.delayX = 0
        self.delayY = 0
        self.partialX = 0
        self.partialY = 0

    # Function
    #   feed
    # Description
    #   Provides new inputs for the cell
    # Params
    #   x: Integer: Input from the inputs lists
    #   y: Integer: Output from logically precedent cell
    def feed(self, x, y):
        self.delayX = self.x
        self.delayY = self.y
        self.x = x
        self.y = y

    # Function
    #   calc
    # Description
    #   Perform calculation and reset outputs using given modes
    def calc(self):
        self.y = self.y + self.x * self.coef
        self.partialX = self.x if not self.slowInput  else self.delayX
        self.partialY = self.y if not self.slowOutput else self.delayY

    # Function
    #   getPartial
    # Description
    #   Get result from the last calculation
    # Returns
    #   List: List of two elements,
    #   the [0] being the original input from the input list
    #   and [1] being the result of the last computation
    def getPartial(self):
        return [self.partialX, self.partialY]
