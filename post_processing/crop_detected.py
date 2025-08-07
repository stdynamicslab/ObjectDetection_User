import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
from ultralytics import YOLO

# Load YOLO model
model = YOLO(r"app\best.pt")

# ---------------- Conversion & Prediction ----------------
def convert_image_to_8bit_png(input_path, output_dir):
    image = cv2.imread(input_path, -1)
    if image is None:
        return None, "Unreadable"

    depth = image.dtype
    filename = os.path.splitext(os.path.basename(input_path))[0]
    out_path = os.path.join(output_dir, filename + ".png")

    try:
        if depth == np.uint16:
            normalized = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
            image_8bit = np.uint8(normalized)
            cv2.imwrite(out_path, image_8bit)
            return out_path, "Converted"

        elif depth == np.uint8 and image.ndim == 3 and image.shape[2] == 3:  # 24-bit RGB
            cv2.imwrite(out_path, image)
            return out_path, "Converted"

        else:
            return None, "Skipped"
    except Exception as e:
        print(f"Error converting {input_path}: {e}")
        return None, "Error"

def predict_and_crop(image_path, save_folder):
    results = model(image_path)[0]
    image = cv2.imread(image_path)

    for i, box in enumerate(results.boxes.xyxy):
        x1, y1, x2, y2 = map(int, box)
        cropped = image[y1:y2, x1:x2]
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        save_path = os.path.join(save_folder, base_name + ".png")
        cv2.imwrite(save_path, cropped)

# ---------------- Processing Logic ----------------
def process_images(paths):
    if not paths:
        return

    base_output = os.path.join(os.getcwd(), "output")
    converted_dir = os.path.join(base_output, "converted_images")
    cropped_dir = os.path.join(base_output, "cropped_images")

    os.makedirs(converted_dir, exist_ok=True)
    os.makedirs(cropped_dir, exist_ok=True)

    progress_bar["maximum"] = len(paths)
    skipped = []
    total = 0

    for idx, path in enumerate(paths):
        progress_bar["value"] = idx + 1
        root.update_idletasks()

        out_img, status = convert_image_to_8bit_png(path, converted_dir)
        if status == "Converted" and out_img:
            predict_and_crop(out_img, cropped_dir)
            total += 1
        elif status == "Skipped":
            skipped.append(os.path.basename(path))

    show_completion_screen(total, base_output, skipped)

# ---------------- Final Screen ----------------
def show_completion_screen(processed_count, output_folder, skipped_files):
    result_win = tk.Toplevel(root)
    result_win.title("✅ Processing Complete")
    result_win.geometry("420x300")
    result_win.resizable(False, False)

    summary = f"✅ All Done!\n\nProcessed: {processed_count} image(s)\n\nSaved in:\n{output_folder}"
    if skipped_files:
        summary += f"\n\n⛔ Skipped ({len(skipped_files)}):\n" + "\n".join(skipped_files[:5])
        if len(skipped_files) > 5:
            summary += f"\n...and {len(skipped_files)-5} more."

    label = tk.Label(result_win, text=summary, font=("Arial", 11), justify="left", wraplength=400)
    label.pack(pady=20)

    btn_frame = tk.Frame(result_win)
    btn_frame.pack(pady=10)

    restart_btn = ttk.Button(btn_frame, text="🔄 Restart", command=lambda: result_win.destroy())
    restart_btn.grid(row=0, column=0, padx=10)

    exit_btn = ttk.Button(btn_frame, text="❌ Exit", command=root.quit)
    exit_btn.grid(row=0, column=1, padx=10)

# ---------------- Browse Handlers ----------------
def browse_file():
    path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.tif *.tiff *.bmp")])
    if path:
        process_images([path])

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        files = [os.path.join(folder, f) for f in os.listdir(folder)
                 if f.lower().endswith(('.png', '.jpg', '.tif', '.tiff', '.bmp'))]
        process_images(files)

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("Raw to Cropped Image Converter (YOLO + Bit-depth)")
root.geometry("500x380")
root.resizable(False, False)
root.configure(bg="#f8f9fa")

frame = ttk.LabelFrame(root, text="Input Image Source", padding=20)
frame.pack(padx=20, pady=20, fill="x")

btn_single = ttk.Button(frame, text="📷 Select Single Image", command=browse_file)
btn_single.pack(pady=10)

btn_folder = ttk.Button(frame, text="📁 Select Folder of Images", command=browse_folder)
btn_folder.pack(pady=10)

