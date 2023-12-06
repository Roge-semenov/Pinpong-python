import pygame
import sys
import asyncio
import random


# Инициализация Pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()

# Глобальные переменные
bg_menu_color = (208, 242, 97)
game_font = pygame.font.Font("freesansbold.ttf", 42)
menu_font = pygame.font.Font("freesansbold.ttf", 62)
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

class MainMenu:
    def __init__(self):
        self.ball_speed_x = 5
        self.ball_speed_y = 5
        self.player_score = 0
        self.opponent_score = 0
        self.score_time = None
        self.ball_speed_coef = 5
        self.player_speed = 0
        self.opponent_speed = 5
        self.click = False

    async def show(self):
        while True:
            screen.fill(bg_menu_color)
            self.draw_text('Главное меню', menu_font, (121, 69, 214), 450, 110)
            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(430, 258, 300, 80)
            button_2 = pygame.Rect(430, 450, 750, 80)

            if button_1.collidepoint((mx, my)) and self.click:
                game_start = Game()
                await game_start.play()
                await Game.play()
            if button_2.collidepoint((mx, my)) and self.click:
                await self.difficulty()

            pygame.draw.rect(screen, (237, 59, 131), button_1)
            pygame.draw.rect(screen, (237, 59, 131), button_2)

            self.draw_text('ИГРАТЬ', menu_font, (78, 19, 129), 450, 270)
            self.draw_text('УСТАНОВ. СЛОЖН.', menu_font, (78, 19, 129), 450, 462)
            difficulty_text = game_font.render(f"тек. сложн.{self.ball_speed_coef}", 1, (78, 19, 129))
            screen.blit(difficulty_text, (450, 670))

            self.click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.click = True

            pygame.display.update()
            clock.tick(60)
            await asyncio.sleep(0)

    def draw_text(self, text, font, color, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y)
        screen.blit(text_obj, text_rect)

    async def difficulty(self):
        while True:
            screen.fill(bg_menu_color)
            self.draw_text('Настройки сложности', menu_font, (121, 69, 214), 450, 110)

            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(430, 258, 300, 80)
            button_2 = pygame.Rect(430, 450, 300, 80)
            button_3 = pygame.Rect(430, 650, 300, 80)
            button_4 = pygame.Rect(430, 850, 300, 80)

            if button_1.collidepoint((mx, my)) and self.click:
                self.ball_speed_coef = 5
            if button_2.collidepoint((mx, my)) and self.click:
                self.ball_speed_coef = 12
            if button_3.collidepoint((mx, my)) and self.click:
                self.ball_speed_coef = 20
            if button_4.collidepoint((mx, my)) and self.click:
                await self.show()  # Возвращение в главное меню

            self.ball_speed_x = self.ball_speed_coef * random.choice((1, -1))
            self.ball_speed_y = self.ball_speed_coef * random.choice((1, -1))

            pygame.draw.rect(screen, (237, 59, 131), button_1)
            pygame.draw.rect(screen, (237, 59, 131), button_2)
            pygame.draw.rect(screen, (237, 59, 131), button_3)
            pygame.draw.rect(screen, (237, 59, 131), button_4)

            self.draw_text('Легко', menu_font, (78, 19, 129), 450, 270)
            self.draw_text('Средне', menu_font, (78, 19, 129), 450, 462)
            self.draw_text('Сложно', menu_font, (78, 19, 129), 450, 662)
            self.draw_text('Выйти', menu_font, (78, 19, 129), 450, 862)

            self.click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.click = True

            pygame.display.update()
            clock.tick(60)
            await asyncio.sleep(0)

