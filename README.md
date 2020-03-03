# whython
A programming language for no reason

# Features:
## Right now there is only a REPL which can do the following:

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