from pygame.sprite import Sprite
import pygame


class Alien(Sprite):
    def __init__(self, screen, setting):
        super(Alien, self).__init__()
        self.screen = screen
        self.setting = setting
        self.image = pygame.image.load('image/f2.bmp')
        self.rect = self.image.get_rect()

        # 外星人初始位置
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人准确位置
        self.x = float(self.rect.x)

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += self.setting.alien_sheed_factor * self.setting.fleet_direction
        self.rect.x = self.x

    def check_adges(self):
        """如果外星人位于屏幕边缘就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.width:
            return True
        elif self.rect.left <= 0:
            return True
