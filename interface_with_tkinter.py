import tkinter as tk
import tkinter.filedialog as fd
from file_extracters import add_material_from_file, add_material_from_pdc, rez_reader, average_burn_up, loadings_file_reader

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        btn_pdc_file = tk.Button(self, text="Выбрать pdc файл",
                             command=self.choose_pdc_file)
        btn_pdc_file.pack(padx=60, pady=10)
        btn_rez_file = tk.Button(self, text="Выбрать rez файл",
                             command=self.choose_rez_file)
        btn_rez_file.pack(padx=60, pady=10)
        btn_loadings_file = tk.Button(self, text="Выбрать файл с загрузками",
                             command=self.choose_rez_file)
        btn_loadings_file.pack(padx=60, pady=10)




    def choose_pdc_file(self):
        pdc_types = []
        for perhaps_number_of_pdc in range(100):
            pdc_types.append(f'.PDC_B{perhaps_number_of_pdc}')
        filetypes = (("файл pdc", pdc_types),
                     ("Любой", "*"))
        filename = fd.askopenfilename(title="Открыть файл", initialdir="/",
                                      filetypes=filetypes)
        if filename:
            pdc_file = pdc_filename

    def choose_rez_file(self):
        filetypes = (("файл rez", '.REZ'),
                     ("Любой", "*"))
        filename = fd.askopenfilename(title="Открыть файл", initialdir="/",
                                      filetypes=filetypes)
        if filename:
            rez_file = rez_filename

    def choose_loading_file(self):
        filetypes = (("файл rez", '.REZ'),
                     ("Любой", "*"))
        filename = fd.askopenfilename(title="Открыть файл", initialdir="/",
                                      filetypes=filetypes)
        if filename:
            loadings_file = loadings_filename




app = App()
app.mainloop()
