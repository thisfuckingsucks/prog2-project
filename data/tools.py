import pygame, os, math

from data.config import color_dark2


def angle_to_direction(angle):
    return int(math.cos(math.radians(angle))), int(- math.sin(math.radians(angle)))

def direction_to_angle(direction, reverse=False):
    if reverse:
        return int(math.degrees(math.atan2(direction[1], -direction[0])))
    else:
        return int(math.degrees(math.atan2(-direction[1], direction[0])))

def rotate_direction(direction, angle):
    current = int(math.degrees(math.atan2(-direction[1], direction[0])))
    new = current + angle
    #print(f"new {new} = current {current} + angle {angle}")
    return angle_to_direction(new)

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
    base_path = os.path.join("resources", "sprites")
    GFX = {}
    for directory in directories:
        path = os.path.join(base_path, directory)
        GFX[directory] = load_all_gfx(path)
    return GFX



_SUB_DIRECTORIES = ["conveyor", "other", "generator", "machine"]
GFX = graphics_from_directories(_SUB_DIRECTORIES)


# additional generator graphic
__rect = GFX["generator"]["generator1"].get_rect()
def __draw_gen_outline(surface):
    pygame.draw.rect(surface, color_dark2, __rect, width=8)
__draw_gen_outline(GFX["generator"]["generator1"])