progress_bar = ttk.Progressbar(root, length=400, mode='determinate')
progress_bar.pack(pady=20)

footer = ttk.Label(root, text="Developed by Piyush | YOLO + Bit-depth Converter", font=("Arial", 9, "italic"), background="#f8f9fa")
footer.pack(pady=10)

root.mainloop()




# import os
# import cv2
# import tkinter as tk
# from tkinter import filedialog, ttk, messagebox
# from PIL import Image
# from ultralytics import YOLO
# import numpy as np

# # Load YOLO model
# model = YOLO(r'E:\Piyush_Thakur\circle_detection\app\best.pt')

# # Directory to save converted 8-bit PNGs
# converted_folder = r'E:\Piyush_Thakur\circle_detection\app\converted_images'
# cropped_folder = r'E:\Piyush_Thakur\circle_detection\app\cropped_output'
# os.makedirs(converted_folder, exist_ok=True)
# os.makedirs(cropped_folder, exist_ok=True)

# # ---------- Conversion Functions ----------

# def convert_image_to_8bit_png(input_path, output_folder):
#     img = cv2.imread(input_path, -1)  # Read unchanged
#     if img is None:
#         return None, "Unreadable"

#     bit_depth = img.dtype

#     if bit_depth == np.uint16:  # 16-bit
#         img_8bit = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
#         img_8bit = np.uint8(img_8bit)
#     elif len(img.shape) == 3 and img.shape[2] == 3:  # 24-bit (8 bits/channel RGB)
#         img_8bit = img
#     else:
#         return None, "Unsupported"

#     filename = os.path.splitext(os.path.basename(input_path))[0] + '.png'
#     save_path = os.path.join(output_folder, filename)
#     cv2.imwrite(save_path, img_8bit)
#     return save_path, "Converted"

# # ---------- Prediction and Cropping ----------

# def predict_and_crop(image_paths, cropped_folder, progress_callback):
#     results = model.predict(source=image_paths, imgsz=640, conf=0.25, save=False, save_txt=False)

#     for i, result in enumerate(results):
#         img = result.orig_img
#         boxes = result.boxes.xyxy.cpu().numpy()
#         img_name = os.path.splitext(os.path.basename(result.path))[0]

#         for j, box in enumerate(boxes):
#             x1, y1, x2, y2 = map(int, box)
#             cropped = img[y1:y2, x1:x2]
#             save_path = os.path.join(cropped_folder, f'{img_name}_crop{j+1}.png')
#             cv2.imwrite(save_path, cropped)

#         progress_callback(i + 1)

# # ---------- GUI Application ----------

# class App:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("YOLO Inference - Image Processor")

#         self.selected_path = None

#         self.label = tk.Label(root, text="Select Image or Folder:")
#         self.label.pack(pady=5)

#         self.select_button = tk.Button(root, text="Select Image or Folder", command=self.select_input)
#         self.select_button.pack(pady=5)

#         self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
#         self.progress.pack(pady=10)

#     def select_input(self):
#         path = filedialog.askopenfilename(title="Select a single image") or filedialog.askdirectory(title="Select a folder")
#         if path:
#             self.selected_path = path
#             self.process_images()

#     def process_images(self):
#         image_paths = []

#         if os.path.isfile(self.selected_path):
#             image_paths = [self.selected_path]
#         elif os.path.isdir(self.selected_path):
#             for file in os.listdir(self.selected_path):
#                 if file.lower().endswith(('.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp')):
#                     image_paths.append(os.path.join(self.selected_path, file))

#         skipped = []
#         converted_paths = []

#         for img_path in image_paths:
#             new_path, status = convert_image_to_8bit_png(img_path, converted_folder)
#             if status == "Converted":
#                 converted_paths.append(new_path)
#             else:
#                 skipped.append(os.path.basename(img_path))

#         if not converted_paths:
#             messagebox.showwarning("No Valid Images", "No 16-bit or 24-bit images found.")
#             return

#         self.progress["maximum"] = len(converted_paths)
#         self.progress["value"] = 0

#         def update_progress(val):
#             self.progress["value"] = val
#             self.root.update_idletasks()

#         predict_and_crop(converted_paths, cropped_folder, update_progress)

#         if skipped:
#             messagebox.showinfo("Skipped Images", f"Skipped {len(skipped)} image(s):\n" + "\n".join(skipped))
#         messagebox.showinfo("Done", "✅ All images processed and cropped!")

# # ---------- Run Application ----------

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = App(root)
#     root.mainloop()
