from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import io
import base64

a = Flask(__name__)

with open('model.pkl', 'rb') as b:
    c = pickle.load(b)

@a.route('/', methods=['GET', 'POST'])
def d():
    if request.method == 'POST':
        e = float(request.form['longitude'])
        f = float(request.form['latitude'])
        g = float(request.form['rainfall'])
        
        h = i(e, f, g)
        j = k(e, f, g, h)
        l = m(j)
        
        return render_template('index.html', prediction=h, img_data=l)
    
    return render_template('index.html', prediction=None, img_data=None)

def i(e, f, g):
    return c.predict([[e, f, g]])[0]

def k(e, f, g, h):
    a = pd.DataFrame({
        'longitude': np.random.uniform(-180, 180, size=1000),
        'latitude': np.random.uniform(-90, 90, size=1000),
        'rainfall': np.random.uniform(0, 200, size=1000),
        'flood': np.random.choice([0, 1], size=1000)
    })
    a['flood'] = (a['rainfall'] > 50).astype(int)
    b = gpd.GeoDataFrame(a, geometry=gpd.points_from_xy(a.longitude, a.latitude))
    
    c = pd.DataFrame({
        'longitude': [e],
        'latitude': [f],
        'rainfall': [g],
        'flood': [h]
    })
    d = gpd.GeoDataFrame(c, geometry=gpd.points_from_xy(c.longitude, c.latitude))
    
    fig, ax = plt.subplots(figsize=(10, 5))
    b.plot(ax=ax, column='flood', cmap='Blues', legend=True, markersize=5, alpha=0.5)
    d.plot(ax=ax, color='red', markersize=100, label='Input Location', alpha=1.0)
    ax.set_title('Flood Risk Map')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.legend()
    
    return fig

def m(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode('utf-8')

if __name__ == '__main__':
    a.run(debug=True)