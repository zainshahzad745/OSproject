import random, pygame, sys, threading
from pygame.locals import *

def mainWindow():
    global input_fields
    input_fields = {
        "qty": "",
        "speed": ""
    }
    size = (993, 739)
    screen = pygame.display.set_mode(size)
    button_x = 370
    button_y = 350
    button_width = 200
    button_height = 50
    background_image = pygame.image.load("s.png")
    screen.blit(background_image, (0, 0))
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.display.update()
    hover = False
    pygame.init()
    size = (993, 739)
    screen = pygame.display.set_mode(size)
    background_image = pygame.image.load("s.png").convert()
    screen.blit(background_image, (0, 0))
    button_x = 370
    button_y = 350
    button_width = 200
    button_height = 50
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    start_color = (255, 0, 0)
    end_color = (255, 153, 51)
    shadow_color = (0, 0, 0)
    shadow_offset = (5, 5)
    font = pygame.font.Font(None, 30)
    text = font.render("Start", True, (255, 255, 255))
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))

    # Create variables to store the input text


    # Create a variable to track which input field is active
    active_field = "qty"

    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalnum() or event.unicode == " ":
                    input_fields[active_field] += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    input_fields[active_field] = input_fields[active_field][:-1]
                elif event.key == pygame.K_RETURN:
                    if active_field == "qty":
                        print(input_fields)
                        input_fields = {
                            "qty": "",
                            "speed": ""
                        }
                        main()
                    else:
                        active_field = list(input_fields.keys())[list(input_fields.keys()).index(active_field) + 1]

        # Draw the input fields
        pygame.draw.rect(screen, (255, 255, 255), (500, 495, 200, 50))
        # pygame.draw.rect(screen, (255, 255, 255), (100, 200, 200, 50))
        # pygame.draw.rect(screen, (255, 255, 255), (100, 300, 200, 50))

        # Draw the input text
        font = pygame.font.Font(None, 32)
        text = font.render(input_fields["qty"], True, (0, 0, 0))
        screen.blit(text, (510, 505))
        global var
        var = input_fields['qty']
        #print(var)
        # Update the display
        pygame.display.update()



#NUM_WORMS = var  # the number of worms in the grid
FPS = 60  # frames per second that the program runs
CELL_SIZE = 20  # how many pixels wide and high each "cell" in the grid is
CELLS_WIDE = 50  # how many cells wide the grid is
CELLS_HIGH = 50  # how many cells high the grid is
GRID = []
for x in range(CELLS_WIDE):
    GRID.append([None] * CELLS_HIGH)
GRID_LOCKS = []
for x in range(CELLS_WIDE):
    column = []
    for y in range(CELLS_HIGH):
        column.append(threading.Lock())  # create one Lock object for each cell
    GRID_LOCKS.append(column)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK
GRID_LINES_COLOR = DARKGRAY
# Calculate total pixels wide and high that the full window is
WINDOWWIDTH = CELL_SIZE * CELLS_WIDE
WINDOWHEIGHT = CELL_SIZE * CELLS_HIGH
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
head = 0
tail = -1
# A global variable that the Worm threads check to see if they should exit.
WORMS_RUNNING = True

