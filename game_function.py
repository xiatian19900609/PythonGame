import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(ship, bullets, screen, setting, play_button, stats, aliens):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            ckeck_keydown_event(event, ship, bullets, screen, setting)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_play_button(play_button, stats, aliens, bullets, ship, setting, screen)


def check_play_button(play_button, stats, aliens, bullets, ship, setting, screen):
    """响应鼠标点击Play按钮"""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        setting.initialize_dynamic_settings()
        # 清空外星人和子弹
        bullets.empty()
        aliens.empty()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        create_fleet(screen, setting, aliens)
        ship.center_ship()


def ckeck_keydown_event(event, ship, bullets, screen, setting):
    """响应按下的事件"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(bullets, setting, ship, screen)


def check_keyup_event(event, ship):
    """响应抬起的事件"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(setting, screen, ship, bullets, aliens, stats, play_button, score_board):
    """更新屏幕"""
    screen.fill(setting.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    if not stats.game_active:
        play_button.draw_button()
        stats.score = 0
        score_board.prep_score()

    score_board.show_score()
    check_high_score(stats, score_board)
    pygame.display.flip()


def update_bullet(bullets, aliens, screen, setting, stats, score_board):
    """更新子弹"""
    # 更新编组里的所有子弹
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(bullets, aliens, screen, setting, stats, score_board)


def check_bullet_alien_collisions(bullets, aliens, screen, setting, stats, score_board):
    """检测外星人和子弹碰撞"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        stats.score += setting.alien_point
        score_board.prep_score()

    if len(aliens) <= 0:
        # 删除现有的子弹，加快游戏节奏，并创建一群新的外星人
        bullets.empty()
        setting.increase_speed()
        create_fleet(screen, setting, aliens)


def fire_bullet(bullets, setting, ship, screen):
    """如果还没有到达限制 ,  就发射一颗子弹"""
    if len(bullets) < setting.bullet_allowed:
        new_bullet = Bullet(setting=setting, ship=ship, screen=screen)
        bullets.add(new_bullet)


def create_fleet(screen, setting, aliens):
    """创建外星人群"""
    # 外星人之间的间距为外星人的宽度
    alien = Alien(screen, setting)
    alien_width = alien.rect.width

    number_aliens_x = get_number_aliens_x(setting, alien_width)

    for number in range(setting.row_number):
        creat_alien(screen, setting, alien_width, aliens, number_aliens_x, number)


def get_number_aliens_x(setting, alien_width):
    """获取一行可以容纳外星人的个数"""
    available_space_x = setting.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def creat_alien(screen, setting, alien_width, aliens, aliens_number, row_number):
    """创建一行所能容纳的外星人"""
    for number in range(aliens_number):
        # 创建一个外星人并将其加入当前行
        alien = Alien(screen, setting)
        alien.x = alien_width + 2 * alien_width * number
        alien.rect.x = alien.x
        alien.rect.y = alien_width + 1.3 * alien.rect.height * row_number
        aliens.add(alien)


def update_aliens(aliens, setting, ship, stats, bullets, screen):
    """更新外星人"""
    check_fleet_edges(aliens, setting)
    aliens.update()

    # 检查是外星人和飞船是否相撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(stats, ship, aliens, bullets, screen, setting)
    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(screen, aliens, stats, ship, bullets, setting)


def ship_hit(stats, ship, aliens, bullets, screen, setting):
    """响应外星人撞到飞船"""
    if stats.ships_left > 0:
        stats.ships_left -= 1
        # 清空外星人和子弹
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人 , 并将飞船移到中央
        create_fleet(screen, setting, aliens)
        ship.center_ship()
        sleep(1)
    else:
        pygame.mouse.set_visible(True)
        stats.game_active = False


def check_fleet_edges(aliens, setting):
    """检测外星人是否触碰边缘"""
    for alien in aliens.sprites():
        if alien.check_adges():
            change_fleet_direction(aliens, setting)
            break


def change_fleet_direction(aliens, setting):
    """修改外星人方向"""
    # 将整群外星人下移,并改变它们方向
    for alien in aliens.sprites():
        alien.rect.y += setting.fleet_drop_sheed
    setting.fleet_direction *= -1


def check_aliens_bottom(screen, aliens, stats, ship, bullets, setting):
    """检测外星人是否触碰到底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(stats, ship, aliens, bullets, screen, setting)


def check_high_score(stats, score_board):
    """检测最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score_board.prep_high_score()
