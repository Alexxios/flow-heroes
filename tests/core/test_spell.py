# import unittest
#
# import pygame
#
# from entities.spells.projectile import FIREBALL
#
# class TestProjectileSpell(unittest.TestCase):
#     def test_fireball(self):
#         pygame.init()
#         screen = pygame.display.set_mode((800, 600))
#         clock = pygame.time.Clock()
#
#         spells = pygame.sprite.Group()
#         fireball = FIREBALL.create(spells, pos=(100, 100))
#
#         running = True
#         while running:
#             if fireball.rect.x > 800:
#                 fireball.kill()
#                 running = False
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
#
#             spells.draw(screen)
#             pygame.display.flip()
#
#             dt = clock.tick(60)
#             spells.update(dt=dt)
#             screen.fill((0, 0, 0))
#
#         pygame.quit()
#
#         assert fireball.SpellState.DEAD == fireball.fsm.state
#
# if __name__ == '__main__':
#     unittest.main()
