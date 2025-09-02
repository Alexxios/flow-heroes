import unittest

import pygame
from src.core.spell import ProjectileSpell, Animation, Vector2

class TestProjectileSpell(unittest.TestCase):
    def test_fireball(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()

        spells = pygame.sprite.Group()
        fireball = ProjectileSpell(
            animation=Animation(pygame.image.load("/Users/glotovaleksei/flow-heroes/assets/gamekit/10 Fire ball/Fire-ball.png")),
            name="fireball",
            dmg=10,
            pos=Vector2(0, 0),
            direction=Vector2(0.2, 0)
        )
        fireball.add(spells)

        running = True
        while running:
            if fireball.rect.x > 800:
                fireball.kill()
                running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            spells.draw(screen)
            pygame.display.flip()

            dt = clock.tick(60)
            spells.update(dt=dt)
            screen.fill((0, 0, 0))

        pygame.quit()

        assert fireball.SpellState.DEAD == fireball.fsm.state

if __name__ == '__main__':
    unittest.main()