class Game(MainMenu):
    def __init__(self):
        super().__init__()
        self.light_grey = (200, 200, 200)
        self.bg_color = pygame.Color('grey12')
        self.player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
        self.opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)
        self.ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)

    async def play(self):
        while True:
            # Обработка пользовательских событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.player_speed += 9
                    if event.key == pygame.K_UP:
                        self.player_speed -= 9
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        self.player_speed -= 9
                    if event.key == pygame.K_UP:
                        self.player_speed += 9
            
            # Игровая логика
            await self.ball_animation()
            self.player_animation()
            self.opponent_ai()
            
            # Отображение игровых объектов
            screen.fill(self.bg_color)
            pygame.draw.rect(screen, self.light_grey, self.player)
            pygame.draw.rect(screen, self.light_grey, self.opponent)
            pygame.draw.ellipse(screen, self.light_grey, self.ball)
            pygame.draw.aaline(screen, self.light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

            #Игровой счет
            if self.score_time:
                self.ball_restart()
            player_text = game_font.render(f"{self.player_score}", True, self.light_grey)
            screen.blit(player_text, (660, 470))

            opponent_text = game_font.render(f"{self.opponent_score}", True, self.light_grey)
            screen.blit(opponent_text, (600, 470))

            pygame.display.flip()
            clock.tick(60)

            await asyncio.sleep(0)

    async def ball_animation(self):
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        # Изменение траектории при достижении границ
        if self.ball.top <= 0 or self.ball.bottom >= screen_height:
            pygame.mixer.Sound.play(pong_sound)
            self.ball_speed_y *= -1

        # Очки игрока
        if self.ball.left <= 0:
            pygame.mixer.Sound.play(score_sound)
            self.player_score += 1
            self.score_time = pygame.time.get_ticks()

        # Очки оппонента
        if self.ball.right >= screen_width:
            pygame.mixer.Sound.play(score_sound)
            self.opponent_score += 1
            self.score_time = pygame.time.get_ticks()

        # Проверка условия победы и переход к экрану победы
        if self.opponent_score >= 3 or self.player_score >= 3:
            await self.win_screen()

        # Коллизия игрока
        if self.ball.colliderect(self.player) and self.ball_speed_x > 0:
            pygame.mixer.Sound.play(pong_sound)
            if abs(self.ball.right - self.player.left) < 10:
                self.ball_speed_x *= -1
            elif abs(self.ball.bottom - self.player.top) < 10 and self.ball_speed_y > 0:
                self.ball_speed_y *= -1
            elif abs(self.ball.top - self.player.bottom) < 10 and self.ball_speed_y < 0:
                self.ball_speed_y *= -1

        # Коллизия оппонента
        if self.ball.colliderect(self.opponent) and self.ball_speed_x < 0:
            pygame.mixer.Sound.play(pong_sound)
            if abs(self.ball.left - self.opponent.right) < 10:
                self.ball_speed_x *= -1
            elif abs(self.ball.bottom - self.opponent.top) < 10 and self.ball_speed_y > 0:
                self.ball_speed_y *= -1
            elif abs(self.ball.top - self.opponent.bottom) < 10 and self.ball_speed_y < 0:
                self.ball_speed_y *= -1

    def player_animation(self):
        self.player.y += self.player_speed
        # Ограничение движения ракетки игрока
        if self.player.top <= 0:
            self.player.top = 0
        if self.player.bottom >= screen_height:
            self.player.bottom = screen_height

    def opponent_ai(self):
        # Алгоритм перемещения ракетки противника
        if self.opponent.top < self.ball.y:
            self.opponent.top += self.opponent_speed
        if self.opponent.bottom > self.ball.y:
            self.opponent.bottom -= self.opponent_speed

        # Ограничение движения ракетки оппонента
        if self.opponent.top <= 0:
            self.opponent.top = 0
        if self.opponent.bottom >= screen_height:
            self.opponent.bottom = screen_height

    def ball_restart(self):
        current_time = pygame.time.get_ticks()
        self.ball.center = (screen_width / 2, screen_height / 2)

        # Отсчет времени перед перезапуском мяча
        if current_time - self.score_time < 700:
            number_three = game_font.render("3", False, self.light_grey)
            screen.blit(number_three, (screen_width / 2 - 10, screen_height / 2 + 20))
        if 700 < current_time - self.score_time < 1400:
            number_two = game_font.render("2", False, self.light_grey)
            screen.blit(number_two, (screen_width / 2 - 10, screen_height / 2 + 20))
        if 1400 < current_time - self.score_time < 2100:
            number_one = game_font.render("1", False, self.light_grey)
            screen.blit(number_one, (screen_width / 2 - 10, screen_height / 2 + 20))

        # Условие для перезапуска мяча
        if current_time - self.score_time < 2100:
            self.ball_speed_x, self.ball_speed_y = 0, 0
        else:
            self.ball_speed_y = self.ball_speed_coef * random.choice((1, -1))
            self.ball_speed_x = self.ball_speed_coef * random.choice((1, -1))
            self.score_time = None

    async def win_screen(self):
        while True:
            screen.fill(bg_menu_color)
            if self.player_score < self.opponent_score:
                win_text = game_font.render(f"Компьютер победил со счетом {self.opponent_score}:{self.player_score}", True, (78, 19, 129))
                screen.blit(win_text, (150, 110))
            else:
                win_text = game_font.render(f"Ты победил со счетом {self.player_score}:{self.opponent_score}", True, (78, 19, 129))
                screen.blit(win_text, (150, 110))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
            clock.tick(60)
            await asyncio.sleep(0)

async def main():
    main_menu = MainMenu()
    await main_menu.show()

asyncio.run(main())