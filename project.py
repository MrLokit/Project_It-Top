import pygame
from pygame.locals import *
import sys
import time
import random

# 1280 на 700

class Game:

    def __init__(self):
        self.w = 1280
        self.h = 700
        self.reset = True
        self.active = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time:0 Accuracy:0 % Wpm:0 '
        self.wpm = 0
        self.end = False
        self.HEAD_C = (255, 0, 0)
        self.TEXT_C = (255, 255, 255)
        self.RESULT_C = (0, 255, 0)


        pygame.init()
        self.open_img = pygame.image.load('type-speed-open.png')
        self.open_img = pygame.transform.scale(self.open_img, (self.w,self.h))


        self.bg = pygame.image.load('background.jpg')
        self.bg = pygame.transform.scale(self.bg, (1280, 720))

        self.screen = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption('Typing Speed Test in English')


    def draw_text(self, screen, msg, y ,fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1,color)
        text_rect = text.get_rect(center=(self.w/2, y))
        screen.blit(text, text_rect)
        pygame.display.update()

    def get_sentence(self):
        f = open('sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence

    def show_results(self, screen):
        if(not self.end):
            # Рассчет времени
            self.total_time = time.time() - self.time_start

            # Рассчет аккуратности написания
            count = 0
            for i,c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count/len(self.word)*100

            # Рассчет слов в минуту
            self.wpm = len(self.input_text)*60/(5*self.total_time)
            self.end = True
            print(self.total_time)

            # Отрисовка результатов
            self.results = 'Time: '+str(round(self.total_time)) +" secs          Accuracy: "+ str(round(self.accuracy)) + "%" + '          Wpm: ' + str(round(self.wpm))

            # Отрисовка кнопки
            self.time_img = pygame.image.load('button.png')
            self.time_rect = pygame.transform.scale(self.time_img, (150, 150))
            screen.blit(self.time_img, (self.w // 2 - 240, self.h - 200))
            self.draw_text(screen, "Reset", self.h - 70, 40, (255, 255, 255))

            print(self.results)
            pygame.display.update()

    def run(self):
        self.reset_game()

        self.running=True
        while(self.running):
            clock = pygame.time.Clock()
            self.screen.fill((0,0,0), (50,350,1180,75))
            pygame.draw.rect(self.screen,self.HEAD_C, (50,350,1180,75), 1)

            # Обновление введенного текста
            self.draw_text(self.screen, self.input_text, 387, 40,(255,255,255))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP: # Начало по нажатию в контейнер
                    x, y = pygame.mouse.get_pos()

                    # Положение контейнера ввода
                    if (x >= 50 and x <= 1230 and y >= 350 and y <= 425):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time()

                        # Положение контейнера кнопки
                    if (x >= 450 and x <= 800 and y >= 550 and self.end):
                        self.reset_game()
                        x, y = pygame.mouse.get_pos()

                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN: # Энтер - закончить
                            print(self.input_text)
                            self.show_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results,500, 40, self.RESULT_C)
                            self.end = True

                        elif event.key == pygame.K_BACKSPACE: # Бэкспейс -  стереть
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass

            pygame.display.update()

        clock.tick(60)

    def reset_game(self):
        self.screen.blit(self.open_img, (0,0))

        pygame.display.update()
        time.sleep(1)

        self.reset=False
        self.end = False

        self.input_text=''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        # Рандомное предложение
        self.word = self.get_sentence()
        if (not self.word): self.reset_game()

        # Заголовок
        self.screen.fill((0,0,0))
        self.screen.blit(self.bg,(0,0))
        msg = "Typing Speed Test in English"
        self.draw_text(self.screen, msg,200, 100,self.HEAD_C)

        # Предложение для написания
        self.draw_text(self.screen, self.word,300, 40,self.TEXT_C)

        pygame.display.update()



Game().run()

