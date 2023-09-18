""" CURSEWORK """
""" Developed by Setoichi"""
import sys, json, os
import time, datetime, pytz
import random, copy
import pygame.gfxdraw
import pygame_gui
from pygame_gui.elements.ui_scrolling_container import UIScrollingContainer
import math
from csv import reader
from pygame.locals import *
from functools import partial
from os import walk, sep, listdir
from collections import deque
import pygame
import pygame.freetype
import re
import tkinter as tk
from tkinter import filedialog

pygame.init()

""" GOD MODE CONSTANTS """
""" (/0_0)/ """ 
PYRECT = pygame.Rect
VECTOR2 = pygame.math.Vector2
PYSURFACE = pygame.Surface
SCALE = pygame.transform.scale


""" GAME OBJECTS """
class Camera:
    
    def __init__(self, game, level_size, display_size, camera_speed, scroll_interpolation):
        self.game = game
        self.level_size = VECTOR2(level_size)
        self.display_size = VECTOR2(display_size)
        self.scroll = VECTOR2(0, 0)
        self.scroll_interpolation = scroll_interpolation
        self.scroll_speed = camera_speed
        self.DEADZONE_RADIUS = 8
        self.in_deadzone = False

        # panning config
        self.pan_speed = camera_speed/2
        self.panning = False
        self.pan_target = None

    def scroll_camera(self, target):
        desired_scroll = VECTOR2(
            target.rect().centerx - self.display_size.x // 2,
            target.rect().centery - self.display_size.y // 2
        )
        
        distance_to_target = (self.scroll - desired_scroll).length()

        # If the camera is outside the deadzone, follow the target normally
        if distance_to_target >= self.DEADZONE_RADIUS:
            self.scroll += ((desired_scroll - self.scroll) * self.scroll_speed) / self.scroll_interpolation * self.game.dt

    def pan_camera(self, target):
        if type(target) == VECTOR2:
            desired_scroll = VECTOR2(
                target.x - self.display_size.x // 2,
                target.y - self.display_size.y // 2
            )
            # Apply interpolation for smooth camera movement
            self.scroll += ((desired_scroll - self.scroll) * self.pan_speed) / self.scroll_interpolation * self.game.dt

    def set_target(self, target, display_size):
        self.display_size = display_size
        # Calculate the desired camera position
        if not self.panning:
            self.scroll_camera(target)
        else:
            self.pan_target = target
            self.pan_camera(self.pan_target)

        # Constrain camera within the level bounds
        self.scroll.x = max(0, min(self.scroll.x, self.level_size.x - self.display_size.x))
        self.scroll.y = max(0, min(self.scroll.y, self.level_size.y - self.display_size.y))

    def get_offset(self):
        return VECTOR2(int(self.scroll.x), int(self.scroll.y))


class Entity(pygame.sprite.Sprite):

    def __init__(self, size: int, position: tuple, speed: int, groups: list):
        super().__init__(groups)
        self.speed = speed
        self.size = VECTOR2(size, size)
        self.position = VECTOR2(position)

        self.image = PYSURFACE(self.size)
        self.rect = PYRECT(self.position, self.size)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect.topleft)

    def update(self):
        pass


class PhysicsEntity:
    
    def __init__(self, game, e_type, position, size, rect_size=VECTOR2(32,32)):
        self.game = game
        self.type = e_type
        self.rect_size = rect_size
        self.position = position
        self.size = VECTOR2(size)
        self.velocity = VECTOR2(0, 0)
        self.jumping = False
        self.falling = False
        self.gravity = True
        self.flip = False

    def rect(self):
        return pygame.Rect((self.position.x, self.position.y), (self.rect_size[0], self.rect_size[1]))

    def horizontal_movement_collision(self, tilemap, movement, dt):
        movement = movement
        self.position.x += movement.x * dt
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.position):
            if entity_rect.colliderect(rect):
                if movement.x > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if movement.x < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.position.x = entity_rect.x

    def vertical_movement_collision(self, tilemap, movement, gravity, dt):
        movement = movement
        if self.gravity:
            self.velocity.y = min(280, self.velocity.y + gravity)
        movement.y = self.velocity.y
        self.position.y += movement.y * dt
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.position):
            if entity_rect.colliderect(rect):
                if movement.y > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if movement.y < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.position.y = entity_rect.y

    def update(self, tilemap, anim_list, gravity, dt):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        movement = VECTOR2(self.velocity.x, self.velocity.y)

        self.horizontal_movement_collision(tilemap=tilemap, movement=movement, dt=dt)
        self.vertical_movement_collision(tilemap=tilemap, movement=movement, gravity=gravity, dt=dt)
        

        if movement.x > 0:
            self.flip = False
        if movement.x < 0:
            self.flip = True

        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        surf.blit(pygame.transform.flip(self.animation.img()[0], self.flip, False), (self.position.x - int(offset[0]) + self.anim_offset.x, self.position.y - int(offset[1]) + self.anim_offset.y))


