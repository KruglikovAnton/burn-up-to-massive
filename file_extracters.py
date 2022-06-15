import numpy as np


def add_material_from_pdc_for_burn_up(file_to_read: str,
                                      materials: list,
                                      dict_of_results: dict,
                                      nuclides: list = ['u235'],
                                      ) -> dict:
    """ Adding nuclear densities from pdc files
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


def add_material_from_pdc_for_table(file_to_read: str, materials: list, nuclides: list = ['u235'],
                                    dict_of_results=None) -> dict:
    """ Adding chosen materials and nuclear densities from pdc files
    """

    if dict_of_results is None:
        dict_of_results = {'MATR': [], 'pdc': [], 'N': [], 'nuclide': []}

    with open(file_to_read, 'r') as file:
        pdc_number = file_to_read[file_to_read.find('.') + 1:]
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
                    dict_of_results['MATR'].append(matr_number)
                    dict_of_results['pdc'].append(pdc_number)
                    dict_of_results['N'].append(adens)
                    dict_of_results['nuclide'].append(nuclide)
        return dict_of_results


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
    """Extracting volumes from rez_file and writing them to output_file
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


def loadings_file_reader(loadings_file: str):
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
                #line for comments
                if line.startswith('#'):
                    continue
                else:
                    cells_dict[next(cells_iterator)].update(fuel_loadings=np.array(list(map(float, line.split()))))
                    continue
    return cells_dict


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
    burn_ups = (initial_concentrations.repeat(n_zones_in_tube) - current_concentrations) / initial_concentrations.repeat(n_zones_in_tube)
    avg_burn_up = np.sum((burn_ups * volumes)) / np.sum(volumes)
    max_burn_up = np.max(burn_ups)
    min_burn_up = np.min(burn_ups)
    return avg_burn_up, max_burn_up, min_burn_up

# def loadings_reader_and_changer()
