import pygame, sys, os
from pygame.locals import *
from moduls.useful_functions import *
from menu_and_game_cycle import load_image


class Particle:
    def __init__(self, x, y, period=30):
        self.x = x
        self.y = y
        self.periond = period

    def update(self):
        if self.periond:
            self.periond -= 1
            #тут звезду надо нарисовать



class Bc_image:
    def __init__(self, x, y, image_name):
        self.image = load_image(image_name)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Sphere:
    image_1 = load_image('sphere_1.png')
    image_2 = load_image('sphere_2.png')

    def __init__(self, x, y, period):
        self.image = Sphere.image_1
        self.period = int(period)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.timer = 0
        self.animation_counter = 0

    def update(self):
        if self.timer < 0:
            self.timer += 1
            if self.timer == 0:
                self.image = Sphere.image_1

    def used(self):
        self.timer = -self.period #тут остановился, нужно делать сферу дальше
        self.image = Sphere.image_2

    def update_animation(self):
        self.animation_counter += 1
        if self.animation_counter == 10:
            self.image = rot_center(self.image, 45)  #rotation
        if self.animation_counter > 10:
            self.animation_counter = 0


class Turrel:
    image = load_image('turrel.png')

    def __init__(self, x, y, direction, l_speed, period):
        self.direction = direction
        if direction == 'right':
            self.rot = 0
        elif direction == 'up':
            self.rot = 90
        elif direction == 'down':
            self.rot = 270
        elif direction == 'left':
            self.rot = 180
        self.image = rot_center(Turrel.image, self.rot)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.timer = 0
        self.period = period
        self.launched = False
        self.launch_speed = l_speed

    def update(self):
        self.timer += 1
        if self.timer >= self.period:
            self.shoot()
            self.timer = 0

    def shoot(self):
        self.launched = True


class Bullet:
    def __init__(self, x, y, x_direction, y_direction, speed, color=(255, 0, 0)):
        self.weight = 3
        self.height = 3
        self.speed = speed
        self.x_direction = x_direction
        self.y_direction = y_direction
        self.rect = Rect(x, y, self.weight, self.height)
        self.color = color
        self.immortal_timer = 30 #пуля будет спавнится прямо в блоке или еще где
                                #надо чтобы она несколько обновлений не удалялась не смотря ни на что

    def update(self):
        if self.immortal_timer:
            self.immortal_timer -= 1
        self.rect.x += self.x_direction*self.speed
        self.rect.y += self.y_direction*self.speed  #эй, ты, да ,ты, иди чекай как класс пули работает, мне лень было (((


class Heart:
    image = load_image('heart.png')
    heart_rotation_1 = load_image('heart_rotation_1.png')
    heart_rotation_2 = load_image('heart_rotation_2.png')
    heart_rotation_3 = load_image('heart_rotation_3.png')
    heart_rotation_4 = load_image('heart_rotation_4.png')
    heart_rotation_5 = load_image('heart_rotation_5.png')
    animation_data = {0: image, 1: heart_rotation_1, 2: heart_rotation_2, 3: heart_rotation_3,
                      4: heart_rotation_4, 5: heart_rotation_5}

    def __init__(self, x, y):
        self.image = Heart.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0
        self.animation_period = 10
        self.n = 5 #animations count
        self.reverse_flag = False

    def update_animation(self):
        self.counter += 1
        n = self.n
        anim_number = self.counter//self.animation_period + 1
        if self.reverse_flag:
            self.image = pygame.transform.flip(Heart.animation_data[abs(anim_number)], True, False)
        else:
            self.image = Heart.animation_data[abs(anim_number)]
        if self.counter > n*self.animation_period-2: #не знаю почему -2, но оно работает не трогай
            self.counter *= -1
            if self.reverse_flag:
                self.reverse_flag = False
            else:
                self.reverse_flag = True


class Red_Block:
    def __init__(self, x, y, weight, height, color=(255, 0, 0)):
        self.rect = Rect(x, y, weight, height)
        self.color = color


class Button:
    def __init__(self, x, y, button_image_name, command, text=None, text_color=(255, 255, 0), a_flag = False):
        self.image = load_image(button_image_name, a_flag)
        self.rect = self.image.get_rect()
        self.rect.x = int(x)
        self.rect.y = int(y)
        self.command = command
        self.text_flag = False
        self.text_img = None
        if text:
            self.font = pygame.font.SysFont(None, 30)
            self.text_img = self.font.render(text, True, text_color)
            self.text_flag = True
            self.bias_x = 30
            self.bias_y = 10

    def clicked(self):
        return self.command


class Button_switch():
    def __init__(self, x, y, button_image_name_off, button_image_name_on, command, bool=False):
        if bool:
            self.image = load_image(button_image_name_on, False)
        else:
            self.image = load_image(button_image_name_off, False)
        self.rect = self.image.get_rect()
        self.rect.x = int(x)
        self.rect.y = int(y)
        self.command = command
        self.bool = bool
        self.button_image_name_off = button_image_name_off
        self.button_image_name_on = button_image_name_on

    def clicked(self):
        if self.bool:
            self.bool = False
            self.image = load_image(self.button_image_name_off, False)
        else:
            self.bool = True
            self.image = load_image(self.button_image_name_on, False)
        return self.command


class Portal:
    image = load_image('portal.png')

    def __init__(self, x, y, new_level_name):
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.new_level_name = new_level_name
        self.animation_counter = 0

    def update_animation(self):
        self.animation_counter += 1
        if self.animation_counter == 5:
            self.image = rot_center(self.image, -60)  #rotation
        if self.animation_counter > 5:
            self.animation_counter = 0