class Projectile:
    def __init__(self, name, type, size, spawn_pos, player, facing_right, game, projectile_image_path:str=""):
        self.name = name
        self.type = type
        self.size = size
        self.player = player
        self.game = game
        self.speed = 10
        self.frame_index = 0
        self.frames_passed = 0
        self.has_anim = False
        self.import_assets(projectile_image_path)
        self.rect = self.animation.animation[0].get_rect()
        self.rect.center = spawn_pos[0], spawn_pos[1]
        if self.has_anim:
            if not facing_right:
                self.speed *= -1
                self.animation.animation = [pygame.transform.flip(image, True, False) for image in self.animation.animation]
            self.image = self.animation.update(0)
    
    def import_assets(self, projectile_image_path):
        path = projectile_image_path
        if path not in {""}:
            self.has_anim = True
            self.animation = []
            full_path = path
            original_images = import_folder(full_path)
            scaled_images = scale_images(original_images, (100, 40))
            self.animation = Animator(self.game, scaled_images, 0.05, loop=True)
        else:
            pass

    def update(self, dt):
        self.move(dt)

        # check if 50 ms has passed since projectile spawning
        self.frames_passed += 1
        if self.frames_passed >= 10:
            self.player.throwing_proj = False

        if self.speed > 0:
            x = self.rect.left
            start_angle, end_angle = (120, 220)
        else:
            x = self.rect.right
            start_angle, end_angle = (60, -60)
        y = self.rect.centery
        x += random.randint(-3, 3)
        y += random.randint(-3, 3)


    def move(self, dt):
        self.rect.x += self.speed
        if self.rect.x < 0 or self.rect.x > self.game.settings["screen_width"]:
            self.projectile = None
            self.throwing_proj = False
        if self.has_anim:
            self.animation.update(dt)

    def draw(self, surf):
        if self.speed > 0:
            x = self.rect.left
        else:
            x = self.rect.right
        #pygame.draw.rect(surf, (0,0,0), self.rect)
        surf.blit(self.image, self.rect.topleft)


