import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
from easygui import *
from PIL import Image, ImageTk
from itertools import count
import tkinter as tk
import string
from rich import print as pprint
from constants import GIF_LABELS, AUDIO, IMAGE as img


def Voice2Sign(img_path: str, audio_src:int):
    def func():
        r = sr.Recognizer()

        isl_gif = GIF_LABELS
        arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        
        with sr.Microphone(device_index=audio_src) as source:
            r.adjust_for_ambient_noise(source)
            i = 0
            while True:
                pprint(
                    f"[yellow]Microphone using :[/yellow] {sr.Microphone.list_working_microphones().get(audio_src)}\n[yellow]I am Listening...[/yellow]")
                audio = r.listen(source)

                # recognize speech using Sphinx
                try:
                    a = r.recognize_google(audio, language='en-IN')
                    pprint(
                        f'[yellow]You Said:[/yellow] [cyan]{a.lower()}[/cyan]\n')
                except:
                    a = input("Can't able to understand, please write :- ").lower()
                    print()

                for c in string.punctuation:
                    a = a.replace(c, "")

                if (a.lower() == 'goodbye' or a.lower() == 'good bye' or a.lower() == 'bye'):
                    pprint("[bright_red]oops! Time To say good bye[/bright_red]")
                    break

                elif (a.lower() in isl_gif):

                    class ImageLabel(tk.Label):
                        """a label that displays images, and plays them if they are gifs"""

                        def load(self, im):
                            if isinstance(im, str):
                                im = Image.open(im)
                            self.loc = 0
                            self.frames = []

                            try:
                                for i in count(1):
                                    self.frames.append(
                                        ImageTk.PhotoImage(im.copy()))
                                    im.seek(i)
                            except EOFError:
                                pass

                            try:
                                self.delay = im.info['duration']
                            except:
                                self.delay = 100

                            if len(self.frames) == 1:
                                self.config(image=self.frames[0])
                            else:
                                self.next_frame()

                        def unload(self):
                            self.config(image=None)
                            self.frames = None

                        def next_frame(self):
                            if self.frames:
                                self.loc += 1
                                self.loc %= len(self.frames)
                                self.config(image=self.frames[self.loc])
                                self.after(self.delay, self.next_frame)
                    root = tk.Tk()
                    lbl = ImageLabel(root)
                    lbl.pack()
                    lbl.load(
                        'assets/ISL_Gifs/{0}.gif'.format(a.lower()))
                    root.mainloop()
                else:
                    for i in range(len(a)):
                        if (a[i] in arr):

                            ImageAddress = 'assets/letters/'+a[i]+'.jpg'
                            ImageItself = Image.open(ImageAddress)
                            ImageNumpyFormat = np.asarray(ImageItself)
                            plt.imshow(ImageNumpyFormat)
                            plt.draw()
                            plt.pause(0.8)
                        else:
                            continue

                plt.close()
    while 1:
        msg = "HEARING IMPAIRMENT ASSISTANT"
        choices = ["Live Voice", "All Done!"]
        reply = buttonbox(msg, image=img_path, choices=choices)
        if reply == choices[0]:
            func()
        if reply == choices[1]:
            break


if __name__ == '__main__':
    Voice2Sign(img_path=img, audio_src=AUDIO)
