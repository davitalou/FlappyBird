import pygame, random, sys

pygame.init()

screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
score = 0
high_score = 0
gravity = 0.14
game_active = True
game_font = pygame.font.SysFont('04B_19.ttf', 40)
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)

def bird_animation():
    new_bird = bird_list[bird_state]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_move * 5, 1)
    return new_bird

def create_pipe():
    random_pipe = random.choice(pipe_height)
    pipe_top = pipe.get_rect(midtop = (432, random_pipe))
    pipe_bottom = pipe.get_rect(midtop = (432, random_pipe - 700))
    return pipe_bottom, pipe_top

def draw_pipe(pipes):
    for pipe1 in pipes:
        if pipe1.bottom >= 700:
            screen.blit(pipe, pipe1)
        else:
            flip_pipe = pygame.transform.flip(pipe, False, True)
            screen.blit(flip_pipe, pipe1)

def pipe_move(pipes):
    for pipe1 in pipes:
        pipe1.centerx -= 2
    return pipes

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.bottom >= 650 or bird_rect.top <= -75:
        hit_sound.play()
        return False
    return True

def score_display(game_state):
    if game_state == 'game over':
        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_surface_rect = high_score_surface.get_rect(center=(220, 140))
        screen.blit(high_score_surface, high_score_surface_rect)
    score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
    score_surface_rect = score_surface.get_rect(center = (60, 40))
    screen.blit(score_surface, score_surface_rect)


backGround = pygame.transform.scale2x(pygame.image.load('FileGame\\assets\\background-night.png'))

floor = pygame.transform.scale2x(pygame.image.load('FileGame\\assets\\floor.png'))
floor_rect = floor.get_rect()
floor_x = 0

down_bird = pygame.transform.scale2x(pygame.image.load('FileGame\\assets\\yellowbird-downflap.png'))
mid_bird = pygame.transform.scale2x(pygame.image.load('FileGame\\assets\\yellowbird-midflap.png'))
up_bird = pygame.transform.scale2x(pygame.image.load('FileGame\\assets\\yellowbird-upflap.png'))
bird_list = [mid_bird, down_bird, up_bird]
bird_state = 0
bird = bird_list[bird_state]
bird_rect = bird.get_rect(center = (100, 384))
bird_move = 0
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 100)

pipe_spawn = pygame.USEREVENT
pygame.time.set_timer(pipe_spawn, 1100)
pipe = pygame.transform.scale2x(pygame.image.load('FileGame\\assets\\pipe-green.png'))
pipe_list = []
pipe_height = [200, 250, 300, 350, 400]
pipe_rect = pipe.get_rect()

game_over = pygame.transform.scale2x(pygame.image.load('FileGame\\assets\\message.png'))
game_over_rect = game_over.get_rect(center = (216, 384))

flap_sound = pygame.mixer.Sound('FileGame\\sound\\sfx_wing.wav')
hit_sound = pygame.mixer.Sound('FileGame\\sound\\sfx_hit.wav')
point_sound = pygame.mixer.Sound('FileGame\\sound\\sfx_point.wav')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                flap_sound.play()
                bird_move = 0
                bird_move -= 5
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_move = 0
                score = 0
        if event.type == bird_flap:
            if bird_state < 2:
                bird_state += 1
            else:
                bird_state = 0

            bird, bird_rect = bird_animation()
        if event.type == pipe_spawn:
            pipe_list.extend(create_pipe())

    screen.blit(backGround, (0, 0))
    if game_active:

        bird_move += gravity
        bird_rect.centery += bird_move
        rotated_bird = rotate_bird(bird)
        screen.blit(rotated_bird, bird_rect)

        game_active = check_collision(pipe_list)
        draw_pipe(pipe_list)
        pipe_list = pipe_move(pipe_list)
        score_display('main game')

        for pipes in pipe_list:
            if bird_rect.centerx == pipes.centerx:
                score += 0.5
                point_sound.play()


    else:
        screen.blit(game_over, game_over_rect)
        high_score = max(score, high_score)
        score_display('game over')
    floor_x -= 1
    screen.blit(floor, (floor_x, 650))
    screen.blit(floor, (floor_x + 432, 650))
    if floor_x <= -432:
        floor_x = 0
    pygame.display.update()
    clock.tick(120)
#screen.blit()