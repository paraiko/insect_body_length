import json
import sys

import pandas as pd
import numpy as np
from itertools import combinations
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import os
from pathlib import Path
#from shapely.algorithms import polylabel

# assign directory
if len(sys.argv) <= 1:
    print("Specify an inputpath as the first argument. \n" + \
          "The script expects a folder <images> with image files \n" + \
          "and a folder <annotations> with NOUS json annotations of those images.")
else:
    inputPath = sys.argv[1]
    print(inputPath)
    imgPath = inputPath + "images/"
    jsonPath = inputPath + "annotation/"

    # iterate over files in imgInputPath
    #os.walk yields tuple with rootpath, subdirs and filenames in path
    # giving file extension
    validExt = ('.png', '.jpg', '.tif', '.bmp')
    for root, subdirs, files in os.walk(imgPath):
        for fn in files:
            # todo for now no magic to make the script safe, just assume the files are there, crash bigtime if not.
            imgF = os.path.join(root, fn)

            # process all image file types
            if fn.endswith(validExt):
                # remove the extension from the name (Path.stem()) and set the Json file path
                jsonF = jsonPath + Path(imgF).stem + ".json"
                print(imgF)
                print(jsonF)
                # todo maybe split the name on "_" to separate NOUS id and original filename.

                with open(jsonF) as f:
                    annot = json.load(f)

                # todo get the original filename from the filename-path for reference

                # get the nous id for the image/annotation combination
                nousId = annot.get('id')

                # count the nr of segmentation annotations in the file
                nrAnnot = (len(annot['data']))

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
                            #print(current_max)
                    print(v1)
                    print(v2)

                    p = Polygon(nv)
                    centroid = p.centroid
                    print(centroid)
                    vm = np.array(centroid)
                    x, y = zip(v1, vm, v2)
                    plt.scatter(x, y)
                    plt.show()

                elif nrAnnot > 1:
                    # todo ideally there is only one, otherwise assume the biggest (by polygon vertices count) is the correct one.
                    # for now just take the first one... :-(
                    print("more than 1 annotation")
                else:
                    print("no annotations")
                    # todo some magic here


