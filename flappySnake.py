import sys, time, random, pygame
from pygame import mixer
from collections import deque
import cv2 as cv, mediapipe as mp
from components.Button import Button
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

pygame.mixer.pre_init(44100, -16, 2, 512)

mixer.init()
pygame.init()

# Initialize required elements/environment
cam = cv.VideoCapture(0)
window_size = (cam.get(cv.CAP_PROP_FRAME_WIDTH), cam.get(cv.CAP_PROP_FRAME_HEIGHT)) # width by height
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Flappy Snake')

# Initialize snake and pipe images
bird_img = pygame.image.load("./assets/snake.png")
bird_img = pygame.transform.scale(bird_img, (bird_img.get_width() / 6, bird_img.get_height() / 6))
bird_frame = bird_img.get_rect()
bird_frame.center = (window_size[0] // 6, window_size[1] // 2)
pipe_frames = deque()
pipe_img = pygame.image.load("./assets/pillar.png")

pipe_starting_template = pipe_img.get_rect()
space_between_pipes = 150

# load background music
pygame.mixer.music.load("./assets/music/arcade.wav")
pygame.mixer.music.play(-1, 0, 20000)

# load button images 
exit_img = pygame.image.load("./assets/exit.png").convert_alpha()

# create button instances
exit_button = Button(100, 200, exit_img, 0.4)   

# Game loop
game_clock = time.time()
stage = 1
pipe_spawn_timer = 0
time_between_pipe_spawn = 40
dist_between_pipes = 500
pipe_velocity = lambda: dist_between_pipes / time_between_pipe_spawn
level = 0
score = 0
did_update_score = False
game_is_running = True

screen.fill((125, 220, 232))
    
for a in range(3,0,-1):
    text = pygame.font.SysFont("Helvetica Bold.ttf", 64).render(str(a), True, (109, 67, 126))
    tr = text.get_rect()
    tr.center = (window_size[0]/2, window_size[1]/2)
    screen.blit(text, tr)
    time.sleep(1)

with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
    while True:
        # Check if game is running
        if not game_is_running:
            # text = pygame.font.SysFont("Helvetica Bold.ttf", 64).render('Game over!', True, (109, 67, 126))
            # tr = text.get_rect()
            # tr.center = (window_size[0]/2, window_size[1]/2)
            # screen.blit(text, tr)
            if exit_button.draw(screen):
                pygame.quit()
                sys.exit()
            pygame.display.update()
            pygame.time.wait(2000)
            cam.release()
            cv.destroyAllWindows()
            

        # Check if user quit window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cam.release()
                cv.destroyAllWindows()
                pygame.quit()
                sys.exit()

        # Get frame
        ret, frame = cam.read()
        if not ret:
            # print("Empty frame, continuing...")
            continue

        # Clear screen
        screen.fill((125, 220, 232))

        # Face mesh
        frame.flags.writeable = False
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = face_mesh.process(frame)
        frame.flags.writeable = True

        # Draw mesh
        if results.multi_face_landmarks and len(results.multi_face_landmarks) > 0:
            # 94 = Tip of nose
            marker = results.multi_face_landmarks[0].landmark[94].y
            bird_frame.centery = (marker - 0.5) * 1.5 * window_size[1] + window_size[1]/2
            if bird_frame.top < 0: bird_frame.y = 0
            if bird_frame.bottom > window_size[1]: bird_frame.y = window_size[1] - bird_frame.height

        # Mirror frame, swap axes because opencv != pygame
        frame = cv.flip(frame, 1).swapaxes(0, 1)

        # Update pipe positions
        for pf in pipe_frames:
            pf[0].x -= pipe_velocity()
            pf[1].x -= pipe_velocity()

        if len(pipe_frames) > 0 and pipe_frames[0][0].right < 0:
            pipe_frames.popleft()

        # Update screen
        pygame.surfarray.blit_array(screen, frame)
        screen.blit(bird_img, bird_frame)
        checker = True
        for pf in pipe_frames:
            # Check if bird went through to update score
            if pf[0].left <= bird_frame.x <= pf[0].right:
                checker = False
                if not did_update_score:
                    score += 1
                    did_update_score = True
            # Update screen
            screen.blit(pipe_img, pf[1])
            screen.blit(pygame.transform.flip(pipe_img, 0, 1), pf[0])
        if checker: did_update_score = False

        # Stage, score text
        text = pygame.font.SysFont("Helvetica Bold.ttf", 50).render(f'Stage {stage}', True, (255, 255, 255))
        temp_surface = pygame.Surface(text.get_size())
        temp_surface.fill((109, 67, 126))
        temp_surface.blit(text, (0, 0))
        screen.blit(temp_surface, (50, 50))
        text = pygame.font.SysFont("Helvetica Bold.ttf", 50).render(f'Score: {score}', True, (255, 255, 255))
        temp_surface = pygame.Surface(text.get_size())
        temp_surface.fill((109, 67, 126))
        temp_surface.blit(text, (0, 0))
        screen.blit(temp_surface, (50, 100))

        # Update screen
        pygame.display.flip()

        # Check if bird is touching a pipe
        if any([bird_frame.colliderect(pf[0]) or bird_frame.colliderect(pf[1]) for pf in pipe_frames]):
            game_is_running = False

        # Time to add new pipes
        if pipe_spawn_timer == 0:
            top = pipe_starting_template.copy()
            top.x, top.y = window_size[0], random.randint(120 - 1000, window_size[1] - 120 - space_between_pipes - 1000)
            bottom = pipe_starting_template.copy()
            bottom.x, bottom.y = window_size[0], top.y + 1000 + space_between_pipes
            pipe_frames.append([top, bottom])

        # Update pipe spawn timer - make it cyclical
        pipe_spawn_timer += 1
        if pipe_spawn_timer >= time_between_pipe_spawn: pipe_spawn_timer = 0

        # Update stage
        if time.time() - game_clock >= 10:
            time_between_pipe_spawn *= 5 / 6
            stage += 1
            game_clock = time.time()

