import pygame
import heapq
from collections import deque
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (100, 100, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_YELLOW = (255, 255, 150)

# Grid cell dimensions
WIDTH = 22
HEIGHT = 22
MARGIN = 3

# Grid size
ROWS = 20
COLS = 20

class Field:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = WHITE
        self.is_wall = False
        self.f_score = None  

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            [(MARGIN + WIDTH) * self.col + MARGIN,
             (MARGIN + HEIGHT) * self.row + MARGIN,
             WIDTH, HEIGHT]
        )
        if self.f_score is not None:
            text = font.render(str(self.f_score), True, BLACK)
            text_rect = text.get_rect(center=(
                (MARGIN + WIDTH) * self.col + MARGIN + WIDTH // 2,
                (MARGIN + HEIGHT) * self.row + MARGIN + HEIGHT // 2))
            screen.blit(text, text_rect)
       

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[Field(row, col) for col in range(cols)] for row in range(rows)]

    def draw(self, screen):
        for row in self.grid:
            for field in row:
                field.draw(screen)

def map_coords(city_row, city_col):
    #(1,1)->(0,0) #上下翻轉
    return ROWS - city_row, city_col - 1

def add_wall_line(start_row, start_col, length, direction):#自動設定直線
    for i in range(length):
        if direction == 'h':
            r, c = start_row, start_col + i
        elif direction == 'v':
            r, c = start_row + i, start_col
        else:
            continue  
        if 0 <= r < ROWS and 0 <= c < COLS:
            grid.grid[r][c].is_wall = True
            grid.grid[r][c].color = BLACK

def heuristic(a, b):#曼哈頓距離,不考慮斜走
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(pos):
    row, col = pos
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < ROWS and 0 <= c < COLS and not grid.grid[r][c].is_wall:
            yield (r, c) #生成器概念，雖然每次也只傳一個值，但會從上次的地方繼續
            
def reconstruct_path(came_from, current, start):
    path = []
    while current in came_from:
        current = came_from[current]
        if current != start:
            grid.grid[current[0]][current[1]].color = (255, 255, 0)  
        path.append(current)
    return path[::-1]

#path planning algorithm
def a_star_search(start, goal):
    open_set = []
    heapq.heappush(open_set, (0,start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            reconstruct_path(came_from, current, start)
            return True
        print("==>curent",current)
        for neighbor in get_neighbors(current):
            print("neighbor",neighbor)
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]: #確認是否為未探詢的點/如果找到更好的路徑
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g #如果是小於原本紀錄的，則可以得到一條相同目的地，但更好的路徑
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal) #A*的核心，g:實際走的距離, h:預估距離 ex曼哈頓或是歐氏距離
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

                if neighbor != goal:
                    grid.grid[neighbor[0]][neighbor[1]].color = BLUE
                    grid.grid[neighbor[0]][neighbor[1]].f_score = int(f_score[neighbor])
                    #reset_temp_path_color() 
                    #draw_temp_path(came_from, neighbor) 
                    screen.fill(BLACK)
                    grid.draw(screen)
                    pygame.display.flip()
                    pygame.time.delay(10)
        print("open_set:",open_set)
        print("===============")
    return False

def bfs_search(start, goal):
    queue = deque()#PIPO
    queue.append(start)
    came_from = {}
    visited = set()
    visited.add(start)

    while queue:
        current = queue.popleft()
        if current == goal:
            reconstruct_path(came_from, current, start)
            return True
        print("==> current", current)
        for neighbor in get_neighbors(current):
            print("neighbor", neighbor)
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

                if neighbor != goal:
                    grid.grid[neighbor[0]][neighbor[1]].color = BLUE
                    screen.fill(BLACK)
                    grid.draw(screen)
                    pygame.display.flip()
                    pygame.time.delay(10)

        print("queue:", list(queue))
        print("===============")

    return False
# --- Pygame setup ---
pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 16)

size = ((WIDTH + MARGIN) * COLS + MARGIN, (HEIGHT + MARGIN) * ROWS + MARGIN)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Labyrinth Grid")

grid = Grid(ROWS, COLS) 

#draw wall
r, c = map_coords(10, 5)
add_wall_line(r, c, 6, 'h')
r, c = map_coords(9 ,10)
add_wall_line(r, c, 9, 'v')
r, c = map_coords(20 ,17)
add_wall_line(r, c, 11, 'v')

#draw Start/Goal
start = (19, 0)
goal = (0, 19)
grid.grid[start[0]][start[1]].color = GREEN 
grid.grid[goal[0]][goal[1]].color = RED   
#a_star_search(start, goal)
bfs_search(start, goal)
done = False
clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get():#抓取視窗事件
        if event.type == pygame.QUIT:#按下視窗關閉按鈕
            done = True
    screen.fill(BLACK)
    grid.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
