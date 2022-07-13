import numpy as np
from itertools import islice


def loadings_file_reader(loadings_file: str) -> dict:
    """ The function reads input loadings.txt file and creates dict with zones' numbers,
    start materials for each fuel assembly and also start loadings
    """
    cells_dict = {}
    cells_order = ['cell_2_2', 'cell_2_3', 'cell_2_4', 'cell_2_5', 'cell_3_2', 'cell_3_3', 'cell_3_4', 'cell_3_5',
                   'cell_4_2', 'cell_4_3', 'cell_4_4', 'cell_4_5', 'cell_5_2', 'cell_5_3', 'cell_5_4', 'cell_5_5']
    cells_iterator = iter(cells_order)
    with open(loadings_file, 'r') as file:
        reading_start_materials = False
        reading_start_loadings = False
        string_number_in_table = 2
        for line in file:
            if line.startswith('#'):
                continue
            if line.startswith('Start mater'):
                reading_start_materials = True
                continue
            if line.startswith('Start loadings'):
                reading_start_loadings = True
                continue
            if reading_start_materials:
                if string_number_in_table > 5:
                    reading_start_materials = False
                    continue
                assert line.split()[0].isdigit(), 'this line should contain only numbers'
                cells_dict[f"cell_2_{string_number_in_table}"], \
                cells_dict[f"cell_3_{string_number_in_table}"], \
                cells_dict[f"cell_4_{string_number_in_table}"], \
                cells_dict[f"cell_5_{string_number_in_table}"] = \
                    {'zones_numbers': []}, {'zones_numbers': []}, {'zones_numbers': []}, {'zones_numbers': []}
                cells_dict[f"cell_2_{string_number_in_table}"]['zones_numbers'], \
                cells_dict[f"cell_3_{string_number_in_table}"]['zones_numbers'], \
                cells_dict[f"cell_4_{string_number_in_table}"]['zones_numbers'], \
                cells_dict[f"cell_5_{string_number_in_table}"]['zones_numbers'] = \
                    map(lambda x: np.arange(int(x), int(x) + 2160), line.split())
                string_number_in_table += 1
                continue
            if reading_start_loadings:
                # line for comments
                if line.startswith('#'):
                    continue
                else:
                    cells_dict[next(cells_iterator)].update(fuel_loadings=np.array(list(map(float, line.split()))))
                    continue
    return cells_dict


def add_material_from_pdc_for_burn_up(file_to_read: str,
                                      materials: list,
                                      dict_of_results: dict,
                                      nuclides: list = ['u235'],
                                      ) -> dict:
    """ Adding nuclear densities from chosen pdc file to already existing dictionary
    """

    dict_of_results['N'] = []
    with open(file_to_read, 'r') as file:
        scanning = False
        for line in file:
            if line.split()[0] == 'MATR' and int(line.split()[1]) in materials:
                matr_number = line.split()[1]
                scanning = True
                continue
            if (line.split()[0] == 'MATR' and int(line.split()[1]) not in materials) or line.startswith('stop'):
                scanning = False
                continue
            if scanning:
                nuclide = line.split()[0]
                if nuclide in list(map(lambda x: x.upper(), nuclides)):
                    adens = line.split()[1]
                    dict_of_results['N'].append(float(adens))
        dict_of_results['N'] = np.array(dict_of_results['N'])
        return dict_of_results





