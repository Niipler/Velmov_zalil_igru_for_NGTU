from moduls.game_objects import *
from moduls.useful_functions import *

FPS = pygame.time.Clock()
pygame.init()
GAME_WINDOW_SIZE = 800, 600
screen = pygame.display.set_mode(GAME_WINDOW_SIZE, 0, 32)


def load_image(name, fl=True, colorkey=-1):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey == -1 and fl:
        colorkey = image.get_at((0, 0))
    image.set_colorkey(colorkey)
    return image


class Main_menu:
    def __init__(self, objects_file_name):
        self.buttons = []
        self.background = None
        with open("data/" + objects_file_name, 'r') as mapFile:
            objects = mapFile.readlines()
            objects = [object.split("==") for object in objects]

        for object in objects:
            if object[0] == 'background':
                self.background = load_image(object[1], False)
            if object[0] == 'button':
                object[1] = object[1].split()
                self.buttons.append(Button(object[1][0], object[1][1], object[1][2], object[1][3]))


def main_menu_cycle(screen, main_menu, game_window_size):
    while True:
        screen.fill((0, 0, 0))
        if main_menu.background:
            screen.blit(main_menu.background, (0, 0))

        for button in main_menu.buttons:
            screen.blit(button.image, (button.rect.x, button.rect.y))
            excretion_button(button, screen)    # выделение кнопочек
        #  drawing the buttons and excretion it
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for button in main_menu.buttons:
                    if x > button.rect.x and x < button.rect.right \
                            and y > button.rect.y and y < button.rect.bottom:
                        play_sound('button_pressed_sound')

                        result = button.clicked() # нажали кнопочку и она что-то делает
                        if result == 'start_last_level':
                            while True:
                                last_level_name = load_last_level_name()
                                n_level_name = game_cycle(last_level_name, screen, load_level_objects(last_level_name, GAME_WINDOW_SIZE))
                                if n_level_name == 'quit':
                                    play_sound('exit_sound')
                                    #print('quit_game_cycle..')
                                    break
                                elif n_level_name == 'killed':
                                    with open("data/last_level.txt", "w") as file:
                                        file.write('level__.1.txt')
                                    with open('data/progress.txt', 'w') as file_2:
                                        file_2.write('level__.1.txt')
                                else:
                                    with open("data/last_level.txt", "w") as file:
                                        file.write(n_level_name)
                        elif result == 'select_level':
                            result = selecting_level_cycle()
                            if result:
                                with open("data/last_level.txt", "w") as file:
                                    file.write(result)
                                while True:
                                    last_level_name = load_last_level_name()
                                    n_level_name = game_cycle(last_level_name, screen,
                                                              load_level_objects(last_level_name, GAME_WINDOW_SIZE))
                                    if n_level_name == 'quit':
                                        play_sound('exit_sound')
                                        #print('quit_game_cycle..')
                                        break
                                    elif n_level_name == 'killed':
                                        with open("data/last_level.txt", "w") as file:
                                            file.write('level__.1.txt')
                                        with open('data/progress.txt', 'w') as file_2:
                                            file_2.write('level__.1.txt')
                                    else:
                                        with open("data/last_level.txt", "w") as file:
                                            file.write(n_level_name)
                        elif result == 'options':
                            options_cycle()
        pygame.display.update()
        FPS.tick(80)


