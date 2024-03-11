#!/usr/bin/env python
# coding: utf-8

# In[ ]:


pip install opencv-python


# In[ ]:


import numpy as np
import cv2
from matplotlib import pyplot as plt
from skimage import io,color,measure
from scipy import ndimage
img=cv2.imread(r"E:\Second year\SEM 2\DC\Images\base0002.tif",0)
cv2.imshow('image',img)

pixels_to_um=0.5
cropped_img=img[0:300,:]

#step 2
plt.hist(img.flat, bins=200,range=(0,255))


# In[ ]:


ret,thresh=cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)


# In[ ]:


kernel=np.ones((3,3),np.uint8)
eroded=cv2.erode(thresh,kernel,iterations=1)
dilated=cv2.dilate(eroded,kernel,iterations =1)
#cv2.imshow("Threshold Image",thresh)
#cv2.imshow("Dilated Image",dilated)
cv2.waitKey(0)

#converting to binary
mask=dilated==255
#io.imshow(mask[250:280,250:280])

#step4
s=[[1,1,1],[1,1,1],[1,1,1]]
labeled_mask,num_labels=ndimage.label(mask,structure=s)
img2=color.label2rgb(labeled_mask,bg_label=0)
cv2.imshow("coloured labels",img2)
#cv2.waitkey(0)


# In[ ]:


clusters=measure.regionprops(labeled_mask,img)


# In[ ]:


print(clusters[0].perimeter)


# In[ ]:


#step6
propList = ['Area',
            'equivalent_diameter', #Added... verify if it works
            'orientation', #Added, verify if it works. Angle btwn x-axis and major axis.
            'MajorAxisLength',
            'MinorAxisLength',
            'Perimeter',
            'MinIntensity',
            'MeanIntensity',
            'MaxIntensity']   


# In[ ]:


output_file=open('image_measurements.csv','w')
output_file.write((','+",".join(propList)+'\n'))


# In[ ]:


for cluster_props in clusters:
    #output cluster properties to the excel file
    output_file.write(str(cluster_props['Label']))
    for i,prop in enumerate(propList):
        if(prop == 'Area'): 
            to_print = cluster_props[prop]*pixels_to_um**2   #Convert pixel square to um square
        elif(prop == 'orientation'): 
            to_print = cluster_props[prop]*57.2958  #Convert to degrees from radians
        elif(prop.find('Intensity') < 0):          # Any prop without Intensity in its name
            to_print = cluster_props[prop]*pixels_to_um
        else: 
            to_print = cluster_props[prop]     #Reamining props, basically the ones with Intensity in its name
        output_file.write(',' + str(to_print))
    output_file.write('\n')

