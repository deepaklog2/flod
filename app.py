import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

a = 1000
b = np.random.uniform(0, 200, size=a)
c = (b > 50).astype(int)
d = pd.DataFrame({
    'rainfall': b,
    'flood': c
})
e = d[['rainfall']]
f = d['flood']
g = RandomForestClassifier(n_estimators=100, random_state=42)
g.fit(e, f)
with open('model.pkl', 'wb') as h:
    pickle.dump(g, h)