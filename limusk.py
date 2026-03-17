import pygame

class limusk(pygame.sprite.Sprite):
    def __init__(self, x, y, laius, kõrgus):
        super().__init__()
        self.orig_image = pygame.image.load("limusk.png")
        self.image = pygame.transform.scale(self.orig_image, (70, 90))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        
        self.speed = 5
        self.laius = laius
        self.kõrgus = kõrgus
      
        self.velocity_y = 0
        self.gravity = 0.2
        self.jump_power = -6
        self.on_ground = True
        
        self.facing_right = True

    def update(self, blokid):
        keys = pygame.key.get_pressed()

        # -------- HORISONTAALNE LIIKUMINE --------
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
            if self.facing_right:
                self.facing_right = False
                self.image = pygame.transform.flip(
                    pygame.transform.scale(self.orig_image, (70, 90)),
                    True, False
                )

        if keys[pygame.K_RIGHT]:
            dx = self.speed
            if not self.facing_right:
                self.facing_right = True
                self.image = pygame.transform.scale(self.orig_image, (70, 90))

        self.rect.x += dx

        # Kokkupõrge külgedelt
        for blokk in blokid:
            if self.rect.colliderect(blokk.rect):
                if dx > 0:
                    self.rect.right = blokk.rect.left
                if dx < 0:
                    self.rect.left = blokk.rect.right

        # -------- HÜPPAMINE --------
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False

        # -------- GRAVITATSIOON --------
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Vertikaalne kokkupõrge
        self.on_ground = False
        for blokk in blokid:
            if self.rect.colliderect(blokk.rect):
                if self.velocity_y > 0:  # kukub alla
                    self.rect.bottom = blokk.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:  # liigub üles
                    self.rect.top = blokk.rect.bottom
                    self.velocity_y = 0

        # -------- PÕRAND --------
        if self.rect.bottom >= self.kõrgus:
            self.rect.bottom = self.kõrgus
            self.velocity_y = 0
            self.on_ground = True

        # -------- EKRAANI PIIRID --------
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.laius:
            self.rect.right = self.laius