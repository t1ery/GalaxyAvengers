import pygame, sys
from bullet import Bullet
from ufo import Ufo
import time


def events(screen, gun, bullets):
    """Обработка события"""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # вправо
            if event.key == pygame.K_d:
                gun.mright = True
            # влево
            elif event.key == pygame.K_a:
                gun.mleft = True
            elif event.key == pygame.K_SPACE:
                new_bullet = Bullet(screen, gun)
                bullets.add(new_bullet)
        elif event.type == pygame.KEYUP:
            # вправо
            if event.key == pygame.K_d:
                gun.mright = False
            # влево
            elif event.key == pygame.K_a:
                gun.mleft = False


def update(bg_color, screen, stats, sc, gun, ufos, bullets):
    """Обновление экрана"""
    screen.fill(bg_color)
    sc.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    gun.output()
    ufos.draw(screen)
    pygame.display.flip()


def update_bullets(screen, stats, sc, ufos, bullets):
    """Обновлять позиции пуль"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    collisions = pygame.sprite.groupcollide(bullets, ufos, True, True)
    if collisions:
        for ufos in collisions.values():
            stats.score += 10 * len(ufos)
        sc.image_score()
        check_high_score(stats, sc)
        sc.image_guns()
    if len(ufos) == 0:
        bullets.empty()
        create_army(screen, ufos)


def gun_kill(stats, screen, sc, gun, ufos, bullets):
    """Столкновение пушки с пришельцами"""
    if stats.guns_left > 0:
        stats.guns_left -= 1
        sc.image_guns()
        ufos.empty()
        bullets.empty()
        create_army(screen, ufos)
        gun.create_gun()
        time.sleep(1)
    else:
        stats.run_game = False
        sys.exit()


def update_ufos(stats, screen, sc, gun, ufos, bullets):
    '''Обновляет позицию пришельцев'''
    ufos.update()
    if pygame.sprite.spritecollideany(gun, ufos):
        gun_kill(stats, screen, sc, gun, ufos, bullets)
    ufos_check(stats, screen, sc, gun, ufos, bullets)


def ufos_check(stats, screen, sc, gun, ufos, bullets):
    '''Проверка, добралась ли армия до края экрана'''
    screen_rect = screen.get_rect()
    for ufo in ufos.sprites():
        if ufo.rect.bottom >= screen_rect.bottom:
            gun_kill(stats, screen, sc, gun, ufos, bullets)
            break


def create_army(screen, ufos):
    """Создание армии пришельцев"""
    ufo = Ufo(screen)
    ufo_width = ufo.rect.width
    number_ufo_x = int((700 - 2 * ufo_width) / ufo_width)
    ufo_height = ufo.rect.height
    number_ufo_y = int((800 - 100 - 2 * ufo_height) / ufo_height)

    for row_number in range(number_ufo_y - 8):
        for ufo_number in range(number_ufo_x):
            ufo = Ufo(screen)
            ufo.x = ufo_width + (ufo_width * ufo_number)
            ufo.y = ufo_height + (ufo_height * row_number)
            ufo.rect.x = ufo.x
            ufo.rect.y = ufo.rect.height + ufo.rect.height * row_number
            ufos.add(ufo)


def check_high_score(stats, sc):
    """Проверка новых рекордов"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sc.image_high_score()
        with open('high_score.txt', 'w') as f:
            f.write(str(stats.high_score))
