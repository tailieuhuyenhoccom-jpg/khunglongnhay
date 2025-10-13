import pygame
import random

# Cài đặt màn hình
WIDTH, HEIGHT = 1279, 673
GROUND_Y = 535

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dino Run')
clock = pygame.time.Clock()

# Lớp Khủng long
class Player:
    def __init__(self, x, y):
        img = pygame.image.load('assets/dino_cleaned.png').convert_alpha()
        img = pygame.transform.flip(pygame.transform.scale(img, (100, 100)), True, False)
        self.image = img
        self.rect = img.get_rect(midbottom=(x, y))
        mask_img = pygame.Surface((100, 100), pygame.SRCALPHA)
        reduced = pygame.transform.scale(img, (70, 90))
        mask_img.blit(reduced, ((100 - 70)//2, (100 - 90)//2))
        self.mask = pygame.mask.from_surface(mask_img)
        self.velocity_y = 0
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = -15
            self.is_jumping = True

    def update(self):
        self.velocity_y += 1
        self.rect.y += self.velocity_y
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.is_jumping = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Lớp Xương rồng
class Obstacle:
    def __init__(self):
        img = pygame.image.load('assets/cay_cleaned.png').convert_alpha()
        img = pygame.transform.scale(img, (100, 100))
        self.image = img
        self.rect = img.get_rect(midbottom=(WIDTH + 20, GROUND_Y))
        mask_img = pygame.Surface((100, 100), pygame.SRCALPHA)
        reduced = pygame.transform.scale(img, (60, 80))
        mask_img.blit(reduced, ((100 - 60)//2, (100 - 80)//2))
        self.mask = pygame.mask.from_surface(mask_img)
        self.passed = False

    def update(self):
        self.rect.x -= 8

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_off_screen(self):
        return self.rect.right < 0

# Lớp điểm số
class Score:
    def __init__(self):
        self.value = 0
        self.font = pygame.font.SysFont('consolas', 30)

    def draw(self, screen):
        text = self.font.render(f'Score: {self.value}', True, (0, 0, 0))
        screen.blit(text, (10, 10))

# Lớp Game
class Game:
    def __init__(self):
        self.bg = pygame.transform.scale(pygame.image.load('assets/Screenshot21-1920x1080-be60aaa26ed9ec18a3761dbef7591fae.png'), (WIDTH, HEIGHT))
        self.player = Player(100, GROUND_Y)
        self.score = Score()
        self.obstacles = []
        self.spawn_timer = 0
        self.running = True

    def reset(self):
        self.__init__()

    def spawn_obstacle(self):
        self.obstacles.append(Obstacle())

    def update(self):
        self.player.update()
        self.spawn_timer += 1
        if self.spawn_timer >= 90:
            self.spawn_obstacle()
            self.spawn_timer = 0

        for obs in self.obstacles:
            obs.update()
            if not obs.passed and obs.rect.centerx < self.player.rect.centerx:
                obs.passed = True
                self.score.value += 1
            offset = (obs.rect.x - self.player.rect.x, obs.rect.y - self.player.rect.y)
            if self.player.mask.overlap(obs.mask, offset):
                self.running = False

        self.obstacles = [obs for obs in self.obstacles if not obs.is_off_screen()]

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        for obs in self.obstacles:
            obs.draw(screen)
        self.player.draw(screen)
        self.score.draw(screen)

# Chạy game
def main():
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if game.running:
                    game.player.jump()
                else:
                    game.reset()

        if game.running:
            game.update()
        game.draw(screen)

        if not game.running:
            font = pygame.font.SysFont('consolas', 40)
            text = font.render('Game Over - Nhấn SPACE để chơi lại', True, (200, 0, 0))
            rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(text, rect)

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()