def add_material_from_pdc_for_prediction(pdc_file_to_read: str,
                                         materials: list,
                                         nuclides: list = ['u235', 'u238', 'pu39', 'xe35', 'sm49']) -> dict:
    """ Adding chosen materials and nuclear densities from pdc files for prediction
    """
    dict_of_results = {}
    for matr_number in materials:
        for nuclide in nuclides:
            dict_of_results[f'{nuclide} in mat{matr_number}'] = []
    with open(pdc_file_to_read, 'r') as pdc_file:
        scanning=False
        for line in pdc_file:
            if line.split()[0] == 'MATR' and int(line.split()[1]) in materials:
                matr_number = line.split()[1]
                scanning = True
                continue
            if (line.split()[0] == 'MATR' and int(line.split()[1]) not in materials) or line.startswith('stop'):
                scanning = False
                continue
            if scanning:
                nuclide = line.split()[0]
                if nuclide in list(map(lambda x: x.upper(), nuclides)):
                    adens = line.split()[1]
                    dict_of_results[f'{nuclide.lower()} in mat{matr_number}'].append(adens)
    for key, value in dict_of_results.items():
        # в 1й топливной зоне всегда содержится 235u, в то время как в твс с свежим топливом отсутствуют pu, xe и sm,
        # поэтому данные ключи необходимо заполнить нулями
        if len(value) != len(dict_of_results['u235 in mat15563']) and key != 'ampule':
            dict_of_results[key].append('0')
    return dict_of_results





def add_material_from_pdc_for_table(fin_file_to_read: str,
                                    pdc_file_to_read: str,
                                    materials: list,
                                    nuclides: list = ['u235', 'u238', 'pu39', 'xe35', 'sm49'],
                                    dict_of_results=None) -> dict:
    """ Adding chosen materials and nuclear densities from pdc files
    """
    if dict_of_results is None:
        dict_of_results = {}
        for matr_number in materials:
            for nuclide in nuclides:
                dict_of_results[f'{nuclide} in mat{matr_number}'] = []
        dict_of_results['Keff'] = []
        dict_of_results['ampule'] = []
    with open(fin_file_to_read, 'r') as fin_file, open(pdc_file_to_read, 'r') as pdc_file:
        for line in fin_file:
            if line.startswith(' Keff comb.'):
                dict_of_results['Keff'].append(line.split()[3])
        scanning = False
        for line in pdc_file:
            if line.split()[0] == 'MATR' and int(line.split()[1]) in materials:
                matr_number = line.split()[1]
                scanning = True
                continue
            if (line.split()[0] == 'MATR' and int(line.split()[1]) not in materials) or line.startswith('stop'):
                scanning = False
                continue
            if scanning:
                nuclide = line.split()[0]
                if nuclide in list(map(lambda x: x.upper(), nuclides)):
                    adens = line.split()[1]
                    dict_of_results[f'{nuclide.lower()} in mat{matr_number}'].append(adens)
    for key, value in dict_of_results.items():
        # в 1й топливной зоне всегда содержится 235u, в то время как в твс с свежим топливом отсутствуют pu, xe и sm,
        # поэтому данные ключи необходимо заполнить нулями
        if len(value) != len(dict_of_results['u235 in mat15563']) and key != 'ampule':
            dict_of_results[key].append('0')
    return dict_of_results


def add_material_from_pdc_for_table_avg_fe(fin_file_to_read: str,
                                           pdc_file_to_read: str,
                                           materials: list,
                                           nuclides: list = ['u235', 'u238', 'pu39', 'xe35', 'sm49'],
                                            dict_of_results=None) -> dict:
    """ Adding chosen materials and nuclear densities from pdc files
    """
    if dict_of_results is None:
        dict_of_results = {}
        for matr_number in materials:
            for nuclide in nuclides:
                dict_of_results[f'{nuclide} in mat{matr_number}'] = []
        dict_of_results['Keff'] = []
        dict_of_results['ampule'] = []
    with open(fin_file_to_read, 'r') as fin_file, open(pdc_file_to_read, 'r') as pdc_file:
        for line in fin_file:
            if line.startswith(' Keff comb.'):
                dict_of_results['Keff'].append(line.split()[3])
        scanning = False
        for line in pdc_file:
            if line.split()[0] == 'MATR' and int(line.split()[1]) in materials:
                matr_number = line.split()[1]
                scanning = True
                continue
            if (line.split()[0] == 'MATR' and int(line.split()[1]) not in materials) or line.startswith('stop'):
                scanning = False
                continue
            if scanning:
                nuclide = line.split()[0]
                if nuclide in list(map(lambda x: x.upper(), nuclides)):
                    adens = line.split()[1]
                    dict_of_results[f'{nuclide.lower()} in mat{matr_number}'].append(adens)
    for key, value in dict_of_results.items():
        # в 1й топливной зоне всегда содержится 235u, в то время как в твс с свежим топливом отсутствуют pu, xe и sm,
        # поэтому данные ключи необходимо заполнить нулями
        if len(value) != len(dict_of_results['u235 in mat15563']) and key != 'ampule':
            dict_of_results[key].append('0')
    return dict_of_results


