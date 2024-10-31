import pygame
import random
import sys

# Initialiser Pygame
pygame.init()

# Configuration de la fenêtre
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man avec fantômes en poursuite")

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 182, 193)

# Paramètres du labyrinthe
TILE_SIZE = 20
maze = [
    "11111111111111111111",
    "10000000000000000001",
    "10111110111110111101",
    "10000000000000000001",
    "10111110111110111101",
    "10000000000000000001",
    "11111111111111111111",
]

# Vitesse de déplacement
SPEED = 5

# Score initial et vies
score = 0
lives = 3  # Pac-Man commence avec 3 vies

# Classe pour Pac-Man
class PacMan:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.direction = pygame.Vector2(0, 0)

    def draw(self):
        pygame.draw.circle(screen, YELLOW, self.rect.center, TILE_SIZE // 2)

    def move(self):
        # Calcule la position prévue après déplacement
        new_rect = self.rect.move(self.direction.x * SPEED, self.direction.y * SPEED)
        if not check_collision_with_maze(new_rect):
            self.rect = new_rect

# Classe pour les Fantômes
class Ghost:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.direction = pygame.Vector2(0, 0)

    def draw(self):
        pygame.draw.circle(screen, RED, self.rect.center, TILE_SIZE // 2)

    def move(self, pacman_pos):
        # Calcul de la direction vers Pac-Man
        dx = pacman_pos[0] - self.rect.centerx
        dy = pacman_pos[1] - self.rect.centery

        # Normaliser la direction pour se diriger vers Pac-Man
        if dx != 0:
            self.direction.x = 1 if dx > 0 else -1
        if dy != 0:
            self.direction.y = 1 if dy > 0 else -1

        # Calculer la prochaine position et vérifier les collisions
        new_rect = self.rect.move(self.direction.x * SPEED, self.direction.y * SPEED)
        if not check_collision_with_maze(new_rect):
            self.rect = new_rect
        else:
            # Si collision, réinitialise la direction pour l'éviter
            self.direction = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))

# Fonction pour vérifier la collision avec les murs du labyrinthe
def check_collision_with_maze(rect):
    col = rect.centerx // TILE_SIZE
    row = rect.centery // TILE_SIZE
    if maze[row][col] == "1":
        return True
    return False

# Fonction pour vérifier la collision avec les fantômes
def check_collision_with_ghosts():
    for ghost in ghosts:
        if pacman.rect.colliderect(ghost.rect):
            return True
    return False

# Fonction pour dessiner le labyrinthe et les pac-gommes
def draw_maze():
    global score
    for row_index, row in enumerate(maze):
        for col_index, tile in enumerate(row):
            x, y = col_index * TILE_SIZE, row_index * TILE_SIZE
            if tile == "1":
                pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
            elif tile == "0":
                # Dessine une pac-gomme
                pygame.draw.circle(screen, PINK, (x + TILE_SIZE // 2, y + TILE_SIZE // 2), 4)
                # Collision avec les pac-gommes
                if pacman.rect.colliderect(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)):
                    maze[row_index] = maze[row_index][:col_index] + " " + maze[row_index][col_index+1:]
                    score += 10  # Ajoute des points

# Fonction pour afficher le score et les vies restantes
def display_score_and_lives():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))

# Fonction pour vérifier la condition de victoire
def check_victory():
    for row in maze:
        if "0" in row:  # Il reste des pac-gommes
            return False
    return True  # Toutes les pac-gommes sont ramassées

# Fonction pour afficher le message de victoire
def display_victory_message():
    font = pygame.font.Font(None, 48)
    victory_text = font.render("Victory!", True, WHITE)
    screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 2))

# Initialisation de Pac-Man et des fantômes
pacman = PacMan(TILE_SIZE + TILE_SIZE // 2, TILE_SIZE + TILE_SIZE // 2)
ghosts = [Ghost(TILE_SIZE * 15 + TILE_SIZE // 2, TILE_SIZE + TILE_SIZE // 2)]

# Boucle principale du jeu
running = True
victory = False
while running:
    screen.fill(BLACK)

    # Écoute des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman.direction = pygame.Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT:
                pacman.direction = pygame.Vector2(1, 0)
            elif event.key == pygame.K_UP:
                pacman.direction = pygame.Vector2(0, -1)
            elif event.key == pygame.K_DOWN:
                pacman.direction = pygame.Vector2(0, 1)

    # Dessiner le labyrinthe et les points
    draw_maze()

    # Mouvement de Pac-Man
    pacman.move()
    pacman.draw()

    # Mouvement et affichage des fantômes
    for ghost in ghosts:
        ghost.move(pacman.rect.center)  # Passe la position de Pac-Man pour le suivi
        ghost.draw()

    # Vérifier la collision avec les fantômes
    if check_collision_with_ghosts():
        lives -= 1
        pacman.rect.topleft = (TILE_SIZE + TILE_SIZE // 2, TILE_SIZE + TILE_SIZE // 2)  # Réinitialiser Pac-Man
        if lives <= 0:
            print("Game Over!")
            running = False

    # Vérifier la condition de victoire
    if check_victory():
        victory = True
        display_victory_message()
        pygame.display.flip()
        pygame.time.delay(2000)  # Attendre pour que le joueur voie le message de victoire
        running = False  # Fin du jeu

    display_score_and_lives()
    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
