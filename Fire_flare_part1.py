#===========================OTSU Automated Threshold==============================
import cv2
import numpy as np
import matplotlib.pyplot as plt
image_read = plt.imread("PROJECT-Fire_flare_Burning_Efficiency/fire_flare_image.png")
image_read1 = image_read*255
heat_map = np.mean(image_read1,axis =2)
heat_map_unit8 = heat_map.astype(np.uint8)
otsu_threshold,fire_mask = cv2.threshold(heat_map_unit8,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
fire_size = np.sum(fire_mask>0)
total_pixel = heat_map.size
coverage_area = (fire_size/total_pixel)*100
print("==============OTSU AUTOMATED RESULTS==============")
print(f"OTSU threshold is {otsu_threshold}")
print(f"OTSU coverage area: {coverage_area}")
fig,(ax1,ax2) = plt.subplots(1,2,figsize=(10,5))
ax1.imshow(image_read)
ax1.set_title("1.Original Flame")
ax1.axis("off")
ax2.imshow(fire_mask)
ax2.set_title(F"2.OTSU isolated flame(Threshold:{otsu_threshold:.1f},Coverage Area:{coverage_area:.1f}%)")
ax2.axis("off")
plt.tight_layout()
plt.savefig("otsu_fire_flare_analysis.png",dpi=300,bbox_inches ="tight")
plt.show()
