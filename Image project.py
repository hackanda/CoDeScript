from zipfile import ZipFile

from PIL import Image , ImageDraw
import pytesseract as pt
import cv2 as cv
import numpy as np

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')

filename = "readonly/small_img.zip"

def readZipFile(file):
    with ZipFile(file , 'r') as myfile:
        images = myfile.infolist()
        return images
    
def create_image(i, j): # Function to create new image and paste the cropeed faces
  image = Image.new("RGB", (i, j), "black")
  return image
    
def itemsinfile(fileimages):  # Function to check all the files in zip
    for item in fileimages:
        print(item)
    print('\n')

def readtext(file): # Function to perform OCR on the images
        data = []
        with ZipFile(file , 'r') as myfile:
            images = myfile.infolist()
            for f in images:
                ifile = myfile.open(f)
                img = Image.open(ifile)
                text = pt.image_to_string(img)
                data += [[img,text]]
        return data
    
    
def Makerec(image,face_cord):    # Just a Test Function to Check the false positive and negatives
    pil_img=image.convert("RGB")
    drawing=ImageDraw.Draw(pil_img) # And lets create our drawing context
    for x,y,w,h in face_cord:
        drawing.rectangle((x,y,x+w,y+h), outline="green" , width = 10)
    display(pil_img)
    
def croppedfaces(image , sizes):   # Function to crop the faces from the main image and return as a list
    pil_img = image.convert('RGB')
    crp_face = []
    for x,y,w,h in sizes:
        temp = pil_img.crop((x,y,x+w,y+h))
        temp = temp.resize((100,100))
        crp_face += [temp]
    return crp_face
        

def detectfaces(mylist): # This Function checks for the text from OCR and bind the image with it
    face_cord = []
    for image,text in mylist:
        if 'Christopher' in text:
            opencvImage = cv.cvtColor(np.array(image), cv.COLOR_BGR2GRAY) #converting pil to opencv image
            faces = face_cascade.detectMultiScale(opencvImage,1.15)
#             Makerec(image,faces.tolist()) # Function that prints rectangle on the faces
            face_cord += [[image,faces.tolist()]] # Creating the list of image with face cordinates
            
    return face_cord

# Print statements are just for testing the flow and status of the program.

fileimages = readZipFile(filename) # Fuction to read the zipfile and return imagelist

print('Reading from file is Done....\n')

itemsinfile(fileimages) # Fuction to print the items in file 

print('Found Items...\n')

imagetodata = readtext(filename) # Function to bind the image with their text and return the list

print('Image and Text Separated...\n')

face_cordinates = detectfaces(imagetodata) # Function to detect the faces and return a list of image with facedata

print('Found Image with face cordinates . Proceeding to crop them...\n')

# face_cordinates = [image , face_boxes]

cropped_faces = []

for image , size in face_cordinates:
    face_list = croppedfaces(image,size)
    temp = face_list[0]
    new = create_image((temp.width * 5) ,temp.height * ((len(face_list)//5)+1))
    x = 0
    y = 0
    for face in face_list:
        new.paste(face,(x,y))
        if x == new.width:
            x = 0
            y = y + face.height
        else:
            x += face.width
    cropped_faces += [new]

print('Made new Image...Now going to show them...\n')
    
for faces in cropped_faces:
    display(faces)





