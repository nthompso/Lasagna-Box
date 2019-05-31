#!/usr/bin/python3

from cmd import Cmd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

class Prompt(Cmd):
  def __init__(self, image_filename):
    super(Prompt, self).__init__()
    self.filename = image_filename
    self.img = mpimg.imread(image_filename)
    plt.imshow(self.img)
    plt.ion()
    plt.show()

  def do_exit(self, inp):
    print("Exiting...")
    return True
    
  def do_rotate(self, inp):
    self.img = np.transpose(self.img, (1,0,2))
    plt.clf()
    plt.imshow(self.img)
    plt.draw()

  def do_save(self, inp):
    # TODO
    return

import sys
if len(sys.argv) < 2:
  print ("Usage: python lbox.py image.png")
  exit(1)

print("type 'exit' to close")
Prompt(sys.argv[1]).cmdloop()
