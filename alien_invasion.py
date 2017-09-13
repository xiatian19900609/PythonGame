import pygame
from setting import Setting
from ship import Ship
import game_function as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from score_board import ScoreBoard


def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    setting = Setting()
    screen = pygame.display.set_mode((setting.screen_width, setting.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 绘制一艘飞船
    ship = Ship(setting=setting, screen=screen)

    stats = GameStats(setting)

    # 创建得分
    score_board = ScoreBoard(screen, stats, setting)

    # 创建子弹编组
    bullets = Group()

    # 创建开始按钮
    button = Button(screen, "Play")
    # 创建外星人编组
    aliens = Group()
    gf.create_fleet(screen=screen, setting=setting, aliens=aliens)

    # 开始游戏主循环
    while True:
        # 监听事件
        gf.check_events(ship, bullets, screen, setting, button, stats, aliens)

        if stats.game_active:
            # 更新飞船状态
            ship.update()
            # 更新子弹
            gf.update_bullet(bullets, aliens, screen, setting, stats, score_board)
            # 更新外星人
            gf.update_aliens(aliens, setting, ship, stats, bullets, screen)

        # 更新屏幕
        gf.update_screen(setting, screen, ship, bullets, aliens, stats, button, score_board)


run_game()
