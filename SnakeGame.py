import pygame
import random
import sys

# 初始化游戏
pygame.init()

# 游戏界面的尺寸
screen_width = 800
screen_height = 600
bg_music_path = "music/Snake Game - Theme Song.mp3"
eat_sound_path = "music/eat_sound.mp3"
game_over_sound_path = "music/game_over_sound.wav"
game_over_image_file = "images/game_over_image.png"

# 定义颜色
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

# 创建游戏界面
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('LPZ贪吃蛇')
pygame.mixer.music.load(bg_music_path)
eat_sound = pygame.mixer.Sound(eat_sound_path)
game_over_sound = pygame.mixer.Sound(game_over_sound_path)

# 控制游戏速度
clock = pygame.time.Clock()
snake_speed = 15

# 蛇的初始位置和移动方向
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
direction = 'RIGHT'
change_to = direction

# 食物的初始位置
food_position = [random.randrange(1, (screen_width // 10)) * 10,
                 random.randrange(1, (screen_height // 10)) * 10]
food_spawn = True

# 记录得分
score = 0

# 游戏状态
game_started = False

# 游戏开始界面
def game_start_screen():
    # 播放背景音乐
    pygame.mixer.music.play(-1)  # -1 表示循环播放
    global game_started  # 声明 game_started 为全局变量
    font = pygame.font.Font('fonts/simsun.ttc', 48)
    text_surface = font.render('贪吃蛇', True, green)
    text_rect = text_surface.get_rect()
    text_rect.center = (screen_width / 2, screen_height / 3)
    
    button_font = pygame.font.Font('fonts/simsun.ttc' , 30)
    button_text_surface = button_font.render('开始游戏', True, black)
    button_text_rect = button_text_surface.get_rect()
    button_text_rect.center = (screen_width / 2, screen_height / 2)
    
    while not game_started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_text_rect.collidepoint(mouse_pos):
                    game_started = True
                    return
        
        screen.fill(black)
        screen.blit(text_surface, text_rect)
        pygame.draw.rect(screen, green, button_text_rect)
        screen.blit(button_text_surface, button_text_rect)
        
        pygame.display.flip()


# 游戏结束
def game_over():
    # 播放游戏结束音效
    game_over_sound.play()
    # 停止背景音乐
    pygame.mixer.music.stop()
    
    game_over_image = pygame.image.load(game_over_image_file)
    scaled_game_over_image = pygame.transform.scale(game_over_image, (406, 106))
    # 在屏幕中央绘制游戏结束图片
    screen.blit(scaled_game_over_image, (screen_width // 2 - scaled_game_over_image.get_width() // 2, screen_height // 2 - scaled_game_over_image.get_height() // 2 - 140))
    
    # 显示最终得分
    font_path = 'fonts/simsun.ttc'  # 自定义字体文件的路径
    final_font = pygame.font.Font(font_path, 24)
    final_score_surface = final_font.render(f'Final Score: {score}', True, red)
    final_score_rect = final_score_surface.get_rect()
    final_score_rect.midtop = (screen_width / 2, screen_height / 2 - 80)
    screen.blit(final_score_surface, final_score_rect)
    
    # 绘制重新开始按钮
    restart_button_rect = pygame.Rect(screen_width / 2 - 100, screen_height / 2 , 200, 50)
    pygame.draw.rect(screen, green, restart_button_rect)
    restart_font = pygame.font.Font(font_path, 30)
    restart_button_text =  restart_font.render("重新开始", True, black)
    restart_button_text_rect = restart_button_text.get_rect()
    restart_button_text_rect.center = restart_button_rect.center
    screen.blit(restart_button_text, restart_button_text_rect)
    
    pygame.display.flip()
    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button_rect.collidepoint(mouse_pos):
                    return  # 重新开始游戏
                
def check_game_over():
    if snake_position[0] < 0 or snake_position[0] > screen_width - 10:
        return True
    if snake_position[1] < 0 or snake_position[1] > screen_height - 10:
        return True
    if snake_position in snake_body[1:]:
        return True
    return False

def generate_food(food_position,food_spawn):
    # 生成食物的随机位置
    if not food_spawn:
        food_position = [random.randrange(1, (screen_width // 10)) * 10,random.randrange(1, (screen_height // 10)) * 10]
    food_spawn = True
    return food_position,food_spawn

def play_eat_sound():
    # 播放吃到食物的音效
    eat_sound.play()

# 游戏主循环
while True:
    if not game_started:
        game_start_screen()
    else:
        if check_game_over():
            game_over()
            # 重新初始化游戏状态
            game_started = False
            score = 0
            # 重新设置贪吃蛇的位置、食物的位置等
            # 蛇的初始位置和移动方向
            snake_position = [100, 50]
            snake_body = [[100, 50], [90, 50], [80, 50]]
            direction = 'RIGHT'
            change_to = direction
            # 食物的初始位置
            food_position = [random.randrange(1, (screen_width // 10)) * 10,random.randrange(1, (screen_height // 10)) * 10]
            food_spawn = True
            snake_speed = 15

        # 游戏逻辑
        # 检查按键事件
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        change_to = 'UP'
                    if event.key == pygame.K_DOWN:
                        change_to = 'DOWN'
                    if event.key == pygame.K_LEFT:
                        change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT:
                        change_to = 'RIGHT'
        # 根据按键事件更新移动方向
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # 根据移动方向更新蛇的位置
        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10

        # 增加蛇的长度
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
            score += 1
            snake_speed += 1
            food_spawn = False
            play_eat_sound()  # 播放吃到食物的音效
        else:
            snake_body.pop()
        
        # 生成食物
        food_position,food_spawn=generate_food(food_position,food_spawn)


        # 更新游戏界面
        screen.fill(black)
        for pos in snake_body:
            pygame.draw.rect(screen, green, pygame.Rect(
                pos[0], pos[1], 10, 10))

        pygame.draw.rect(screen, white, pygame.Rect(
            food_position[0], food_position[1], 10, 10))
        
        font = pygame.font.SysFont(None, 24)
        # 显示分数
        score_surface = font.render(f'Score: {score}', True, white)
        score_rect = score_surface.get_rect()
        score_rect.topright = (screen_width - 10, 10)
        screen.blit(score_surface, score_rect)
        
        # 显示速度
        speed_text = font.render(f'Speed: {snake_speed}', True, white)
        speed_rect=speed_text.get_rect()
        speed_rect.topright = (screen_width - 10, 30)
        screen.blit(speed_text, speed_rect)
        
    
    pygame.display.update()
    clock.tick(snake_speed)
