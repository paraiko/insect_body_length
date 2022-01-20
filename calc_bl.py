import json
import sys
import pandas as pd
import numpy as np
from itertools import combinations
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import os
from pathlib import Path
import cv2
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
    for root, subdirs, files in os.walk(jsonPath):
        for fn in files:
            # todo: Add magic to make the script safe, for now just assume the files are there, crash bigtime if not.
            jsonF = os.path.join(root, fn)

            # process all json files
            if fn.endswith('.json'):
                print("processing: " + jsonF)
                # Split the name on "_" to separate NOUS id and original filename.
                fnSplits = fn.split('_')
                maxI = len(fnSplits)-1
                origImgF = ""
                # Rebuild original filename
                for i in range(0, maxI):
                    if i == 0:
                        origImgF = fnSplits[i]
                    else:
                        origImgF += "_" + fnSplits[i]
                print(origImgF)

                # parse the json annotations into a huge dict.
                # todo: add checks on validity and success.
                with open(jsonF) as f:
                    annot = json.load(f)

                # get the nous id and the image id for the image/annotation combination from the json
                nousId = annot.get('id')
                imgId = annot.get('image_id')

                # remove the extension from the name (Path.stem()) and set the Json file path \
                # ImgBaseName = imgPath + Path(jsonF).stem

                # Reconstruct the image filename and guess the extension.
                imgBaseName = imgPath + origImgF + "_" + imgId
                img = cv2.imread(imgBaseName + ".jpg")
                # check if image read was successful and try .png if not, etc.
                if not np.any(img):
                    img = cv2.imread(imgBaseName + ".png")
                elif not np.any(img):
                    img = cv2.imread(imgBaseName + ".tif")
                elif not np.any(img):
                    img = cv2.imread(imgBaseName + ".tiff")
                elif not np.any(img):
                    img = cv2.imread(imgBaseName + ".bmp")
                elif not np.any(img):
                    print(" cannot find file fName")
                    break

                print(img.shape)




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


