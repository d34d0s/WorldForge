from CURSEWORK import *

HOME_SCREEN_WIDTH = 1600
HOME_SCREEN_HEIGHT = 1000
WHITE = (255, 255, 255)
BLACK = (0,0,0)
DEFAULT_FONT_SIZE = 24
FONT = './slkscr.ttf'
# Chosen_Theme = 'Supporter'
Chosen_Theme = 'Beta-Forge'

# tool cooldowns
# time based on seconds
UNDO_CD = 0.07

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
        "accent": [255,255,255],
        "secondary": [80,80,80],
        "hover": [122, 80, 220],
        "text": [255,255,255],
        "grid": [125,125,125],
        "arrow color": [255,255,255],
        "supporter color": [255,180,0],
    },
    "Supporter": {
        "main": [40,40,60],
        "accent": [255,25,25],
        "secondary": [22, 80, 60],
        "hover": [0,0,0],
        "text": [255,255,255],
        "grid": [225,255,40],
        "arrow color": [255,255,255],
        "supporter color": [255,180,0],
    },
}
[226,255,48]