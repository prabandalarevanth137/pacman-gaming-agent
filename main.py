import pygame
import sys
import heapq
import random

pygame.init()

# ======================================
# WINDOW SETTINGS
# ======================================

WIDTH = 900
HEIGHT = 550
CELL = 45

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman AI Project")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# ======================================
# COLORS
# ======================================

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# ======================================
# MAZE
# ======================================

# 1 = Wall
# 2 = Food
# 3 = Power Pellet
# 0 = Empty

maze = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,1],
[1,2,1,1,1,2,1,1,1,2,1,1,1,2,1,1,1,2,1],
[1,2,2,2,1,2,2,2,1,2,1,2,2,2,1,2,2,2,1],
[1,1,1,2,1,1,1,2,1,2,1,2,1,1,1,2,1,1,1],
[1,2,2,2,2,2,1,2,2,2,2,2,1,2,2,2,2,2,1],
[1,2,1,1,1,2,1,1,1,1,1,2,1,2,1,1,1,2,1],
[1,2,2,2,1,2,2,2,2,2,1,2,2,2,1,2,2,2,1],
[1,1,1,2,1,1,1,1,1,2,1,1,1,2,1,1,1,2,1],
[1,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

# ======================================
# PLAYER
# ======================================

pacman_x = 1
pacman_y = 1

score = 0
lives = 3

# ======================================
# POWER MODE
# ======================================

power_mode = False
power_timer = 0

# ======================================
# CHERRY
# ======================================

cherry_x = 9
cherry_y = 5
cherry_visible = True

# ======================================
# SINGLE GHOST
# ======================================

ghosts = [
    {"x": 17, "y": 9, "color": RED}
]

# ======================================
# DRAW MAZE
# ======================================

def draw_maze():

    for y, row in enumerate(maze):

        for x, cell in enumerate(row):

            rect = pygame.Rect(
                x * CELL,
                y * CELL,
                CELL,
                CELL
            )

            # Walls
            if cell == 1:

                pygame.draw.rect(
                    screen,
                    BLUE,
                    rect
                )

            # Empty path
            else:

                pygame.draw.rect(
                    screen,
                    BLACK,
                    rect
                )

            # Food pellets
            if cell == 2:

                pygame.draw.circle(
                    screen,
                    WHITE,
                    (
                        x * CELL + CELL // 2,
                        y * CELL + CELL // 2
                    ),
                    5
                )

            # Power pellets
            if cell == 3:

                pygame.draw.circle(
                    screen,
                    GREEN,
                    (
                        x * CELL + CELL // 2,
                        y * CELL + CELL // 2
                    ),
                    10
                )

# ======================================
# DRAW PACMAN
# ======================================

def draw_pacman():

    pygame.draw.circle(
        screen,
        YELLOW,
        (
            pacman_x * CELL + CELL // 2,
            pacman_y * CELL + CELL // 2
        ),
        CELL // 2 - 4
    )

# ======================================
# DRAW GHOST
# ======================================

def draw_ghosts():

    for ghost in ghosts:

        pygame.draw.circle(
            screen,
            ghost["color"],
            (
                ghost["x"] * CELL + CELL // 2,
                ghost["y"] * CELL + CELL // 2
            ),
            CELL // 2 - 4
        )

# ======================================
# DRAW CHERRY
# ======================================

def draw_cherry():

    if cherry_visible:

        pygame.draw.circle(
            screen,
            RED,
            (
                cherry_x * CELL + CELL // 2,
                cherry_y * CELL + CELL // 2
            ),
            12
        )

# ======================================
# DRAW SCORE & LIVES
# ======================================

def draw_score():

    text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    screen.blit(text, (10, HEIGHT - 40))

    # Lives display

    for i in range(lives):

        pygame.draw.circle(
            screen,
            YELLOW,
            (
                220 + i * 40,
                HEIGHT - 20
            ),
            12
        )

# ======================================
# HEURISTIC
# ======================================

def heuristic(a, b):

    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# ======================================
# A* SEARCH
# ======================================

def astar(start, goal):

    open_set = []

    heapq.heappush(
        open_set,
        (0, start, [])
    )

    visited = set()

    while open_set:

        cost, current, path = heapq.heappop(open_set)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            return path

        x, y = current

        neighbors = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)
        ]

        for nx, ny in neighbors:

            if maze[ny][nx] != 1 and (nx, ny) not in visited:

                new_cost = len(path) + 1

                priority = (
                    new_cost +
                    heuristic((nx, ny), goal)
                )

                heapq.heappush(
                    open_set,
                    (
                        priority,
                        (nx, ny),
                        path + [(nx, ny)]
                    )
                )

    return []

# ======================================
# RESET GAME
# ======================================

