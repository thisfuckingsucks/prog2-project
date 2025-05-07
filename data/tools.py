import pygame, os


def set_direction(self, x):
    if x == (1, 0):
        angle = 90
    elif x == (0, -1):
        angle = 180
    elif x == (-1, 0):
        angle = 270
    else:
        angle = 0
    for i in range(len(self.sprites)):
        self.sprites[i] = pygame.transform.rotate(self.sprites[i], angle)
    self.direction = x
    print(angle)

def load_images(images):
    surfaces = []
    for i in images:
        surfaces.append(pygame.image.load(i))
    return surfaces

def load_all_gfx(directory,colorkey=(255,0,255),accept=(".png",".jpg",".bmp")):
    """
    Load all graphics with extensions in the accept argument.  If alpha
    transparency is found in the image the image will be converted using
    convert_alpha().  If no alpha transparency is detected image will be
    converted using convert() and colorkey will be set to colorkey.
    """
    graphics = {}
    for pic in os.listdir(directory):
        name,ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(directory,pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name]=img
    return graphics

def graphics_from_directories(directories):
    base_path = os.path.join(os.pardir,"resources", "sprites")
    GFX = {}
    for directory in directories:
        path = os.path.join(base_path, directory)
        GFX[directory] = load_all_gfx(path)
    return GFX


_SUB_DIRECTORIES = ["conveyor", "other"]
GFX = graphics_from_directories(_SUB_DIRECTORIES)

