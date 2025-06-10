
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

> _You can upload a screenshot of the app here for better visuals._

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

## 📁 File Structure

```
.
├── Dsp Project.py        # Main application code
├── README.md             # This file
└── .gitignore            # Python build artifacts ignore rules
```

## 👨‍💻 Author

Omar Mohamed Ahmed Abo Elmaaty  
Faculty of Computer and Information Sciences, Mansoura University  
Section 4 | 3rd-Year Student  

## 📝 License

This project is open source and free to use.
