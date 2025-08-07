# 🟠 Circular Pattern Cropper

A lightweight and user-friendly tool to **automatically detect and crop circular patterns** from raw grayscale images using a trained YOLOv8 model. Simply launch the tool, select your image(s), and receive neatly cropped circular regions — no training, no setup required.

---

## 🎯 What This Tool Does

✅ Uses a pre-trained YOLOv8 model to detect circular patterns  
✅ Provides a simple **GUI** to select input image(s) or folder  
✅ Outputs cropped circular regions automatically  
✅ Supports both single image and batch image processing  

---

## 📦 Repository Contents

```
CircularPatternCropper/
├── post_processing/
│   └── crop_detected.py         # Main GUI tool for cropping
├── weights/
│   └── best.pt                  # Pre-trained YOLOv8 model weights
├── samples/
│   ├── input_sample.png
│   └── cropped_output.png
├── requirements.txt            # Python dependencies
└── README.md
```

---

## 🖥️ How to Use

### 1. 🔧 Install Dependencies

We recommend using a virtual environment:

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 2. 🚀 Run the Tool

```bash
python post_processing/crop_detected.py
```

This will open a GUI where you can:

- Select a **folder** of raw images *(recommended)*  
- OR choose a **single image file***

The detected circular patterns will be cropped and saved automatically in an `output/` directory.

---

## 📸 Sample Output

| Input Image                  | Cropped Output             |
|-----------------------------|----------------------------|
| ![<img width="1600" height="1600" alt="sample1" src="https://github.com/user-attachments/assets/95771714-8acb-476c-860f-acc16f012b2a" />]| <img width="1043" height="1035" alt="sample1_cropped" src="https://github.com/user-attachments/assets/68c755d9-bc96-4c85-a795-e78a22217f67" /> |
| ![](samples/input_sample.png) | ![](samples/cropped_output.png) |
| ![](samples/input_sample.png) | ![](samples/cropped_output.png) |

---

## 📁 Output Directory Structure

After processing, you'll find:

```
output/
├── image1_circle_1.png
├── image1_circle_2.png
├── ...
```

Each cropped image corresponds to a detected circular pattern in the input image(s).

---

## 📥 Model Download (if not included)

If `weights/best.pt` is not present, you can download it from the [model release page](https://github.com/yourusername/CircularPatternCropper/releases) and place it inside the `weights/` folder.

---

## 🙏 Acknowledgments

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) for the detection backbone

---

## 📬 Questions or Suggestions?

Feel free to open an [Issue](https://github.com/yourusername/CircularPatternCropper/issues) or [Pull Request](https://github.com/yourusername/CircularPatternCropper/pulls) if you'd like to contribute or report bugs.

---
