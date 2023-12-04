from PIL import Image
import numpy as np
import math
import os

import Util.gridSolver
import Util.colorHelper
import Util.guiDisplay

DIR_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
INPUT_IMAGE_PATH  = "input_images/"
OUTPUT_IMAGE_PATH = "output_images/"

def getGridFromImg(image_path, cell_len=1):
    s = (-1, -1)
    e = (-1, -1)

    with open(image_path, 'r+b') as f:
        with Image.open(f) as img:
            image_width, image_height = img.size
            horizontal_cell_count = math.floor(image_width / cell_len)
            vertical_cell_count = math.floor(image_height / cell_len)
            image_celled_width = cell_len * horizontal_cell_count
            image_celled_height = cell_len * vertical_cell_count
            pixels = img.load()
            for y in np.arange(image_height):
                for x in np.arange(image_width):
                    r, g, b, a = pixels[x, y]
                    if Util.colorHelper.START_COLOR == (r, g, b):
                        s = (math.floor(x / cell_len), math.floor(y / cell_len))
                    elif Util.colorHelper.END_COLOR == (r, g, b):
                        e = (math.floor(x / cell_len), math.floor(y / cell_len))
                        
            grid = np.array([[0 for x in range(horizontal_cell_count)] for y in range(vertical_cell_count)])
            new_img_pixels = np.array([[(0, 0, 0) for x in range(horizontal_cell_count)] for y in range(vertical_cell_count)])
            for y in np.arange(0, image_celled_height, cell_len):
                for x in np.arange(0, image_celled_width, cell_len):
                    r, g, b, a = pixels[x, y]
                    new_img_pixels[math.floor(y / cell_len)][math.floor(x / cell_len)] = (r, g, b)
                    grid[math.floor(y / cell_len)][math.floor(x / cell_len)] = Util.colorHelper.COLOR_TO_WEIGHT_LOOKUP.get((r, g, b), 1)
            
            new_img_pixels[s[1]][s[0]] = Util.colorHelper.START_COLOR
            new_img_pixels[e[1]][e[0]] = Util.colorHelper.END_COLOR
            return grid, s, e, new_img_pixels


def saveUpdatedImgFromGrid(min_path, new_img_pixels, algo_type):
    if min_path == []: return
    pixels = new_img_pixels.copy()
    for y in range(len(pixels)):
        for x in range(len(pixels[0])):
            if min_path[y][x] == Util.gridSolver.VISITED_SYMBOL:
                pixels[y][x] = Util.colorHelper.scaleColorValue(pixels[y][x], 0.75)
            elif min_path[y][x] == Util.gridSolver.PATH_SYMBOL:
                pixels[y][x] = Util.colorHelper.PATH_COLOR
    img = Image.fromarray(np.uint8(pixels), 'RGB')
    
    stem, ext = filename.split('.')
    full_output_path = os.path.join(DIR_PATH, OUTPUT_IMAGE_PATH, f"{stem}_{algo_type}.{ext}").replace('\\', '/')
    img.save(full_output_path)
    return full_output_path


if __name__ == "__main__":
    CELL_SIZE = 1
    for filename in os.listdir(INPUT_IMAGE_PATH):
        if filename.endswith('.png'):
            img_path = os.path.join(INPUT_IMAGE_PATH, filename)
            grid, start, end, new_img_pixels = getGridFromImg(img_path, CELL_SIZE)
            print(f"Proccessing: {img_path}")
            
            min_dist, min_path = Util.gridSolver.BFS(grid, start, end)
            img_path_1 = saveUpdatedImgFromGrid(min_path, new_img_pixels, "BFS")

            min_dist, min_path = Util.gridSolver.Dijkstra(grid, start, end)
            img_path_2 = saveUpdatedImgFromGrid(min_path, new_img_pixels, "Dijkstra")

            min_dist, min_path = Util.gridSolver.Astar(grid, start, end)
            img_path_3 = saveUpdatedImgFromGrid(min_path, new_img_pixels, "Astar")
            
            try:
                app = Util.guiDisplay.App()
                app.addImages(img_path_1, img_path_2, img_path_3)
                app.mainloop()
            except Exception as e:
                pass
                
            