def wolfram_block_identifier(mcu_input_file: str):
    n_line = 350000
    ampules_cells = ['RI64', 'RI73', 'MH64', 'MH74', 'RI83']
    with open(mcu_input_file, 'r') as file:
        lines = islice(file, n_line, None)
        scanning = False
        for line in lines:
            if line.startswith('NET    L1'):
                scanning = True
                continue
            if scanning:
                if line.startswith('END'):
                    break
                else:
                    if line.startswith('T04'):
                        ampule_name = line.split()[6]
                        if ampule_name in ampules_cells:
                            return 1
                        else:
                            return 0
                    else:
                        continue


def add_material_from_file(file_to_read: str, materials: list, nuclides: list, dict_of_results=None) -> dict:
    """Adding chosen materials and nuclear densities from var file
    """

    if dict_of_results is None:
        dict_of_results = {'MATR': [], 'pdc': [], 'N': [], 'nuclide': []}

    with open(file_to_read, 'r') as file:
        scanning = False
        for line in file:
            if line.split()[0] == 'MATR' and int(line.split()[1]) in materials:
                matr_number = line.split()[1]
                scanning = True
                continue
            if line.split()[0] == 'MATR' and int(line.split()[1]) not in materials:
                scanning = False
                continue
            if scanning:
                nuclide = line.split()[0]
                if nuclide in list(map(lambda x: x.upper(), nuclides)):
                    adens = line.split()[1]
                    dict_of_results['MATR'].append(matr_number)
                    dict_of_results['pdc'].append('var_file')
                    dict_of_results['N'].append(adens)
                    dict_of_results['nuclide'].append(nuclide)
            if line.startswith('END'):
                break
        return dict_of_results


def rez_reader(rez_file: str, output_dict: dict, materials: list):
    """Extracting volumes from rez_file and writing them to output_dict
    """

    with open(rez_file, 'r') as file_to_read:
        scanning = False
        output_dict['volume'] = []
        for line in file_to_read:
            if line.startswith(' Material Type'):
                scanning = True
                continue
            if scanning:
                if line.split()[0].isdigit():
                    if int(line.split()[0]) in materials:
                        output_dict['volume'].append(line.split()[2])
                if line.split()[0] == str(np.max(materials)):
                    break
        output_dict['volume'] = np.array(output_dict['volume']).astype('float32')


def average_burn_up(volumes: np.array, loadings: np.array, current_concentrations: np.array,
                    n_zones_in_tube: int = 360, n_av: object = 0.6023, a_u235: object = 235.043929) -> float:
    """
    Calculates average burn_up in the chosen volumes
    """
    fuel_elements_volumes = []
    for i in range(0, volumes.size, 360):
        fuel_elements_volumes.append(np.sum(volumes[i: i + 360]))
    initial_concentrations = loadings * n_av / a_u235 / fuel_elements_volumes
    # assert(initial_concentrations.repeat(n_zones_in_tube))
    burn_ups = (initial_concentrations.repeat(
        n_zones_in_tube) - current_concentrations) / initial_concentrations.repeat(n_zones_in_tube)
    avg_burn_up = np.sum((burn_ups * volumes)) / np.sum(volumes)
    max_burn_up = np.max(burn_ups)
    min_burn_up = np.min(burn_ups)
    return avg_burn_up, max_burn_up, min_burn_up

# def loadings_reader_and_changer()
