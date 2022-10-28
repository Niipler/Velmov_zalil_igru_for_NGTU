import pygame, sys, os
from pygame.locals import *
import moduls.game_objects


def play_sound(sound_name):
    if sound_name == 'button_pressed_sound':
        pass
    #print(sound_name)


def draw_setka(screen, game_window_size):
    square_size = 20
    square_color = (0, 200, 240)
    for i in range(game_window_size[0] // square_size):
        pygame.draw.line(screen, square_color, (square_size*i, 0), (square_size*i, game_window_size[1]), 1)
    for i in range(game_window_size[1] // square_size):
        pygame.draw.line(screen, square_color, (0, square_size*i), (game_window_size[0], square_size*i), 1)


def load_option(command):
    file_r = open('data/options.txt', 'r')
    options = [el.split() for el in file_r.readlines()]
    for option in options:
        if option[0] == command:
            if option[-1] == 'T':
                file_r.close()
                return True
            file_r.close()
            return False
    file_r.close()
    return False


def change_options(change):
    file_r = open('data/options.txt', 'r')
    options = [el.split() for el in file_r.readlines()]
    for option in options:
        if option[0] == change:
            if option[-1] == 'F':
                option[-1] = 'T'
            else:
                option[-1] = 'F'
    file_r.close()
    file_w = open('data/options.txt', 'w')
    for option in options:
        file_w.write(str(' '.join(option)) + '\n')
    file_w.close()


def excretion_button(button, screen):
    x, y = pygame.mouse.get_pos()
    if x > button.rect.x and x < button.rect.right \
            and y > button.rect.y and y < button.rect.bottom:
        pygame.draw.rect(screen, (0, 255, 0), (
            button.rect.x, button.rect.y, button.rect.right -
            button.rect.x, button.rect.bottom - button.rect.y), 4)


def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def load_last_level_name():
    #print("Loading last level_name...")
    file = open('data/last_level.txt', 'r')
    last_level_name = file.read()
    #print('start_button_pressed=True, last_level_name == ', last_level_name)
    file.close()
    return last_level_name


def load_level_objects(level_name, game_window_size):
    data_for_return = []
    with open("data/"+level_name, 'r') as mapFile:
        objects = mapFile.readlines()
        objects = [i.split() for i in objects]
        for el in objects:
            if el[0] == 'Block':
                data_for_return.append(moduls.game_objects.Block(int(el[1]), int(el[2]), int(el[3]), int(el[4])))
            elif el[0] == 'Red_Block':
                data_for_return.append(moduls.game_objects.Red_Block(int(el[1]), int(el[2]), int(el[3]), int(el[4])))
            elif el[0] == 'Turrel':
                data_for_return.append(moduls.game_objects.Turrel(int(el[1]), int(el[2]), el[3], int(el[4]), int(el[5])))
            elif el[0] == 'Moving_Block':
                data_for_return.append(moduls.game_objects.Moving_Block(int(el[1]), int(el[2]), int(el[3]), int(el[4]), int(el[5]), int(el[6]), int(el[7])))
            elif el[0] == 'Phantom_Block':
                if len(el) == 5:
                    data_for_return.append(moduls.game_objects.Phantom_Block(int(el[1]), int(el[2]), int(el[3]), int(el[4])))
                else:
                    data_for_return.append(moduls.game_objects.Phantom_Block(int(el[1]), int(el[2]), int(el[3]), int(el[4]), el[5]))
            elif el[0] == 'Player':
                data_for_return.append(moduls.game_objects.Player((int(el[1]), int(el[2])), game_window_size))
            elif el[0] == 'Portal':
                data_for_return.append(moduls.game_objects.Portal(int(el[1]), int(el[2]), el[3]))
            elif el[0] == 'Heart':
                data_for_return.append(moduls.game_objects.Heart(int(el[1]), int(el[2])))
            elif el[0] == 'Sphere':
                data_for_return.append(moduls.game_objects.Sphere(int(el[1]), int(el[2]), int(el[3])))
            elif el[0] == 'Bc_image':
                data_for_return.append(moduls.game_objects.Bc_image(int(el[1]), int(el[2]), el[3]))
    return data_for_return


def collision(block_data, not_static_object, game_window_size):
    ### collision
    local_flag_for_collied_flag = True  # чтобы работал player.collied_flag
    # player.collied_flag чтобы занулять ускорение игрока, когда он сталкивается с поверхностью блока
    # будь то пол или стена или потолок
    for block in block_data:
        if type(block) == moduls.game_objects.Moving_Block:
            additional_collision_x_tollerance = 4*block.speed_x # ммммм... костыль
        else:
            additional_collision_x_tollerance = 0
        #добавочная поправка на скорость, т.к. движущийся блок тоже имеет скорость

        if not_static_object.rect.colliderect(block.rect):
            not_static_object.collied_flag = True
            local_flag_for_collied_flag = False
            if abs(block.rect.top - not_static_object.rect.bottom) < not_static_object.collision_y_tollerance:
                not_static_object.rect.y = block.rect.top - not_static_object.height

            elif abs(block.rect.bottom - not_static_object.rect.top) < not_static_object.collision_y_tollerance:
                not_static_object.rect.y = block.rect.bottom

            elif abs(block.rect.right - not_static_object.rect.left) < not_static_object.collision_x_tollerance\
                    + additional_collision_x_tollerance:
                not_static_object.rect.x = block.rect.right

            elif abs(block.rect.left - not_static_object.rect.right) < not_static_object.collision_x_tollerance \
                    + additional_collision_x_tollerance:
                not_static_object.rect.x = block.rect.left - not_static_object.width

            elif not_static_object.rect.colliderect(block.rect):
                not_static_object.rect.y = block.rect.top - not_static_object.height
                print("It's f*cking wizard!!")

                # !!!need make something to player be outside block (death -(0^0-) )
                # пох?й просто буду выталкивать вверх \_('^')_/
                #а нет не пох*й, добавлю поправку на скорость перемещающегося блока, а вот уже потом пох^й

        else:
            if local_flag_for_collied_flag:
                not_static_object.collied_flag = False
    # horizontal border
    if not_static_object.rect.x < 0:
        not_static_object.rect.x = 0
        #
        not_static_object.collied_flag = True
    elif not_static_object.rect.x > game_window_size[0] - not_static_object.width:
        not_static_object.rect.x = game_window_size[0] - not_static_object.width
        #
        not_static_object.collied_flag = True
    ### vertical border
    if not_static_object.rect.y < 0:
        not_static_object.rect.y = 0
        #
        not_static_object.collied_flag = True
    elif not_static_object.rect.y > game_window_size[1] - not_static_object.height:
        not_static_object.rect.y = game_window_size[1] - not_static_object.height
        #
        not_static_object.collied_flag = True
    ######Youuuuuu shoudn't passs!!!!!
    # # # # # # # #
    #  #  #  #  #  #  #  #  #
    return not_static_object.rect.x, not_static_object.rect.y, not_static_object.collied_flag