def reset_game():

    global pacman_x
    global pacman_y
    global score
    global lives
    global power_mode
    global cherry_visible
    global ghosts

    pacman_x = 1
    pacman_y = 1

    score = 0
    lives = 3

    power_mode = False

    cherry_visible = True

    ghosts = [
        {"x": 17, "y": 9, "color": RED}
    ]

# ======================================
# GAME OVER SCREEN
# ======================================

def game_over():

    while True:

        screen.fill(BLACK)

        text = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        restart_text = font.render(
            "Press R to Restart",
            True,
            WHITE
        )

        quit_text = font.render(
            "Press Q to Quit",
            True,
            WHITE
        )

        screen.blit(text, (250, 180))
        screen.blit(restart_text, (300, 280))
        screen.blit(quit_text, (320, 340))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:

                    reset_game()
                    return

                if event.key == pygame.K_q:

                    pygame.quit()
                    sys.exit()

# ======================================
# WIN SCREEN
# ======================================

def win_game():

    while True:

        screen.fill(BLACK)

        text = big_font.render(
            "YOU WIN!",
            True,
            GREEN
        )

        restart_text = font.render(
            "Press R to Restart",
            True,
            WHITE
        )

        quit_text = font.render(
            "Press Q to Quit",
            True,
            WHITE
        )

        screen.blit(text, (280, 180))
        screen.blit(restart_text, (300, 280))
        screen.blit(quit_text, (320, 340))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:

                    reset_game()
                    return

                if event.key == pygame.K_q:

                    pygame.quit()
                    sys.exit()

# ======================================
# MAIN GAME LOOP
# ======================================

while True:

    # EVENTS

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

    # ======================================
    # PLAYER MOVEMENT
    # ======================================

    keys = pygame.key.get_pressed()

    new_x = pacman_x
    new_y = pacman_y

    if keys[pygame.K_LEFT]:
        new_x -= 1

    if keys[pygame.K_RIGHT]:
        new_x += 1

    if keys[pygame.K_UP]:
        new_y -= 1

    if keys[pygame.K_DOWN]:
        new_y += 1

    # Valid movement

    if maze[new_y][new_x] != 1:

        pacman_x = new_x
        pacman_y = new_y

        # Eat food

        if maze[pacman_y][pacman_x] == 2:

            maze[pacman_y][pacman_x] = 0

            score += 10

        # Eat power pellet

        if maze[pacman_y][pacman_x] == 3:

            maze[pacman_y][pacman_x] = 0

            score += 50

            power_mode = True

            power_timer = pygame.time.get_ticks()

        # Eat cherry

        if (
            pacman_x == cherry_x
            and
            pacman_y == cherry_y
            and
            cherry_visible
        ):

            cherry_visible = False

            score += 200

            power_mode = True

            power_timer = pygame.time.get_ticks()

    # ======================================
    # POWER TIMER
    # ======================================

    if power_mode:

        current_time = pygame.time.get_ticks()

        if current_time - power_timer > 5000:

            power_mode = False

    # ======================================
    # GHOST AI
    # ======================================

    for ghost in ghosts:

        # Run away in power mode

        if power_mode:

            possible_moves = []

            directions = [
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1)
            ]

            for dx, dy in directions:

                nx = ghost["x"] + dx
                ny = ghost["y"] + dy

                if maze[ny][nx] != 1:

                    possible_moves.append((nx, ny))

            if possible_moves:

                move = random.choice(possible_moves)

                ghost["x"] = move[0]
                ghost["y"] = move[1]

        else:

            path = astar(
                (ghost["x"], ghost["y"]),
                (pacman_x, pacman_y)
            )

            # Slow ghost movement

            if path and random.randint(0, 100) < 35:

                ghost["x"], ghost["y"] = path[0]

    # ======================================
    # COLLISION
    # ======================================

    for ghost in ghosts:

        if (
            pacman_x == ghost["x"]
            and
            pacman_y == ghost["y"]
        ):

            # Eat ghost

            if power_mode:

                ghost["x"] = 17
                ghost["y"] = 9

                score += 100

            # Lose life

            else:

                lives -= 1

                pacman_x = 1
                pacman_y = 1

                pygame.time.delay(1000)

                if lives <= 0:

                    game_over()

    # ======================================
    # WIN CONDITION
    # ======================================

    food_left = False

    for row in maze:

        if 2 in row or 3 in row:

            food_left = True

    if not food_left:

        win_game()

    # ======================================
    # DRAW EVERYTHING
    # ======================================

    screen.fill(BLACK)

    draw_maze()
    draw_pacman()
    draw_ghosts()
    draw_cherry()
    draw_score()

    pygame.display.update()

    clock.tick(8)