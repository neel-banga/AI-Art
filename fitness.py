from PIL import Image
from random import randint
import numpy
import os
from tqdm import tqdm 

FRAME = 1024

data = numpy.zeros((FRAME, FRAME, 3), dtype=numpy.uint8)

def make_combos(start = 0, end = FRAME):
    combinations = []

    for i in range(start, end+1):
        for j in range(start, end+1):
            combinations.append([i, j])

    num_combinations = len(combinations)
    a = [[0] * 2 for _ in range(num_combinations)]

    for idx, combo in enumerate(combinations):
        a[idx] = combo

    return a

def resize_image(img_path, width = FRAME, height = FRAME):
    image = Image.open(img_path)
    resized_image = image.resize((width, height))
    os.remove(img_path)
    resized_image.save(img_path)

def get_pixel_values(image_path):
    image = Image.open(image_path)
    pixel_data = image.load()

    return pixel_data

    width, height = image.size

    for y in range(height):
        for x in range(width):
            pixel_value = pixel_data[x, y]
            print(f"Pixel at ({x}, {y}): {pixel_value}")

def fitness(image, target_image = 'starry.png', human_input = False):
    
    a = make_combos()
    current_pixels = get_pixel_values(image)
    target_pixels = get_pixel_values(target_image)
    loss = 0
    l = 0

    def get_pixel_value(num, val1, val2):
        if num == 0:
            return val1+val2
        if num == 1:
            return val1*val2
        if num == 2:
            return val1/val2

    for row in tqdm(a):
        x, y = row
        try:
            rc, gc, bc = current_pixels[x,y]
            rt, gt, bt = target_pixels[x,y]
        except:
            continue

        operation1, operation2, operation3 = randint(0,2), randint(0,2), randint(0,2)

        loss += (get_pixel_value(operation1, rt ,randint(1,20)) - rc) + (get_pixel_value(operation2, bt ,randint(1,20)) - bc) +(get_pixel_value(operation3, gt ,randint(1,20)) - gc)

    if human_input:
        while True:
            rating = int(input('Rate The Image On A Scale From 1-10: '))
            if 0 < rating < 11:
                break
            else:
                print('Invalid')

        # 1024 * 1024 * 256 = 268435456
        print(loss)
        loss -= FRAME * FRAME * 256 * human_input

    return loss

def save_image(data, path):
    image = Image.fromarray(data)
    image.save(path)
    #return image

#print(fitness('img.png'))