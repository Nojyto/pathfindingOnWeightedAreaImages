from PIL import Image
import numpy as np
import math
import os

import Util.gridSolver

INPUT_IMAGE_PATH = "input_images/"
OUTPUT_IMAGE_PATH = "output_images/"

def getGridFromImg(image_path, cell_len):
    weight_color_lookup = {(185, 122, 87) : 0, (63, 72, 204): 2, (127, 127, 127): 200}
    endpoint_color_lookup = {(237, 28, 36): "start", (34, 177, 76): "end"}
    s = (-1, -1)
    e = (-1, -1)
    # st = set()
    with open(image_path, 'r+b') as f:
        with Image.open(f) as img:
            image_width, image_height = img.size
            image_celled_width = cell_len * math.floor(image_width / cell_len)
            image_celled_height = cell_len * math.floor(image_height / cell_len)
            pixels = img.load()

            for y in np.arange(image_height):
                for x in np.arange(image_width):
                    r, g, b, a = pixels[x, y]
                    # st.add((r, g, b, a))
                    endpoint_state = endpoint_color_lookup.get((r, g, b), "")
                    if endpoint_state == "": continue

                    if endpoint_state == "start":
                        s = (math.floor(x / cell_len), math.floor(y / cell_len))
                    elif endpoint_state == "end":
                        e = (math.floor(x / cell_len), math.floor(y / cell_len))
                        
            grid = np.array([[0 for x in range(math.floor(image_width / cell_len))] for y in range(math.floor(image_height / cell_len))])
            org_img_pixels = np.array([[(0, 0, 0) for x in range(math.floor(image_width / cell_len))] for y in range(math.floor(image_height / cell_len))])
            for y in np.arange(0, image_celled_height, cell_len):
                for x in np.arange(0, image_celled_width, cell_len):
                    r, g, b, a = pixels[x, y]
                    org_img_pixels[math.floor(y / cell_len)][math.floor(x / cell_len)] = (r, g, b)
                    grid[math.floor(y / cell_len)][math.floor(x / cell_len)] = weight_color_lookup.get((r, g, b), 1)
            
            org_img_pixels[s[1]][s[0]] = (237, 28, 36) 
            org_img_pixels[e[1]][e[0]] = (34, 177, 76)
            # print(st)
            return grid, s, e, org_img_pixels


def saveUpdatedImgFromGrid(min_path, org_img_pixels, algo_type, min_dist):
    pixels = org_img_pixels.copy()
    for y in range(len(min_path)):
        for x in range(len(min_path)):
            if min_path[y][x] == Util.gridSolver.PATH_SYMBOL:
                pixels[y][x] = (0, 0, 0)
    img = Image.fromarray(np.uint8(pixels), 'RGB')
    
    print(f"{algo_type} dist:\t", min_dist)
    stem, ext = filename.split('.')
    img.save(os.path.join(OUTPUT_IMAGE_PATH, f"{stem}_{algo_type}.{ext}"))


if __name__ == "__main__":
    for filename in os.listdir(INPUT_IMAGE_PATH):
        if filename.endswith('.png'):
            img_path = os.path.join(INPUT_IMAGE_PATH, filename)

            grid, start, end, org_img_pixels = getGridFromImg(img_path, 1)
            
            # Util.gridSolver.printGrid(grid)
            
            min_dist, min_path = Util.gridSolver.BFS(grid, start, end)
            saveUpdatedImgFromGrid(min_path, org_img_pixels, "BFS", min_dist)

            min_dist, min_path = Util.gridSolver.Dijkstra(grid, start, end)
            saveUpdatedImgFromGrid(min_path, org_img_pixels, "Dijkstra", min_dist)

            min_dist, min_path = Util.gridSolver.Astar(grid, start, end)
            saveUpdatedImgFromGrid(min_path, org_img_pixels, "Astar", min_dist)