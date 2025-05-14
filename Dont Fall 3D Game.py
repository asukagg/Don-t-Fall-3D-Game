from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math, time, random

WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 700
GRID_SIZE = 5
PLATFORM_SIZE = 40
c_radius = 10  
c_angle = 175  
c_z = 200     
c_speed = 10   
fov = 120      
ratio = float(WINDOW_WIDTH) / WINDOW_HEIGHT  
near_clip = 0.1 
far_clip = 2000 

platforms = [[True for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
player_pos = [0, 0, 25]
player_vel = [0, 0, 0]
on_ground = True
score = 0
spark = None
portal = None
red_tile = None
red_time = 0
start_time = time.time()
last_platform_timer = time.time()

spikes = []  # List of (x, y, spawn_time, height)
spike_timer = time.time() 

laser_active = False
laser_timer = time.time()
laser_position = 0 
laser_direction = 1  
laser_speed = 0.1
laser_axis = 0  # 0: X axis, 1: Y axis 

game_over = False
# laser_active=True #test
# laser_axis=True #test

def draw_text(x, y, text):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(1, 1, 1)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_platform(x, y, active=True, flashing=False,color=False):
    glPushMatrix()
    glTranslatef(x * PLATFORM_SIZE, y * PLATFORM_SIZE, 0)
    if not active:
        glColor3f(0.4, 0.6, 1)
    elif flashing:
       glColor3f(1, 0, 0)
    else:
        if color==False:
            glColor3f(0.2, 1, 0.2)
        else:
            glColor3f(1, 0.6, 0)
    glutSolidCube(PLATFORM_SIZE * 0.9)

    glPopMatrix()

def draw_player():
    glPushMatrix()
    glTranslatef(*player_pos)
    glColor3f(0.2, 0.2, 1)
    glutSolidCube(20)
    glTranslatef(0, 0, 10)
    glColor3f(1, 1, 0)
    glutSolidSphere(9, 15, 15)
    glPopMatrix()

def draw_spark():
    if spark:
        glPushMatrix()
        glTranslatef(spark[0]*PLATFORM_SIZE, spark[1]*PLATFORM_SIZE, 25)
        glColor3f(1, 1, 0)
        glutSolidSphere(5, 10, 10)
        glPopMatrix()
def draw_portal():
    if portal:
        glPushMatrix()
        glTranslatef(portal[0]*PLATFORM_SIZE, portal[1]*PLATFORM_SIZE, 25)
        glColor3f(0.53, 0, 0.83)
        glutSolidSphere(20, 20, 20)
        glPopMatrix()
def draw_laser():
    if laser_active:
        glPushMatrix()
        glColor3f(1, 0, 0) 
        grid_end = PLATFORM_SIZE * GRID_SIZE  
        glLineWidth(3.0) 
        glBegin(GL_LINES)
        if laser_axis == 0:  # X-axis sweep
            x_pos = laser_position * PLATFORM_SIZE-25
            glVertex3f(x_pos, -20, 25)  # Start at Y=0
            glVertex3f(x_pos, grid_end-25, 25) 
        else:         # Y-axis sweep
            y_pos = laser_position * PLATFORM_SIZE-25
            glVertex3f(-20, y_pos, 25)  # Start at X=0
            glVertex3f(grid_end-25, y_pos, 25) 
        glEnd()
        glLineWidth(1.0)
            
        glPopMatrix()

def draw_spikes():
    for spike in spikes:
        x, y, spawn_time, height = spike
        glPushMatrix()
        glTranslatef(x * PLATFORM_SIZE, y * PLATFORM_SIZE, height / 2)
        glColor3f(0.5, 0.5, 0.5)
        glScalef(5, 5, height / 5)  # lomba cylinder
        glutSolidCube(2)  
        glPopMatrix()

def get_current_tile():
    x = int(player_pos[0] / PLATFORM_SIZE)
    y = int(player_pos[1] / PLATFORM_SIZE)
    return (x, y)

def update_game():
    global red_tile, red_time, on_ground, score, spark, laser_active, laser_timer,portal,GRID_SIZE
    global laser_position, laser_direction, laser_axis, game_over
    global spikes, spike_timer
    
    if game_over:
        return

    player_vel[2] -= 0.5
    for i in range(3):
        player_pos[i] += player_vel[i]

    if player_pos[2] < 0:
        game_over = True
        return

    tile = get_current_tile()
    if 0 <= tile[0] < GRID_SIZE and 0 <= tile[1] < GRID_SIZE:
        if platforms[tile[0]][tile[1]]:
            if player_pos[2] <= 25:
                player_pos[2] = 25
                player_vel[2] = 0
                on_ground = True
            if red_tile == tile and time.time() - red_time >= 1:
                platforms[tile[0]][tile[1]] = False
        else:
            if player_pos[2] <= 0:
                game_over = True
    else:
        game_over = True

    if red_tile and time.time() - red_time > 1:
        platforms[red_tile[0]][red_tile[1]] = False
        red_tile = None

    if not spark and random.random() < 0.01:
        while True:
            sx, sy = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if platforms[sx][sy]:
                spark = (sx, sy)
                break

    if not portal and random.random() < 0.01:
        while True:
            px, py = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if platforms[px][py]:
                portal = (px, py)
                break

    if spark:
        dx = abs(player_pos[0] - spark[0] * PLATFORM_SIZE)
        dy = abs(player_pos[1] - spark[1] * PLATFORM_SIZE)
        if dx < 10 and dy < 10:
            score += 10
            spark = None

    if portal:
        dx = abs(player_pos[0] - portal[0] * PLATFORM_SIZE)
        dy = abs(player_pos[1] - portal[1] * PLATFORM_SIZE)
        if dx < 10 and dy < 10:
            reset_game()
            # score += 10
            portal = None

    now = time.time()
    # Laser activation/deactivation logic
    if not laser_active and now - laser_timer > 20:
        laser_active = True
        laser_timer = now
        laser_axis = random.randint(0, 1)  # 0 for X, 1 for Y
        laser_position = 0 
        laser_direction = 1  
    elif laser_active:
        # sweeping logic
        laser_position += laser_direction * laser_speed
        #laser @ end of the grid
        if laser_position >= GRID_SIZE or laser_position < 0:
            if now - laser_timer > 10: 
                laser_active = False
                laser_timer = now
            else:
                # Reverse direction
                laser_direction *= -1
                laser_position += laser_direction * laser_speed 
        
        # Check if laser hits player
        player_tile_x = player_pos[0] / PLATFORM_SIZE
        player_tile_y = player_pos[1] / PLATFORM_SIZE
        
        # Check for collision with laser
        if laser_active:
            if laser_axis == 0 and abs(player_tile_x - laser_position) <0.2  and abs(player_pos[2] - 25) < 0.5:
                game_over = True  
            elif laser_axis == 1 and abs(player_tile_y - laser_position) <0.2 and abs(player_pos[2] - 25) < 0.5:
                game_over = True
                
    # Spikes logic
    now = time.time()
    if now - spike_timer > 5:  # Spawn a new spike every 5 seconds
        if len(spikes) < 5:  #5 spikes at a time
            while True:
                sx, sy = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
                if platforms[sx][sy]:  # Only spawn on active platforms
                    spikes.append((sx, sy, now, 0))  # New spike with height 0
                    break
        spike_timer = now

    # spikes (rise and retract)
    new_spikes = []
    for spike in spikes:
        x, y, spawn_time, height = spike
        if now - spawn_time < 3:  # Rise 3 seconds
            height = min(height + 2, 30) 
        else:  # Retract 
            height = max(height - 2, 0)  # Retract to 0
        if height > 0: 
            new_spikes.append((x, y, spawn_time, height))

        #collision with player
        if height > 25: 
            px, py = player_pos[0], player_pos[1]
            if abs(px - x * PLATFORM_SIZE) < 10 and abs(py - y * PLATFORM_SIZE) < 10:
                # score = max(0, score - 2) 
                score = 0 
                # game_over=True

    spikes = new_spikes

def setup_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov, ratio, near_clip, far_clip)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    c_x = c_radius * math.sin(math.radians(c_angle))
    c_y = c_radius * math.cos(math.radians(c_angle))
    center = (GRID_SIZE - 1) * PLATFORM_SIZE / 2
    gluLookAt(c_x, c_y, c_z, center, center, 0, 0, 0, 1)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    setup_camera() 
    glPushMatrix()
    glColor3f(0.4, 0.6, 1)
    glutSolidSphere(1000, 20, 20)
    glPopMatrix()
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            flashing = (red_tile == (i, j))
            if (i%2==0 and j%2==0) or (i%2!=0 and j%2!=0):
                draw_platform(i, j, platforms[i][j], flashing, True)
            else:
                draw_platform(i, j, platforms[i][j], flashing)

    draw_player()
    draw_spark()
    draw_portal()
    draw_laser()
    draw_spikes()

    draw_text(10, 670, f"Time: {int(time.time() - start_time)} | Score: {score}")
    if game_over:
        draw_text(400, 350, "GAME OVER. Press 'R' to Restart")

    glutSwapBuffers()

def reshape(w, h):
    global ratio
    glViewport(0, 0, w, h)
    ratio = float(w) / h if h != 0 else 1.0 

def timer(value):
    global red_tile, red_time, last_platform_timer
    if not game_over:
        update_game()
        if time.time() - last_platform_timer > 5:
            while True:
                i, j = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
                if platforms[i][j]:
                    red_tile = (i, j)
                    red_time = time.time()
                    last_platform_timer = time.time()
                    break
    glutPostRedisplay()
    glutTimerFunc(33, timer, 0)

def keyboard(key, x, y):
    global player_pos, player_vel, on_ground, game_over
    step = PLATFORM_SIZE
    if game_over and key == b'r':
        reset_game(True)
    if not game_over:
        if key == b'w':
            player_pos[0] += step
        elif key == b'a':
            player_pos[1] += step
        elif key == b's':
            player_pos[0] -= step
        elif key == b'd':
            player_pos[1] -= step
        elif key == b' ' and on_ground:
            player_vel[2] = 10
            on_ground = False


def special_keys(key, x, y):
    global c_angle, c_radius, c_z
    if key == GLUT_KEY_LEFT:
        c_angle += 5 
        c_angle %= 360
    elif key == GLUT_KEY_RIGHT:
        c_angle -= 5 
        c_angle %= 360
    elif key == GLUT_KEY_UP:
        c_radius -= c_speed
        c_radius = max(20, c_radius)  
    elif key == GLUT_KEY_DOWN:
        c_radius += c_speed
        c_radius = min(1000, c_radius) 
    

def reset_game(manual=False):
    global player_pos, player_vel, on_ground, score, spark, red_tile, red_time,portal
    global platforms, start_time, last_platform_timer, laser_active, laser_timer
    global laser_position, laser_direction, laser_axis, game_over, GRID_SIZE
    global spikes, spike_timer
    if GRID_SIZE==5 and not manual:
        GRID_SIZE=4
    elif GRID_SIZE==4:
        GRID_SIZE=5
    player_pos[:] = [0, 0, 25]
    player_vel[:] = [0, 0, 0]
    on_ground = True
    if manual:
        score = 0
    portal = None
    spark = None
    red_tile = None
    red_time = 0
    platforms = [[True for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    start_time = time.time()
    last_platform_timer = time.time()
    laser_active = False
    laser_timer = time.time()
    laser_position = 0
    laser_direction = 1
    laser_axis = 0
    game_over = False
    spike_timer = time.time() 
    spikes = []  

def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0, 0, 0, 1)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Don't Fall - 3D Game")
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutTimerFunc(33, timer, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()