from PIL import Image

img = Image.open(r"Lenna.jpeg")
width, height = img.size

for x in range(width):
  for y in range(1):
    coordinate = x, y
    print (img.getpixel(coordinate))  
  