class Moving_Block:
    def __init__(self, x, y, weight, height, direction_x, max_x, min_x, color=(255, 255, 255)):
        self.rect = Rect(x, y, weight, height)
        self.color = color
        self.direction_x = direction_x  #direction is -1 or 0 or 1
        self.speed_x = 1
        self.max_x = max_x
        self.min_x = min_x
        self.weight = weight

    def update(self):
        if self.direction_x:
            self.rect.x += self.speed_x * self.direction_x
        if self.rect.x + self.weight >= self.max_x or self.rect.x <= self.min_x:
            self.direction_x *= -1


class Phantom_Block:
    def __init__(self, x, y, weight, height, color_kod='white'):
        self.rect = Rect(x, y, weight, height)
        if color_kod == 'white':
            self.color = (255, 255, 255)
        elif color_kod == 'red':
            self.color = (255, 0, 0)
        self.surface = pygame.Surface((self.rect.width, self.rect.height))
        self.surface.fill((100, 100, 100))
        self.vision_flag = True

    def update(self, player):
        if self.rect.colliderect(player):
            self.vision_flag = False
        else:
            self.vision_flag = True


class Block:
    def __init__(self, x, y, weight, height, color=(255, 255, 255)):
        self.rect = Rect(x, y, weight, height)
        self.color = color


class Player:
    horizontal_speed = 3
    flying_speed = 5  # just flying speed
    image = load_image('player.png')

    def __init__(self, spawn_coords, game_window_size):
        self.game_window_size = game_window_size

        self.spawn_coords = spawn_coords
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = spawn_coords
        self.move_right = False
        self.move_left = False
        self.width = self.rect[2]
        self.height = self.rect[3]
        self.collision_x_tollerance = Player.horizontal_speed + 1
        self.collision_y_tollerance = Player.flying_speed + 1

        self.immortal_mode_flag = False

        self.flying_mode_flag = False  # yep its flying mode flag
        self.move_up = False
        self.move_down = False

        self.space_pressed_flag = False

        self.sphere_jumped_flag = False

        self.on_ground_flag = False  # if on ground it's should be true
        self.min_y_acceleration = 1
        self.y_acceleration = self.min_y_acceleration

        self.collied_flag = False

        self.max_hp = 5
        self.load_hp()
        self.empty_heart_image = load_image('empty_heart.png')
        self.full_heart_image = load_image('full_heart.png')
        self.hp_bar_x = 15
        self.hp_bar_y = 20

    def add_hp(self):
        if self.hp != self.max_hp:
            self.hp += 1
            with open('data/player_hp.txt', 'w') as file:
                file.write(str(self.hp))
                play_sound('add_hp')

    def load_hp(self):
        with open('data/player_hp.txt') as file:
            self.hp = int(file.read().strip())
            self.hp = min(self.hp, self.max_hp)

    def update_hp(self):
        self.hp -= 1
        self.rect.x, self.rect.y = self.spawn_coords
        if self.hp == 0:
            with open('data/player_hp.txt', 'w') as file:
                file.write(str(self.max_hp))
                self.hp = self.max_hp
                play_sound('player_regress')
                return True  # return True должен откатывать игру в самое начало
        else:
            with open('data/player_hp.txt', 'w') as file:
                file.write(str(self.hp))
            return False

    def draw_hp_bar(self, screen):
        for i in range(self.max_hp):
            if self.hp < i+1:
                screen.blit(self.empty_heart_image, (self.hp_bar_x + 20*i, self.hp_bar_y))
            else:
                screen.blit(self.full_heart_image, (self.hp_bar_x + 20 * i, self.hp_bar_y))

    def gravity(self):
        if self.y_acceleration < 3:  #
            self.y_acceleration += 0.15
        self.rect.y += self.y_acceleration

    def move_horizontal_update(self):
        if self.move_right:
            self.rect.x += self.horizontal_speed
        if self.move_left:
            self.rect.x -= self.horizontal_speed

    def flying_update(self):
        if self.move_up:
            self.rect.y -= self.flying_speed
        if self.move_down:
            self.rect.y += self.flying_speed

    def on_ground_check(self, block_data):
        # is player on ground check
        self.rect.y += 1
        if self.rect.y > self.game_window_size[1] - self.height:  # if on bottom of the screen
            self.on_ground_flag = True
        else:
            for block in block_data:  # if on block
                if self.rect.colliderect(block.rect):
                    self.on_ground_flag = True
                    break
                else:
                    self.on_ground_flag = False
        self.rect.y -= 1
        ###

    def jump_update(self):
        if self.space_pressed_flag and self.on_ground_flag:
            self.y_acceleration = -4
            play_sound('player_jumped')
        elif self.sphere_jumped_flag:
            self.y_acceleration = -4
            play_sound('player_jumped')
            self.sphere_jumped_flag = False #если подпрыгнули на сфере все тоже самое, но флаг зануляем

    def on_moving_block_update(self, moving_block_data):
        for moving_block in moving_block_data:
            self.rect.y += 1
            if self.rect.colliderect(moving_block):
                self.rect.x += moving_block.direction_x*moving_block.speed_x
            self.rect.y -= 1

    def update(self, block_data, moving_block_data):
        # players movement update
        self.move_horizontal_update()
        if self.flying_mode_flag:
            self.flying_update()
        else:
            self.gravity()  # a piece of shit

        ###
        self.rect.x, self.rect.y, self.collied_flag = collision(block_data+moving_block_data, self, self.game_window_size)  # yep collision is here

        # if collied flag true player slide along the wall or stay on block
        if self.collied_flag:
            self.y_acceleration = self.min_y_acceleration
        #
        #
        self.on_moving_block_update(moving_block_data)
        #
        self.jump_update()
        self.on_ground_check(block_data+moving_block_data)  # check player position for jump
        #