class Tilemap:
    
    def __init__(self, map_name, game, tileset, tile_size=32, physics_tiles_names:set()={''}):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.map_name = map_name
        self.offgrid_tiles = []
        self.NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (0, 0),(1, 0), (1, 1), (0, 1), (1, -1), (-1, 1),]
        self.PHYSICS_TILES = set(physics_tiles_names)
    
    def get_map_size(self, in_tiles=True):
        if in_tiles:
            max_x = 0
            max_y = 0
            for location in self.tilemap:
                x, y = map(int, location.split(';'))
                max_x = max(max_x, x)
                max_y = max(max_y, y)
            return VECTOR2(max_x + 1, max_y + 1)
        else:
            max_x = 0
            max_y = 0
            for location in self.tilemap:
                tile = self.tilemap[location]
                max_x = max(max_x, tile['position'][0] * self.tile_size)
                max_y = max(max_y, tile['position'][1] * self.tile_size)
            return VECTOR2(int(max_x + self.tile_size), int(max_y + self.tile_size))

    def solid_tile_check(self, position):
        tile_location = str(int(
            position[0] // self.tile_size)) + ";" + str(int(position[1] // self.tile_size))
        if tile_location in self.tilemap:
            if self.tilemap[tile_location]['id'] in self.PHYSICS_TILES:
                return self.tilemap[tile_location]

    def extract_tile_info(self, tile_id, keep=False):
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['id']) in tile_id:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)

        for location in self.tilemap.copy():
            tile = self.tilemap[location]
            if (tile['id']) in tile_id:
                matches.append(tile.copy())
                matches[-1]['position'] = matches[-1]['position'].copy()
                matches[-1]['position'] *= self.tile_size
                matches[-1]['position'] *= self.tile_size
                if not keep:
                    del self.tilemap[location]
        return matches

    def tiles_around(self, position):
        tiles = []
        tile_location = (int(position.x // self.tile_size),
                         int(position.y // self.tile_size))
        for offset in self.NEIGHBOR_OFFSETS:
            check_location = str(
                tile_location[0] + int(offset[0])) + ';' + str(tile_location[1] + int(offset[1]))
            if check_location in self.tilemap:
                tiles.append(self.tilemap[check_location])
        return tiles

    def physics_rects_around(self, position):
        rects = []
        for tile in self.tiles_around(position):
            if tile['type'] in self.PHYSICS_TILES:
                rects.append(pygame.Rect(tile['position'][0] * self.tile_size,
                             tile['position'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects

    def export_as_png(self, save_path):
        # Get the map size in pixels
        map_size = self.get_map_size(in_tiles=False)

        # Create a surface to render the map
        export_surface = pygame.Surface(map_size)

        # Fill the surface with a background color (e.g., white)
        export_surface.fill((255, 255, 255))

        # Render each tile onto the surface
        for location in self.tilemap:
            tile = self.tilemap[location]
            tile_image = self.game.assets[f'tileset'][tile['id']]
            position = (tile['position'][0] * self.tile_size, tile['position'][1] * self.tile_size)
            export_surface.blit(tile_image, position)

        # Create the full path for saving the image
        export_filename = f'{self.map_name}.png'
        full_export_path = os.path.join(save_path, export_filename)

        # Save the surface as a PNG image
        pygame.image.save(export_surface, full_export_path)
        print(f"Map exported as {full_export_path}")

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[f'tileset'][tile['id']], (
                tile['position'][0] - int(offset[0]), tile['position'][1] - int(offset[1])))

        for x in range(int(offset[0]) // self.tile_size, (int(offset[0]) + surf.get_width()) // self.tile_size + 1):
            for y in range(int(offset[1]) // self.tile_size, (int(offset[1]) + surf.get_height()) // self.tile_size + 1):
                location = str(x) + ';' + str(y)
                if location in self.tilemap:
                    tile = self.tilemap[location]
                    surf.blit(self.game.assets[f'tileset'][tile['id']], (tile['position'][0] * self.tile_size - int(
                        offset[0]), tile['position'][1] * self.tile_size - int(offset[1])))


""" USER INTERFACE """
class Button:
    def __init__(self, game, text, pos, function, base=(0,0,300,81), hovered=(0,0,300,81), base_color=(77,77,77,50), hover_color=(77, 77, 77, 100), text_color=(230, 230, 230), text_size=30, hovered_pos=None, id=None):
        self.game = game
        self.text = text
        self.function = function
        self.init_rects(base, hovered)
        self.rect.center = pos
        self.text_color = text_color
        self.base_color = base_color
        self.hover_color = hover_color
        self.size = text_size
        self.id = id

        if hovered_pos is None:
            self.hovered_pos = pos
        else:
            self.hovered_pos = hovered_pos
        self.is_hovered = False

    def init_rects(self, base, hovered):
        if isinstance(base, str):
            self.base = get_image(base)
            self.rect = self.base.get_rect()
            self.surf = PYSURFACE((self.rect[2], self.rect[3]), pygame.SRCALPHA)
            self.base_func = self.draw_image
        else:
            self.base = PYRECT(base)
            self.rect = self.base.copy()
            self.surf = PYSURFACE((base[2], base[3]), pygame.SRCALPHA)
            self.base_func = self.draw_rect
        self.center = self.surf.get_rect().center

        if isinstance(hovered, str):
            self.hovered = get_image(hovered)
            self.hover_func = self.draw_image
        else:
            self.hovered = PYRECT(hovered)
            self.hover_func = self.draw_rect

    def update(self, event):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos[0], pos[1]):
            self.is_hovered = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #play_sound("Assets/sounds/click.mp3")

                if isinstance(self.function, type):
                    self.game.scene_manager.scenes = [self.function(self.game)]
                    return

                if self.function != None:
                        if self.function == pygame.quit:
                            self.function()
                            sys.exit()
                        elif self.id is not None:
                            self.function(self.id)
                        else:
                            self.function()
        else:
            self.is_hovered = False

    def draw(self):
        self.surf.fill((0,0,0,0))
        if self.is_hovered:
            self.hover_func(self.hovered, self.hover_color)
        else:
            self.base_func(self.base, self.base_color)
        if self.text:
            draw_text(self.surf, self.text, self.center, self.size, self.text_color)
        self.game.screen.blit(self.surf, self.rect.topleft)

    def draw_rect(self, rect, color):
        pygame.draw.rect(self.surf, color, rect)

    def draw_image(self, image, color):
        self.surf.blit(image, (0,0))


class TextAnimation:
    SCORE_ADD_SOUND = ''
    # SCORE_ADD_SOUND = 'assets/sounds/score_add.wav'
    INCREMENT = 1
    INCREMENT_DELAY = 0.04
    FONT_SIZE = 50
    CAP_RESET_TIME = 2.0  # Time in seconds to reset the score after capping
    START_COLOR = (255, 255, 0)  # Bright yellow starting color
    END_COLOR = (255, 0, 0)  # Red ending color
    MAX_HITS_FOR_COLOR_CHANGE = 10  # Number of hits to reach the red color
    FADE_DURATION = 1.0

    def __init__(self, game):
        self.game = game
        self.max_score = 0
        self.score = 0
        self.hits = 0
        self.capped = False
        self.cap_timer = 0.0  # Timer to track time since capping
        self.increment_timer = 0.0  # Timer to control increment frequency
        self.fading = False  # Track if the text is currently fading
        self.fade_timer = 0.0  # Timer to control the fade duration
        self.text_surface = PYSURFACE((200, 100), pygame.SRCALPHA)  # Alpha-supported surface, adjust size as needed
        self.target_player = None

    def apply_damage(self, damage):
        """Applies damage and handles score increment, sound effect, and hit count."""
        if self.score == self.max_score:
            self.play_sound(repeat=False)
        self.max_score += damage
        self.capped = False
        self.hits += 1

    def increment_score(self):
        """Increments the score gradually until it reaches the max score."""
        self.increment_timer += self.game.dt
        if self.increment_timer >= self.INCREMENT_DELAY:
            self.increment_timer = 0.0  # Reset the increment timer
            if self.score < self.max_score:
                self.score += self.INCREMENT
                if self.score >= self.max_score:
                    self.score = self.max_score
                    self.cap_timer = 0.0
                    self.capped = True

    def reset_score(self):
        """Resets the score if capped and no new score is added for CAP_RESET_TIME seconds."""
        if self.capped:
            self.cap_timer += self.game.dt
            if self.cap_timer >= self.CAP_RESET_TIME:
                self.fading = True  # Start fading instead of immediate reset

        if self.fading:
            self.fade_timer += self.game.dt
            if self.fade_timer >= self.FADE_DURATION:
                self.__init__(self.game)

    def play_sound(self, repeat):
        """Plays the sound effect for score addition."""
        pass#play_sound(self.SCORE_ADD_SOUND, repeat)

    def draw_text(self, player_x, player_y):
        """Draws the score text with appropriate color adjustments."""
        if self.max_score != 0:
            # Calculate the color based on the hits and defined colors
            t = min(self.hits / self.MAX_HITS_FOR_COLOR_CHANGE, 1.0)  # Transition factor between 0 and 1
            color = (
                int(self.START_COLOR[0] + t * (self.END_COLOR[0] - self.START_COLOR[0])),
                int(self.START_COLOR[1] + t * (self.END_COLOR[1] - self.START_COLOR[1])),
                0,
                0
            )

            text_size = self.FONT_SIZE + (self.hits // 5)

            # Apply the fade effect if fading
            if self.fading:
                alpha = int(255 * (1.0 - (self.fade_timer / self.FADE_DURATION)))
                self.text_surface.fill((0, 0, 0, 0))  # Clear the surface with transparent color
                draw_text(self.text_surface, str(self.score), (0, 0), text_size, (color[0], color[1], color[2]), center=False)
                self.text_surface.set_alpha(alpha)  # Set the alpha value for the entire surface
            else:
                draw_text(self.text_surface, str(self.score), (0, 0), text_size, (color[0], color[1], color[2]), center=False)
                self.text_surface.set_alpha(255)

            self.game.screen.blit(self.text_surface, (player_x + 10, player_y - 50))

    def animate(self, damage=None):
        """Main animation method that coordinates the animation process."""
        if self.target_player is not None:
            self.text_surface.fill((0,0,0,0))
            pos = self.target_player.rect.topright
            x, y = pos
            if damage is not None:
                self.apply_damage(damage)
                self.fading = False  # Reset the fade if new damage comes in
                self.fade_timer = 0.0
            self.increment_score()
            self.reset_score()
            self.draw_text(x, y)


class Slider:
    def __init__(self, x, y, w, h, volume):
        self.circle_x = x
        self.volume = volume
        self.sliderRect = PYRECT(x, y, w, h)
        self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.sliderRect)
        self.circle = pygame.draw.circle(screen, (255, 240, 255), (self.circle_x, (self.sliderRect.h / 2 + self.sliderRect.y)), self.sliderRect.h * 1.5)

    def get_volume(self):
        return self.volume

    def set_volume(self, num):
        self.volume = num

    def update_volume(self, x):
        if x < self.sliderRect.x:
            self.volume = 0
        elif x > self.sliderRect.x + self.sliderRect.w:
            self.volume = 100
        else:
            self.volume = int((x - self.sliderRect.x) / float(self.sliderRect.w) * 100)

    def on_slider(self, x, y) -> bool:
        if self.on_slider_hold(x, y) or self.sliderRect.x <= x <= self.sliderRect.x + self.sliderRect.w and self.sliderRect.y <= y <= self.sliderRect.y + self.sliderRect.h:
            # print("mouse on slider")
            return True
        else:
            return False

    def on_slider_hold(self, x, y):
        if ((x - self.circle_x) * (x - self.circle_x) + (y - (self.sliderRect.y + self.sliderRect.h / 2)) * (y - (self.sliderRect.y + self.sliderRect.h / 2)))\
            <= (self.sliderRect.h * 1.5) * (self.sliderRect.h * 1.5):
            return True
        else:
            return False

    def handle_event(self, screen, x):
        if x < self.sliderRect.x:
            self.circle_x = self.sliderRect.x
        elif x > self.sliderRect.x + self.sliderRect.w:
            self.circle_x = self.sliderRect.x + self.sliderRect.w
        else:
            self.circle_x = x
        self.draw(screen)
        self.update_volume(x)


""" SUPPORT CLASSES """
class Animator:
    def __init__(self, game, animation, frame_duration, loop=False):
        self.game = game
        self.animation = animation
        self.frame_duration = frame_duration
        self.current_time = 0
        self.frame_index = 0
        self.loop = loop
        self.done = False
        self.image = PYSURFACE((32, 32))

    def update(self, dt):
        # add time in ms since last frame
        self.current_time += dt

        # when cumulative time reaches the frame_duration
        if self.current_time > self.frame_duration:

            if self.frame_index >= len(self.animation) - 1:

                # set the flag for an animation that should not repeat
                if not self.loop:
                    self.done = True
                else:
                    self.frame_index = 0
            else:
                self.frame_index += 1

            # reset the cumulative time for the next frame
            self.current_time = 0

        # return the current frame of the animation list
        self.image = self.animation[self.frame_index]
        return self.animation[self.frame_index]

    def reset(self):
        self.current_time = 0
        self.frame_index = 0
        self.done = False


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.image_masks = []
        [self.image_masks.append(pygame.mask.from_surface(image)) for image in self.images]
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
    
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return [self.images[int(self.frame / self.img_duration)], self.image_masks]


class GenerateColorGradient:
    def __init__(self, init_color, target_color):
        # Init color fade vars
        self.steps = 200
        self.color = init_color
        self.colorFrom = list(init_color)
        self.colorTo = list(target_color)
        self.inv_steps = 1.0 / self.steps
        self.step_R = (self.colorTo[0] - self.colorFrom[0]) * self.inv_steps
        self.step_G = (self.colorTo[1] - self.colorFrom[1]) * self.inv_steps
        self.step_B = (self.colorTo[2] - self.colorFrom[2]) * self.inv_steps
        self.r = self.colorFrom[0]
        self.g = self.colorFrom[1]
        self.b = self.colorFrom[2]
        self.target_reached = False

    def calc_steps(self, colorTo):
        self.colorFrom = self.color
        self.colorTo = colorTo
        self.step_R = (self.colorTo[0] - self.colorFrom[0]) * self.inv_steps
        self.step_G = (self.colorTo[1] - self.colorFrom[1]) * self.inv_steps
        self.step_B = (self.colorTo[2] - self.colorFrom[2]) * self.inv_steps

    def next(self):
        self.r += self.step_R
        self.g += self.step_G
        self.b += self.step_B
        self.color = (int(self.r), int(self.g), int(self.b))

        # check if target has been reached
        if all([(self.step_R >= 0 and self.r >= self.colorTo[0]) or (self.step_R <= 0 and self.r <= self.colorTo[0]),
            (self.step_G >= 0 and self.g >= self.colorTo[1]) or (self.step_G <= 0 and self.g <= self.colorTo[1]),
            (self.step_B >= 0 and self.b >= self.colorTo[2]) or (self.step_B <= 0 and self.b <= self.colorTo[2])]):
            self.target_reached = True
        
        return list(self.color)

    def lerp(self, a, b, t):
        return a + (b - a) * t

    def brighten_gradient(self, gradient_colors, factor=1.5):
        brightened_colors = []
        for i, color in enumerate(gradient_colors):
            t = i / (len(gradient_colors) - 1)
            r = int(self.lerp(self.colorFrom[0], self.colorTo[0], t))
            g = int(self.lerp(self.colorFrom[1], self.colorTo[1], t))
            b = int(self.lerp(self.colorFrom[2], self.colorTo[2], t))
            
            brightened_color = (min(int(r * factor), 255), min(int(g * factor), 255), min(int(b * factor), 255))
            brightened_colors.append(brightened_color)
        
        return brightened_colors

    """ 
    Returns a list of all the colors in between the 
    initial color and target color 
    """
    def generate_gradient(self, test=False):
        gradient = []
        while not self.target_reached:
            gradient.append(self.next())
            color = self.next()
            gradient.append((color[0], color[1], color[2]))
        gradient = self.brighten_gradient(gradient)
        return gradient


class Particle:
    
    def __init__(self, game, type, position=VECTOR2(0, 0), velocity=VECTOR2(0, 0), frame=0, animation:bool=False, animation_images_path:str="", animation_speed:int=0, loop_animation:bool=False):
        self.game = game
        self.position = position
        self.type = type
        self.velocity = velocity
        self.has_animation = False
        if animation:
            self.has_animation = True
            self.animation = Animation(import_folder(animation_images_path), animation_speed, loop_animation).copy()
            self.animation.frame = frame

    def update(self):
        kill = False
        if self.has_animation and self.animation.done:
            kill = True

        self.position.x += self.velocity.x
        self.position.y += self.velocity.y

        if self.has_animation:
            self.animation.update()

        return kill

    def render(self, surface, offset):
        if self.has_animation:
            image = self.animation.img()[0]
            surface.blit(image, (self.position.x - offset[0] - image.get_width() // 2, self.position.y - offset[1] - image.get_width() // 2))


class ParticleSystem:
    def __init__(self, game):
        self.game = game
        self.particles = []

    def emit(self, particle_type, particle_count, position, velocity=VECTOR2(0, 0), frame=0):
        for _ in range(particle_count):
            particle = Particle(self.game, particle_type, position, velocity, frame)
            self.particles.append(particle)

    def update(self):
        particles_to_remove = []
        for particle in self.particles:
            if particle.update():
                particles_to_remove.append(particle)
        for particle in particles_to_remove:
            self.particles.remove(particle)

    def render(self, surface, offset):
        for particle in self.particles:
            particle.render(surface, offset)


""" SUPPORT FUNCTIONS """
def check_for_quit(event, quit_button):
    quit = False

    if event.type == pygame.QUIT:
        quit = True

    elif event.type == pygame.KEYDOWN:
        if event.key == quit_button:
            quit = True
    
    if quit:
        print('\n~\tGame Closed\n')
        pygame.quit()
        sys.exit()


def clamp(num: int, min_value: int, max_value: int):
    """ Returns the number you input as long as its between the max and min values. """
    return max(min(num, max_value), min_value)


_text_library = {}
def draw_text(surf, ttf_path:str, text:str, pos:VECTOR2, size=30, color=(255,255,255), bg_color=None, center=True):
    global _text_library
    text_surf = _text_library.get(f"{text}{color}{size}")
    if text_surf is None:
        font = pygame.font.Font(ttf_path, size)
        # font = pygame.font.Font('assets/ui/font/minotaur.ttf', size)
        text_surf = font.render(text, True, color, bg_color)
        _text_library[f"{text}{color}{size}"] = text_surf
    x, y = pos
    if center:
        surf.blit(text_surf, (x - (text_surf.get_width() // 2), y - (text_surf.get_height() // 2)))
    else:
        surf.blit(text_surf, (x, y))


_image_library = {}
def get_image(path: str):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', sep).replace('\\', sep)
        image = pygame.image.load(canonicalized_path).convert_alpha()
        _image_library[path] = image
    return image


def generate_light_gradient(radius, color, intensity=1, step_radius=1, alpha=1) -> pygame.Surface:
    # make a surface the size of the largest circle's diameter (radius * 2)
    surface = PYSURFACE((int(radius) * 2, int(radius) * 2), pygame.SRCALPHA)
    surface.convert_alpha()

    current_radius = radius
    amount_of_circles = radius // step_radius

    # for every circle in amount_of_circles
    for layer in range(amount_of_circles):

        # create a new surface for the new circle (same size as original)
        layer_surface = PYSURFACE((int(radius) * 2, int(radius) * 2), pygame.SRCALPHA)
        layer_surface.convert_alpha()
        layer_surface.set_alpha(alpha)

        # draw the new circle on the new surface using the current_radius
        pygame.draw.circle(layer_surface, [intensity * value for value in color], (radius, radius), current_radius, width=5)  # width determines how much each circle overlaps each other

        # blit the circle layer onto the main surface
        surface.blit(layer_surface, (0, 0))

        # update the current_radius and alpha for the next circle layer
        current_radius -= step_radius
        alpha += 1

    # return the main surface that has all the circle layers drawn on it
    return surface


def import_folder(path):
    surface_list = []
    for _, __, image_files in walk(path):
        sorted_files = sorted(image_files, key=natural_key)
        for image in sorted_files:
            full_path = path + '/' + image
            image_surf = get_image(full_path)
            surface_list.append(image_surf)

    return surface_list


def import_folder_numerical(path: str) -> list:
    surface_list = []
    file_list = []
    for _, __, image_files in walk(path):
        for index, image in enumerate(image_files):
            file_list.append(image)

        # sort images based on numerical values in the image names: run1.png will always come before run12.png as walk doesnt sort files returned.
        file_list.sort(key=lambda image: int(
            ''.join(filter(str.isdigit, image))))

        for index, image in enumerate(file_list):
            full_path = path + '/' + image
            image_surf = get_image(full_path).convert_alpha()
            image_surf.set_colorkey([0, 0, 0])
            surface_list.append(image_surf)

    return surface_list


def import_csv_layout(path: str) -> list:
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map


def import_cut_graphics(path: str, tile_size: int) -> list:
    surface = get_image(path)
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = PYSURFACE(
                (tile_size, tile_size), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), PYRECT(
                x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)

    return cut_tiles


def cut_graphics(tileset: PYSURFACE, tile_size: int) -> list:
    surface = tileset
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = PYSURFACE(
                (tile_size, tile_size), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), PYRECT(
                x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)

    return cut_tiles


def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


def palette_swap(image: pygame.Surface, old_color: list, new_color: list) -> pygame.Surface:
    image_copy = PYSURFACE(image.get_size())
    image_copy.fill(new_color)
    image.set_colorkey(old_color)
    image_copy.blit(image, (0, 0))
    return image_copy


_sound_library = {}
def play_sound(path: str, stop=None):
    global _sound_library
    sound = _sound_library.get(path)
    if sound == None:
        canonicalized_path = path.replace('/', sep).replace('\\', sep)
        sound = pygame.mixer.Sound(canonicalized_path)
        _sound_library[path] = sound
    if stop is None:
        sound.play()
    elif stop:
        sound.stop()
    else:
        sound.play(10)


def scale_images(images: list, size: tuple) -> list:
    """ returns scaled image assets """
    scaled_images = []
    for image in images:
        scaled_images.append(pygame.transform.scale(image, size))
    return scaled_images


def sine_wave_value() -> int:
    value = math.sin(pygame.time.get_ticks())
    if value >= 0:
        return 255
    else:
        return 0


def text_line_wrap(surface: pygame.Surface, text: str, color: str, rect: PYRECT, font: pygame.Font, aa=False, bkg=None, size=32):
    rect = PYRECT(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], True, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text


