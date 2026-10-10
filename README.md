# 🏭 Industrial Flare Stack Thermal Vision Analyzer

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Array%20Ops-013243?logo=numpy&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Hey there! 👋 Welcome to my computer vision project. 

In refineries and chemical plants, flare stacks burn off dangerous waste gases. If a flame goes out (**a flameout event**) or burns too weakly, unburnt toxic gases escape into the atmosphere. 

I built this Python pipeline to process thermal infrared camera feeds, measure flame size, and automatically assess combustion health in real time. To make this project production-ready, I built it in **two distinct phases**—moving from a simple manual proof-of-concept to an adaptive, dynamic thresholding pipeline using OpenCV.

---

## 💡 The Problem I Wanted to Solve

Monitoring flare stacks manually or using rigid rules doesn't work well outdoors. Sunlight shifts throughout the day, weather changes, and smoke density varies. 

I wanted to answer two core engineering questions:
1. **Can we reliably isolate the burning plume from background sky noise under changing conditions?**
2. **Can we use spatial pixel coverage as a real-time proxy for combustion health and safety alerts?**

---

## 🛠️ How I Built It (The 2-Part Evolution)

### 1️⃣ Part 1: The Manual Baseline
I started by building a basic proof-of-concept script:
* **Flattening Channels:** I loaded thermal images and flattened 3D RGB channels into a 2D heat-intensity matrix using NumPy (`np.mean(image, axis=2)`).
* **Manual Cutoff:** I applied a static hardcoded threshold (`heat_map > 100`) to isolate bright pixels.
* **The Catch:** While this worked on a test image, fixed numbers fail in production. If the sun comes out or heavy fog rolls in, a fixed cutoff either misses the flame completely or picks up background noise.

### 2️⃣ Part 2: Upgrading to Otsu’s Automated Thresholding
To solve the environmental problem, I refactored the pipeline using **OpenCV**:
* **Data Type Precision (`uint8`):** I scaled image values to an 8-bit unsigned integer range (`np.uint8`, values 0–255). I avoided signed integers (`int8`) because values above 127 wrap around into negative numbers, causing data corruption.
* **Histogram Analysis:** I implemented `cv2.threshold` with `cv2.THRESH_OTSU`. Instead of guessing a fixed cutoff, Otsu’s algorithm looks at the pixel intensity histogram of each frame, separates the dark background peak from the bright flame peak, and calculates the exact optimal threshold automatically.
* **Real-Time Adaptation:** Because the threshold recalculates per frame, the system seamlessly handles outdoor lighting changes, overcast skies, and shifting smoke.

---

## 📊 Quick Comparison: Manual vs. Otsu Thresholding

| Feature | Part 1: Manual Baseline | Part 2: Otsu's Adaptive Pipeline |
| :--- | :--- | :--- |
| **Cutoff Selection** | Hardcoded static number | Dynamic frame-by-frame calculation |
| **Outdoor Weather Handling** | Rigid (Breaks when background light changes) | Adaptive (Recalculates based on frame histogram) |
| **Data Format** | Scaled Float / Generic Array | Unsigned 8-bit Integer (`np.uint8`) |
| **OpenCV Integration** | Basic NumPy boolean mask | OpenCV `cv2.THRESH_OTSU` |

---

## 🔥 Physics & Domain Logic: Why Flame Size Matters

Once the flame plume is isolated, the script calculates the **Spatial Flame Coverage Area (%)** relative to the total camera feed:

$$\text{Coverage Area (\%)} = \left( \frac{\text{Isolated Flame Pixels}}{\text{Total Frame Pixels}} \right) \times 100$$

Here is how the system translates pixel area into industrial safety logic:

* **High Coverage Area (Strong Burn):** Indicates a large, high-temperature reaction zone ($>1,000^\circ\text{C}$). The flame has enough energy to achieve high Destruction and Removal Efficiency (DRE), cleanly converting waste gas into $\text{CO}_2$ and water vapor.
* **Low Coverage Area (Weak Burn):** Signals a small or flickering flame where thermal energy is dissipating too quickly into cold ambient air, risking incomplete combustion.
* **Zero Coverage Area (0%):** Triggers an immediate **FLAMEOUT ALERT**—the pilot is out, and unburnt toxic gas is escaping.

---

## 📁 Project Structure

```text
flare-stack-thermal-vision/
│
├── data/
│   └── fire_flare_image.png         # Input thermal camera feed
│
├── src/
│   ├── Fire_flare_part1.py          # Manual baseline script
│   └── Fire_flare_part2.py          # Production OpenCV Otsu pipeline
│
├── output/
│   └── Fire_flare_analysisresult.png # Visual side-by-side diagnostic plot
│
├── .gitignore                       # Git ignore rules
├── LICENSE                          # MIT License
├── README.md                        # Documentation
└── requirements.txt                 # Dependencies
