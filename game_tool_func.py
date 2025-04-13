import pygame


def load_images(images):
    surfaces = []
    for i in images:
        surfaces.append(pygame.image.load(i))
    return surfaces