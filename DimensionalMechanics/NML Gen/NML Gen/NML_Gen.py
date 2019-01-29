def GenerateFile():
    import os

    directory = "C:\\Users\\Bridger Zoske\\testing\\test\\NMLGen.NML"
    dataType = "image" 
    performance = "low,med,high"
    #video and image
    channels = "testCannels"
    shape = "30"
    #audio
    maxlen = "1366"
    nbands = "96"
    #all
    flat = "10"
    validationSplit = "0.2"
    batch_size = "5"

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
    if (dataType == "image"):
        #TODO: set shape based off performance
        f.writelines(['      -> image: [shape=[' + shape + ', ' + shape + '], channels=' + channels + ']' + '\n',
                     '      -> ImageDataGenerator: [rescale= 0.003921568627451] ;' + '\n'])
    elif (dataType == "video"):
        #TODO: set shape based off performance
        f.writelines(['      -> video: [shape=[' + shape + ', ' + shape + '], channels=' + channels + ']' + '\n',
                     '      -> ImageDataGenerator: [];' + '\n'])
    elif (dataType == "audio"):
        #TODO: set maxlen and nbands baased off performance
        f.writelines(['        -> audio: [maxlen = ' + maxlen + ', nbands = ' + nbands + ']' + '\n',
                     '        -> AudioDataGenerator: [];' + '\n'])
    
    #TODO: set batch_size based off performance
    f.writelines(['  output:' + '\n',
                 '    y ~ from "Label"' + '\n',
                 '      -> flat: ['+ flat +']' + '\n',
                 '      -> FlatDataGenerator: [] ;' + '\n',
                 '  params:' + '\n',
                 '    batch_size = '+ batch_size +',' + '\n',
                 '    validation_split = ' + validationSplit + ' ;' + '\n',
                 '\n',
                 'architecture:' + '\n'])
    if (dataType == "image"):
        f.write('  input:  x ~ image: [shape=[' + shape + ', ' + shape + '], channels=' + channels + '] ;' + '\n')
    elif (dataType == "audio"):
        f.write('  input: x ~ audio: [maxlen = ' + maxlen + ', nbands = ' + nbands + '];' + '\n')
    elif (dataType == "video"):
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
GenerateFile()