def selecting_level_cycle():
    selecting_level_cycle_buttons = [Button(0, 0, 'exit_button.png', 'exit')]
    a = ['level__.1.txt', 'level__.2.txt', 'level__.3.txt', 'level__.4.txt', 'level__.5.txt', 'level__.6.txt', 'level__.7.txt']
    for file_name in a:
        l_number = int(file_name.split('.')[1])
        if l_number > 4:
            selecting_level_cycle_buttons.append(
                Button(410, 70 * (l_number-4), 'level_icon.png', file_name, 'Уровень ' + file_name.split('.')[1], (0, 0, 0)))
        else:
            selecting_level_cycle_buttons.append(
                Button(100, 70 * l_number, 'level_icon.png', file_name, 'Уровень ' + file_name.split('.')[1], (0, 0, 0)))
    del a
    del l_number

    #на иконках левела сделать текст с названием уровня

    while True:
        screen.fill((0, 0, 0))
        for button in selecting_level_cycle_buttons:
            screen.blit(button.image, (button.rect.x, button.rect.y))
            if button.text_img:
                screen.blit(button.text_img, (button.rect.x + button.bias_x, button.rect.y + button.bias_y))
            excretion_button(button, screen)    # выделение кнопочек

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for button in selecting_level_cycle_buttons:
                    if x > button.rect.x and x < button.rect.right \
                            and y > button.rect.y and y < button.rect.bottom:
                        play_sound('button_pressed_sound')
                        result = button.clicked()
                        if result == 'exit':
                            play_sound('exit_sound')
                            return
                        else:
                            with open('data/progress.txt', 'r') as file:
                                if file.read() >= result:
                                    return result
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return

        pygame.display.update()
        FPS.tick(80)


def options_cycle():
    option_cycle_buttons = []
    option_cycle_buttons.append(Button(0, 0, 'exit_button.png', 'exit'))
    option_cycle_buttons.append(Button_switch(250, 20, 'switch_setka_button_off.png', 'switch_setka_button_on.png',
                                              'switch_setka', load_option('switch_setka')))
    option_cycle_buttons.append(Button_switch(250, 210, 'switch_fly_mode_button_off.png', 'switch_fly_mode_button_on.png',
                                              'switch_fly', load_option('switch_fly')))
    option_cycle_buttons.append(Button_switch(250, 400, 'switch_immortal_mode_button_off.png',
                                              'switch_immortal_mode_button_on.png', 'switch_immortal', load_option('switch_immortal')))

    while True:
        screen.fill((0, 0, 0))

        for button in option_cycle_buttons:
            screen.blit(button.image, (button.rect.x, button.rect.y))
            excretion_button(button, screen)    # выделение кнопочек

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for button in option_cycle_buttons:
                    if x > button.rect.x and x < button.rect.right \
                            and y > button.rect.y and y < button.rect.bottom:
                        play_sound('button_pressed_sound')

                        result = button.clicked()
                        if result == 'exit':
                            play_sound('exit_sound')
                            return
                        else:
                            change_options(result)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
        pygame.display.update()
        FPS.tick(80)


