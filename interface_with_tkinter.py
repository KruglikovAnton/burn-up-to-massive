import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from pathlib import Path
from file_extracters import add_material_from_pdc_for_burn_up, \
    rez_reader, average_burn_up, loadings_file_reader, add_material_from_pdc_for_prediction
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import pickle



class App(tk.Tk):
    def __init__(self):
        self.pdc_file = None
        self.rez_file = None
        self.loadings_file = None
        self.ampule_check = 0

        super().__init__()

        btn_pdc_file = tk.Button(self, text="Выбрать pdc файл",
                                 command=self.choose_pdc_file)
        btn_pdc_file.pack(padx=60, pady=10)

        btn_rez_file = tk.Button(self, text="Выбрать rez файл",
                                 command=self.choose_rez_file)
        btn_rez_file.pack(padx=60, pady=10)

        btn_loadings_file = tk.Button(self, text="Выбрать файл с загрузками",
                                      command=self.choose_loading_file)
        btn_loadings_file.pack(padx=60, pady=10)

        btn_burn_it_file = tk.Button(self, text="JUST BURN IT",
                                     command=self.just_burn_it)
        btn_burn_it_file.pack(padx=60, pady=10)

        ampule_check = tk.Checkbutton(self,
                                      text='Ампула в 6-4',
                                      variable=self.ampule_check,
                                      onvalue=1, offvalue=0)
        ampule_check.pack()

    def show_error(self):
        msg = "Не все файлы выбраны"
        mb.showerror("Ошибка", msg)

    def choose_pdc_file(self):
        pdc_types = []
        for perhaps_number_of_pdc in range(100):
            pdc_types.append(f'.PDC_B{perhaps_number_of_pdc}')
        filetypes = (("файл pdc", pdc_types),
                     ("Любой", "*"))
        self.pdc_file = Path(fd.askopenfilename(title="Открыть файл", initialdir="/",
                                           filetypes=filetypes)).absolute()
        print(self.pdc_file)

    def choose_rez_file(self):
        filetypes = (("файл rez", '.REZ'),
                     ("Любой", "*"))
        self.rez_file = Path(fd.askopenfilename(title="Открыть файл", initialdir="/",
                                           filetypes=filetypes)).absolute()

    def choose_loading_file(self):
        filetypes = (("файл txt", '.txt'),
                     ("Любой", "*"))
        self.loadings_file = Path(fd.askopenfilename(title="Открыть файл", initialdir="/",
                                                filetypes=filetypes)).absolute()

    def just_burn_it(self):
        # print(pdc_filename, rez_filename, loadings_filename)
        if not all([self.pdc_file, self.rez_file, self.loadings_file]):
            self.show_error()
        else:
            some_dict = loadings_file_reader(self.loadings_file)

            for cell in some_dict.keys():
                print(cell)
                rez_reader(rez_file=self.rez_file,
                           output_dict=some_dict[cell],
                           materials=some_dict[cell]['zones_numbers'])
                add_material_from_pdc_for_burn_up(file_to_read=self.pdc_file,
                                                  materials=some_dict[cell]['zones_numbers'],
                                                  dict_of_results=some_dict[cell])
                some_dict[cell]['burn_up'] = average_burn_up(volumes=some_dict[cell]['volume'],
                                                             loadings=some_dict[cell]['fuel_loadings'],
                                                             current_concentrations=some_dict[cell]['N'])
                X = pd.DataFrame(
                    add_material_from_pdc_for_prediction(
                        '2021-09b.PDC_B0',
                        materials=np.arange(15563, 50123))
                ).astype(float)

            NUM_ZONES_PER_FE = 360

            df_avg_conc = pd.DataFrame()
            for nuclide in ['u235', 'u238', 'pu39', 'xe35', 'sm49']:
                for num_matr in range(15563, 50123, NUM_ZONES_PER_FE):
                    df_avg_conc[
                        f'avg_c_in_{num_matr}_to_{num_matr + NUM_ZONES_PER_FE - 1}_for_{nuclide}'] = X.filter(
                        items=[f'{nuclide} in mat{num}' for num in range(num_matr, num_matr + NUM_ZONES_PER_FE)],
                        axis=1).apply(
                        axis=1, func=np.mean)

            df_avg_conc['ampule'] = self.ampule_check

            model = pickle.load(open('model.pkl', 'rb'))
            y_pred = model.predict(df_avg_conc)

            print(some_dict)
            burn_ups = np.zeros((6, 8))
            for key, value in some_dict.items():
                burn_ups[int(key[-1]) - 1][int(key[-3]) - 1] = value['burn_up'][0]
            burn_ups = np.around(burn_ups * 100, decimals=1)
            x_labels = [str(i) for i in range(1, 9)]
            y_labels = [str(i) for i in range(1, 7)]
            fig, ax = plt.subplots()
            im = ax.imshow(burn_ups)
            ax.set_xticks(range(0, 8), labels=x_labels)
            ax.set_yticks(range(0, 6), labels=y_labels)
            for i in range(1, 5):
                for j in range(1, 5):
                    ax.text(j, i, burn_ups[i, j],
                            ha="center", va="center", color="w")

            props = dict(boxstyle='round', facecolor='wheat')
            ax.text(0.65, 0.6,
                    s=f'Reactivity margin \n {y_pred[0]: .2f}%',
                    transform=ax.transAxes,
                    fontsize=14,
                    verticalalignment='top',
                    bbox=props)

            x_minorLocator = AutoMinorLocator(2)
            y_minorLocator = AutoMinorLocator(2)
            ax.xaxis.set_minor_locator(x_minorLocator)
            ax.yaxis.set_minor_locator(y_minorLocator)
            ax.xaxis.tick_top()
            ax.tick_params(length=0, which='both', axis='both')
            ax.grid(which='minor', color="w", linestyle='-', linewidth=1)
            plt.show()
