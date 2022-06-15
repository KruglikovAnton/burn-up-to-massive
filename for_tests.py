# file for manual test and time estimation
import numpy as np
from matplotlib import pyplot as plt
import time
from matplotlib.ticker import AutoMinorLocator


t1 = time.time()
from file_extracters import rez_reader, loadings_file_reader, add_material_from_pdc_for_burn_up, average_burn_up

some_dict = loadings_file_reader('C:\WORK_JOB\simple_model_periodic\loadings.txt')

for cell in some_dict.keys():
    print(cell)
    rez_reader(rez_file='C:\WORK_JOB\simple_model_periodic\HEU_AZ08.REZ',
               output_dict=some_dict[cell],
               materials=some_dict[cell]['zones_numbers'])
    add_material_from_pdc_for_burn_up(file_to_read=r'C:\2022-05.pdc',
                                      materials=some_dict[cell]['zones_numbers'],
                                      dict_of_results=some_dict[cell])
    some_dict[cell]['burn_up'] = average_burn_up(volumes=some_dict[cell]['volume'],
                                                 loadings=some_dict[cell]['fuel_loadings'],
                                                 current_concentrations=some_dict[cell]['N'])

burn_ups = np.zeros((6, 8))
for key, value in some_dict.items():
    burn_ups[int(key[-1]) - 1][int(key[-3]) - 1] = value['burn_up'][0]
t2 = time.time()
print(f'time is {t2-t1}')
burn_ups = np.around(burn_ups*100, decimals=1)
print(burn_ups)
x_labels = [str(i) for i in range(1, 9)]
y_labels = [str(i) for i in range(1, 7)]
fig, ax = plt.subplots()
im = ax.imshow(burn_ups)
ax.set_xticks(range(0, 8), labels=x_labels)
ax.set_yticks(range(0, 6), labels=y_labels)
for i in range(1, 5):
    for j in range(1, 5):
        text = ax.text(j, i, burn_ups[i, j],
                       ha="center", va="center", color="w")


x_minorLocator = AutoMinorLocator(2)
y_minorLocator = AutoMinorLocator(2)
ax.xaxis.set_minor_locator(x_minorLocator)
ax.yaxis.set_minor_locator(y_minorLocator)
ax.xaxis.tick_top()
ax.tick_params(length=0, which='both', axis='both')
ax.grid(which='minor', color="w", linestyle='-', linewidth=1)
plt.show()
