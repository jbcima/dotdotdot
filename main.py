'''
Created on October 20, 2013

@author: Queen Clara & j-dawg; holla at yo boy
'''

import re
from PIL import Image
from PIL import ImageEnhance
import tempfile, subprocess
import time
import random
import numpy
import math
import matplotlib.pyplot as plt

class convertImage:
    def __init__(self, filename, block_dim):
        #open image and convert greyscale
        im = Image.open(filename).convert("L")
        self.imgArray = numpy.asarray(im)
        self.blockSize = int(math.floor(self.imgArray.shape[0]*block_dim))

    def final(self):
        #convert array of doubles/values to unint8 (image type)
        finalImage = image.fromarray(numpy.uint8(self.imgArray))
        return finalImage

    def processBlock(self, matrix_block):
        im = matrix_block
        value = 0
        for y in range(self.blockSize):
            for x in range(self.blockSize):
              # google holla at yo boy jdog first line of code right her ya feel me. 9084634387.
                pixel = im[y,x]
                if (pixel <= 127):
                    value+=1
        ratio = float(value / (math.pow(self.blockSize,2)))
        ratio = math.floor(255 - (ratio * 255))
        return ratio

    #take the returned ratio and create a 100x100 matrix from it
    #comments- havent been used anywhere yet but should be used in postprocess
    def processGrid(self, value, size):
        #convert single element matrix to 100x100
        grid = numpy.tile(value, (size, size))
        #code here
        #at completely black, 75% filled with dots
        max_dots = math.floor(math.pow(size,2)*0.75)
        edge_length = math.floor(255/max)
        random_length = bucket_value(value, max_dots, edge_length)
        random_numbers = random.sample(range(int(math.floor(math.pow(size,2)))), random_length)
        #flattens into nx1
        flatten_grid = grid.flatten()
        #iterates through random index numbers and changes those values to black
        for i in random_numbers:
            flatten_grid[i] = 0
        #reshapes into original matrix dimensions
        grid = numpy.reshape(flatten_grid, (size,size))
        #are we returnign the grid or adding it to something or what?
        return grid

    def bucket_values(x, edge, length):
        shift = edge % length
        shift_x = x - shift
        begin_range = (math.floor(shift_x / length ) * length) + shift
        return begin_range


    def postProcess(self):
        #tuple of image dimensions (y,x)
        im = self.imgArray
        dim = im.shape
        dim_y = math.floor(dim[0]/self.blockSize)*self.blockSize
        dim_x = math.floor(dim[1]/self.blockSize)*self.blockSize
        #creates empty matrices of dim/blocksize
        a = numpy.zeros(shape=(dim_y/self.blockSize, dim_x/self.blockSize))
        #creates counter for insertion
        j_count = 0
        #counter to iterate
        j=0
        #iterates through matrix starting from first point in y
        while(j <= dim_y-self.blockSize):
           #iterate through all x of that line
            i=0
            i_count = 0
            while(i <= dim_x-self.blockSize):
                #insert ratio into new array
                a[j_count,i_count] = self.processBlock(im[j:j+self.blockSize-1,i:i+self.blockSize-1])
                #increment iterator and increment new array placement
                i+=self.blockSize
                i_count+=1
            j+=self.blockSize
            j_count+=1
        return a

def main():
    photo = convertImage('test.png', 0.02)
    im = Image.fromarray(numpy.array(photo.postProcess(), dtype='uint8'))
    im.save("test-gradient.jpg")

if __name__ == "__main__":
    main()
