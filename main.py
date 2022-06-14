import os
import re
import time
import numpy as np
import pandas as pd

# from file_extracters import add_material_from_file, add_material_from_pdc, rez_reader, average_burn_up
#
# # Для отслеживания времени работы программы
# t1 = time.time()
# # Списки для сохранения имен файлов формата pdc и fin
# list_of_pdc = []
# list_of_fin = []
#
# # В случае, если pdc_b0 нет, необходимо использовать файл задания варианта, из которого будут взяты материальные составы
# use_var_file = False
# # os.chdir(os.getcwd() + r'\\ber')
# # Сохраняем имена файлов в соотвутствующие списки
# for file in os.listdir():
#     if file.lower().find('pdc_') != -1:
#         list_of_pdc.append(file)
#     elif file.lower().find('pdc_b0') != -1:
#         use_var_file = True
#     elif file.lower().find('fin') != -1:
#         list_of_fin.append(file)
# # print(list_of_pdc)
#
# #
# # Задаем имя входного файла, списки нуклидов и материалов
# name_var = '2021-09B'
# nuclides = {'u235'}
# materials = list(range(15563, 50123))
#
# final_df = pd.DataFrame({})
#
# cells_dict = {}
# cells_order = ['cell_2_2', 'cell_2_3', 'cell_2_4', 'cell_2_5', 'cell_3_2', 'cell_3_3', 'cell_3_4', 'cell_3_5',
#                'cell_4_2', 'cell_4_3', 'cell_4_4', 'cell_4_5', 'cell_5_2', 'cell_5_3', 'cell_5_4', 'cell_5_5']
#
# with open('loadings.txt', 'r') as file:
#     reading_start_materials = False
#     reading_start_loadings = False
#     string_number_in_table = 2
#     for line in file:
#         if line.startswith('#'):
#             continue
#         if line.startswith('Start mater'):
#             reading_start_materials = True
#             continue
#         if line.startswith('Start loadings'):
#             reading_start_loadings = True
#             continue
#         if reading_start_materials:
#             if string_number_in_table > 5:
#                 reading_start_materials = False
#                 continue
#             print('go_write')
#             assert line.split()[0].isdigit(), 'this line should contain only numbers'
#             cells_dict[f"cell_{string_number_in_table}_2"], \
#             cells_dict[f"cell_{string_number_in_table}_3"], \
#             cells_dict[f"cell_{string_number_in_table}_4"], \
#             cells_dict[f"cell_{string_number_in_table}_5"] = \
#                 {'zones_numbers': []}, {'zones_numbers': []}, {'zones_numbers': []}, {'zones_numbers': []}
#             cells_dict[f"cell_{string_number_in_table}_2"]['zones_numbers'], \
#             cells_dict[f"cell_{string_number_in_table}_3"]['zones_numbers'], \
#             cells_dict[f"cell_{string_number_in_table}_4"]['zones_numbers'], \
#             cells_dict[f"cell_{string_number_in_table}_5"]['zones_numbers'] = \
#                 map(lambda x: np.arange(int(x), int(x) + 2160), line.split())
#             string_number_in_table += 1
#             continue
#         number_of_cell_in_list = 0
#         if reading_start_loadings:
#             if line.startswith('#'):
#                 continue
#             else:
#                 cells_dict[cells_order[number_of_cell_in_list]]\
#                     .update(fuel_loadings=np.array(list(map(float, line.split()))))
# print(cells_dict)

# core_dict["cell_2_2"]["zones"] = np.arange(22043, 24203)
# core_dict["cell_2_3"]["zones"] = np.arange(45803, 47963)
# core_dict["cell_2_4"]["zones"] = np.arange(15563, 17723)
# core_dict["cell_2_5"]["zones"] = np.arange(19883, 22043)
# core_dict["cell_3_2"]["zones"] = np.arange(30683, 32843)
# core_dict["cell_3_3"]["zones"] = np.arange(39323, 41483)
# core_dict["cell_3_4"]["zones"] = np.arange(28523, 30683)
# core_dict["cell_3_5"]["zones"] = np.arange(47963, 50123)
# core_dict["cell_4_2"]["zones"] = np.arange(32843, 35003)
# core_dict["cell_4_3"]["zones"] = np.arange(41483, 43643)
# core_dict["cell_4_4"]["zones"] = np.arange(26363, 28523)
# core_dict["cell_4_5"]["zones"] = np.arange(37163, 39323)
# core_dict["cell_5_2"]["zones"] = np.arange(24203, 26363)
# core_dict["cell_5_3"]["zones"] = np.arange(35003, 37163)
# core_dict["cell_5_4"]["zones"] = np.arange(43643, 45803)
# core_dict["cell_5_5"]["zones"] = np.arange(17723, 19883)


