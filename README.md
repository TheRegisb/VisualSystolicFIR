# Systolic FIR visual simulator
Visual example of a fully-systolic Finite Impulse Response, or FIR, as to operate a convolution on two numbers lists.

The graphical representation is done usign the Curses library and thus required the application to be started in a terminal.

Every cells is displayed as a square with inputs and outputs pins, connected to other cells, with their register value displayed as such.
Delay units are represented as their register value too, in between the cells.

Having an array larger than the size of the screen leads to undefined behaviour.

# Prerequisite
Python 3 and, for Windows users, the `windows-curses` Python library.

Installing the library can be done using the following command `pip3 install windows-curses`.

# Usage
In the project folder, run the following command `python UnidirSlowFIR [-h] [-i INPUT] [-c COEF] [--slowInput | --slowOutput]`

```
aguments:
  --slowInput           Activate slow input convolution method.
  --slowOutput          Activate slow output convolution method.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        List of comma separated numbers to process.
  -c COEF, --coef COEF  List of comma separated numbers to process the input list with.
```

# License
Every files in this repository is licensed under the Apache License 2.0.

# Credits
Régis BERTHELOT, 2019.