class Worm(threading.Thread):
    def __init__(self, name='Worm', maxsize=None, color=None, speed=50):
        threading.Thread.__init__(self)
        self.name = name
        if maxsize is None:
            self.maxsize = random.randint(4, 10)
            if random.randint(0, 4) == 0:
                self.maxsize += random.randint(10, 20)
        else:
            self.maxsize = maxsize
        if color is None:
            self.color = (random.randint(60, 255), random.randint(60, 255), random.randint(60, 255))
        else:
            self.color = color

        if speed is None:
            self.speed = random.randint(20, 500)  # wait time before movements will be between 0.02 and 0.5 seconds
        else:
            self.speed = speed

        # The body starts as a single segment at a random location (but make sure
        # it is unoccupied.)
        while True:
            startx = random.randint(0, CELLS_WIDE - 1)
            starty = random.randint(0, CELLS_HIGH - 1)
            GRID_LOCKS[startx][starty].acquire()  # block until this thread can acquire the lock
            if GRID[startx][starty] is None:
                break  # found an unoccupied cell in the grid

        GRID[startx][starty] = self.color  # modify the shared data structure
        GRID_LOCKS[startx][starty].release()
        # The worm's body starts as a single segment, and keeps growing until it
        # reaches full length.
        self.body = [{'x': startx, 'y': starty}]
        self.direction = random.choice((UP, DOWN, LEFT, RIGHT))
    def run(self):

        while True:
            if not WORMS_RUNNING:
                return
            # Randomly decide to change direction
            if random.randint(0, 100) < 20:
                self.direction = random.choice((UP, DOWN, LEFT, RIGHT))
            nextx, nexty = self.getNextPosition()
            origx, origy = nextx, nexty
            if origx not in (-1, CELLS_WIDE) and origy not in (-1, CELLS_HIGH):
                gotLock = GRID_LOCKS[origx][origy].acquire(
                    timeout=1)  # don't return (that is, block) until this thread can acquire the lock
                if not gotLock:
                    continue
            if nextx in (-1, CELLS_WIDE) or nexty in (-1, CELLS_HIGH) or GRID[nextx][nexty] is not None:
                self.direction = self.getNewDirection()
                if self.direction is None:
                    # No places to move, so try reversing our worm.
                    self.body.reverse()  # Now the head is the tail and the tail is the head.
                    self.direction = self.getNewDirection()

                if self.direction is not None:
                    # It is possible to move in some direction, so re ask for the next postion.
                    nextx, nexty = self.getNextPosition()
            if origx not in (-1, CELLS_WIDE) and origy not in (-1, CELLS_HIGH):
                GRID_LOCKS[origx][origy].release()

            if self.direction is not None:
                GRID_LOCKS[nextx][nexty].acquire()
                # Space on the grid is free, so move there.
                GRID[nextx][nexty] = self.color  # update the GRID state
                GRID_LOCKS[nextx][nexty].release()
                self.body.insert(0, {'x': nextx, 'y': nexty})  # update this worm's own state

                if len(self.body) > self.maxsize:
                    gotLock = GRID_LOCKS[self.body[tail]['x']][self.body[tail]['y']].acquire(timeout=2)
                    if not gotLock:
                        self.maxsize -= 1
                        # print('chop %s' % (self.name))
                    GRID[self.body[tail]['x']][self.body[tail]['y']] = None  # update the GRID state
                    GRID_LOCKS[self.body[tail]['x']][self.body[tail]['y']].release()
                    del self.body[tail]  # update this worm's own state (heh heh, worm butt)
            else:
                self.direction = random.choice(
                    (UP, DOWN, LEFT, RIGHT))  # can't move, so just do nothing for now but set a new random direction
            pygame.time.wait(self.speed)
    def getNextPosition(self):

        if self.direction == UP:
            nextx = self.body[head]['x']
            nexty = self.body[head]['y'] - 1
        elif self.direction == DOWN:
            nextx = self.body[head]['x']
            nexty = self.body[head]['y'] + 1
        elif self.direction == LEFT:
            nextx = self.body[head]['x'] - 1
            nexty = self.body[head]['y']
        elif self.direction == RIGHT:
            nextx = self.body[head]['x'] + 1
            nexty = self.body[head]['y']
        else:
            assert False, 'Bad value for self.direction: %s' % self.direction

        return nextx, nexty
    def getNewDirection(self):
        x = self.body[head]['x']
        y = self.body[head]['y']
        # a list of possible directions the worm can move.
        newDirection = []
        if y - 1 not in (-1, CELLS_HIGH) and GRID[x][y - 1] is None:
            newDirection.append(UP)
        if y + 1 not in (-1, CELLS_HIGH) and GRID[x][y + 1] is None:
            newDirection.append(DOWN)
        if x - 1 not in (-1, CELLS_WIDE) and GRID[x - 1][y] is None:
            newDirection.append(LEFT)
        if x + 1 not in (-1, CELLS_WIDE) and GRID[x + 1][y] is None:
            newDirection.append(RIGHT)
        if newDirection == []:
            return None  # None is returned when there are no possible ways for the worm to move.
        return random.choice(newDirection)

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Threadworms')
    worms = []  # a list that contains all the worm objects
    for i in range(int(var)):
        worms.append(Worm(name='Worm %s' % i))
        worms[-1].start()  # Start the worm code in its own thread.
    DISPLAYSURF.fill(BGCOLOR)
    while True:  # main game loop
        handleEvents()
        drawGrid()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
