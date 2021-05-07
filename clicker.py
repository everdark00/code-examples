import pygame
import time


SCREEN_L = 1200
SCREEN_H = 800


class AutoCleaker:
    def __init__(self, value, worktime, cost, max_count):
        self.start_time = time.time()
        self.value = value
        self.worktime = worktime
        self.cost = cost
        self.max_count = max_count

    def give_coins(self, time):
        if int((time - self.start_time)) % self.worktime == 0:
            return self.value
        else:
            return 0


class Cleaker:
    def __init__(self):
        self.clicks = 0
        self.speed = 1

    def cleak(self):
        return self.speed


class Button:
    pos = (0, 0, 0, 0)

    def __init__(self, screen, position, color, text1, text2):
        self.pos = position
        pygame.draw.rect(screen, color, self.pos)
        font_obj = pygame.font.Font('freesansbold.ttf', 22)
        text1_surface_obj = font_obj.render(text1, True, (255, 255, 255), (0, 0, 122))
        text1_rect_obj = text1_surface_obj.get_rect()
        text1_rect_obj.center = (self.pos[0] + self.pos[2]//2, self.pos[1] + self.pos[3]//4)
        screen.blit(text1_surface_obj, text1_rect_obj)
        text2_surface_obj = font_obj.render(text2, True, (255, 255, 255), (0, 0, 122))
        text2_rect_obj = text2_surface_obj.get_rect()
        text2_rect_obj.center = (self.pos[0] + self.pos[2]//2, self.pos[1] + 3*self.pos[3]//4)
        screen.blit(text2_surface_obj, text2_rect_obj)

    def on_button(self, position):
        if self.pos[0] < position[0] < self.pos[0] + self.pos[2] and self.pos[1] < position[1] < self.pos[1] + self.pos[3]:
            return True
        else:
            return False


class MainButton(Button):
    pos = (0, 0)
    rad = 0

    def __init__(self, screen, c_pos, color, text):
        self.pos = c_pos
        self.rad = 150
        self.Cleaker = Cleaker()
        pygame.draw.circle(screen, color, c_pos, 150, 0)
        font_obj = pygame.font.Font('freesansbold.ttf', 22)
        text_surface_obj = font_obj.render(text, True, (255, 255, 255), (0, 0, 122))
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.center = (c_pos[0], c_pos[1])
        screen.blit(text_surface_obj, text_rect_obj)

    def push(self):
        return self.Cleaker.cleak

    def on_button(self, position):
        if (position[0] - self.pos[0])**2 + (position[1] - self.pos[1]) ** 2 < 150 ** 2:
            return True
        else:
            return False

    def type(self):
        return "main_button"


class MiniCleakerButton(Button):
    def push(self, balance):
        bought_cleaker = AutoCleaker(1, 1, 10, 100)
        if bought_cleaker.cost <= balance:
            balance -= bought_cleaker.cost
            return (bought_cleaker, balance)
        else:
            return None

    def type(self):
        return "shop_button"


class MidCleakerButton(Button):
    def push(self, balance):
        bought_cleaker = AutoCleaker(5, 1, 100, 80)
        if bought_cleaker.cost <= balance:
            balance -= bought_cleaker.cost
            return (bought_cleaker, balance)
        else:
            return None

    def type(self):
        return "shop_button"


class BigCleakerButton(Button):
    def push(self, balance):
        bought_cleaker = AutoCleaker(100, 5, 1000, 50)
        if bought_cleaker.cost <= balance:
            balance -= bought_cleaker.cost
            return (bought_cleaker, balance)
        else:
            return None

    def type(self):
        return "shop_button"


class HugeCleakerButton(Button):
    def push(self, balance):
        bought_cleaker = AutoCleaker(500, 10, 2000, 40)
        if bought_cleaker.cost <= balance:
            balance -= bought_cleaker.cost
            return (bought_cleaker, balance)
        else:
            return None

    def type(self):
        return "shop_button"


class MegaCleakerButton(Button):
    def push(self, balance):
        bought_cleaker = AutoCleaker(800, 2, 10000, 20)
        if bought_cleaker.cost <= balance:
            balance -= bought_cleaker.cost
            return (bought_cleaker, balance)
        else:
            return None

    def type(self):
        return "shop_button"


class UltraCleakerButton(Button):
    def push(self, balance):
        bought_cleaker = AutoCleaker(1000, 1, 30000, 10)
        if bought_cleaker.cost <= balance:
            balance -= bought_cleaker.cost
            return (bought_cleaker, balance)
        else:
            return None

    def type(self):
        return "shop_button"


class Label:
    dynamic_info = 0

    def __init__(self, screen, label_color, text_color, static_text, dynamic_text, pos):
        self.info = int(dynamic_text[0])
        self.Pos = pos
        self.label_color = label_color
        self.text_color = text_color
        pygame.draw.rect(screen, self.label_color, pos)
        self.font_obj = pygame.font.Font('freesansbold.ttf', 22)
        static_text_surface_obj = self.font_obj.render(static_text, True, self.text_color, self.label_color)
        static_text_rect_obj = static_text_surface_obj.get_rect()
        static_text_rect_obj.center = (pos[0] + pos[2] // 3, pos[1] + pos[3] // 2)
        screen.blit(static_text_surface_obj, static_text_rect_obj)
        self.dynamic_text_surface_obj = self.font_obj.render(dynamic_text, True, self.text_color, self.label_color)
        self.dynamic_text_rect_obj = self.dynamic_text_surface_obj.get_rect()
        self.dynamic_text_rect_obj.center = (pos[0] + 3 * pos[2] // 4, pos[1] + pos[3] // 2)
        screen.blit(self.dynamic_text_surface_obj, self.dynamic_text_rect_obj)

    def update(self, screen, new_text):
        pygame.draw.rect(screen, self.label_color, (self.Pos[0]+7*self.Pos[2] // 12, self.Pos[1], self.Pos[2] // 3, self.Pos[3]))
        self.dynamic_text_surface_obj = self.font_obj.render(new_text, True, self.text_color, self.label_color)
        self.dynamic_text_rect_obj = self.dynamic_text_surface_obj.get_rect()
        self.dynamic_text_rect_obj.center = (self.Pos[0] + 3 * self.Pos[2] // 4, self.Pos[1] + self.Pos[3] // 2)
        screen.blit(self.dynamic_text_surface_obj, self.dynamic_text_rect_obj)


class WarningLabel:
    warning_time = 0

    def __init__(self, screen, label_color, text_color, position):
        self.screen = screen
        self.label_color = label_color
        self.text_color = text_color
        self.pos = position
        self.font_obj = pygame.font.Font('freesansbold.ttf', 22)
        pygame.draw.rect(self.screen, self.label_color, self.pos)

    def warn(self, text):
        pygame.draw.rect(self.screen, self.label_color, self.pos)
        self.warning_time = time.time()
        static_text_surface_obj = self.font_obj.render(text, True, self.text_color, self.label_color)
        static_text_rect_obj = static_text_surface_obj.get_rect()
        static_text_rect_obj.center = (self.pos[0] + self.pos[2] // 2, self.pos[1] + self.pos[3] // 2)
        self.screen.blit(static_text_surface_obj, static_text_rect_obj)

    def remove_warn(self):
        if time.time() - self.warning_time > 3:
            pygame.draw.rect(self.screen, self.label_color, self.pos)


class GameSession:
    Cleaker = Cleaker()
    Auto_cleakers = []
    Buttons = []
    Buttons_and_labels = {}
    balance = 0
    sys_start_time = 0

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_L, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.FPS = 10

    def set(self):
        background = pygame.image.load('background.jpg')
        self.screen.blit(background, [0, 0])
        Main_button = MainButton(self.screen, (250, SCREEN_H // 2), (0, 0, 122), "Cleak here!")
        first_shop_button = MiniCleakerButton(self.screen, (5*SCREEN_L // 7, 4*SCREEN_H // 30, 250, 100), (0, 0, 122), "Mini-cleaker 10$", "1$ / sec")
        second_shop_button = MidCleakerButton(self.screen, (5*SCREEN_L // 7, 8*SCREEN_H // 30, 250, 100), (0, 0, 122), "Mid cleaker 100$", "10$ / sec")
        third_shop_button = BigCleakerButton(self.screen, (5*SCREEN_L // 7, 12*SCREEN_H // 30, 250, 100), (0, 0, 122), "Big cleaker 1000$", "100$ / 5 sec")
        fourth_shop_button = HugeCleakerButton(self.screen, (5*SCREEN_L // 7, 16*SCREEN_H // 30, 250, 100), (0, 0, 122), "Huge cleaker 2000$", "500$ / 10 sec")
        fifth_shop_button = MegaCleakerButton(self.screen, (5*SCREEN_L // 7, 20*SCREEN_H // 30, 250, 100), (0, 0, 122), "Mega cleaker 10000$", "800$ / 5 sec")
        sixth_shop_button = UltraCleakerButton(self.screen, (5*SCREEN_L // 7, 24*SCREEN_H // 30, 250, 100), (0, 0, 122), "Ultra cleaker 30000$", "1000$ / sec")
        self.warns = WarningLabel(self.screen, (255, 255, 255), (255, 0, 0), (SCREEN_L // 2, 10, 505, 70))
        self.stat_label = Label(self.screen, (255, 255, 255), (0, 0, 0), "Click number:", str(self.balance), (10, 10, 350, 70))
        bought_label_1_u = Label(self.screen, (255, 255, 255), (0, 0, 0), "Bought:", "0", (SCREEN_L // 2, 8 * SCREEN_H // 60, 250, 50))
        bought_label_1_d = Label(self.screen, (255, 255, 255), (0, 0, 0), "Mines:", "0 p/s", (SCREEN_L // 2, 11 * SCREEN_H // 60, 250, 59))
        bought_label_2_u = Label(self.screen, (255, 255, 255), (0, 0, 0), "Bought:", "0", (SCREEN_L // 2, 16*SCREEN_H // 60, 250, 50))
        bought_label_2_d = Label(self.screen, (255, 255, 255), (0, 0, 0), "Mines:", "0 p/s", (SCREEN_L // 2, 19 * SCREEN_H // 60, 250, 59))
        bought_label_3_u = Label(self.screen, (255, 255, 255), (0, 0, 0), "Bought:", "0", (SCREEN_L // 2, 24 * SCREEN_H // 60, 250, 50))
        bought_label_3_d = Label(self.screen, (255, 255, 255), (0, 0, 0), "Mines:", "0 p/s", (SCREEN_L // 2, 27 * SCREEN_H // 60, 250, 59))
        bought_label_4_u = Label(self.screen, (255, 255, 255), (0, 0, 0), "Bought:", "0", (SCREEN_L // 2, 32*SCREEN_H // 60, 250, 50))
        bought_label_4_d = Label(self.screen, (255, 255, 255), (0, 0, 0), "Mines:", "0 p/s", (SCREEN_L // 2, 35 * SCREEN_H // 60, 250, 59))
        bought_label_5_u = Label(self.screen, (255, 255, 255), (0, 0, 0), "Bought:", "0", (SCREEN_L // 2, 40 * SCREEN_H // 60, 250, 50))
        bought_label_5_d = Label(self.screen, (255, 255, 255), (0, 0, 0), "Mines:", "0 p/s", (SCREEN_L // 2, 43 * SCREEN_H // 60, 250, 59))
        bought_label_6_u = Label(self.screen, (255, 255, 255), (0, 0, 0), "Bought:", "0", (SCREEN_L // 2, 48*SCREEN_H // 60, 250, 50))
        bought_label_6_d = Label(self.screen, (255, 255, 255), (0, 0, 0), "Mines:", "0 p/s", (SCREEN_L // 2, 51 * SCREEN_H // 60, 250, 59))
        pygame.display.update()
        self.Buttons_and_labels = {Main_button: self.stat_label, first_shop_button: (bought_label_1_u, bought_label_1_d), second_shop_button: (bought_label_2_u, bought_label_2_d), third_shop_button: (bought_label_3_u, bought_label_3_d),
                                   fourth_shop_button: (bought_label_4_u, bought_label_4_d), fifth_shop_button: (bought_label_5_u, bought_label_5_d), sixth_shop_button: (bought_label_6_u, bought_label_6_d)}
        self.Buttons = self.Buttons_and_labels.keys()

    def game(self):
        self.sys_start_time = time.time()
        tick = 0
        while True:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = event.pos
                        for button in self.Buttons:
                            if button.on_button(pos) and button.type() == "main_button":
                                self.balance += self.Cleaker.cleak()
                                self.stat_label.update(self.screen, str(self.balance))
                            elif button.on_button(pos) and button.type() == "shop_button":
                                bought_cleaker = button.push(self.balance)
                                if bought_cleaker is None:
                                    self.warns.warn("You have not got enough money!")
                                elif self.Buttons_and_labels[button][0].dynamic_info > bought_cleaker[0].max_count - 1:
                                    self.warns.warn("You have too much auto-cleakers!")
                                else:
                                    self.balance = bought_cleaker[1]
                                    self.Auto_cleakers.append(bought_cleaker[0])
                                    self.Buttons_and_labels[button][0].dynamic_info += 1
                                    self.Buttons_and_labels[button][0].update(self.screen, str(self.Buttons_and_labels[button][0].dynamic_info))
                                    self.Buttons_and_labels[button][1].update(self.screen, str(self.Buttons_and_labels[button][0].dynamic_info * bought_cleaker[0].value/bought_cleaker[0].worktime) + "p/s")
                if event.type == pygame.QUIT:
                    quit()
            if tick == 10:
                for cleaker in self.Auto_cleakers:
                    self.balance += cleaker.give_coins(time.time())
                    self.stat_label.update(self.screen, str(self.balance))
                tick = 0
            self.warns.remove_warn()
            tick += 1
            pygame.display.update()


GS = GameSession()
GS.set()
GS.game()
