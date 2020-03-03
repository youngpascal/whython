import main

##################################
# SHELL LOOP FOR INPUT
##################################

while True:
    text = input('why > ')
    result, error = main.run('<stdin>', text)

    if error: print(error.as_string())
    else: print(result)