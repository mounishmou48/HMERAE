import pygame
import numpy as np
from pygame.locals import QUIT
from pygame.surfarray import array2d
import preprocess
import dataset
import network


resolution = (1280, 720)
background_color = (255, 255, 255)
white = (255, 255, 255)
draw_color = (0, 0, 0)
draw_thickness = 7
left_mouse_button = (1, 0, 0)
start_position = (0, 0)

pygame.init()
screen = pygame.display.set_mode(resolution)
background = pygame.Surface(screen.get_size())
background.fill(background_color)

font = pygame.font.SysFont("monospace", 48)
equ_label = None
ans_label = None

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                #screen.fill(white)
                background = pygame.Surface(screen.get_size())
                background.fill(background_color)
                #pygame.display.update()
        elif event.type == pygame.MOUSEMOTION:
            end_position = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed() == left_mouse_button:
                pygame.draw.line(background, draw_color, start_position, end_position, draw_thickness)
            start_position = end_position
        elif event.type == pygame.MOUSEBUTTONUP:
            pixels = np.asarray(array2d(background))
            pixels = np.divide(pixels, 16777215)
            pixels = pixels.transpose()
            chars = preprocess.extract_chars(pixels)
            chars = chars.reshape(chars.shape[0], dataset.IMG_ROWS, dataset.IMG_COLS, 1)
            pred = network.model.predict_classes(chars, verbose=0)
            pred_str = str()
            for p in pred:
                pred_str += dataset.CLASS_INDEX[p]
            pred_str = pred_str.replace('star', '*').replace('slash', '/')
            equ_label = font.render('equ = ' + pred_str, 1, (0, 255, 0))
            if (pred_str[-1].isdigit() or pred_str[-1] is ')') and pred_str.count('(') is pred_str.count(')'):
                ans_label = font.render('ans = ' + str(eval(pred_str)), 1, (0, 255, 0))

            # for i, char in enumerate(chars):
            #     scipy.misc.imsave(')_' + str(i) + '.png', char)
    screen.blit(background, (0, 0))
    if equ_label is not None:
        screen.blit(equ_label, (20, resolution[1] - 100))
    if ans_label is not None:
        screen.blit(ans_label, (20, resolution[1] - 50))
    pygame.display.flip()
