import math
import numpy as np
##if you want to output as image grid truly suggest you to study matplotlib
##from esri website:"...one-cell sink Is Next To the physical edge Of the raster Or has at least one NoData cell As a neighbor, it Is Not filled due To insufficient neighbor information.
##for the streamline, you will have to key in a threshold value


def D8(raster):
    arr = []
    row = []
    for i in range(1,len(raster)-1):
        row = []
        for j in range(1,len(raster[i])-1):
                    
            A = raster[i][j]#center data
            B = raster[i][j + 1]
            C = raster[i + 1][j + 1]
            D = raster[i + 1][j]
            E = raster[i + 1][j - 1]
            F = raster[i][j - 1]
            G = raster[i - 1][j - 1]
            H = raster[i - 1][j]
            I = raster[i - 1][j + 1]
            # assume distance = 1
            slope = A - B
            max_slp = slope  #define the value for max_slp
            dirt = 1 #east

            slope = (A - C) / math.sqrt(2)
            if slope > max_slp:
                max_slp = slope
                dirt = 2 #southeast

            slope = A - D
            if slope > max_slp:
                max_slp = slope
                dirt = 4 #south

            slope = (A - E) / math.sqrt(2)
            if slope > max_slp:
                max_slp = slope
                dirt = 8 #southwest

            slope = A - F
            if slope > max_slp:
                max_slp = slope
                dirt = 16 #west

            slope = (A - G) / math.sqrt(2)
            if slope > max_slp:
                max_slp = slope
                dirt = 32 #northwest

            slope = A - H
            if slope > max_slp:
                max_slp = slope
                dirt = 64 #north

            slope = (A - I) / math.sqrt(2)
            if slope > max_slp:
                max_slp = slope
                dirt = 128 #northeast
            row.append(dirt)
        arr.append(row)
    arr = np.array(arr)
    return arr

def flow(arr):
    arr1= np.multiply(arr,0)
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            try:
                if arr[i][j] == 1:
                    arr1[i][j+1] = arr1[i][j+1] + 1 + arr1[i][j]
                elif arr[i][j] == 2:
                    arr1[i+1][j+1] = arr1[i+1][j+1]+1 + arr1[i][j]
                elif arr[i][j] == 4:
                    arr1[i+1][j] = 1 + arr1[i][j] + arr1[i+1][j]
                elif arr[i][j] == 8:
                    arr1[i+1][j-1] = 1 + arr1[i][j]+arr1[i+1][j-1]
                elif arr[i][j] == 16:
                    arr1[i][j-1]= 1 + arr1[i][j]+arr1[i][j-1]
                elif arr[i][j] == 32:
                    arr1[i-1][j-1] = 1 + arr1[i][j]+arr1[i-1][j-1]
                elif arr[i][j] == 64:
                    arr1[i-1][j] = 1 + arr1[i][j]+arr1[i-1][j]
                elif arr[i][j] == 128:
                    arr1[i-1][j+1] = 1 + arr1[i][j]+arr1[i-1][j+1]    
            except:
                pass
    return arr1



def PourPoint(flow):
    i= np.argmax(flow)
    pt = np.max(flow)
    return pt

def stream(flow, pt):
    threshold = eval(input("Key in the threshold value:"))
    if threshold > pt:
        print('Threshold value must not exceed pour point, which is:', pt)
        return stream(flow, pt)
    else:
        for i in range(len(flow)):
            for j in range(len(flow[i])):
                if flow[i][j]>threshold:
                    flow[i][j] = 1
                else:
                    flow[i][j]=0
        return flow 
    
raster = np.array([
    [78,72,69,71,58,49],
    [74,67,56,49,46,50],
    [69,53,44,37,38,48],
    [64,58,55,22,31,24],
    [68,61,47,21,16,19],
    [74,53,34,12,11,12]
    ])
print('Raster =','\n',raster,'\n')
arr = D8(raster)
print('Flow Direction =','\n',arr,'\n')
flow=flow(arr)
print('Flow Accumulation =','\n',flow,'\n')
pt = PourPoint(flow)
print('Pour Point =',pt,'\n')
stream = stream(flow, pt)
print('Streanline =','\n',stream)
