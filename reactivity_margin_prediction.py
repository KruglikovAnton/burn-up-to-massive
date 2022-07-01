from pathlib import Path
from file_extracters import wolfram_block_identifier
import numpy as np
import pandas as pd

from file_extracters import add_material_from_pdc_for_table

dict_for_df = None
p = Path(r'\\LFTIR-Pesnya\Common\.')
for path in [folder for folder in p.iterdir() if folder.is_dir()]:
    # Для каждой папки с загрузкой работы реактора
    if path.name.startswith('#') and path.name[2].isdigit():
        # Для каждой папки внутри загрузки
        for folder in path.iterdir():
            # Папки с вариантами расчетов запасов реактивности содержат ZR, например ZR_KR_vars, ##ZR_vars и т.д.
            if folder.name.find('ZR') != -1:
                # Находим варианты, которые точно были посчитаны, следовательно присутствует файл .FIN и также проверяем,
                # чтобы название уже папки с вариантом содержало ZR
                for fin_path in list(folder.glob('**/*.FIN')):
                    if fin_path.parent.parent.name.find('ZR') != -1 and fin_path.parent.name.find('ZR') != -1 or \
                            fin_path.parent.name.lower().startswith('result') and \
                            fin_path.parent.parent.name.find('ZR') != -1:
                        # Поскольку могли забыть скопировать файл с изотопными составами, нужно обязательно проврить
                        # его наличие помимо файла FIN. Изотопные составы находятся в файле .PDC
                        pdc_path = fin_path.with_suffix('.PDC')
                        file_path = fin_path.parent / fin_path.stem
                        print(f'file: {file_path}')
                        # Аналогично могли забыть скопировать файл самого варианта, а только FIN и PDC, поэтому
                        # дополнительно проверяем присутствие входного файла, это текстовый файл такого же названия,
                        # но без расширения.
                        if pdc_path.exists() and file_path.exists():
                            dict_for_df = add_material_from_pdc_for_table(fin_file_to_read=fin_path,
                                                                          pdc_file_to_read=pdc_path,
                                                                          materials=np.arange(15563, 50123),
                                                                          dict_of_results=dict_for_df
                                                                          )
                            dict_for_df['ampule'].append(wolfram_block_identifier(file_path))
                            print(len(dict_for_df['Keff']), len(dict_for_df[f'u235 in mat20000']),
                                  dict_for_df['ampule'])

main_df = pd.DataFrame(dict_for_df)
main_df['Keff'] = main_df['Keff'].astype('float32')
main_df['reactivity_margin'] = (main_df['Keff'] - 1) * 100 / main_df['Keff']
main_df.to_csv('final_with_ampules.csv')
