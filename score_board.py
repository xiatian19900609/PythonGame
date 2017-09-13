import pygame


class ScoreBoard():
    def __init__(self, screen, stats, setting):
        self.screen = screen
        self.stats = stats
        self.setting = setting
        self.screen_rect = screen.get_rect()

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()
        self.prep_high_score()

    def prep_score(self):
        """将得分放在屏幕右上角"""
        rounded_score = round(self.stats.score, -1)
        score = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score, True, self.text_color, self.setting.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高分放在屏幕上中央"""
        rounded_high_socre = round(self.stats.high_score)
        high_score = "{:,}".format(rounded_high_socre)
        self.high_score_image = self.font.render(high_score, True, self.text_color, self.setting.bg_color)
        self.high_socre_rect = self.high_score_image.get_rect()
        self.high_socre_rect.centerx = self.screen_rect.centerx
        self.high_socre_rect.top = self.score_rect.top

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_socre_rect)