def handleEvents():
    global WORMS_RUNNING
    for event in pygame.event.get():  # event handling loop
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            WORMS_RUNNING = False  # Setting this to False tells the Worm threads to exit.
            pygame.quit()
            sys.exit()

def drawGrid():
    # Draw the grid lines.
    for x in range(0, WINDOWWIDTH, CELL_SIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, GRID_LINES_COLOR, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELL_SIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, GRID_LINES_COLOR, (0, y), (WINDOWWIDTH, y))
    for x in range(0, CELLS_WIDE):
        for y in range(0, CELLS_HIGH):
            gotLock = GRID_LOCKS[x][y].acquire(timeout=0.02)
            if not gotLock:
                continue

            if GRID[x][y] is None:
                pygame.draw.rect(DISPLAYSURF, BGCOLOR,
                                 (x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 1, CELL_SIZE - 1))
                GRID_LOCKS[x][y].release()  # We're done reading GRID, so release the lock.
            else:
                color = GRID[x][y]  # read the GRID data structure
                GRID_LOCKS[x][y].release()
                darkerColor = (max(color[0] - 50, 0), max(color[1] - 50, 0), max(color[2] - 50, 0))
                pygame.draw.rect(DISPLAYSURF, darkerColor, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(DISPLAYSURF, color,
                                 (x * CELL_SIZE + 4, y * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8))

def setGridSquares(squares, color=(192, 192, 192)):
    squares = squares.split('\n')
    if squares[0] == '':
        del squares[0]
    if squares[-1] == '':
        del squares[-1]
    for y in range(min(len(squares), CELLS_HIGH)):
        for x in range(min(len(squares[y]), CELLS_WIDE)):
            GRID_LOCKS[x][y].acquire()
            if squares[y][x] == ' ':
                GRID[x][y] = None
            elif squares[y][x] == '.':
                pass
            else:
                GRID[x][y] = color
            GRID_LOCKS[x][y].release()



def first_Worm():
    pygame.init()
    size = (993, 739)
    screen = pygame.display.set_mode(size)
    background_image = pygame.image.load("test42.png").convert()
    screen.blit(background_image, (0, 0))
    button_x = 370
    button_y = 350
    button_width = 200
    button_height = 50
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    start_color = (255, 0, 0)
    end_color = (255, 153, 51)
    shadow_color = (0, 0, 0)
    shadow_offset = (5, 5)
    hover=False
    font = pygame.font.Font(None, 30)
    text = font.render("Start", True, (255, 255, 255))
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                if button_rect.collidepoint(mouse_pos):
                    hover = True
                else:
                    hover = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_rect.collidepoint(mouse_pos):
                    second_Worm()
                    pass
        screen.blit(background_image, (0, 0))
        if hover:
            pygame.draw.rect(screen, end_color, button_rect)
            pygame.draw.rect(screen, start_color, button_rect, 2)
        else:
            pygame.draw.rect(screen, start_color, button_rect)
        pygame.draw.rect(screen, shadow_color,
                        (button_x + shadow_offset[0], button_y + shadow_offset[1], button_width, button_height))
        screen.blit(text, text_rect)
        pygame.display.update()


def second_Worm():
    pygame.init()
    size = (993, 739)
    screen = pygame.display.set_mode(size)
    background_image = pygame.image.load("intro 1.png").convert()
    screen.blit(background_image, (0, 0))
    button_x = 590
    button_y = 550
    button_width = 200
    button_height = 50
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    start_color = (255, 0, 0)
    end_color = (255, 153, 51)
    shadow_color = (0, 0, 0)
    hover=False
    shadow_offset = (5, 5)
    font = pygame.font.Font(None, 30)
    text = font.render("NEXT", True, (255, 255, 255))
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                if button_rect.collidepoint(mouse_pos):
                    hover = True
                else:
                    hover = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_rect.collidepoint(mouse_pos):
                    Third_Worm()
                    pass
        screen.blit(background_image, (0, 0))
        if hover:
            pygame.draw.rect(screen, end_color, button_rect)
            pygame.draw.rect(screen, start_color, button_rect, 2)
        else:
            pygame.draw.rect(screen, start_color, button_rect)
        pygame.draw.rect(screen, shadow_color,
                        (button_x + shadow_offset[0], button_y + shadow_offset[1], button_width, button_height))
        screen.blit(text, text_rect)
        pygame.display.update()

def Third_Worm():
    pygame.init()
    size = (993, 739)
    screen = pygame.display.set_mode(size)
    background_image = pygame.image.load("intro 2.png").convert()
    screen.blit(background_image, (0, 0))
    button_x = 590
    button_y = 560
    button_width = 200
    button_height = 50
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    start_color = (255, 0, 0)
    end_color = (255, 153, 51)
    shadow_color = (0, 0, 0)
    hover=False
    shadow_offset = (5, 5)
    font = pygame.font.Font(None, 30)
    text = font.render("NEXT", True, (255, 255, 255))
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))


    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                if button_rect.collidepoint(mouse_pos):
                    hover = True
                else:
                    hover = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if button_rect.collidepoint(mouse_pos):
                    mainWindow()
                    pass
        screen.blit(background_image, (0, 0))
        if hover:
            pygame.draw.rect(screen, end_color, button_rect)
            pygame.draw.rect(screen, start_color, button_rect, 2)
        else:
            pygame.draw.rect(screen, start_color, button_rect)
        pygame.draw.rect(screen, shadow_color,
                        (button_x + shadow_offset[0], button_y + shadow_offset[1], button_width, button_height))
        screen.blit(text, text_rect)

        #text = font.render(input_fields["email"], True, (0, 0, 0))
        #screen.blit(text, (110, 310))
        pygame.display.update()

