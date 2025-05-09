import pygame
import openai
import sys
import os
from PIL import Image
from lab import  lab_map, draw_lab, player_position, goal_position
from vor import Enemy, img_enemy1, img_enemy2, img_enemy3

#сцена
width = 800
height = 600
back = pygame.display.set_mode((width, height))

pygame.display.set_caption('The Draconic Age')
icon = pygame.image.load('Dragon.png')
pygame.display.set_icon(icon)

pygame.init()
pygame.mixer.init()

#Зображення
def load_tif_image(path, size):
    img = Image.open(path)
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    data = img.tobytes()
    surface = pygame.image.fromstring(data, img.size, img.mode)
    return pygame.transform.smoothscale(surface, size)

def load_images():
    main_menu_bg = load_tif_image('img/Цей бешкетник може бути де завгодно! (1).tif', (800, 600))
    menu_game_bg = load_tif_image('img/menu_game.tif', (800, 600))
    game1_bg = load_tif_image('img/game1/lab_one.tif', (800, 600))
    game2_bg = load_tif_image('img/game1/lab_one.tif', (800, 600))
    return main_menu_bg, menu_game_bg, game1_bg, game2_bg

main_menu_bg, main_game_bg, game1_bg, game2_bg = load_images()

# score_manager.py
def load_score(path='res/txt/score.txt'):
    try:
        with open(path, 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

def save_score(score, path='res/txt/score.txt'):
    with open(path, 'w') as f:
        f.write(str(score))



#шрифт
import pygame
def load_font(path, size):
    return pygame.font.Font(path, size)

def load_fonts():
    font_path = 'res/JosefinSans-SemiBold.ttf'
    font8 = load_font(font_path, 36)
    font9 = load_font(font_path, 20)
    font10 = load_font(font_path, 24)
    return font8, font9, font10

font8, font9, font10 = load_fonts()
#змінні
white = (255, 255, 255)
black = (0,0,0)
gray = (200, 200, 200)
total_score = 0
box = pygame.Rect(50, 500, 700, 50)
color_inactive = gray
color_active = (0, 255, 0)
color = color_inactive
active = False
text = ''
chat_history = []
tile_size = 40

#вороги
enemy1 = Enemy(0, 512, (200, 250), img_enemy1, (40,40), (0.1))
enemy2 = Enemy(102, 400, (520, 570), img_enemy2, (50,40), (0.1))
enemy3 = Enemy(92, 320, (320, 370), img_enemy3, (40,40), (0.1))
enemies = pygame.sprite.Group(enemy1, enemy2, enemy3)

#
def draw_chat():
    y = 50
    for msg in chat_history[-10:]:
        msg_surface = font9.render(msg, True, black)
        back.blit(msg_surface, (50, y))
        y += 30

#кнопки
def draw_button(text, x, y, w, h, base_color, hover_color, action=None, alpha=255, border_radius=0):
    mouse_pos = pygame.mouse.get_pos()
    rect = pygame.Rect(x, y, w, h)
    current_color = hover_color if rect.collidepoint(mouse_pos) else base_color

    button_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    color_with_alpha = (*current_color, alpha)
    pygame.draw.rect(button_surface, color_with_alpha, button_surface.get_rect(), border_radius=border_radius)
    back.blit(button_surface, (x, y))

    text_surface = font8.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    back.blit(text_surface, text_rect)

    if action and pygame.mouse.get_pressed()[0] and rect.collidepoint(mouse_pos):
        action()


def draw_circle_button(text, x, y, radius, color, action=None, alpha=0):
    circle_surface = pygame.Surface((radius *  2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(circle_surface, (*color,alpha), (radius, radius), radius)
    back.blit(circle_surface, (x - radius, y - radius))

    text_surface = font10.render(text, True, (158, 189, 230))
    text_rect = text_surface.get_rect(center=(x, y))
    back.blit(text_surface, text_rect)

    for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
        if event.button == 1:
            mouse_x, mouse_y = event.pos
            if (mouse_x - x) ** 2 + (mouse_y - y) ** 2 <= radius**2:
                if action:
                    action()

#функції для кнопок
def start_game():
    start_back()

def info_game():
    info_back()

def settings_game():
    settings_back()


#меню
def return_to_main_menu():
    main_menu()

def main_menu():

    while True:
        back.fill(white)
        back.blit(main_menu_bg, (0, 0))
        button_x = width - 220
        buttonSet_y = 450

        buttonI_y = 300
        buttonS_y = 150

        button_w = 180
        button_h = 60

        draw_button("Start", button_x, buttonS_y, button_w, button_h, (116, 122, 82), (156, 162, 118), start_back, 255, 0)
        draw_button("Info", button_x, buttonI_y, button_w, button_h, (137, 97, 111), (170, 131, 144), info_back, 255, 0)
        draw_button("Settings", button_x, buttonSet_y, button_w, button_h, (200, 150, 100), (213, 171, 129), settings_back, 255, 0)

        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        print("Info")
                        sys.exit()
                        back.blit(img, (0, 0))
                        pygame.display.update()


#меню ігр
def start_back():
    while True:


        back.fill((240, 240, 240))
        back.blit(main_menu, (0, 0))
        font_big = pygame.font.SysFont(None, 80)
        text = font_big.render('', True, (50, 50, 50))
        text_rect = text.get_rect(center=(width // 2, height // 2))
        back.blit(text, text_rect)
        draw_button('Menu', width // 2 + 133, height // 2 + 175, 250, 75, (63, 103, 55), (200, 200, 200),return_to_main_menu, 30, 22)
        draw_button('', width // 2 - 375, height // 2 - 242, 220, 220, (100, 200, 100), (63, 103, 55), game_one,18)
        draw_button('', width // 2 - 113, height // 2 - 242, 220, 220, (100, 200, 100), (63, 103, 55), game_two, 18)
        draw_button('', width // 2 + 149, height // 2 - 242, 220, 220, (100, 200, 100), (63, 103, 55), start1_back,12)

        draw_button("", width // 2 - 113, height // 2 + 33 , 220, 220, (100, 200, 100), (63, 103, 55), start1_back, 18)
        draw_button("", width // 2 - 375, height // 2 + 33, 220, 220, (100, 200, 100), (63, 103, 55), start1_back, 18)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

pygame.display.update()

#меню лабіринт
def start1_back():
    global score, session_score, total_score
    lab_image = pygame.image.load('img/inf.jpg')
    lab_image = pygame.transform.scale(lab_image, (800, 800))
    score = 0
    total_score = 0
    session_score = 0

    while True:
        back.blit(lab_image, (0, 0))



        enemies.update()
        enemies.draw(back)

        draw_lab(back, lab_map)
        draw_score(back)
        add_score(10)
        if player_reaches_goal(player_position, goal_position):
            add_score(50)

        session_score += 1
        total_score += session_score
        save_score(total_score)
        print('За сессію:', session_score)
        print('всього:', total_score)
        #font_big = pygame.font.SysFont(font9, 80)
        text = font9.render('', True, (50, 50, 50))
        text_rect = text.get_rect(center=(width // 2, height // 2))
        back.blit(text, text_rect)
        draw_button('Menu', width // 2 - 365, height // 2 - 200, 100, 50, (63, 91, 120), (200, 200, 200), return_to_main_menu)
        draw_circle_button('?', width // 2 - 350, height // 2 + 200, 30, (100, 200, 100), open_que)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

pygame.display.update()

def game_one():
    global score, session_score, total_score
    session_score = 0
    frame_counter = 0
    while True:
        back.blit(game1_bg, (0, 0))

        enemies.update()
        enemies.draw(back)

        draw_lab(back, lab_map)
        draw_score(back)

        frame_counter += 1
        if frame_counter % 60 == 0:
            add_score(10)
            session_score += 10
            total_score += 10

        if player_reaches_goal(player_position, goal_position):
            add_score(50)
            session_score += 50
            total_score += 50

            save_score(total_score)
            print('За сессію:', session_score)
            print('всього:', total_score)

            text = font9.render('', True, (50, 50, 50))
            text_rect = text.get_rect(center=(width // 2, height // 2))
            back.blit(text, text_rect)
            pygame.display.update()
            draw_button('Menu', width // 2 - 365, height // 2 - 200, 100, 50, (63, 91, 120), (200, 200, 200),
                        return_to_main_menu)
            draw_circle_button('?', width // 2 - 350, height // 2 + 200, 30, (100, 200, 100), open_que)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            pygame.display.update()



#
def game_two():
    global score, session_score, total_score
    session_score = 0
    frame_counter = 0
    while True:
        back.blit(game2_bg, (0, 0))

        enemies.update()
        enemies.draw(back)
        draw_lab(back, lab_map)
        draw_score(back)
        frame_counter += 1
        if frame_counter % 60 == 0:
            add_score(10)
            session_score += 10
            total_score += 10

        if player_reaches_goal(player_position, goal_position):
            add_score(50)
            session_score += 50
            total_score += 50

            save_score(total_score)
            print('За сессію:', session_score)
            print('всього:', total_score)

            text = font9.render('', True, (50, 50, 50))
            text_rect = text.get_rect(center=(width // 2, height // 2))
            back.blit(text, text_rect)

            draw_button('Menu', width // 2 - 365, height // 2 - 200, 100, 50, (63, 91, 120), (200, 200, 200),return_to_main_menu)
            draw_circle_button('?', width // 2 - 350, height // 2 + 200, 30, (100, 200, 100), open_que)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            pygame.display.update()



#переклад
current_language = 'ua'

def load_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f'none')
        return None

def display_text_from_file(file_path, start_y=320, text_size=40):
    try:
        with open(file_path, 'r', encoding= 'utf-8') as file:
            lines = file.readlines()
            font = pygame.font.SysFont(None, text_size)
            x = 10
            y = start_y
            for line in lines:
                text_surface =font.render(line.strip(), True, (255, 255, 255))
                text_rect = text_surface.get_rect(topleft=(x,y))
                back.blit(text_surface, text_rect)
                y += text_size + 10

    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено.")

def toggle_language():
    global current_language
    current_language = 'en' if current_language == 'ua' else 'ua'

#музика та ефекти

music_on = True
music_path = os.path.join(os.path.dirname(__file__), "res/sounds/Angels Airwaves - The Adventure.mp3")

def toggle_music():
    global music_on
    if music_on:
        pygame.mixer.music.pause()
        music_on = False
    else:
        pygame.mixer.music.unpause()
        music_on = True


def settings_back():
    global total_score
    global music_on
    font_big = pygame.font.SysFont(None, 60)


    score_text = font_big.render(f'score {total_score}', True, (127, 92, 116))
    score_rect = score_text.get_rect(center=(width // 2, height //2 + 150))

    while True:
        back.fill((240, 240, 240))
        back.blit(score_text, score_rect)

        music_text = "Music: ON" if music_on else "Music: OFF"
        draw_button(music_text, width //560 - 10, height // 78, 300, 60,(100, 200, 100), (200, 200, 200), toggle_music, 100)

        draw_button('Menu', width // 2 - 150, height // 2, 300, 60, (100, 200, 100), (200, 200, 200), return_to_main_menu, 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()

def load_music():
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1, 0.0)
        print("Music loaded and playing")
    except pygame.error as e:
        print("Could not load music:", e)

pygame.display.update()


#коіни та відображення
total_score = 0

def player_reaches_goal(player_position, goal_position):
    if player_position == goal_position:
        return True

    return False


def some_game_event():
    global total_score
    total_score += 10

def add_score(points):
    global total_score
    total_score += points

def draw_score(surface):
    #font = pygame.font.SysFont(None, 40)  # Выбираем шрифт
    score_text = font8.render(f"Score: {total_score}", True, (255,255,255))
    surface.blit(score_text, (10, 10))

def scoreS():
    try:
        with open ('res/txt/score.txt', 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

def save_score(score):
    with open('res/txt/score.txt', 'w') as f:
        f.write(str(score))

font = pygame.font.SysFont(None, 60)

#віконце.Лабіринт
def open_que():
    show_queue_window()

def show_queue_window():
    queue_window = pygame.Surface((300, 300))
    queue_window.fill((137, 167, 200))

    font4 = pygame.font.SysFont('Verdana', 13)
    try:
        with open('res/txt/lab.txt', 'r', encoding ='utf-8') as f:

            labInf = f.readlines()
    except FileNotFoundError:
        pass

    oy = 8
    for line in labInf:
        text = font4.render(line.strip(), True, (50, 50, 50))
        text_rect = text.get_rect(center=(queue_window.get_width() // 2, oy))
        queue_window.blit(text, (10, oy))
        oy += text.get_height() + 6

    back.blit(queue_window, (0, 150))
    pygame.display.update()

    window_open = True
    while window_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    window_open = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    window_open = False


#правила
def info_back():
    inf_image = pygame.image.load('img/inf.jpg')
    inf_image = pygame.transform.scale(inf_image, (800, 800))

    inc_image = pygame.image.load('img/cat_inf.png')
    inc_image = pygame.transform.scale(inc_image, (500, 500))

    while True:
        back.fill((240, 240, 240))
        back.blit(inf_image, (0, 0))
        back.blit(inc_image, (480, 80))

        draw_button("Language", width // 2 - 90, height - 100 - 400, 180, 50, (63, 91, 120), (137, 167, 200), toggle_language)
        draw_circle_button("Okay", width // 2, height - 100 - 320, 47, (63, 91, 120), return_to_main_menu, alpha=0)

        if current_language == 'en':
            display_text_from_file('res/txt/informationEng.txt', text_size=24)
        else:

            display_text_from_file('res/txt/information.txt', text_size=24)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if width // 2 - 90 <= mouse_pos[0] <= width // 2 - 90 + 180 and height - 100 <= mouse_pos[
                        1] <= height - 100 + 50:
                        toggle_language()


def settings_back():

    global total_score
    global music_on
    font_big = pygame.font.SysFont(None, 60)


    score_text = font8.render(f'score {total_score}', True, (255, 50, 50))
    score_rect = score_text.get_rect(center=(width // 2, height //2 + 150))

    while True:
        back.fill((240, 240, 240))
        back.blit(score_text, score_rect)

        music_text = "Music: ON" if music_on else "Music: OFF"
        draw_button(music_text, width //2 - 150, height // 4, 300, 60,(108, 112, 81), (124, 128, 96),toggle_music)

        draw_button('Menu', width // 2 - 150, height // 2, 300, 60, (100, 200, 100), (200, 200, 200),return_to_main_menu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()



load_music()
main_menu()