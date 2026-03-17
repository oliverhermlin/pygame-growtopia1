import pygame
import limusk
import block
import os
import random
import spike
import worldlock

pygame.init()

laius = 630
kõrgus = 422
aken = pygame.display.set_mode((laius, kõrgus))
pygame.display.set_caption("Growtopia")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

taustapilt = pygame.image.load("mouteverest.jpg")
clock = pygame.time.Clock()

tegelane_limusk = limusk.limusk(laius // 2, kõrgus - 15, laius, kõrgus)

peategelane = pygame.sprite.Group()
peategelane.add(tegelane_limusk)

# blokkide group
blokid = pygame.sprite.Group()
spiked = pygame.sprite.Group()
worldlocks = pygame.sprite.Group()

# ✅ SPIKEDE GENERATION (AINULT 1 KORD!)
for i in range(3):
    x = random.randint(0, (laius // 50) - 1) * 50
    y = random.randint(0, (kõrgus // 50) - 1) * 50

    uus_spike = spike.Spike(x, y)
    spiked.add(uus_spike)
for i in range(5):
    x = random.randint(0, (laius // 50) - 1) * 50
    y = random.randint(0, (kõrgus // 2) - 1) * 50  # ainult ülemine pool

    wl = worldlock.WorldLock(x, y)
    worldlocks.add(wl)
    
    skoor = 0
    font = pygame.font.SysFont(None, 36)

käib = True
while käib:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            käib = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            # BLOKI LISAMINE (parem klikk)
            MAX_BLOKKE = 5
            if event.button == 3:
                if len(blokid) < MAX_BLOKKE:
                  x, y = pygame.mouse.get_pos()

                x = (x // 50) * 50
                y = (y // 50) * 50
           
       
                uus_blokk = block.Block(x, y)
                blokid.add(uus_blokk)

            # BLOKI EEMALDAMINE (vasak klikk)
                for tegelane in peategelane:
                  hits = pygame.sprite.spritecollide(tegelane, worldlocks, True)
                  if hits:
                     skoor += len(hits)

            if event.button == 1:
                x, y = pygame.mouse.get_pos()

                x = (x // 50) * 50
                y = (y // 50) * 50

                for blokk in blokid:
                    if blokk.rect.x == x and blokk.rect.y == y:
                        blokk.kill()

    # UPDATE
    peategelane.update(blokid)

  

    # 💀 SPIKE COLLISION
    for tegelane in peategelane:
        if pygame.sprite.spritecollideany(tegelane, spiked):
            tegelane.rect.centerx = laius // 2
            tegelane.rect.bottom = kõrgus
            tegelane.velocity_y = 0

    # DRAW
    aken.blit(taustapilt, (0, 0))

    blokid.draw(aken)
    spiked.draw(aken)
    worldlocks.draw(aken)  # worldlockide draw enne tegelast
    peategelane.draw(aken)

    text = font.render(f"Skoor: {skoor}", True, (255, 255, 255))
    aken.blit(text, (10, 10))
    clock.tick(60)
    pygame.display.flip()

pygame.quit()