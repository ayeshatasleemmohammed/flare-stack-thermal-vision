#===========================Manual Threhold=======================================
import numpy as np
import matplotlib.pyplot as plt
image_read = plt.imread("PROJECT-Fire_flare_Burning_Efficiency/fire_flare_image.png")
image_read1 = image_read*255
print(image_read1)
fire_mask = np.mean(image_read1,axis = 2) > 100
fire_size = np.sum(fire_mask)
if fire_size ==0 :
    print("No Fire detected at all!!")
elif fire_size <100 :
    print("Fire is weak")
elif fire_size>= 100:
    print("Fire is healthy and strong")
fig, (ax1,ax2)=plt.subplots(1,2,figsize = (10,5))
ax1.imshow(image_read)
ax1.set_title("1.Original Thermal Photo")
ax1.axis("off")
total_pixels = image_read1.shape[0]*image_read1.shape[1]
coverage_area = (fire_size/total_pixels)*100
ax2.imshow(fire_mask,cmap = "hot")
ax2.set_title(f"2. Isolated Fire Area (Coverage area: {coverage_area:.1f}%)")
print(f"Coverage Area is:{coverage_area:.1f}%")
ax2.axis("off")
plt.tight_layout()
plt.savefig("Fire_flare_analysisresult.png",dpi = 300)
plt.show()