# if use_var_file:
#     final_df = pd.concat([final_df, pd.DataFrame(add_material_from_file(name_var, materials, nuclides))])
#
# for pdc_file in list_of_pdc:
#     final_df = pd.concat([final_df, pd.DataFrame(add_material_from_pdc(pdc_file, materials, nuclides))])
# final_df = final_df.reset_index().drop(columns=['index'])
# final_df['pdc_number'] = final_df['pdc']. \
#     apply(lambda x: int(''.join(re.findall('\d', x[-5:]))) if x != 'var_file' else 0)
#
# final_df['MATR'] = final_df['MATR'].astype('int64')
# final_df.sort_values(by='pdc_number', inplace=True)
#
# # final_df.pivot(index = 'pdc_number', columns='nuclide', values='N').fillna(0).to_string('results.txt')
# final_df.to_string('results.txt')
#
# # final_df.to_string('results.txt')
# t2 = time.time()
# print((t2 - t1))
#
# volumes_dict = {}
# rez_reader('HEU_AZ08.REZ', 'volumes.txt', materials=list(range(15563, 50123)), output_dict=volumes_dict)
core_dict = {}
for i in range(2, 6):
    for j in range(2, 6):
        core_dict[f'cell_{i}_{j}'] = {'type':
                                          'fuel',
                                      'start_loadings':
                                          {
                                              '1st_tube': 59.66374269,
                                              '2d_tube': 53.46491228,
                                              '3d_tube': 47.26608187,
                                              '4th_tube': 41.06725146,
                                              '5th_tube': 34.86842105,
                                              '6th_tube': 28.66959064
                                          }
                                      } \
            if 1 < i < 6 and 1 < j < 6 else {'type': 'reflector'}

core_dict["cell_2_2"]["zones"] = np.arange(22043, 24203)
core_dict["cell_2_3"]["zones"] = np.arange(45803, 47963)
core_dict["cell_2_4"]["zones"] = np.arange(15563, 17723)
core_dict["cell_2_5"]["zones"] = np.arange(19883, 22043)
core_dict["cell_3_2"]["zones"] = np.arange(30683, 32843)
core_dict["cell_3_3"]["zones"] = np.arange(39323, 41483)
core_dict["cell_3_4"]["zones"] = np.arange(28523, 30683)
core_dict["cell_3_5"]["zones"] = np.arange(47963, 50123)
core_dict["cell_4_2"]["zones"] = np.arange(32843, 35003)
core_dict["cell_4_3"]["zones"] = np.arange(41483, 43643)
core_dict["cell_4_4"]["zones"] = np.arange(26363, 28523)
core_dict["cell_4_5"]["zones"] = np.arange(37163, 39323)
core_dict["cell_5_2"]["zones"] = np.arange(24203, 26363)
core_dict["cell_5_3"]["zones"] = np.arange(35003, 37163)
core_dict["cell_5_4"]["zones"] = np.arange(43643, 45803)
core_dict["cell_5_5"]["zones"] = np.arange(17723, 19883)
print(core_dict["cell_2_2"]["zones"])
# print(type(final_df['MATR'][0]))
#
# for value in core_dict.values():
#     if value['type'] == 'fuel':
#         value['volumes'] = np.array([float(volumes_dict[str(zone)]) for zone in value['zones']])
#
# for key, value in core_dict.items():
#     if value['type'] == 'fuel':
#         value['burn_up'] = average_burn_up(volumes=value['volumes'],
#                                            loadings=np.array(list(value['start_loadings'].values())),
#                                            current_concentrations=final_df[(final_df['pdc'] == 'PDC_B0') &
#                                                                            (final_df['MATR'].isin(list(value['zones'])))] \
#                                            .sort_values(by='MATR').N.astype('float64').values)

print(core_dict)
