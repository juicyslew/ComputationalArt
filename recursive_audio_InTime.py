""" TODO: Put your header comment here """

import random
import math
from PIL import Image
import os
import pygame as pg
#from multiprocessing import Pool
import time

def imPlay(im, screen):
    mode = im.mode
    size = im.size
    data = im.tobytes()
    py_image = pg.image.fromstring(data, size, mode)
    screen.blit(py_image,(0,0))
    pg.display.flip()

def build_random_function(min_depth, max_depth, depth = 0):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested listy
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    normfuncs = [['cos_pi_x','cos_pi_2','cos_pi_x'],['sin_pi', 'sin_pi_2', 'sin_pi_x'],'e^x','cos_pi','sin_pi',['avg','avg_2'],'prod']
    #,'avg_x_z','avg_y_z'],'avg' ['abs_x','abs_y','abs_z']
    endfuncs = ['x','y','z']
    i = 0

    dep = round(random.random() * (max_depth - min_depth) + min_depth)
    if depth < dep-1:
        depth += 1
        f = normfuncs[math.floor(random.random() * len(normfuncs))]
        if type(f) == list:
            f = f[math.floor(random.random() * len(f))]
        x = build_random_function(min_depth, max_depth, depth)
        y = build_random_function(min_depth, max_depth, depth)
        z = build_random_function(min_depth, max_depth, depth)
        return [f,x,y,z]
    else:
        f = endfuncs[math.floor(random.random() * len(endfuncs))]
        return f


def evaluate_random_function(f, x, y, z):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    if len(f) == 1:
        done = True
    else:
        done = False
    if done:
        if f[0] == 'x':
            return x
        if f[0] == 'y':
            return y
        if f[0] == 'z':
            return z
    else:
        if f[0] == 'sin_pi_2':
            x = evaluate_random_function(f[1],x,y,z)
            y = evaluate_random_function(f[2],x,y,z)
            return math.sin(math.pi*x*y)
        elif f[0] == 'cos_pi_2':
            x = evaluate_random_function(f[1],x,y,z)
            y = evaluate_random_function(f[2],x,y,z)
            return math.cos(math.pi*x*y)
        elif f[0] == 'cos_pi_x':
            x = evaluate_random_function(f[1],x,y,z)
            return math.cos(math.pi*x)
        elif f[0] == 'sin_pi_x':
            x = evaluate_random_function(f[1],x,y,z)
            return math.sin(math.pi*x)
        elif f[0] == 'cos_pi':
            x = evaluate_random_function(f[1],x,y,z)
            y = evaluate_random_function(f[2],x,y,z)
            z = evaluate_random_function(f[3],x,y,z)
            return math.cos(math.pi*y*x*z)
        elif f[0] == 'sin_pi':
            x = evaluate_random_function(f[1],x,y,z)
            y = evaluate_random_function(f[2],x,y,z)
            z = evaluate_random_function(f[3],x,y,z)
            return math.sin(math.pi*y*x*z)
        elif f[0] == 'e^x':
            x = evaluate_random_function(f[1],x,y,z)
            return math.exp(x-1)
        elif f[0] == 'avg_2':
            x = evaluate_random_function(f[1],x,y,z)
            y = evaluate_random_function(f[2],x,y,z)
            return 1/2 * (x+y)
        elif f[0] == 'avg':
            x = evaluate_random_function(f[1],x,y,z)
            y = evaluate_random_function(f[2],x,y,z)
            z = evaluate_random_function(f[3],x,y,z)
            return 1/3 * (x+y+z)
        elif f[0] == 'prod':
            x = evaluate_random_function(f[1],x,y,z)
            y = evaluate_random_function(f[2],x,y,z)
            z = evaluate_random_function(f[3],x,y,z)
            return x*y*z
#evaluate_random_function(['avg',['cos_pi',['x'], ['y']],['y']], 0, .2)
#evaluate_random_function(['prod',['cos_pi',['avg',['x'],['y']]],['sin_pi',['x'],['y']]], .75, -.5) #Actually Test This

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    res = (val - input_interval_start)/(input_interval_end - input_interval_start)*(output_interval_end - output_interval_start)+output_interval_start
    return res


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(num_pics, screen, c, mindep, maxdep, x_size=350, y_size=350):
    os.system('rm frame*')
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(mindep,maxdep)
    green_function = build_random_function(mindep,maxdep)
    blue_function = build_random_function(mindep,maxdep)

    print('r: ')
    print(red_function)
    print('g: ')
    print(green_function)
    print('b: ')
    print(blue_function)

    t = 0
    while t < num_pics:
        name = 'frame' + str(t)+'.png'

        # Create image and loop over all pixels
        im = Image.new("RGB", (x_size, y_size))
        pixels = im.load()
        for i in range(x_size):
            for j in range(y_size):
                x = remap_interval(i, 0, x_size, -1, 1)
                y = remap_interval(j, 0, y_size, -1, 1)
                z = remap_interval(t, 0, num_pics, -1, 1)
                pixels[i, j] = (
                        color_map(evaluate_random_function(red_function, x, y, z)),
                        color_map(evaluate_random_function(green_function, x, y, z)),
                        color_map(evaluate_random_function(blue_function, x, y, z))
                        )
        imPlay(im, screen)
        t+=1


if __name__ == '__main__':
    frame_num = 80
    x_size = 80
    y_size = 80
    mindep = 3
    maxdep = 4
    filename = 'testmov13'
    pg.init()
    size=(x_size,y_size)
    screen = pg.display.set_mode(size)
    c = pg.time.Clock() # create a clock object for timing
    #import doctest
    #doctest.run_docstring_examples(build_random_function, globals())

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art(frame_num, screen, c, mindep, maxdep, x_size, y_size)

    #producer = Process(target=generate_art, args=(q, frame_num, x_size, y_size,))
    #producer.start()

    #visualizer = Process(target=imSave, args=(q,))
    #visualizer.start()

    #visualizer.join()
    #os.system('avconv -i frame%d.png -vb 20M ' + filename + '.avi')

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    # test_image("noise.png")
