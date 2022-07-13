import numpy as np
import pandas as pd

from file_extracters import add_material_from_pdc_for_prediction

X = pd.DataFrame(add_material_from_pdc_for_prediction('2021-09b.PDC_B0', materials=np.arange(15563, 50123)))


