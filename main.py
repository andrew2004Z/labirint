import pygame as pg
from random import random
from collections import deque


def get_rect(x, y):
    return x * TILE + 1, y * TILE + 1, TILE - 2, TILE - 2


def get_next_nodes(x, y):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows and not grid[y][x] else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]

def load_wall_coords(filename):
    with open(filename, 'r') as file:
        return [list(map(int, line.strip().split())) for line in file]

cols, rows = load_wall_coords("maze.txt")[0]
TILE = 60

pg.init()
sc = pg.display.set_mode([cols * TILE, rows * TILE])
clock = pg.time.Clock()
# grid

sp_walls = load_wall_coords("maze.txt")[1:]

grid = [[0 for col in range(cols)] for row in range(rows)]
for i in sp_walls:
    grid[i[0]][i[1]] = 1
# dict of adjacency lists
graph = {}
for y, row in enumerate(grid):
    for x, col in enumerate(row):
        if not col:
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y)

# BFS settings
start = (0, 0)
queue = deque([start])
visited = {start: None}
cur_node = start

while True:
    # fill screen
    sc.fill(pg.Color('black'))
    # draw grid
    [[pg.draw.rect(sc, pg.Color('darkorange'), get_rect(x, y), border_radius=TILE // 5)
      for x, col in enumerate(row) if col] for y, row in enumerate(grid)]
    # draw BFS work
    [pg.draw.rect(sc, pg.Color('forestgreen'), get_rect(x, y)) for x, y in visited]
    [pg.draw.rect(sc, pg.Color('darkslategray'), get_rect(x, y)) for x, y in queue]

    # BFS logic
    if queue:
        cur_node = queue.popleft()
        next_nodes = graph[cur_node]
        for next_node in next_nodes:
            if next_node not in visited:
                queue.append(next_node)
                visited[next_node] = cur_node
    # draw path
    path_head, path_segment = cur_node, cur_node
    c = 0
    while path_segment:
        pg.draw.rect(sc, pg.Color('white'), get_rect(*path_segment), TILE, border_radius=TILE // 3)
        path_segment = visited[path_segment]
        c += 1
    print(c)
    pg.draw.rect(sc, pg.Color('blue'), get_rect(*start), border_radius=TILE // 3)
    pg.draw.rect(sc, pg.Color('magenta'), get_rect(*path_head), border_radius=TILE // 3)
    # pygame necessary lines
    [exit() for event in pg.event.get() if event.type == pg.QUIT]
    pg.display.flip()
    clock.tick(20)