import json
import pandas as pd
import numpy as np
from itertools import combinations
from scipy import ndimage
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import shapely
from shapely.algorithms import polylabel


#fn = 'input/annotation/zv_001_001_61e86ab00caa22145f34004e.json'
fn = 'input/annotation/zv_001_002_61e86ac00caa22145f34004f.json'

with open(fn) as f:
    annot = json.load(f)

# todo
# get the original filename from the filemame-path for reference


# get the nous id for the image/annotation combination
nousId = annot.get('id')

# count the nr of segmentation annotations in the file
nrAnnot = (len(annot['data']))

verticesx = pd.DataFrame(annot.get('data')[0].get('shapes')[0].get('geometry')['points'])
print(verticesx)
if nrAnnot == 1:
    #labelId = each.get('id')
    vertices = pd.DataFrame(annot.get('data')[0].get('shapes')[0].get('geometry')['points'])
    nv = np.array(vertices)
    #print(nv)
    current_max = 0
    v1 = [0, 0]
    v2 = [0, 0]
    for a, b in combinations(np.array(vertices), 2):
        current_distance = np.linalg.norm(a - b)
        if current_distance > current_max:
            current_max = current_distance
            v1 = a
            v2 = b
            #print(str(a)+","+str(b))
    print(current_max)
    print(v1)
    print(v2)

    test = ndimage.center_of_mass(np.array(vertices))
    print(test)

    #p = Polygon([[0,0], [0,1], [1,1], [0,1]])
    p = Polygon(nv)
    centroid = p.centroid
    print(centroid)
    vm = np.array(centroid)
    x, y = zip(v1, vm, v2)
    plt.scatter(x,y)
    plt.show()

elif nrAnnot > 1:
    # todo Ideally there is only one, otherwise assume the biggest (by polygon vertices count) is the correct one.
    # for now just take the first one... :-(
    print("blaat")
else:
    print("no annotations")
    # todo some magic here

# print(data[1].get('id'))
# print(data[1].get('shapes'))

# blaat = annot.get('data', {}).get('id')
## take the first  (for now, later parse all of them)

# result = dict.items(dict.itemsannot)
# print(blaat)

#df2 = pd.json_normalize(annot, record_path=['data'])
#df2 = pd.json_normalize(annot, max_level=8)
#df3 = annot.get('data')
#df4 = df3.get('shapes')

#print(df4)

