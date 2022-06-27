from pathlib import Path
import numpy as np
from file_extracters import add_material_from_pdc_for_table

p = Path(r'\\LFTIR-Pesnya\Common\.')
for path in [folder for folder in p.iterdir() if folder.is_dir()]:
    #Для каждой папки с загрузкой работы реактора
    if path.name.startswith('#') and path.name[2].isdigit():
        #Для каждой папки внутри загрузки
        for folder in path.iterdir():
            if folder.name.startswith('ZR'):
                if list(folder.glob('**/*.FIN')) != []:
                    fin_file = list(folder.glob('**/*.FIN'))[0]
                if list(folder.glob('**/*.PDC')) != []:
                    pdc_file = list(folder.glob('**/*.PDC'))[0]
                if fin_file and pdc_file:
                    add_material_from_pdc_for_table(fin_file_to_read=fin_file,
                                                    pdc_file_to_read=pdc_file,
                                                    materials=np.arange(15563, 50123)
                                                    )
                else:
                    continue