# def Fourth_Worm():
#     pygame.init()
#     size = (993, 739)
#     screen = pygame.display.set_mode(size)
#     background_image = pygame.image.load("test42.png").convert()
#     screen.blit(background_image, (0, 0))
#     button_x = 590
#     button_y = 560
#     hover=False
#     button_width = 200
#     button_height = 50
#     button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
#     start_color = (255, 0, 0)
#     end_color = (255, 153, 51)
#     shadow_color = (0, 0, 0)
#     shadow_offset = (5, 5)
#     font = pygame.font.Font(None, 30)
#     text = font.render("Start", True, (255, 255, 255))
#     text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.MOUSEMOTION:
#                 mouse_pos = event.pos
#                 if button_rect.collidepoint(mouse_pos):
#                     hover = True
#                 else:
#                     hover = False
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 mouse_pos = event.pos
#                 if button_rect.collidepoint(mouse_pos):
#                     mainWindow()
#                     pass
#         screen.blit(background_image, (0, 0))
#         if hover:
#             pygame.draw.rect(screen, end_color, button_rect)
#             pygame.draw.rect(screen, start_color, button_rect, 2)
#         else:
#             pygame.draw.rect(screen, start_color, button_rect)
#         pygame.draw.rect(screen, shadow_color,
#                         (button_x + shadow_offset[0], button_y + shadow_offset[1], button_width, button_height))
#         screen.blit(text, text_rect)
#         pygame.display.update()
#

first_Worm()