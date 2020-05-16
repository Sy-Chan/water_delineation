import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
##if you want to output as image grid truly suggest you to study matplotlib
##from esri website:"...one-cell sink Is Next To the physical edge Of the raster Or has at least one NoData cell As a neighbor,
##it Is Not filled due To insufficient neighbor information.
##With the Force all edge cells to flow outward parameter in the default unchecked setting (NORMAL in Python), a cell at the edge of the surface raster will flow
##toward the inner cell with the steepest drop in z-value. If the drop is less than or equal to zero, the cell will flow out of the surface raster.
##for the streamline, you will have to key in a threshold value

#D8 algorithm
def D8(raster,flow_inward=True):
    highest = np.max(raster)
    lowest = np.min(raster)
    row1=[highest] * len(raster[0])
    min1=np.where(raster==lowest)
    row2=row1.copy()
    row2[int(min1[1])]=lowest
    arr = np.vstack((row1,raster,row2))
    arr=np.insert(arr, [0], highest, axis=1)
    raster=np.insert(arr, [len(raster[0])+1], highest, axis=1)
    #assume all edge cell flow inward, except lowest point as outlets
    #thus add 2 rows and columns with highest value surround the raster, except the one with lowest value
    
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
#flow accumulation
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


#Find the pour point from flow accumulation
def PourPoint(flow):
    i= np.argmax(flow)
    pt = np.max(flow)
    return pt

#find the streamline
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

#plot function is to visualize the value in grid with color
def plot(arr,color='gray'):

    fig, ax = plt.subplots()
    #gray or gray_r
    #cmap indicate the color of grid
    #try refer https://matplotlib.org/2.0.2/examples/color/colormaps_reference.html for more information
    im = ax.imshow(arr,cmap=color)
    
    # Loop over data dimensions and create text annotations.
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            text = ax.text(j, i, arr[i, j],
                           ha="center", va="center", color="r")
            #color here is the text color
            # more info in:https://matplotlib.org/tutorials/colors/colors.html

    ax.set_title(input("give a title to your plot: "))
    fig.tight_layout()
    plt.show()
    
raster = np.array([
    [78,72,69,71,58,49],
    [74,67,56,49,46,50],
    [69,53,44,37,38,48],
    [64,58,55,22,31,24],
    [68,61,47,21,16,19],
    [74,53,34,12,11,12]
    ])

plot(raster)
print('Raster =','\n',raster,'\n')
arr = D8(raster)
plot(arr,'gist_rainbow_r')
print('Flow Direction =','\n',arr,'\n')
flow=flow(arr)
plot(flow)
print('Flow Accumulation =','\n',flow,'\n')
pt = PourPoint(flow)
print('Pour Point =',pt,'\n')
stream = stream(flow, pt)
plot(stream)
print('Streamline =','\n',stream)
