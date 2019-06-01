#!/usr/bin/python3

from cmd import Cmd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import scipy
import scipy.ndimage

from parser import gen_parser
from zoom import clipped_zoom

class Prompt(Cmd):
    intro = 'Welcome to lbox. Type help or ? to list commands.\n'
    prompt = '(lbox) '
    def __init__(self, image_filename):
        super(Prompt, self).__init__()
        self.filename = image_filename
        self.img = mpimg.imread(image_filename)
        plt.imshow(self.img)
        plt.ion()
        plt.show()
        self.refresh()

    def refresh(self):
        plt.clf()
        plt.imshow(self.img)
        plt.draw()
        plt.pause(0.0001)

    def do_exit(self, inp):
        print("Exiting...")
        return True

    def do_EOF(self, line):
        print("Exiting...")
        return True

    def default(self, inp):
        split = inp.split()
        cmd = split[0]
        inp = ' '.join(split[1:]) if len(split) > 1 else ''

        try:
            f = getattr(self, cmd)
        except:
            print(f"Unknown command '{cmd}'")
            return

        try:
            parse, spec = gen_parser(f)
        except Exception as e:
            print(f"Internal error: {e}")
            return

        try:
            args = parse(inp)
        except Exception as e:
            spec = ' '.join(f"{n} [{t.__name__}]" for n,t in spec)
            print(f"Invalid argument! usage:")
            print(f"  {cmd} {spec}")
            return
        try:
            f(*args)
        except Exception as e:
            print(f"Internal error: {e}")
        return

    #############################################
    ############## Functions Below ##############
    #############################################

    def rotate(self, degrees : float):
        self.img = scipy.ndimage.rotate(self.img, degrees, reshape=False)
        self.refresh()

    def zoom(self, factor : float):
        self.img = clipped_zoom(self.img, factor)
        self.refresh()

    #############################################
    ############## Functions Above ##############
    #############################################


import sys
if len(sys.argv) < 2:
  print ("Usage: python lbox.py image.png")
  exit(1)

print("type 'exit' to close")
Prompt(sys.argv[1]).cmdloop()
