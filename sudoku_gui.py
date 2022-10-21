from board import Board
from cube import Cube
from button import Button
import pygame

pygame.init()
screenWidth = 900
screenHeight = 700
error = 0

window = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Sudoku")
clock = pygame.time.Clock()

#load button images
play_img = pygame.image.load('play_button.png')
wrong_number_img = pygame.image.load('wrong_number.png')
easy_img = pygame.image.load('easy.png')
medium_img = pygame.image.load('medium.png')
hard_img = pygame.image.load('hard.png')
new_game_img = pygame.image.load('new_game.png')
exit_img = pygame.image.load('exit.png')
selected_img = pygame.image.load('selected.png')

#create button instances
start_button = Button(300, 100, play_img, 1)
easy_button = Button(350, 200, easy_img, 1)
medium_button = Button(350, 300, medium_img, 1)
hard_button = Button(350, 400, hard_img, 1)
new_game_button = Button(600, 400, new_game_img, 1)
exit_button = Button(600, 500, exit_img, 1 )


#font
pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 30)


def draw_board(board, win):
    # Draw Grid Lines
    space = 100
    gap = 50
    #gap = board._length / 9
    win.fill((255,255,255))



    for i in range(board._length+1):
        if i % 3 == 0:
            thick = 4
        else:
            thick = 1
        pygame.draw.line(win, (0,0,0), (0 + space, i*gap + space), (board._length * gap + space, i*gap + space), thick)
        pygame.draw.line(win, (0,0,0), (i * gap + space, 0 + space), (i * gap + space, board._length*gap + space), thick)

    # Draw Cubes
    for i in range(board._length):
        for j in range(board._length):
            draw_cube(board._cubes[i][j], win)

def draw_cube(cube, win):
    fnt = pygame.font.SysFont("comicsans", 40)

    space = 100
    gap = 50
    #gap = cube._width / 9
    x = cube._column * gap
    y = cube._row * gap

    if not(cube._value == 0):
        text = fnt.render(str(cube._value), 1, (0, 0, 0))
        win.blit(text, (x + (gap/2 - text.get_width()/2) + space, y + (gap/2 - text.get_height()/2) + space))

    # if self.selected:
    #     pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)


def click(board, pos):
    """
    :param: pos
    :return: (row, col)
    """
    gap = 50
    space = 100
    if pos[0] < board._length * gap + space  and pos[1] < board._length * gap + space:
        x = (pos[0] - space) // gap
        y = (pos[1] - space) // gap
        return (int(y),int(x))
    else:
        return None

def wrong_number(window, error):
    x = 50 + error * 50
    y = screenHeight - 100
    window.blit(wrong_number_img, (x,y))


def finish(window):
    text = font.render("Congratulations!!!", False, [0,0,150])
    window.blit(text, (600, 200))
    pygame.display.flip()
    


#stages
FIRST_STAGE = True
SECOND_STAGE = False
THIRD_STAGE = False
FOURTH_STAGE = False




board = Board()
run = True
# pętla główna
while run:
    
    #FIRST STAGE
    if FIRST_STAGE:
        window.fill((100, 100, 241))

        if start_button.draw(window):
            print('clicked')
            FIRST_STAGE = False
            SECOND_STAGE = True
 
    if SECOND_STAGE:
        window.fill((100, 100, 241))
        if easy_button.draw(window):
            quantity_numbers_to_delete = 3
            SECOND_STAGE = False
            THIRD_STAGE = True
        if medium_button.draw(window):
            quantity_numbers_to_delete = 30
            SECOND_STAGE = False
            THIRD_STAGE = True
        if hard_button.draw(window):
            quantity_numbers_to_delete = 45
            SECOND_STAGE = False
            THIRD_STAGE = True

    if THIRD_STAGE:
        window.fill((255, 255, 255))
        board.random_board_square(quantity_numbers_to_delete)
        draw_board(board, window)
        if new_game_button.draw(window):
            board.clear()
            errors = 0
            THIRD_STAGE = True
            FOURTH_STAGE = False
            #and do third_stage_again
        else:
            THIRD_STAGE = False
            FOURTH_STAGE = True

    if FOURTH_STAGE:
        if new_game_button.draw(window):
            board.clear()
            errors = 0
            THIRD_STAGE = True
            FOURTH_STAGE = False
        if exit_button.draw(window):
            board.clear()
            errors = 0
            FIRST_STAGE = True
            FOURTH_STAGE = False


    key = None

    # obsługa zdarzeń 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9

        if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = click(board, pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    print(board._selected)
                    print(key)
                # if board._selected:
                #     window.blit(selected_img, (board._selected[1]*50 +100, board._selected[0]*50 +100))
        
        if board._selected and key is not None:
            print(key)
            print(board._selected)
            if not board.draw_number(key):
                wrong_number(window, error)
                error += 1
            if board.is_finished():
                finish(window)
                print("Finish")
            
            draw_board(board, window)
            key = None

    pygame.display.update()

pygame.quit()