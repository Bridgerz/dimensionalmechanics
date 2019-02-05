import wizard, os, sys

def Demo():
    directory = "C:\\Users\\Bridger Zoske\\Desktop\\SmartTix2\\dimensionalmechanics\\DimensionalMechanics\\Wizard\\Testing"
    directories = {}

    with os.scandir(directory) as itr:
        for entry in itr:
            if entry.is_dir():
                directories[entry.path] = []
    
    for directory in directories:
        path = "C:\\Users\\Bridger Zoske\\Desktop\\SmartTix2\\dimensionalmechanics\\DimensionalMechanics\\Wizard\\InputData.txt"
        file = open(path, "w+")
        file.seek(0)
        file.truncate()
        lines = [directory,"0","0","0","1"]
        file.write('\n'.join(lines))
        file.close()
        file = open(path, "r")
        sys.stdin = file
        wizard.main()

if __name__ == '__main__':
    Demo()