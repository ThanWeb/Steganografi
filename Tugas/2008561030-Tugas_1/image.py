from PIL import Image

def encode():
  inputImage = input("Enter image name(with extension): ")
  image = Image.open(inputImage, 'r')

  data = input("Enter data to be encoded: ")
  if (len(data) == 0):
    raise ValueError('Data is empty')
  
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
  image.save('output.bmp')

def decode():
  inputImage = input("Enter image name(with extension): ")
  image = Image.open(inputImage, 'r')
  image_d = image.getdata()

  res = str()
  for x in range(image_d[0][2]):
    res += (chr(image_d[x + 1][2]))

  return 'Decoded Word : ' + res  

def main():	
  inMenu = int(input(":: JPEG Steganography ::\n""1. Encode\n2. Decode\n3. Exit\nSelect: "))
  isContinue = 1
    
  if (inMenu == 1):
    encode() 
        
  elif (inMenu == 2):
    print(decode())
        
  elif(inMenu == 3):
    isContinue = 0
    print("End program.")        
		
  else:
    raise Exception("Enter correct input")
    return isContinue

if __name__ == '__main__' :
	isRun = 1
	while(isRun == 1):
		isRun = main()
