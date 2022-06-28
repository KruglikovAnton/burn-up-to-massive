from pathlib import Path
import numpy as np
import pandas as pd

from file_extracters import add_material_from_pdc_for_table
dict_for_df=None
p = Path(r'\\LFTIR-Pesnya\Common\.')
for path in [folder for folder in p.iterdir() if folder.is_dir()]:
    # Для каждой папки с загрузкой работы реактора
    if path.name.startswith('#') and path.name[2].isdigit():
        # Для каждой папки внутри загрузки
        for folder in path.iterdir():
            if folder.name.startswith('ZR'):
                for fin_path in list(folder.glob('**/*.FIN')):
                    if fin_path.parent.parent.name.find('ZR') != -1 and fin_path.parent.name.find('ZR') != -1 or\
                            fin_path.parent.name.lower().startswith('result') and fin_path.parent.parent.name.find('ZR') != -1:
                        pdc_path = fin_path.with_suffix('.PDC')
                        if pdc_path.exists():
                            dict_for_df = add_material_from_pdc_for_table(fin_file_to_read=fin_path,
                                                                          pdc_file_to_read=pdc_path,
                                                                          materials=np.arange(15563, 50123),
                                                                          dict_of_results=dict_for_df
                                                                          )

main_df = pd.DataFrame(dict_for_df)
main_df['Keff'] = main_df['Keff'].astype('float32')
main_df['reactivity_margin'] = (main_df['Keff'] - 1) * 100 / main_df['Keff']
main_df.to_csv('final.csv')