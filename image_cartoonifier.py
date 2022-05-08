from multiprocessing.spawn import import_main_path
import cv2
import easygui
import numpy as np
import imageio
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
#####
def upload():
    imagePath = easygui.fileopenbox()
    cartoonify(imagePath)
#####
def cartoonify(imagePath):
    ###
    orgImage = cv2.imread(imagePath)
    orgImage = cv2.cvtColor(orgImage, cv2.COLOR_BGR2RGB)
    if orgImage is None:
        print("Can't find image file, Choose another one.")
        sys.exit()
    resizedImage1 = cv2.resize(orgImage, (960, 540))
    ###
    grayImage = cv2.cvtColor(orgImage, cv2.COLOR_BGR2GRAY)
    resizedImage2 = cv2.resize(grayImage, (960, 540))
    ###
    smoothGrayImage = cv2.medianBlur(grayImage, 5)
    resizedImage3 = cv2.resize(smoothGrayImage, (960, 540))
    ###
    edgedImage = cv2.adaptiveThreshold(smoothGrayImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    resizedImage4 = cv2.resize(edgedImage, (960, 540))
    ###
    colorImage = cv2.bilateralFilter(orgImage, 9, 300, 300)
    resizedImage5 = cv2.resize(colorImage, (960, 540))
    ###
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=edgedImage)
    resizedImage6 = cv2.resize(cartoonImage, (960, 540))
    ###
    images=[resizedImage1, resizedImage2, resizedImage3, resizedImage4, resizedImage5, resizedImage6]

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    save1=Button(win, text = "Save Cartoonified Image", command = lambda: save(resizedImage4, imagePath), padx = 30, pady = 5)
    save1.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
    save1.pack(side=TOP,pady=50)
    
    plt.show()
#####
def save(resizedImage4, imagePath):
    name = "cartoonified_image"
    path1 = os.path.dirname(imagePath)
    extention = os.path.splitext(imagePath)[1]
    path = os.path.join(path1, name+extention)
    cv2.imwrite(path, cv2.cvtColor(resizedImage4, cv2.COLOR_RGB2BGR))
    I = "Image saved by name " + name + " at " + path
    tk.messagebox.showinfo(title="Cartoonified Image Saved", message=I)
#####
win = tk.Tk()
win.geometry("400x400")
win.title("Cartoonify Your Image")
win.configure(background="white")
label = Label(win, background = '#d5e0e3', font=("calibri", 20, "bold"))
#####
upload = Button(win, text = "Cartoonify Your Image", command = upload, padx = 10, pady = 5)
upload.configure(background = "#3d9eff", foreground = "black", font = ("calibri", 10, "bold"))
upload.pack(side = TOP, pady=50)
#####
win.mainloop()