def game_cycle(level_name, screen, objects):
    with open('data/progress.txt') as file:
        l_name = file.read()
        if int(l_name.split('.')[1]) < int(level_name.split('.')[1]):   #если уже заходили на тот уровень, можно быстро туда тепнуться через меню
            with open('data/progress.txt', 'w') as file_2:
                file_2.write(level_name)

    red_block_data = []
    block_data = []
    portal_data = []
    phantom_block_data = []
    moving_block_data = []
    turrels_data = []
    heart_data = []
    bullets_data = []
    sphere_data = []
    bc_images_data = []
    for game_object in objects:
        if type(game_object) == Player:
            player = game_object
        elif type(game_object) == Block:
            block_data.append(game_object)
        elif type(game_object) == Turrel:
            turrels_data.append(game_object)
        elif type(game_object) == Red_Block:
            red_block_data.append(game_object)
        elif type(game_object) == Portal:
            portal_data.append(game_object)
        elif type(game_object) == Phantom_Block:
            phantom_block_data.append(game_object)
        elif type(game_object) == Moving_Block:
            moving_block_data.append(game_object)
        elif type(game_object) == Heart:
            heart_data.append(game_object)
        elif type(game_object) == Sphere:
            sphere_data.append(game_object)
        elif type(game_object) == Bc_image:
            bc_images_data.append(game_object)

    exit_window_flag = False
    exit_window_surface = pygame.Surface((800, 600))
    exit_window_surface.fill((50, 50, 50))
    exit_window_surface.set_alpha(200)
    exit_window_button = Button(250, 20, 'exit_from_level_button.png', 'exit_from_level')
    open_option_cycle_button = Button(250, 210, 'options_button.png', 'open_options')
    suicide_button = Button(300, 400, 'suicide_button.png', 'suicide', None, (255, 255, 0), True)

    player.flying_mode_flag = load_option('switch_fly')
    player.immortal_mode_flag = load_option('switch_immortal')
    drawing_setka_flag = load_option('switch_setka')

    player_killed_flag = False

    while True:
        screen.fill((0, 0, 0))

        if player_killed_flag:
            return 'killed'

        if drawing_setka_flag:
            draw_setka(screen, GAME_WINDOW_SIZE)
        for obj in phantom_block_data:#если есть коллизия с секреткой фон на задний план
            if player.rect.colliderect(obj.rect):
                screen.blit(obj.surface, (obj.rect.x, obj.rect.y))
            # я сделяль красиво~~~~ \(~v~)\
        for obj in bc_images_data:
            screen.blit(obj.image, (obj.rect.x, obj.rect.y))
        for obj in sphere_data:
            screen.blit(obj.image, (obj.rect.x, obj.rect.y))
            obj.update()
            obj.update_animation()
        for obj in block_data:
            pygame.draw.rect(screen, obj.color, obj.rect)
        for obj in moving_block_data:
            pygame.draw.rect(screen, obj.color, obj.rect)
            if not exit_window_flag:
                obj.update()
        for obj in red_block_data:
            pygame.draw.rect(screen, obj.color, obj.rect)
            if not player.immortal_mode_flag:
                if player.rect.colliderect(obj.rect):
                    player_killed_flag = player.update_hp()
                    play_sound('player_hurt')
        for obj in bullets_data:
            pygame.draw.rect(screen, obj.color, obj.rect)
            if not exit_window_flag:
                obj.update()
            del_flag = False
            if obj.rect.x > GAME_WINDOW_SIZE[0] or obj.rect.x < 0 \
                    or obj.rect.y > GAME_WINDOW_SIZE[1] or obj.rect.y < 0:
                del_flag = True
            else:
                if not obj.immortal_timer:
                    for el in block_data+moving_block_data+red_block_data:
                        if obj.rect.colliderect(el):
                            del_flag = True
            if del_flag:
                del bullets_data[bullets_data.index(obj)]
            if not player.immortal_mode_flag:
                if player.rect.colliderect(obj.rect):
                    player_killed_flag = player.update_hp()
                    bullets_data = []
                    play_sound('player_hurt')
        for obj in portal_data:
            screen.blit(obj.image, (obj.rect.x, obj.rect.y))
            obj.update_animation()
        for obj in turrels_data:
            screen.blit(obj.image, (obj.rect.x, obj.rect.y))
            obj.update()
            if obj.launched:
                if obj.rot == 0:
                    bullets_data.append(
                        Bullet(obj.rect.x+obj.rect.width//2, obj.rect.y+obj.rect.height//2, 1, 0, obj.launch_speed))
                elif obj.rot == 90:
                    bullets_data.append(
                        Bullet(obj.rect.x + obj.rect.width // 2, obj.rect.y + obj.rect.height // 2, 0, -1, obj.launch_speed))
                elif obj.rot == 180:
                    bullets_data.append(
                        Bullet(obj.rect.x + obj.rect.width // 2, obj.rect.y + obj.rect.height // 2, -1, 0, obj.launch_speed))
                elif obj.rot == 270:
                    bullets_data.append(
                        Bullet(obj.rect.x + obj.rect.width // 2, obj.rect.y + obj.rect.height // 2, 0, 1, obj.launch_speed))
            obj.launched = False
        for obj in heart_data:
            screen.blit(obj.image, (obj.rect.x, obj.rect.y))
            if not exit_window_flag:
                obj.update_animation()
                if player.rect.colliderect(obj.rect):
                    player.add_hp()
                    del heart_data[heart_data.index(obj)]
        for obj in phantom_block_data: #если нет коллизии с секреткой, то типо блок
            if not player.rect.colliderect(obj.rect):
                pygame.draw.rect(screen, obj.color, obj.rect)

        ##player
        screen.blit(player.image, (player.rect.x, player.rect.y))
        player.draw_hp_bar(screen)
        if not exit_window_flag:
            if not player.immortal_mode_flag:
                player.update(block_data, moving_block_data)
                # подаем в функцию коллизии все блоки имхо функция для них одна и та же
            else:
                player.update(block_data + red_block_data, moving_block_data)  # если игрок бессмертный, значит
                # нужна коллизия с убивающими объектами
        ##/player


        if exit_window_flag:
            screen.blit(exit_window_surface, (0, 0))
            screen.blit(exit_window_button.image, (exit_window_button.rect.x, exit_window_button.rect.y))
            screen.blit(open_option_cycle_button.image, (open_option_cycle_button.rect.x, open_option_cycle_button.rect.y))
            screen.blit(suicide_button.image, (suicide_button.rect.x, suicide_button.rect.y))
            excretion_button(exit_window_button, screen)
            excretion_button(open_option_cycle_button, screen)
            excretion_button(suicide_button, screen)

        # All events
        for event in pygame.event.get():
            if event.type == QUIT:
                return 'quit'
            # exit from game_cycle
            if event.type == MOUSEBUTTONDOWN and exit_window_flag:
                x, y = pygame.mouse.get_pos()
                if x > exit_window_button.rect.x and x < exit_window_button.rect.right \
                        and y > exit_window_button.rect.y and y < exit_window_button.rect.bottom:
                    return 'quit'
                elif x > open_option_cycle_button.rect.x and x < open_option_cycle_button.rect.right \
                        and y > open_option_cycle_button.rect.y and y < open_option_cycle_button.rect.bottom:
                    options_cycle()
                    player.flying_mode_flag = load_option('switch_fly')
                    player.immortal_mode_flag = load_option('switch_immortal')
                    drawing_setka_flag = load_option('switch_setka')
                    #чтобы настройки обновлялись
                elif x > suicide_button.rect.x and x < suicide_button.rect.right \
                        and y > suicide_button.rect.y and y < suicide_button.rect.bottom:
                    player_killed_flag = player.update_hp()
                    play_sound('suicide')
                # здесь кнопки в менюшке эскейпа были

            # # KeyDown and KeyUp events
            if event.type == KEYDOWN:
                if event.key == K_d:
                    player.move_right = True
                if event.key == K_a:
                    player.move_left = True
                # # # # # # # #
                # jump
                if event.key == K_SPACE:
                    player.space_pressed_flag = True
                    for sphere in sphere_data:
                        if player.rect.colliderect(sphere) and sphere.timer == 0:
                            sphere.used()
                            player.sphere_jumped_flag = True
                # # # # # # # #
                #exit window
                if event.key == K_ESCAPE:
                    if exit_window_flag:
                        exit_window_flag = False
                        play_sound('closed_exit_window')
                    else:
                        exit_window_flag = True
                        play_sound('opened_exit_window')
                # # # # # # # #
                #teleport to other level if player collide with portal
                if event.key == K_t:
                    for portal in portal_data:
                        if player.rect.colliderect(portal.rect):
                            play_sound('Teleporting to other level')
                            #print('Teleported to - ', portal.new_level_name)
                            return portal.new_level_name
                # # # # # # # #

            if event.type == KEYUP:
                if event.key == K_d:
                    player.move_right = False
                if event.key == K_a:
                    player.move_left = False
                if event.key == K_SPACE:
                    player.space_pressed_flag = False

            #  #  #  #  #  #  #  #  #
            # for flying
            if player.flying_mode_flag:
                if event.type == KEYDOWN:
                    if event.key == K_w:
                        player.move_up = True
                    if event.key == K_s:
                        player.move_down = True
                if event.type == KEYUP:  # It's raining men Aleluia It's raining men Hey-Hey...
                    if event.key == K_w:
                        player.move_up = False
                    if event.key == K_s:
                        player.move_down = False
            # # # # # #
        #   #   #   #   #   #   #   #   #
        pygame.display.update()
        FPS.tick(80)


if __name__ == "__main__":
    main_menu = Main_menu('menu_objects.txt')
    main_menu_cycle(screen, main_menu, GAME_WINDOW_SIZE)

