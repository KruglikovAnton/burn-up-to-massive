from pathlib import Path

p = Path(r'\\LFTIR-Pesnya\Common\.')
for path in [folder for folder in p.iterdir() if folder.is_dir()]:
    #Для каждой папки с загрузкой работы реактора
    if path.name.startswith('#') and path.name[2].isdigit():
        #Для каждой папки внутри загрузки
        for folder in path.iterdir():
            if folder.name.startswith('ZR'):
                print(list(p.glob('**/*.FIN')))
                #print(path.name, folder.name)


