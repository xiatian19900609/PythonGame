from pygame.sprite import Sprite
import pygame


class Bullet(Sprite):
    """一个对飞船发射的子弹进行管理的类"""

    def __init__(self, setting, screen, ship):
        """在飞船所处的位置创建一个子弹对象"""
        super(Bullet, self).__init__()
        self.screen = screen
        # 在(0,0)处创建一个表示子弹矩形 , 再设置正确位置
        self.rect = pygame.Rect(0, 0, setting.bullet_width, setting.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)
        self.color = setting.bullet_color
        self.sheed_factor = setting.bullet_sheed_factor

    def update(self):
        """子弹向上移动"""
        # 更新表示子弹位置的小数值
        self.y -= self.sheed_factor
        # 更新表示子弹的rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
