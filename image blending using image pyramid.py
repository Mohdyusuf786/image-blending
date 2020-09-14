import cv2
import numpy as np

apple=cv2.imread('apple.copy.jpg')
orange=cv2.imread('orange1.jpg')
apple=cv2.resize(apple, (400,400))
orange=cv2.resize(orange, (400,400))
#to attach to images side by side
apple_orange=np.hstack((orange[:,:200],apple[:,210:]))
#now we have to blur in the middle so that the image looks like one image
#copy image1 in a new variable
copy_apple=apple.copy()
gp_apple=[copy_apple] #making a list for image 1 and its first element is image itself
#gaussian pyramid for apple image
for i in range(6):
    copy_apple=cv2.pyrDown(copy_apple)
    gp_apple.append(copy_apple) #appending the pyr down image to the list of first image
#copy image2 in a new variable
copy_orange=orange.copy()
gp_orange=[copy_orange] #making a list for image 2 and its first element is image itself
#gaussian pyramid for orange image
for i in range(6):
    copy_orange=cv2.pyrDown(copy_orange)
    gp_orange.append(copy_orange) #appending the pyr down image to the list of second image
copy_apple=gp_apple[5]#assigning the first image list last element to copied variable
lp_apple=[copy_apple]#again making alist for image one whose first element is the last element of previous list
#laplacian pyramid for apple image
for i in range(5,0,-1):
    size=(gp_apple[i-1].shape[1],gp_apple[i-1].shape[0])
    gaussian=cv2.pyrUp(gp_apple[i],dstsize=size)
    laplacian_apple=cv2.subtract(gp_apple[i-1],gaussian)
    lp_apple.append(laplacian_apple)
#same process with orange image
copy_orange=gp_orange[5]#assigning the first image list last element to copied variable
lp_orange=[copy_orange]#again making alist for image one whose first element is the last element of previous list
#laplacian pyramid for apple image
for i in range(5,0,-1):
    size=(gp_orange[i-1].shape[1],gp_orange[i-1].shape[0])
    gaussian=cv2.pyrUp(gp_orange[i],dstsize=size)
    laplacian_orange=cv2.subtract(gp_orange[i-1],gaussian)
    lp_orange.append(laplacian_orange)
#now add left and right halves of the images in each level of pyramid
apple_orange_pyramid=[] #an empty list
for apple_lap,orange_lap in zip(lp_apple,lp_orange):
    cols,rows,ch=apple_lap.shape
    laplacian=np.hstack((orange_lap[:,0:int(cols/2)],apple_lap[:,int(cols/2):]))
    apple_orange_pyramid.append(laplacian)
#now reconstruct
apple_orange_reconstruct=apple_orange_pyramid[0]
for i in range(1,6):
    size=(apple_orange_pyramid[i].shape[1],apple_orange_pyramid[i].shape[0])
    apple_orange_reconstruct=cv2.pyrUp(apple_orange_reconstruct,dstsize=size)
    apple_orange_reconstruct=cv2.add(apple_orange_pyramid[i],apple_orange_reconstruct)

cv2.imshow("apple",apple)
cv2.imshow("orange",orange)
cv2.imshow("apple_orange",apple_orange)
cv2.imshow("apple_orange_reconstruct",apple_orange_reconstruct)
#perfect result
cv2.waitKey(0)
cv2.destroyAllWindows()
