import pygame
import random
import math

# --- Constantes de la Simulation ---
SCREEN_WIDTH = 1275
SCREEN_HEIGHT = 660
FPS = 60
NUMBER_OF_BOIDS = 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# --- Classe Boid ---
class Boid:
    def __init__(self, x, y):
        # Position (Liste [x, y])
        self.position = [x, y]
        
        # Vitesse (Liste [vx, vy]) : Aléatoire pour un démarrage dynamique
        self.velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]
        
        # Accélération (Liste [ax, ay]) : Initialisée à zéro
        self.acceleration = [0, 0]
        
        # Constantes
        self.max_speed = 4
        self.size = 5 # Taille pour le dessin
        
    def draw(self, screen):
        # Pour l'instant, dessinez un simple cercle (point)
        pygame.draw.circle(screen, WHITE, (int(self.position[0]), int(self.position[1])), self.size)

    def update(self, all_boids):
        # --- Mouvement de Base (Ignorant les règles de flocage pour l'instant) ---
        
        # 1. Mise à jour de la vitesse (V = V + A)
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        
        # 2. Limiter la vitesse (Pour éviter qu'il ne s'emballe)
        # Ceci est une version simplifiée, nous améliorerons la limite vectorielle plus tard.
        if math.hypot(self.velocity[0], self.velocity[1]) > self.max_speed:
            self.velocity = [v * self.max_speed / math.hypot(self.velocity[0], self.velocity[1]) 
                             for v in self.velocity]
        
        # 3. Mise à jour de la position (P = P + V)
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
        # 4. Gérer les bords de l'écran (Wrapping/Tore)
        self.check_edges()
        
        # Réinitialiser l'accélération pour l'étape suivante (important !)
        self.acceleration = [0, 0]


    def check_edges(self):
        # Vérification si le Boid sort par la droite/gauche
        if self.position[0] > SCREEN_WIDTH:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.position[0] = SCREEN_WIDTH
            
        # Vérification si le Boid sort par le bas/haut
        if self.position[1] > SCREEN_HEIGHT:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = SCREEN_HEIGHT

# --- Fonction principale ---
def main():
    # 1. Initialisation
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simulation de Boids")
    clock = pygame.time.Clock()

    # 2. Création des Boids
    boids = []
    for _ in range(NUMBER_OF_BOIDS):
        # Créer les boids à des positions aléatoires
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        boids.append(Boid(x, y))

    # 3. Boucle Principale du Jeu
    running = True
    while running:
        # --- A. Gérer les Entrées (Input) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- B. Mise à Jour de la Logique (Update) ---
        # Chaque boid calcule ses règles et met à jour sa position
        for boid in boids:
            boid.update(boids) # all_boids est nécessaire même si nous ne l'utilisons pas encore

        # --- C. Rendu Graphique (Draw) ---
        screen.fill(BLACK) # Effacer l'écran
        
        for boid in boids:
            boid.draw(screen) # Dessiner chaque boid
            
        pygame.display.flip() # Mettre à jour l'affichage
        
        # Gérer la fréquence d'images
        clock.tick(FPS) 

    pygame.quit()

if __name__ == '__main__':
    main()