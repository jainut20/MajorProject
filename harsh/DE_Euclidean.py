import random
import cv2
import math
import imageio
from skimage import measure
from skimage.metrics import structural_similarity as ssim
import pickle
import numpy as np
import os
import shutil
import time
from matplotlib import pyplot as plt
for filename in os.listdir('output1/'):
    filepath = os.path.join('output1/', filename)
    try:
        shutil.rmtree(filepath)
    except OSError:
        os.remove(filepath)

list = os.listdir("temp/")
def help_init():
    READ_LOCATION = "temp/_"
    #start_time1 = time.time()
    with open("test.txt", "rb") as fp:   # Unpickling
        b = pickle.load(fp)
    out=[]
    start=1
    mid=2
    end=3
    im1 = cv2.imread(READ_LOCATION + str(start) + ".jpg",0)
    im2 = cv2.imread(READ_LOCATION + str(mid) + ".jpg",0)
    im3 = cv2.imread(READ_LOCATION + str(end) + ".jpg",0)
    a1=ssim(im1,im2)
    a2=ssim(im2,im3)
    b1=cv2.norm(im1, im2, cv2.NORM_L2)
    b2=cv2.norm(im2, im3, cv2.NORM_L2)
    for i in range(3,len(b)):
        mid=i
        end=i+1
        im2 = cv2.imread(READ_LOCATION + str(mid) + ".jpg",0)
        im3 = cv2.imread(READ_LOCATION + str(end) + ".jpg",0)
        a1=a2
        a2=ssim(im2,im3)
        b1=b2
        b2=cv2.norm(im2, im3, cv2.NORM_L2)
        if (a1<a2 and a2>0.5 and b1>b2) or (a1<0.5 and a2<0.5):
            out.append(mid)
    #print("Total time take by helper is : %s seconds" % (time.time() - start_time))    
    print(out)
    return out

out=help_init()
MAX_NUMBER_OF_FRAMES = len(list)-1

TOTAL_KEY_FRAMES = len(out)

STOPPING_ITERATION = 15

NUMBER_OF_NP_CANDIDATES = len(out)

# Location to read images from.
# NOTE: "_" is used to follow a naming convention
# eg. _20.jpg, _21.jpg etc...
READ_LOCATION = "temp/_"

# Location to write GIF images to.
WRITE_BUFFER_LOCATION = "output1/"

# Population matrix.
NP = []

# Mutation vector.
MV = []

# Trail vector.
TV = []

# Scale factor.
F = 0.9

# Cr probability value.
Cr = 0.6

# Calculate AED for a chromosome.
def getAED( KF ):
    ED_sum = 0
    for i in range(1, TOTAL_KEY_FRAMES - 1):
        while True:
            try:
                im1 = cv2.imread(READ_LOCATION + str(KF[i]) + ".jpg",0)
                im2 = cv2.imread(READ_LOCATION + str(KF[i+1]) + ".jpg",0)
                ED_sum += cv2.norm(im1, im2, cv2.NORM_L2)
            except:
                print(i, KF, KF[i], KF[i+1])
            break
    return ED_sum/(TOTAL_KEY_FRAMES - 1)

# INITIALISATION : Generates population NP of 10 parent vectors (and AEDs).
def initialize_NP():
    NP.append(out)
    NP[-1].append(getAED(NP[-1]))
    print(NP[-1])
    for i in range(NUMBER_OF_NP_CANDIDATES-1):
        NP.append(sorted(random.sample(range(1, MAX_NUMBER_OF_FRAMES+1), TOTAL_KEY_FRAMES)))
        NP[-1].append(getAED(NP[-1]))
        print(NP[-1])

# MUTATION
def mutation(num):
    R = random.sample(NP,3)
    global MV
    MV[:] = []
    MV_value = 0
    for i in range(TOTAL_KEY_FRAMES):
        MV_value = int(NP[num][i] + F*(R[1][i] - R[2][i]))
        if(MV_value < 1):
            MV.append(1)
        elif(MV_value > MAX_NUMBER_OF_FRAMES):
            MV.append(MAX_NUMBER_OF_FRAMES)
        else:
            MV.append(MV_value)
    MV.sort()
    MV.append(getAED(MV))

# CROSSOVER (uniform crossover with Cr = 0.6).
def crossover(parent, mutant):
    print("mutant: ", mutant)
    print("parent: ", parent)
    for j in range(TOTAL_KEY_FRAMES) :
        if(random.uniform(0,1) < Cr) :
            TV.append(mutant[j])
        else:
            TV.append(parent[j])
    TV.sort()
    TV.append(getAED(TV))
    print("TV    : ", TV)

# SELECTION : Selects offspring / parent based on higher ED value.
def selection(parent, trail_vector):
    if(trail_vector[-1] > parent[-1]):
        parent[:] = trail_vector
        print("yes", parent)
    else:
        print("no")

# bestParent returns the parent with then maximum ED value.
def bestParent(population):
    Max_AED_value = population[0][-1]
    Best_Parent_Index = population[0]
    for parent in population:
        if (parent[-1] > Max_AED_value):
            Max_AED_value = parent[-1]
            Best_Parent_Index = parent
    return Best_Parent_Index



start_time = time.time()
initialize_NP()
x=[]
y=[]
for GENERATION in range(STOPPING_ITERATION):
    temp=[]
    for i in range(NUMBER_OF_NP_CANDIDATES):
        print("---------------------", "PARENT:", i+1 , "GENERATION:", GENERATION+1, "---------------------")
        mutation(i)
        crossover(NP[i], MV)
        selection(NP[i], TV)
        print(NP[i])
        temp.append(NP[i][-1])
        TV[:] = []
        print("")
    x.append(GENERATION)
    y.append(max(temp))
    print("")
best_parent = bestParent(NP)
best_parent.pop()
print("best solution is: ", best_parent)
with open("test.txt", "rb") as fp:   # Unpickling
    b = pickle.load(fp)
timings = []
for frame_number in best_parent[:-1]:
        cv2.imwrite(WRITE_BUFFER_LOCATION + str(frame_number) + ".jpg",imageio.imread(READ_LOCATION + str(frame_number) + '.jpg'))
        timings.append(b[frame_number-1])
print("Total time take by DE_Eucledian is : %s seconds" % (time.time() - start_time))
print("Video index timings : ",timings)
update_timings = []
for i in range(len(best_parent)-1):
    start=best_parent[i]
    end=best_parent[i+1]
    im1 = cv2.imread(READ_LOCATION + str(start) + ".jpg",0)
    im2 = cv2.imread(READ_LOCATION + str(end) + ".jpg",0)
    flag=0
    for j in range(1,end-start-1):
        temp1=cv2.imread(READ_LOCATION + str(start+j) + ".jpg",0)
        diff1 = cv2.absdiff(im1, temp1)
        non_zero_count1 = np.count_nonzero(diff1)
        diff2 = cv2.absdiff(im2, temp1)
        non_zero_count2 = np.count_nonzero(diff2)
        if non_zero_count1>non_zero_count2:
            update_timings.append(b[start+j-1])
            flag=1
            break
    if flag==0:
        update_timings.append(b[start-1])
print("Update Video index timings : ",update_timings)
with open("test2.txt", "wb") as fp:   #Pickling
    pickle.dump(update_timings, fp)
plt.plot(x,y)
# naming the x axis
plt.xlabel('Generation')
# naming the y axis
plt.ylabel('Eucledian Distance')
plt.title('DE_Eucledian')
plt.savefig("eu.png")