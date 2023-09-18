from CURSEWORK import *

RENDER_SCALE = 1.0
HOME_SCREEN_WIDTH = 1600
HOME_SCREEN_HEIGHT = 1000
WHITE = (255, 255, 255)
BLACK = (0,0,0)

EDITOR_SCREEN_WIDTH = 1600
EDITOR_SCREEN_HEIGHT = 1000
EDITOR_SCREEN_SIZE = (EDITOR_SCREEN_WIDTH, EDITOR_SCREEN_HEIGHT)

editor_zoom = 3.6
EDITOR_DISPLAY_WIDTH = EDITOR_SCREEN_WIDTH / editor_zoom
EDITOR_DISPLAY_HEIGHT = EDITOR_SCREEN_HEIGHT / editor_zoom
EDITOR_DISPLAY_SIZE = (EDITOR_DISPLAY_WIDTH, EDITOR_DISPLAY_HEIGHT)

BASE_IMG_PATH = '../assets/images/'
MAP_PATH_SHORTCUT = '../MAPS/map'

editor_controls = {
    'fullscreen': pygame.K_F11,
    'menu': pygame.K_ESCAPE,
    'fill': pygame.K_f,
    'undo': [pygame.K_LCTRL, pygame.K_z],
    'toggle grid': pygame.K_g,
    'show grid': pygame.K_v,
    'show tiles': pygame.K_t,
    'show fps': pygame.K_F8,
    'move left': pygame.K_a,
    'move right': pygame.K_d,
    'move up': pygame.K_w,
    'move down': pygame.K_s,
    'place tile': 1,
    'del tile': 3,
}


THEMES = {
    "Beta-Forge": {
        "main": [0,0,0],
        "secondary": [80,80,80],
        "accent": [255,255,255],
        "text": [255,255,255],
        "grid": [125,125,125]
    }
}