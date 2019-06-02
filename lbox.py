#!/usr/bin/python3

from cmd import Cmd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import scipy
import scipy.ndimage

from cmd_parser import gen_parser
from zoom import clipped_zoom

class Prompt(Cmd):
    intro = 'Welcome to lbox. Type help or ? to list commands.\n'
    prompt = '(lbox) '
    def __init__(self, image_filename):
        super(Prompt, self).__init__()
        self.filename = image_filename
        self.img = mpimg.imread(image_filename)
        self.row,self.col,self.ch = self.img.shape
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

    def imfilter(self, filt : str):
        filt = filt.upper()
        supported = True
        if filt == "GAUSSIAN":
            filt_func = lambda x: scipy.ndimage.gaussian_filter(x, sigma=3) 
        elif filt == "MEDIAN":
            filt_func = lambda x: scipy.ndimage.median_filter(x, size=(3,3))
        else:
            print("Filter type not supported")
            return    
        for idx in range(self.ch): #only works for rgb?
            self.img[:,:,idx] = filt_func(self.img[:,:,idx])
        self.refresh()
    
    def noisy(self, noise: str):
        noise = noise.upper()
        if noise == "GAUSSIAN":
            noise = np.random.normal(0,.05,(self.row,self.col,self.ch))
            temp = np.array(self.img[:,:,:2] + noise[:,:,:2])
            temp[temp > 1] = 1
            temp[temp < 0] = 0
            self.img[:,:,:2] = temp
        elif noise == "S&P":
            svp = 0.5 #amount of salt vs. pepper
            p_val = 0.02 #probability of salt or pepper
            s_coords = [np.random.randint(0, i-1, int(p_val*self.row*self.col*self.ch*svp)) for i in (self.row,self.col,self.ch)]
            p_coords = [np.random.randint(0, i-1, int(p_val*self.row*self.col*self.ch*svp)) for i in (self.row,self.col,self.ch)]
            temp = self.img
            temp[s_coords] = 1
            temp[p_coords] = 0
            self.img[:,:,:2] = temp[:,:,:2]
        else:
            print("Noise type not supported")
            return
        print('success')
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
