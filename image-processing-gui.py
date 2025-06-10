import cv2
import numpy as np
from skimage import color
from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class PictureProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Picture Processing App")
        self.image = None
        self.original = None
        self.history = []

        self.setup_ui()

    def setup_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10)

        self.upload_btn = tk.Button(top_frame, text="Upload", width=10, command=self.upload_image)
        self.upload_btn.pack(side=tk.LEFT, padx=5)

        self.undo_btn = tk.Button(top_frame, text="Undo", width=10, command=self.undo)
        self.undo_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(top_frame, text="Reset", width=10, command=self.reset)
        self.reset_btn.pack(side=tk.LEFT, padx=5)

        self.save_btn = tk.Button(top_frame, text="Save", width=10, command=self.save_image)
        self.save_btn.pack(side=tk.LEFT, padx=5)

        preview_frame = tk.Frame(self.root, bd=2, relief=tk.SUNKEN, width=400, height=400)
        preview_frame.pack(pady=10)

        self.image_label = tk.Label(preview_frame)
        self.image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.image_label.drop_target_register(DND_FILES)
        self.image_label.dnd_bind('<<Drop>>', self.drop_image)

        self.placeholder_label = tk.Label(preview_frame, text="Upload or drop your photo", fg="gray", font=("Arial", 14))
        self.placeholder_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=10)

        operations1 = [
            ("Remove Noise", self.remove_noise),
            ("Adjust Contrast", self.adjust_contrast),
        ]

        operations2 = [
            ("BGR to Gray", self.bgr_to_gray),
            ("Gray to Binary", self.gray_to_binary),
        ]

        operations3 = [
            ("BGR to RGB", self.bgr_to_rgb),
            ("Improve Quality", self.improve_quality),
        ]

        for ops in [operations1, operations2, operations3]:
            row = tk.Frame(buttons_frame)
            row.pack(pady=5)
            for (text, command) in ops:
                btn = tk.Button(row, text=text, width=18, command=command)
                btn.pack(side=tk.LEFT, padx=3)

        filter_row = tk.Frame(buttons_frame)
        filter_row.pack(pady=10)

        tk.Label(filter_row, text="Filter:").pack(side=tk.LEFT, padx=5)

        self.filter_var = tk.StringVar()
        self.filter_var.set("Sketch")
        self.filter_options = ["Sketch", "Sepia", "Negative", "Emboss", "Blur"]
        self.filter_menu = tk.OptionMenu(filter_row, self.filter_var, *self.filter_options)
        self.filter_menu.pack(side=tk.LEFT, padx=5)

        self.filter_btn = tk.Button(filter_row, text="Apply Filter", width=15, command=self.apply_filter)
        self.filter_btn.pack(side=tk.LEFT, padx=5)

    def drop_image(self, event):
        path = event.data.strip('{}')
        if os.path.isfile(path) and path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            self.original = cv2.imread(path)
            self.image = self.original.copy()
            self.history.clear()
            self.display_image(self.image)
        else:
            messagebox.showerror("Invalid File", "Please drop a valid image file.")

    def upload_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
        if path:
            self.original = cv2.imread(path)
            self.image = self.original.copy()
            self.history.clear()
            self.display_image(self.image)

    def display_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil = img_pil.resize((400, 400))
        img_tk = ImageTk.PhotoImage(img_pil)
        self.image_label.configure(image=img_tk)
        self.image_label.image = img_tk
        self.placeholder_label.place_forget()

    def backup(self):
        if self.image is not None:
            self.history.append(self.image.copy())

    def undo(self):
        if self.history:
            self.image = self.history.pop()
            self.display_image(self.image)
        else:
            messagebox.showinfo("Undo", "No more steps to undo!")

    def reset(self):
        if self.original is not None:
            self.image = self.original.copy()
            self.history.clear()
            self.display_image(self.image)
        else:
            self.placeholder_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            messagebox.showerror("Error", "No image uploaded yet!")

    def remove_noise(self):
        if self.check_image():
            self.backup()
            self.image = cv2.medianBlur(self.image, 3)
            self.display_image(self.image)

    def adjust_contrast(self):
        if self.check_image():
            self.backup()
            lab = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            cl = clahe.apply(l)
            merged = cv2.merge((cl, a, b))
            self.image = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
            self.display_image(self.image)

    def bgr_to_gray(self):
        if self.check_image():
            self.backup()
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)
            self.display_image(self.image)

    def gray_to_binary(self):
        if self.check_image():
            self.backup()
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            self.image = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
            self.display_image(self.image)

    def bgr_to_rgb(self):
        if self.check_image():
            self.backup()
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.display_image(self.image)

    def improve_quality(self):
        if self.check_image():
            self.backup()
            self.adjust_contrast()
            self.remove_noise()

    def apply_filter(self):
        if not self.check_image():
            return
        self.backup()
        filter_name = self.filter_var.get()
        img = self.image

        if filter_name == "Sketch":
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            inv = 255 - gray
            blur = cv2.GaussianBlur(inv, (21, 21), 0)
            sketch = cv2.divide(gray, 255 - blur, scale=256)
            self.image = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

        elif filter_name == "Sepia":
            kernel = np.array([[0.272, 0.534, 0.131],
                               [0.349, 0.686, 0.168],
                               [0.393, 0.769, 0.189]])
            sepia = cv2.transform(img, kernel)
            self.image = np.clip(sepia, 0, 255).astype(np.uint8)

        elif filter_name == "Negative":
            self.image = cv2.bitwise_not(img)

        elif filter_name == "Emboss":
            kernel = np.array([[ -2, -1, 0],
                               [ -1,  1, 1],
                               [  0,  1, 2]])
            self.image = cv2.filter2D(img, -1, kernel)

        elif filter_name == "Blur":
            self.image = cv2.GaussianBlur(img, (9, 9), 0)

        self.display_image(self.image)

    def save_image(self):
        if self.check_image():
            path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
            if path:
                cv2.imwrite(path, self.image)
                messagebox.showinfo("Saved", f"Image saved to {path}")

    def check_image(self):
        if self.image is None:
            messagebox.showerror("Error", "Please upload an image first!")
            return False
        return True

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = PictureProcessingApp(root)
    root.mainloop()