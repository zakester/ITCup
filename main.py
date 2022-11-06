import cv2
import mediapipe as mp
import time
import pygame, pymunk, sys
import math
import pymunk.pygame_util
import statistics

FPS = 50

def current_milli_time():
    return round(time.time() * 1000)


def pygame_exit():
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()



def calculate_distance(p1, p2):
  d = math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)
  if (d > 300):
    d = 300
  return d

def calculate_angle(p1, p2):
	return math.atan2(p2[1] - p1[1], p2[0] - p1[0])



def create_ball_physics(space):
  body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
  body.position = (20,340)
  shape = pymunk.Circle(body, 19)
  shape.mass = 10
  shape.elasticity = 0.95
  shape.friction = 0.4
  shape.collision_type = 1

  space.add(body, shape)
  return shape

def ball_shape(ball):
  x = int(ball.body.position.x)
  y = int(ball.body.position.y)
  angle = math.degrees(ball.body.angle)

  blitRotateCenter(screen, ball_surface, (x-20, y-20), -angle)
  #screen.blit(ball_surface_with_rotation, (x-20,y-20))
  pygame.draw.circle(screen, (0,255,255), (x+20-20,y+20-20), 3)

def onBallOutOfRange(space, ball):
  x = int(ball.body.position.x)
  y = int(ball.body.position.y)
  

  if (x > 640 or y > 480 or x < 0 or y < 0):
    space.remove(ball, ball.body)
    return create_ball_physics(space)
  else:
    return None
    
y_list = []
def onLose(space, ball):
  y = int(ball.body.position.y)
  b = None
  global heLost

  if (heLost == True):
    global loses
    loses = loses + 1
    global text_loses
    text_loses = my_font.render(f'Loses: {loses}', False, (0, 0, 0))
    heLost = False
    space.remove(ball, ball.body)
    b = create_ball_physics(space)

  if (len(y_list) < 5):
    y_list.append(y)
  else:
    if (statistics.mean(y_list) == 386):
      space.remove(ball, ball.body)
      b = create_ball_physics(space)
    y_list.clear()
  return b

def blitRotateCenter(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect)


def cursor(x, y):
  pygame.draw.circle(screen, (255,255,255), (x, y), 5)


def create_floor(space):
  body = pymunk.Body(body_type=pymunk.Body.STATIC)
  body.position = (320, 480)
  shape = pymunk.Poly.create_box(body, (640, 150))
  shape.elasticity = 0.5
  shape.friction = 0.9
  space.add(body, shape)
  return shape


def floor_shape(floor):
  x = int (floor.body.position.x)
  y = int (floor.body.position.y)
  pygame.draw.rect(screen, (25,20,0), pygame.Rect(x-320, y-75, 640, 150), 100)


def create_wall(space, position, size, elasticity=0.6, friction=0.9):
  body = pymunk.Body(body_type=pymunk.Body.STATIC)
  body.position = position

  shape = pymunk.Poly.create_box(body, size)
  shape.elasticity = elasticity
  shape.friction = friction
  shape.collision_type = 2

  space.add(body, shape)

  return shape


def wall_shape(walls):
  for wall in walls:
    x = int(wall.body.position.x)
    y = int(wall.body.position.y)
    pos = wall.bb.left, wall.bb.top
    w = wall.bb.right - wall.bb.left
    h = wall.bb.top - wall.bb.bottom

    pygame.draw.rect(screen, (255,255,255), pygame.Rect(pos[0], y-(h/2), w, h))


def create_boundaries(space, width, height):
  rects = [
		[(width/2, height - 10), (width, 10)],
		[(width/2, 0), (width, 10)],
		[(0, height/2), (10, height)],
		[(width, height/2), (10, height)]
	]
  
  for pos, size in rects:
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Poly.create_box(body, size)
    shape.elasticity = 0.4
    shape.friction = 0.5
    
    
    space.add(body, shape)
    
  

def create_trophy(space):
  body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
  body.position = (600, 370)
  
  shape = pymunk.Poly.create_box(body, (20, 60))
  shape.mass = 5
  shape.elasticity = 0.4
  shape.friction = 0.9
  shape.collision_type = 3
  
  
  
  space.add(body, shape)

  return shape

def trophy_shape(trophy):
    #x = int(trophy.body.position.x)
    
    y = int(trophy.body.position.y)
    pos = trophy.bb.left, trophy.bb.top
    w = trophy.bb.right - trophy.bb.left
    h = trophy.bb.top - trophy.bb.bottom
    
    #pygame.draw.rect(screen, (255,255,255), pygame.Rect(pos[0], y-(h/2), w, h))

loses = 0
heLost = False
def ball_wall_collision(arbiter, space, data):
  global heLost
  heLost = True



