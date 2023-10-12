from PIL import Image

img = Image.open('example.jpeg')
img_d = img.getdata()
width, height = img.size

cover = Image.open('cover.bmp')
cover_d = cover.getdata()

new_image = []

for index, x in enumerate(img_d):
  if (index % 2) == 0:
    new_image.append(img_d[index])
  else:
    new_image.append(cover_d[index])

# print(new_image)
cover.putdata(new_image)
cover.save('output.bmp')
  