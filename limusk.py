import pygame

class limusk(pygame.sprite.Sprite):
    def __init__(self, x, y, laius, kõrgus):
        super().__init__()
        self.orig_image = pygame.image.load("limusk.png")  # originaalpilt
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
        
        self.facing_right = True  # alguses vaatab paremale

    def update(self):
        keys = pygame.key.get_pressed()
        
        # Vasak / parem liikumine
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.facing_right:  # kui praegu vaatab paremale
                self.facing_right = False
                self.image = pygame.transform.flip(
                    pygame.transform.scale(self.orig_image, (70, 90)),
                    True, False
                )

        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if not self.facing_right:  # kui praegu vaatab vasakule
                self.facing_right = True
                # Flipime tagasi originaalpildile (horisontaalne False)
                self.image = pygame.transform.scale(self.orig_image, (70, 90))

        # Hüppamine
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False

        # Gravitatsioon
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Põrand
        if self.rect.bottom >= self.kõrgus:
            self.rect.bottom = self.kõrgus
            self.velocity_y = 0
            self.on_ground = True

        # Ekraani piirid
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.laius:
            self.rect.right = self.laius