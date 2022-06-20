import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from file_extracters import add_material_from_pdc_for_burn_up, rez_reader, average_burn_up, loadings_file_reader
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator


class App(tk.Tk):
    def __init__(self):
        self.pdc_file = None
        self.rez_file = None
        self.loadings_file = None

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

        pdc_filename, rez_filename, loadings_filename = None, None, None

    def show_error(self):
        msg = "Не все файлы выбраны"
        mb.showerror("Ошибка", msg)

    def choose_pdc_file(self):
        pdc_types = []
        for perhaps_number_of_pdc in range(100):
            pdc_types.append(f'.PDC_B{perhaps_number_of_pdc}')
        filetypes = (("файл pdc", pdc_types),
                     ("Любой", "*"))
        self.pdc_file = fd.askopenfilename(title="Открыть файл", initialdir="/",
                                          filetypes=filetypes)


    def choose_rez_file(self):
        filetypes = (("файл rez", '.REZ'),
                     ("Любой", "*"))
        self.rez_file = fd.askopenfilename(title="Открыть файл", initialdir="/",
                                          filetypes=filetypes)


    def choose_loading_file(self):
        filetypes = (("файл txt", '.txt'),
                     ("Любой", "*"))
        self.loadings_file = fd.askopenfilename(title="Открыть файл", initialdir="/",
                                               filetypes=filetypes)


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

            print(some_dict)
            burn_ups = np.zeros((6, 8))
            for key, value in some_dict.items():
                burn_ups[int(key[-1]) - 1][int(key[-3]) - 1] = value['burn_up'][0]
            burn_ups = np.around(burn_ups * 100, decimals=1)
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
