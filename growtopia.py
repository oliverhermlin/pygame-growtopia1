import pygame
import limusk
import block
import os

pygame.init()

laius = 630
kõrgus = 422
aken = pygame.display.set_mode((laius,kõrgus))
pygame.display.set_caption("Growtopia")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

taustapilt = pygame.image.load("mouteverest.jpg")
clock = pygame.time.Clock()

tegelane_limusk = limusk.limusk(laius // 2, kõrgus - 15, laius, kõrgus)

peategelane = pygame.sprite.Group()
peategelane.add(tegelane_limusk)

# blokkide group
blokid = pygame.sprite.Group()

käib = True
while käib:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            käib = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            # BLOKI LISAMINE (parem klikk)
            if event.button == 3:
                x, y = pygame.mouse.get_pos()

                x = (x // 50) * 50
                y = (y // 50) * 50

                uus_blokk = block.Block(x, y)
                blokid.add(uus_blokk)

            # BLOKI EEMALDAMINE (vasak klikk)
            if event.button == 1:
                x, y = pygame.mouse.get_pos()

                x = (x // 50) * 50
                y = (y // 50) * 50

                for blokk in blokid:
                    if blokk.rect.x == x and blokk.rect.y == y:
                        blokk.kill()

    peategelane.update()

    aken.blit(taustapilt, (0, 0))

    blokid.draw(aken)
    peategelane.draw(aken)

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
