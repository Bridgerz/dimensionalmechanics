import os
def GenerateFile(inputDict):
    #constants
    MAXLEN = '1366'
    LOWSHAPE = '24'
    MEDSHAPE = '32'
    HIGHSHAPE = '128'
    LOWBATCH = '16'
    MEDBATCH = '64'
    HIGHBATCH = '1024'

    directory = inputDict["directory"]
    mode = inputDict["mode"]
    dataType = inputDict["type"]
    performance = inputDict["performance"]

    if not "channels" in inputDict.keys():
        channels = ''
    else:
        channels = str(inputDict["channels"])

    if not "bands" in inputDict.keys():
        bands = ''
    else:
        bands = str(inputDict["bands"])

    if not "validationSplit" in inputDict.keys():
        validationSplit = '0.2'
    else:
        validationSplit = str(inputDict["validationSplit"])

    #flat = inputDict["flat"]
    flat = "10"

        

    
    #create file if path does not exist
    with open(os.path.join(directory, 'GEN_NML'), 'w+') as f:
        f.writelines(['oracle(\"mode\") = \"classification\"' + '\n',
                     '\n',
                     'source:' + '\n',
                     '  bind = \"' + directory + '\" ;' + '\n',
                     '  input:' + '\n',
                     '    x ~ from "Path"' + '\n'])
        if dataType == 0 or dataType == 1:
            shape = ''
            if performance == 0:
                shape = LOWSHAPE
            elif performance == 1:
                shape = MEDSHAPE
            elif performance == 2:
                shape = HIGHSHAPE

            f.writelines(['      -> image: [shape=[' + shape + ', ' + shape + '], channels=' + channels + ']' + '\n',
                         '      -> ImageDataGenerator: [rescale= 0.003921568627451] ;' + '\n'])

        elif dataType == 2:
            f.writelines(['        -> audio: [maxlen = ' + MAXLEN + ', bands = ' + bands + ']' + '\n',
                         '        -> AudioDataGenerator: [];' + '\n'])
        
        batch_size = ''
        if performance == 0:
            batch_size = LOWBATCH
        elif performance == 1:
            batch_size = MEDBATCH
        elif performance == 2:
            batch_size = HIGHBATCH

        f.writelines(['  output:' + '\n',
                     '    y ~ from "Label"' + '\n',
                     '      -> flat: ['+ flat +']' + '\n',
                     '      -> FlatDataGenerator: [] ;' + '\n',
                     '  params:' + '\n',
                     '    batch_size = '+ batch_size +',' + '\n',
                     '    validation_split = ' + validationSplit + ' ;' + '\n',
                     '\n',
                     'architecture:' + '\n'])
        if dataType == 0:
            f.write('  input:  x ~ image: [shape=[' + shape + ', ' + shape + '], channels=' + channels + '] ;' + '\n')
        elif dataType == 2:
            f.write('  input: x ~ audio: [maxlen = ' + MAXLEN + ', bands = ' + bands + '];' + '\n')
        elif dataType == 1:
            f.write('  input: x ~ video: [shape=[' + shape + ', ' + shape + '], channels=' + channels + '] ;' + '\n')

        f.writelines(['  output: y ~ flat: ['+ flat +'] ;' + '\n',
                     '\n',
                     '  x -> auto- > y;' + '\n',
                     '\n',
                     'train:' + '\n',
                     '  compile:' + '\n',
                     '    optimizer = auto,' + '\n',
                     '    loss = auto,' + '\n',
                     '    metrics = [\'accuracy\'] ;' + '\n',
                     '\n',
                     '  run:' + '\n',
                     '    epochs = 4 ;' + '\n\n',
                     '  dashboard: ;' + '\n'])