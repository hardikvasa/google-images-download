from tkinter import  *
from tkinter.filedialog import askdirectory
import tkinter as tk
import subprocess  #to execute command in python script
import os
import signal
import sys
from tkinter import messagebox

import atexit
#  add a chkecker for windows and other operation systems to check it .. 
root = Tk()
frame = tk.Frame(root)


root.title("Google Image Downloader")
root.geometry("500x400")
text2 = Text(root, height=5, width=50)#size hesaplama
scroll = Scrollbar(root,command=text2.yview)#text2 her dafe cagirmasini
text2.configure(yscrollcommand=scroll.set)#nasil olacagini yazdim 
text2.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic')) 
text2.tag_configure('big', font=('Verdana', 14))#cizge nasil olacagini bilter
text2.insert(END,'         Google Image Downloader  ', 'big')




var = StringVar()
var3 = StringVar()#key word 
var1 = StringVar()#Choose Path
var2=StringVar()#Not if not seleceted you will got Default as stringini
var4=StringVar()
keywordvar=StringVar()



#keywordlabel= Label( root, textvariable=keywordvar, relief=RAISED )#yazacak olna lab
#label = Label( root, textvariable=var, relief=RAISED )#yazacak olna lab
label1 = Label( root, textvariable=var1, relief=RAISED )#Choose Path
label2 = Label( root, textvariable=var2, relief=RAISED )#Not if not seleceted you will got Default as
label3 = Label( root, textvariable=var3, relief=RAISED )#Not if not seleceted you will got Default as
label4= Label( root, textvariable=var4, relief=RAISED )#key  word



# label 1 ve label 3

path = StringVar()#bu callback  label icin  kullandim chose path icin 
Entry(root, width=70, textvariable=path).place(y=113,x=40)#text  icin 
path.set("")




keywords = StringVar()#bu test  fonksiyon iciin  icin  kullandim chose path icin 
Entry(root, textvariable=keywords,width=40,fg="blue",selectbackground='violet').place(y=160,x=135)#text  icin 



def callback():   
    name= askdirectory() #dosya acmak icin   ve yolu almak icin 
    path.set(name)#burda text  yazdiriyorum    
    
    
text2.pack()





def  fetch():#ikinci fonksiyon  bir harf yazmak icin  
    
    if path.get() != "":
        pythonCode =subprocess.Popen("py google_images_download.py  -k \"" + keywords.get() +"\" -o "+ path.get() ,  shell=True ) #burada value alip  gonderiyor 
    else :
        pythonCode =subprocess.Popen("py google_images_download.py  -k\"" + keywords.get()+"\"" ,shell=True)
    
 




var1.set("Choose Path")

var3.set(" Key word ")

label1.place(y=90)

Button(text="Path", command=callback, width=16 ,background="red").pack()
#label.pack()

label3.place(y=160)   

Button(text=' Download ', command=fetch, 
        width=16,background="green").place(y=180,x=190)#burada botton
#keywordlabel.pack()


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        # fetch().pythonCode.kill() // check how to kill subproccess
        root.destroy()


root.protocol( "WM_DELETE_WINDOW", on_closing )

mainloop()
