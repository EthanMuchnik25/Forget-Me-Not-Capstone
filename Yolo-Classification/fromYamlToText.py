yamlFile = 'data.yaml'
textFile = 'allcategories.txt'
finalTextFile = 'C:\\Users\\muchn\Documents\\Classes\\18500\Forget-Me-Not-Capstone\\Yolo-Classification\\categories.txt'
with open((yamlFile), 'r') as file:
    data = file.read()
    

    
    # get name dictionary from yaml file
    import yaml
    data = yaml.load(data, Loader=yaml.FullLoader)
    names = data['names']


    #Use each line of the text file to get the value of the names and write them to a new text file
    with open(textFile, 'r') as file:
        lines = file.readlines()
        with open(finalTextFile, 'w') as text:
            for line in lines:
                line = line.strip()
                
                # write the value in yaml file that each line in textfile corresponds to
                text.write(f"{names[int(line)]}\n")
            
            print("Conversion successful!")    