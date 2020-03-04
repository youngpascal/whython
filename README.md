# whython
A programming language for no reason

# Features:
## Right now there is only a REPL.

## To run the REPL:
   
- Clone this repo with `git clone https://github.com/youngpascal/whython`

- type `python3 shell.py` in the terminal

## Syntax & Logic:

- Basic math operations and error handling:

    `why > 5 + 5` will return 10

    `why > 10 / 0` will return a Divide by Zero Error

    `why > *` will return an Illegal Syntax Error

- Variables:

    `why > VAR x = 1` will set x equal to 1

    `why > x` will return the value of x

    `why > x + 2` will add 2 to the value of x

- If / Then / Else / Elif

    `why > VAR x = IF 1 == 1 THEN 1 ELSE 0` will set x equal to 1

    `why > VAR x = IF 1 != 1 THEN 1 ELIF 1==1 THEN 0 ELSE 3` will set x equal to 0

- For / While
 
    `why > VAR x = 1`

    `why > FOR i = 1 TO 10 STEP 2 THEN VAR x = x * i` will loop [x = x * i] while i < 10 with {optional: step} being the amount to add to {iterator: i} each loop

    `why > WHILE x < 10 THEN VAR x = x + 1` will loop [x = x + 1] while x < 10 

- Functions

    `why > FUN add (a, b) -> a + b` will create a function add()

    `why > add(1, 2)` will output 3

    `why > FUN () -> 1 + 2` will create an anonymous function that outputs 3