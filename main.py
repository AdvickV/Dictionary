from tkinter import *
from tkinter.messagebox import showerror
from PIL import Image, ImageTk
import requests
import urllib.request
import json.decoder
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)

WORD = "None"


def get_word():
    global WORD
    try:
        headers = {
            "Authorization": "Token a7de8ba0688c95476ad1e13d0343b90f24b693d9"
        }

        response = requests.get(f"https://owlbot.info/api/v4/dictionary/{word_entry.get()}", headers=headers)
        response.raise_for_status()

        data = response.json()["definitions"][0]

        definition.config(text=data["definition"])
        example.config(text=data["example"])
        grammar_type.config(text=data["type"])
        WORD = response.json()["word"]

        try:
            urllib.request.urlretrieve(data["image_url"], f"search-word-images/{response.json()['word']}.jpg")

            new_img = Image.open(f"search-word-images/{response.json()['word']}.jpg")
            new_img = new_img.resize((400, 300))
            new_img = ImageTk.PhotoImage(new_img)
            image.config(image=new_img)
            image.photo = new_img
        except TypeError:
            new_img = Image.open("images/dictionary.jpg")
            new_img = new_img.resize((400, 300))
            new_img = ImageTk.PhotoImage(new_img)
            image.config(image=new_img)
            image.photo = new_img

    except json.decoder.JSONDecodeError:
        showerror("No Word", "Please enter a word to get it's meaning.")
    except requests.exceptions.HTTPError:
        showerror("No Definition Found", "There is no definition for that word. Please try a different one.")


def pronounce():
    engine.say(WORD)
    engine.runAndWait()


window = Tk()
window.title("Dictionary")
window.geometry("+0+0")
window.config(padx=50, pady=50, bg="chartreuse2")

instruction_label = Label(text="Type a word here!", font=("Comic Sans MS", 25, "bold"), fg="blue", bg="chartreuse2")
instruction_label.grid(column=0, row=0, columnspan=2)

word_entry = Entry(width=50)
word_entry.grid(column=0, row=1, columnspan=2, pady=10)

search_b = Button(text="Search Word", command=get_word)
search_b.grid(column=0, row=2, columnspan=2, pady=10)

img = Image.open("images/dictionary.jpg")
img = img.resize((400, 300))
img = ImageTk.PhotoImage(img)
image = Label(image=img)
image.grid(column=0, row=3, columnspan=2)

definition_label = Label(text="Definition:", font=("Times New Roman", 20, "bold"), fg="maroon", bg="chartreuse2")
definition_label.grid(column=0, row=4)

definition = Label(text="None", font=("Times New Roman", 20, "bold"), fg="DodgerBlue", bg="chartreuse2", wraplength=500)
definition.grid(column=1, row=4, pady=10)

pronunciation_label = Label(text="Pronunciation:", font=("Times New Roman", 20, "bold"), fg="maroon", bg="chartreuse2")
pronunciation_label.grid(column=0, row=5)

speak_image = PhotoImage(file="images/speak.png")
pronunciation = Button(image=speak_image, bd=0, bg="chartreuse2",
                       background="chartreuse2", activebackground="chartreuse2", command=pronounce)
pronunciation.grid(column=1, row=5)

example_label = Label(text="Example:", font=("Times New Roman", 20, "bold"), fg="maroon", bg="chartreuse2")
example_label.grid(column=0, row=6, pady=10)

example = Label(text="None", font=("Times New Roman", 20, "bold"), fg="DodgerBlue", bg="chartreuse2", wraplength=500)
example.grid(column=1, row=6)

type_label = Label(text="Type:", font=("Times New Roman", 20, "bold"), fg="maroon", bg="chartreuse2")
type_label.grid(column=0, row=7)

grammar_type = Label(text="None", font=("Times New Roman", 20, "bold"), fg="DodgerBlue", bg="chartreuse2")
grammar_type.grid(column=1, row=7)

window.mainloop()