wins = 0
heWins = False
def ball_trophy_collision(arbiter, space, data):
  global heWins
  heWins = True
  global ball
  ball = onWin(space, ball)
  global canShoot
  canShoot = True

  


def onWin(space, ball):
  global heWins
  global wins
  global text_wins

  b = None

  if (heWins == True):
    space.remove(ball, ball.body)
    b = create_ball_physics(space)
    wins = wins + 1
    text_wins = my_font.render(f'Wins: {wins}', False, (0, 0, 0))


  return b







'''
pygame init
'''


pygame.init()
screen = pygame.display.set_mode((640,480))
clock = pygame.time.Clock()
ball_surface = pygame.image.load('img/ball.png').convert_alpha()
ball_surface = pygame.transform.scale(ball_surface, (40, 40))


my_font = pygame.font.SysFont('Comic Sans MS', 30)
text_wins = my_font.render(f'Wins: {wins}', False, (0, 0, 0))
text_loses = my_font.render(f'Loses: {loses}', False, (0, 0, 0))




'''
pymunk init
'''
space = pymunk.Space()
space.gravity = (0, 2000)
# add ball to space
ball = create_ball_physics(space)
boundaries = create_boundaries(space, 640, 480)
floor = create_floor(space)

trophy = create_trophy(space)
walls = [create_wall(space, (500, 90), (25, 190)), create_wall(space, (500,330), (25, 150))]


ball_wall_collision_handler = space.add_collision_handler(1, 2)
ball_wall_collision_handler.separate = ball_wall_collision

ball_trophy_collision_henlder = space.add_collision_handler(1, 3)
ball_trophy_collision_henlder.separate = ball_trophy_collision

draw_options = pymunk.pygame_util.DrawOptions(screen)



'''
mediapip init
'''
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands







def isFingerOpen(y_tip, y_pip):
  if (y_tip < y_pip):
    return True
  else:
    return False











canShoot = True
applayForce = False


starting_pos = (0, 0)
ending_pos = (0, 0)

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5, max_num_hands=1) as hands:
  while cap.isOpened():
    success, image = cap.read()


    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue


    pygame_exit()


    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image, 1)

    #image = overlayPNG(image, ball_img, [100, 100])

    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image_height, image_width, _ = image.shape


    x = 0
    y = 0

    def_pos_x = starting_pos[0] - ending_pos[0]
    def_pos_y = starting_pos[1] - ending_pos[1]
    screen.fill((255,100,150))
    screen.blit(text_wins, (10, 10))
    screen.blit(text_loses, (10, 30))

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:

        x = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width)
        y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height)

        y_index_pip = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * image_height)

        y_middle_finger_tip = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * image_height)
        y_middle_finger_pip = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * image_height)


        cv2.circle(image, (x, y), 3, (255, 255, 255), -1)
        isInside = False
        if (isFingerOpen(y_middle_finger_tip, y_middle_finger_pip) == False and isFingerOpen(y, y_index_pip) == True and canShoot == True):
          applayForce = True

          starting_pos = (int(ball.body.position.x), int(ball.body.position.y))
          ending_pos = (x, y)

          pygame.draw.line(screen, (25, 25, 25), starting_pos, ending_pos, 3)

            
        else:
          starting_pos = (int(ball.body.position.x), int(ball.body.position.y))
          ending_pos = (x, y)
          line = [starting_pos, ending_pos]
          if (applayForce == True and canShoot == True):
            ball.body.body_type = pymunk.Body.DYNAMIC
            
            angle = calculate_angle(*line)
            force = calculate_distance(*line) * 50
            
            if (force > 15000):
              force = 15000
            fx = (math.cos(angle) * force)
            fy = (math.sin(angle) * force)
            pygame.draw.line(screen, (255,255,255), starting_pos, (fx,fy))
            
            
            ball.body.angle = 0
            

            ball.body.apply_impulse_at_local_point((fx, fy), (0,0))
            canShoot = False
            applayForce = False
          else:
            ball.body.apply_impulse_at_local_point((0,0), (0,0))
          

          


        

    #cv2.imshow('MediaPipe Hands', image)

    

    


    #create_boundaries(space, 640, 480)
    space.debug_draw(draw_options)
    floor_shape(floor=floor)
    wall_shape(walls=walls)
    trophy_shape(trophy=trophy)
    b = onBallOutOfRange(space, ball)
    if b != None:
      ball = b
    if (canShoot == False):
      b = onLose(space, ball)
      if b != None:
        ball = b
        canShoot = True

      
    
    ball_shape(ball=ball)

    
    cursor(x, y)
    pygame.display.update()
    space.step(1/FPS)
    clock.tick(FPS)




    if cv2.waitKey(5) & 0xFF == 27:
      break



cap.release()