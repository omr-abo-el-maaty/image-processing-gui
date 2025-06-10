
# Image Processing GUI App

A simple drag-and-drop graphical user interface (GUI) for basic image processing tasks using **TkinterDnD2**, **OpenCV**, and **PIL**. This app enables users to upload or drag-and-drop images, apply filters and operations, and save the processed result.

## 🧰 Features

- Upload and drop images (JPG, PNG, BMP)
- Undo & Reset operations
- Save the processed image
- Image filters:
  - Sketch
  - Sepia
  - Negative
  - Emboss
  - Blur
- Processing operations:
  - Remove Noise (Median Blur)
  - Adjust Contrast (CLAHE)
  - Convert BGR to Gray
  - Convert Gray to Binary
  - Convert BGR to RGB
  - Improve Quality (Noise removal + Contrast)

## 🖼️ Interface Preview

![image](https://github.com/user-attachments/assets/99abd5e7-6cec-4a69-936b-763ec96d54ab)


## 🛠️ Requirements

Install dependencies with:

```bash
pip install opencv-python pillow scikit-image tkinterdnd2
```

## 🚀 How to Run

```bash
python "Dsp Project.py"
```

Make sure you are using a Python environment where `tkinterdnd2` is properly installed and supported.


