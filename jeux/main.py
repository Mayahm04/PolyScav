import pygame
import sys
import random
import math

# Initialisation
pygame.init()

# --- Constantes générales ---
WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (60, 60, 60)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Last Wave")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)

# --- Joueur ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 30
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.speed = 5
        self.ammo = 30  # Ressource limitée : munitions

    def update(self, keys):
        dx = dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = self.speed

        self.rect.x += dx
        self.rect.y += dy

        # Garder dans l'écran
        self.rect.x = max(0, min(WIDTH - self.size, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.size, self.rect.y))

    def shoot(self, target_pos, bullet_group, all_sprites):
        if self.ammo <= 0:
            return
        # Direction vers la souris
        start_pos = self.rect.center
        dir_x = target_pos[0] - start_pos[0]
        dir_y = target_pos[1] - start_pos[1]
        length = math.hypot(dir_x, dir_y)
        if length == 0:
            return
        dir_x /= length
        dir_y /= length
        bullet = Bullet(start_pos, (dir_x, dir_y))
        bullet_group.add(bullet)
        all_sprites.add(bullet)
        self.ammo -= 1

# --- Bullet ---
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.Surface((6, 6))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=pos)
        self.speed = 10
        self.dir_x, self.dir_y = direction

    def update(self, *_):
        self.rect.x += int(self.dir_x * self.speed)
        self.rect.y += int(self.dir_y * self.speed)
        # Sortie de l'écran → kill
        if (self.rect.right < 0 or self.rect.left > WIDTH or
                self.rect.bottom < 0 or self.rect.top > HEIGHT):
            self.kill()

# --- Ennemis de base ---
class EnemyBase(pygame.sprite.Sprite):
    def __init__(self, color, speed, hp=1):
        super().__init__()
        self.size = 30
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.hp = hp

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()

# Type 1 : Chaser (poursuit le joueur)
class ChaserEnemy(EnemyBase):
    def __init__(self):
        super().__init__(RED, speed=2)
        # Spawn sur un bord de l'écran
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            self.rect.center = (0, random.randint(0, HEIGHT))
        elif side == "right":
            self.rect.center = (WIDTH, random.randint(0, HEIGHT))
        elif side == "top":
            self.rect.center = (random.randint(0, WIDTH), 0)
        else:
            self.rect.center = (random.randint(0, WIDTH), HEIGHT)

    def update(self, player, *_):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        dx /= dist
        dy /= dist
        self.rect.x += int(dx * self.speed)
        self.rect.y += int(dy * self.speed)

# Type 2 : Patrouilleur horizontal
class PatrolEnemy(EnemyBase):
    def __init__(self):
        super().__init__(GREEN, speed=3)
        self.rect.center = (random.randint(50, WIDTH - 50),
                            random.randint(50, HEIGHT - 50))
        self.direction = random.choice([-1, 1])

    def update(self, *args):
        self.rect.x += self.direction * self.speed
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1

# --- Boss ---
class Boss(EnemyBase):
    def __init__(self):
        super().__init__(GREY, speed=2, hp=20)
        self.size = 80
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(GREY)
        self.rect = self.image.get_rect(center=(WIDTH // 2, 80))

    def update(self, player, *_):
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        dx /= dist
        dy /= dist
        self.rect.x += int(dx * self.speed)
        self.rect.y += int(dy * self.speed)

# --- Pickup de munitions ---
class AmmoPickup(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((200, 200, 50))
        self.rect = self.image.get_rect(center=pos)

# --- Fonction de reset du jeu ---
def create_new_game():
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    ammo_pickups = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    wave = 1
    score = 0
    boss = None
    boss_spawned = False
    enemies_to_spawn = 5
    return (player, all_sprites, enemies, bullets,
            ammo_pickups, wave, score, boss, boss_spawned, enemies_to_spawn)

# --- Boucle principale ---
def main():
    (player, all_sprites, enemies, bullets, ammo_pickups,
     wave, score, boss, boss_spawned, enemies_to_spawn) = create_new_game()

    game_over = False

    running = True
    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    player.shoot(mouse_pos, bullets, all_sprites)
            else:
                # Game over : restart avec R
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    (player, all_sprites, enemies, bullets, ammo_pickups,
                     wave, score, boss, boss_spawned,
                     enemies_to_spawn) = create_new_game()
                    game_over = False

        if not game_over:
            # --- Spawn ennemis si besoin ---
            if len(enemies) < enemies_to_spawn and not boss_spawned:
                # 50% de chance pour chaque type
                if random.random() < 0.5:
                    enemy = ChaserEnemy()
                else:
                    enemy = PatrolEnemy()
                enemies.add(enemy)
                all_sprites.add(enemy)

            # Spawn boss après quelques vagues
            if wave >= 3 and not boss_spawned:
                boss = Boss()
                enemies.add(boss)
                all_sprites.add(boss)
                boss_spawned = True

            # Chance de spawn un pickup de munitions
            if random.random() < 0.002 and len(ammo_pickups) < 3:
                pickup = AmmoPickup(
                    (random.randint(40, WIDTH - 40),
                     random.randint(40, HEIGHT - 40))
                )
                ammo_pickups.add(pickup)
                all_sprites.add(pickup)

            # --- Updates ---
            player.update(keys)

            for enemy in enemies:
                if isinstance(enemy, ChaserEnemy) or isinstance(enemy, Boss):
                    enemy.update(player)
                else:
                    enemy.update()

            bullets.update()

            # Collisions bullets ↔ ennemis
            hits = pygame.sprite.groupcollide(
                enemies, bullets, False, True
            )
            for enemy, bullet_list in hits.items():
                enemy.take_damage(len(bullet_list))
                if not enemy.alive():
                    score += 1

            # Collisions joueur ↔ ennemis
            if pygame.sprite.spritecollideany(player, enemies):
                game_over = True

            # Collisions joueur ↔ pickups
            pickups_hit = pygame.sprite.spritecollide(
                player, ammo_pickups, True
            )
            for _ in pickups_hit:
                player.ammo += 10

            # Progression : si assez d'ennemis tués → prochaine vague
            # (ici, simple : tous les X points)
            if score // 10 + 1 > wave and not boss_spawned:
                wave += 1
                enemies_to_spawn += 3  # + d'ennemis à chaque vague

            # Victoire si boss est mort
            if boss_spawned and (boss is None or not boss.alive()):
                game_over = True  # on pourrait aussi afficher "You Win"

        # --- Rendu ---
        screen.fill(BLACK)

        if not game_over:
            all_sprites.draw(screen)

            # HUD
            ammo_text = font.render(f"Ammo: {player.ammo}", True, WHITE)
            score_text = font.render(f"Score: {score}", True, WHITE)
            wave_text = font.render(f"Wave: {wave}", True, WHITE)
            screen.blit(ammo_text, (10, 10))
            screen.blit(score_text, (10, 40))
            screen.blit(wave_text, (10, 70))

            if boss_spawned:
                boss_hp = boss.hp if boss and boss.alive() else 0
                boss_text = font.render(f"Boss HP: {boss_hp}", True, RED)
                screen.blit(boss_text, (WIDTH - 200, 10))
        else:
            # Écran de game over
            game_over_text = font.render("Game Over", True, WHITE)
            restart_text = font.render(
                "Appuie sur R pour recommencer", True, WHITE
            )
            score_text = font.render(f"Score final: {score}", True, WHITE)
            rect1 = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
            rect2 = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
            rect3 = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            screen.blit(game_over_text, rect1)
            screen.blit(restart_text, rect2)
            screen.blit(score_text, rect3)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
