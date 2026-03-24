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

MAX_BLOKKE = 5
font = pygame.font.SysFont(None, 36)


def start_game():
    tegelane_limusk = limusk.limusk(laius // 2, kõrgus - 15, laius, kõrgus)
    peategelane = pygame.sprite.Group()
    peategelane.add(tegelane_limusk)

    blokid = pygame.sprite.Group()
    spiked = pygame.sprite.Group()
    worldlocks = pygame.sprite.Group()

    skoor = 0
    suri = False
    järgmine_spike_skoor = 5  

    def spawn_worldlock():
        """Spawn worldlock tühjale alale"""
        worldlocks.empty()
        while True:
            x = random.randint(0, (laius // 50) - 1) * 50
            y = random.randint(0, ((kõrgus // 2) // 50) - 1) * 50
            temp_rect = pygame.Rect(x, y, 50, 50)
            if not temp_rect.colliderect(tegelane_limusk.rect) and all(not temp_rect.colliderect(b.rect) for b in blokid):
                break
        wl = worldlock.WorldLock(x, y)
        worldlocks.add(wl)

    def spawn_spikes(count=3):
        """Spawn spike'id tühjale alale"""
        spiked.empty()  
        for _ in range(count):
            while True:
                x = random.randint(0, (laius // 50) - 1) * 50
                y = random.randint(0, (kõrgus // 50) - 1) * 50
                temp_rect = pygame.Rect(x, y, 50, 50)
                if not temp_rect.colliderect(tegelane_limusk.rect) and all(not temp_rect.colliderect(b.rect) for b in blokid):
                    break
            uus_spike = spike.Spike(x, y)
            spiked.add(uus_spike)


    spawn_spikes()
    spawn_worldlock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x = (x // 50) * 50
                y = (y // 50) * 50

                if not suri:
                    if event.button == 3:  # lisa blokk
                        olemas = any(blokk.rect.topleft == (x, y) for blokk in blokid)
                        if not olemas and len(blokid) < MAX_BLOKKE:
                            uus_blokk = block.Block(x, y)
                            blokid.add(uus_blokk)

                    if event.button == 1:  # eemalda blokk
                        for blokk in blokid:
                            if blokk.rect.topleft == (x, y):
                                blokk.kill()
                else:
                    uuesti_rect = pygame.Rect(laius//2 - 100, kõrgus//2, 200, 50)
                    if uuesti_rect.collidepoint(event.pos):
                        return

        if not suri:
            peategelane.update(blokid)

            # WORLDLOCK kokkupõrge
            for tegelane in peategelane:
                hits = pygame.sprite.spritecollide(tegelane, worldlocks, True)
                if hits:
                    skoor += len(hits)
                    spawn_worldlock()

                    # Spike'id muutuvad iga worldlock kokkupuutega
                    spawn_spikes()

                    # Iga 5 skoori tagant lisatakse üks uus spike
                    if skoor >= järgmine_spike_skoor:
                        spawn_spikes(1)
                        järgmine_spike_skoor += 5

            # SPIKE kokkupõrge
            for tegelane in peategelane:
                if pygame.sprite.spritecollideany(tegelane, spiked):
                    suri = True 

        # DRAW
        aken.blit(taustapilt, (0, 0))
        blokid.draw(aken)
        spiked.draw(aken)
        worldlocks.draw(aken)
        peategelane.draw(aken)

    
        text = font.render(f"Skoor: {skoor}", True, (255, 20, 147))
        aken.blit(text, (10, 10))


        if suri:
            suri_text = pygame.font.SysFont(None, 48).render("Suri!", True, (255, 0, 0))
            uuesti_text = pygame.font.SysFont(None, 36).render("Mängi uuesti", True, (255, 255, 255))
            aken.blit(suri_text, (laius//2 - suri_text.get_width()//2, kõrgus//2 - 50))
            uuesti_rect = pygame.Rect(laius//2 - 100, kõrgus//2, 200, 50)
            pygame.draw.rect(aken, (0, 128, 0), uuesti_rect)
            aken.blit(uuesti_text, (uuesti_rect.x + 20, uuesti_rect.y + 10))

        clock.tick(60)
        pygame.display.flip()


def menu():
    font_big = pygame.font.SysFont(None, 60)
    font_small = pygame.font.SysFont(None, 36)
    while True:
        aken.blit(taustapilt, (0, 0))
        title = font_big.render("Growtopia", True, (0, 0, 0))
        start_text = font_small.render("Alusta mängu", True, (0, 0, 0))
        title_rect = title.get_rect(center=(laius // 2, kõrgus // 3))
        start_rect = start_text.get_rect(center=(laius // 2, kõrgus // 2))
        aken.blit(title, title_rect)
        aken.blit(start_text, start_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    return


menu()
while True:
    start_game()