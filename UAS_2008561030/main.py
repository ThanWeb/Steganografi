import tkinter as tk
import pathlib
import os
import cv2
import numpy as np

from tkinter import filedialog
from PIL import Image, ImageFilter
from datetime import datetime

root = tk.Tk()
root.state('zoomed')

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.minsize(width = int(screen_width / 2), height = int(screen_height / 2))

root.title("Project Akhir Steganografi oleh Hans")
root.iconbitmap('assets/favicon.ico')
root.configure(bg = 'white', padx = 20, pady = 20)

heading = tk.Label(root, text = "Selamat Datang", font = ('Arial', 16), padx = 8, pady = 4)
heading.pack()

def browse_image():
  file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.bmp")])
  browse_image_entry.delete(0, tk.END)
  browse_image_entry.insert(0, file_path)

def is_image(file_path):
  image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
  return any(file_path.lower().endswith(ext) for ext in image_extensions)

def write_image(file_path, folder_path):
  now = datetime.now()
  ext = pathlib.Path(file_path).suffix
  filename = now.strftime("%m-%d-%Y-%H-%M-%S" + ext)

  original_folder, original_filename = os.path.split(filename)
  decryption_folder = os.path.join(original_folder, folder_path)
  os.makedirs(decryption_folder, exist_ok=True)

  decrypted_file_path = os.path.join(decryption_folder, original_filename)
  os.rename(filename, decrypted_file_path)

def start_encode_mode():
  heading.config(text = "Encode Text to Image")
  browse_image_button.pack(side = tk.TOP)
  browse_image_button.config(text = "Browse Image")
  browse_image_entry.pack(side = tk.TOP)
  browse_image_entry.delete(0, tk.END)
  string_entry_label.pack(side = tk.TOP)
  string_entry.pack(side = tk.TOP)
  string_entry.delete(0, tk.END)
  encode_button.pack(side = tk.TOP)

  decode_button.forget()
  decoded_string.forget()
  distortion_button.forget()

def start_decode_mode():
  heading.config(text = "Decode Text from Image")
  browse_image_button.pack(side = tk.TOP)
  browse_image_button.config(text = "Browse Image")
  browse_image_entry.pack(side = tk.TOP)
  browse_image_entry.delete(0, tk.END)
  decode_button.pack(side = tk.TOP)
  decoded_string.pack(side = tk.TOP)

  string_entry_label.forget()
  string_entry.forget()
  encode_button.forget()
  distortion_button.forget()

def start_distortion_mode():
  heading.config(text = "Image Distortion")
  browse_image_button.pack(side = tk.TOP)
  browse_image_button.config(text = "Browse Image")
  browse_image_entry.pack(side = tk.TOP)
  browse_image_entry.delete(0, tk.END)
  distortion_button.pack(side = tk.TOP)

  string_entry_label.forget()
  string_entry.forget()
  encode_button.forget()
  decode_button.forget()
  decoded_string.forget()

def encode():
  input_image = browse_image_entry.get()

  if input_image == "":
    heading.config(text = "Please select an image", fg = "red")
    return
  
  if is_image(input_image) == False:
    heading.config(text = "This file is not an image", fg = "red")
    return

  image = Image.open(input_image, 'r')
  data = string_entry.get()

  if (len(data) == 0):
    heading.config(text = "Please write something", fg = "red")
    return
  
  res = []
  res.append(len(data))

  for index, x in enumerate(data):
    res.append(ord(data[index]))

  new_image = []
  image_d = image.getdata()

  for index, x in enumerate(image_d):
    if (index) <= res[0]:
      temp = (image_d[index][0], image_d[index][1], res[index])
      new_image.append(temp)
    else:
      new_image.append(image_d[index])

  image.putdata(new_image)
  print(new_image[0])

  now = datetime.now()
  ext = pathlib.Path(input_image).suffix
  filename = now.strftime("%m-%d-%Y-%H-%M-%S" + ext)

  image.save("output/" + "encode/" + filename)
  heading.config(text = "Encode Success", fg = "green")

def decode():
  input_image = browse_image_entry.get()

  if input_image == "":
    heading.config(text = "Please select an image", fg = "red")
    return
  
  if is_image(input_image) == False:
    heading.config(text = "This file is not an image", fg = "red")
    return

  image = Image.open(input_image, 'r')
  image_d = image.getdata()
  print(image_d[0])

  res = str()
  for x in range(image_d[0][2]):
    res += (chr(image_d[x + 1][2]))

  decoded_string.config(text = "Decoded string: " + res)

def distortion():
  input_image = browse_image_entry.get()

  if input_image == "":
    heading.config(text = "Please select an image", fg = "red")
    return
  
  if is_image(input_image) == False:
    heading.config(text = "This file is not an image", fg = "red")
    return
  
  image = cv2.imread(input_image)
  height, width = image.shape[:2]
  distortion_map = np.zeros_like(image, dtype = np.float32)

  for y in range(height):
    for x in range(width):
      new_x = (x + 10 * np.sin(2 * np.pi * y / 128.0)).astype(int)
      new_y = (y + 10 * np.cos(2 * np.pi * x / 128.0)).astype(int)

      if new_x >= 0 and new_x < width and new_y >= 0 and new_y < height:
        distortion_map[y, x] = image[new_y, new_x]

  distorted_img = cv2.remap(image, distortion_map[..., 0], distortion_map[..., 1], cv2.INTER_LINEAR)        
  now = datetime.now()
  ext = pathlib.Path(input_image).suffix
  filename = now.strftime("%m-%d-%Y-%H-%M-%S" + ext)

  cv2.imwrite("output/" + "distortion/" + filename, distorted_img)
  heading.config(text = "Distoriton Success", fg = "green")

  cv2.imshow('Distorted Image', distorted_img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

menu_bar = tk.Menu(root)
menu_bar.add_cascade(label = "Encode Text to Image", command = start_encode_mode)
menu_bar.add_cascade(label = "Decode Text from Image", command = start_decode_mode)
menu_bar.add_cascade(label = "Image Distortion", command = start_distortion_mode)
menu_bar.add_cascade(label = "Exit", command = root.quit)

browse_image_button = tk.Button(root, text = "Browse Image", command = browse_image, font = ('Arial', 8), padx = 8, pady = 4)
browse_image_entry = tk.Entry(root, width = 64)
string_entry = tk.Entry(root, text = "Write here", bg = 'white', fg = 'black', width = 64)
string_entry_label = tk.Label(root, text = "Enter string to encode")
encode_button = tk.Button(root, text = "Encode", command = encode, font = ('Arial', 8), padx = 8, pady = 4, bg = "green", fg = "white")
decode_button = tk.Button(root, text = "Decode", command = decode, font = ('Arial', 8), padx = 8, pady = 4, bg = "blue", fg = "white")
decoded_string = tk.Label(root, text = "Decoded string : ...")
distortion_button = tk.Button(root, text = "Distortion", command = distortion, font = ('Arial', 8), padx = 8, pady = 4, bg = "purple", fg = "white")

root.config(menu = menu_bar)
root.mainloop()