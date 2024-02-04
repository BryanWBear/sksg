import pygame
import sys

BOARD_SIZE = 9
CELL_SIZE = 50
SCREEN_SIZE = BOARD_SIZE * CELL_SIZE

killer_sudoku_puzzle = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

non_rectangular_cages = [
    ([(0, 0), (0, 1), (1, 1), (1, 0)], 10),
    ([(3, 0), (3, 1), (4, 2), (5, 1), (5, 0), (4, 0)], 20),
]

def draw_board(screen):
    for i in range(1, BOARD_SIZE):
        if i % 3 == 0:
            pygame.draw.line(screen, (0, 0, 0), (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_SIZE), 4)
            pygame.draw.line(screen, (0, 0, 0), (0, i * CELL_SIZE), (SCREEN_SIZE, i * CELL_SIZE), 4)
        else:
            pygame.draw.line(screen, (0, 0, 0), (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_SIZE), 2)
            pygame.draw.line(screen, (0, 0, 0), (0, i * CELL_SIZE), (SCREEN_SIZE, i * CELL_SIZE), 2)

    font = pygame.font.Font(None, 36)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if killer_sudoku_puzzle[row][col] != 0:
                text = font.render(str(killer_sudoku_puzzle[row][col]), True, (0, 0, 0))
                screen.blit(text, (col * CELL_SIZE + 20, row * CELL_SIZE + 10))

    for cage_vertices, cage_sum in non_rectangular_cages:
        pygame.draw.polygon(screen, (200, 200, 200), [(x * CELL_SIZE, y * CELL_SIZE) for x, y in cage_vertices], 0)
        pygame.draw.lines(screen, (0, 0, 0), False, [(x * CELL_SIZE, y * CELL_SIZE) for x, y in cage_vertices], 2)

        cage_text = font.render(str(cage_sum), True, (0, 0, 0))
        screen.blit(cage_text, (sum(x for x, _ in cage_vertices) * CELL_SIZE / len(cage_vertices) + 10,
                                sum(y for _, y in cage_vertices) * CELL_SIZE / len(cage_vertices)))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Killer Sudoku Board")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        draw_board(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()