import collections, os

params = ('directory', 'mode', 'performance', 'type', 'channels', 'bands')

class Option:
    def __init__(self, prompt, varType, isValid, dependencies = []):
        self.prompt = prompt
        self.varType = varType
        self.isValid = isValid
        self.dependencies = dependencies

options = {
    'directory': Option("Training data directory (absolute path): ", "str", lambda x: os.path.isdir(x)),
    'mode': Option("Desired mode (basic=0, advanced=1): ", "int", lambda x: x in range(2)),
    'performance': Option("Performance spec (low=0, med=1, high=2): ", "int", lambda x: x in range(3)),
    'type': Option("Data type (image=0, video=1, audio=2): ", "int", lambda x: x in range(3)),
    'channels': Option("Picture channels (b&w=1, rgb=3, rgba=4): ", "int", lambda x: x in (1,3,4), [('type', range(2))]), 
    'bands': Option("Audio bands (96-96): ", "int", lambda x: x in (96,), [('type', (2,))])
}

buffer = {}

def getInput(option):
    value = str(input(option.prompt))
    error = False
    if (option.varType == "int"):
        try:
            value = int(value)
        except ValueError:
            error = True

    while not error and not option.isValid(value):
        print("Input", value, "was invalid. Try again.")
        value = str(input(option.prompt))
        error = False
        if (option.varType == "int"):
            try:
                value = int(value)
            except ValueError:
                error = True
    return value

for param in params:
    option = options[param]
    show = True
    for d in option.dependencies:
        if buffer[d[0]] not in d[1]:
            show = False
    
    if show:
        value = getInput(option)
        buffer[param] = value

print(buffer)
