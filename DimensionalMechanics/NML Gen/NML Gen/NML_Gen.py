import os
def GenerateFile(inputDict):
    #constants
    MAXLEN = '1366'
    NBANDS = '96'
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
    channels = inputDict["channels"]

    #flat = inputDict["flat"]
    flat = "10"
    validationSplit = inputDict["validationSplit"]
    if validationSplit == '':
        validationSplit = '0.2'


    #create file if path does not exist
    if not os.path.exists(directory):
        f = open(directory, "w")
        f.close()

    f = open(directory, "r+")

    f.writelines(['oracle(\"mode\") = \"classification\"' + '\n',
                 '\n',
                 'source:' + '\n',
                 '  bind = \"' + directory + '\" ;' + '\n',
                 '  input:' + '\n',
                 '    x ~ from "path"' + '\n'])
    if dataType == 'image' or dataType == 'video':
        if performance == 'low':
            shape = LOWSHAPE
        elif performance == 'medium':
            shape = MEDSHAPE
        elif performance == 'high':
            shape = HIGHSHAPE

        f.writelines(['      -> image: [shape=[' + shape + ', ' + shape + '], channels=' + channels + ']' + '\n',
                     '      -> ImageDataGenerator: [rescale= 0.003921568627451] ;' + '\n'])

    elif dataType == 'audio':
        f.writelines(['        -> audio: [maxlen = ' + MAXLEN + ', nbands = ' + NBANDS + ']' + '\n',
                     '        -> AudioDataGenerator: [];' + '\n'])
    if performance == 'low':
        batch_size = LOWBATCH
    elif performance == 'medium':
        batch_size = MEDBATCH
    elif performance == 'high':
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
    if dataType == 'image':
        f.write('  input:  x ~ image: [shape=[' + shape + ', ' + shape + '], channels=' + channels + '] ;' + '\n')
    elif dataType == 'audio':
        f.write('  input: x ~ audio: [maxlen = ' + MAXLEN + ', nbands = ' + NBANDS + '];' + '\n')
    elif dataType == 'video':
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
                 '    epochs = 4 ;' + '\n',
                 '  dashboard: ;' + '\n'])
    f.close()