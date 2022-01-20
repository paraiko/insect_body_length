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

safeOutputImg = True

# assign directory
if len(sys.argv) <= 1:
    print("Specify an input path as the first argument. \n" + \
          "The script expects a folder <images> with image files \n" + \
          "and a folder <annotations> with NOUS json annotations of those images.")
else:
    inputPath = sys.argv[1]
    print(inputPath)
    imgPath = inputPath + "images/"
    jsonPath = inputPath + "annotation/"

    if safeOutputImg:
        path = imgPath + "output/"
        if not (os.path.exists(path) and os.path.isdir(path)):
            os.mkdir(path)

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
                print(imgBaseName)
                ext = '.jpg'
                imgName = imgBaseName + ext
                img = cv2.imread(imgName)
                # check if image read was successful and try .png if not, etc.
                if not np.any(img):
                    ext = '.png'
                    imgName = imgBaseName + ext
                    img = cv2.imread(imgName)
                elif not np.any(img):
                    ext = '.tif'
                    imgName = imgBaseName + ext
                    img = cv2.imread(imgName)
                elif not np.any(img):
                    ext = '.tiff'
                    imgName = imgBaseName + ext
                    img = cv2.imread(imgName)
                elif not np.any(img):
                    ext = '.bmp'
                    imgName = imgBaseName + ext
                    img = cv2.imread(imgName)
                elif not np.any(img):
                    print(" cannot find file fName")
                    break

                imgY = img.shape[0]
                imgX = img.shape[1]
                imgDim = [imgX, imgY]
                print(imgDim)
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

                    # draw the detect points and lines on the image.
                    print(type(v1))
                    imgDim = np.array(imgDim)
                    v1 = v1 * imgDim
                    v1 = v1.astype(int)
                    vm = vm * imgDim
                    vm = vm.astype(int)
                    v2 = v2 * imgDim
                    v2 = v2.astype(int)

                    newImg = cv2.circle(img, v1, radius=3, color=(0, 0, 255), thickness=-1)
                    newImg = cv2.circle(newImg, vm, radius=3, color=(0, 255, 0), thickness=-1)
                    newImg = cv2.circle(newImg, v2, radius=3, color=(255, 0, 0), thickness=-1)
                    newIMG = cv2.line(newImg, v1, vm, (255, 255, 255), thickness=1)
                    newIMG = cv2.line(newImg, vm, v2, (255, 255, 255), thickness=1)
                    cv2.imshow('with points', newImg)
                    cv2.waitKey(3000)
                    cv2.destroyAllWindows()
                    if safeOutputImg:
                        newImgName = imgPath + "output/" + origImgF + "_" + imgId + len" + ext
                        print('newImgname: '+ newImgName)
                        cv2.imwrite(newImgName, newImg)
                    #plt.scatter(x, y)
                    #plt.show()

                elif nrAnnot > 1:
                    # todo ideally there is only one, otherwise assume the biggest (by polygon vertices count) is the correct one.
                    # for now just take the first one... :-(
                    print("more than 1 annotation")
                else:
                    print("no annotations")
                    # todo some magic here


