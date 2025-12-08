import random
import pygame
import affichage 
from logique import Boid 
# Importe SpatialGrid depuis utils
from utils import SpatialGrid 

# ----------------------------------------------------------------------
# --- PARAMÈTRES ET PATCHING ---
# ----------------------------------------------------------------------
# Augmentons à 1000 pour tester l'optimisation
affichage.NUMBER_OF_BOIDS = 10
affichage.Boid = Boid

# Définir la taille de la cellule de la grille. Elle doit être >= au rayon max de perception (50.0).
CELL_SIZE = 50 

def patched_main():
    
    # 1. Initialisation
    pygame.init()
    screen = pygame.display.set_mode((affichage.SCREEN_WIDTH, affichage.SCREEN_HEIGHT))
    pygame.display.set_caption(f"Simulation de {affichage.NUMBER_OF_BOIDS} Boids (Optimisé O(N))")
    clock = pygame.time.Clock()

    # INITIALISATION DE LA GRILLE SPATIALE
    spatial_grid = SpatialGrid(
        affichage.SCREEN_WIDTH, 
        affichage.SCREEN_HEIGHT, 
        CELL_SIZE
    )

    # 2. Création des Boids
    boids = []
    for _ in range(affichage.NUMBER_OF_BOIDS):
        x = random.randint(0, affichage.SCREEN_WIDTH)
        y = random.randint(0, affichage.SCREEN_HEIGHT)
        boids.append(affichage.Boid(x, y)) 

    # 3. Boucle Principale du Jeu
    running = True
    while running:
        # ... (Gestion des Entrées inchangée)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- A. LOGIQUE D'OPTIMISATION DE LA GRILLE ---
        spatial_grid.reset()
        for boid in boids:
            spatial_grid.add_boid(boid) # Tous les Boids sont placés dans la bonne cellule

        # --- B. Mise à Jour de la Logique (Update) ---
        for boid in boids:
            # Récupérer UNIQUEMENT les voisins locaux
            neighbors = spatial_grid.get_neighbors(boid) 
            
            # Appel la méthode update avec la liste restreinte de voisins
            boid.update(neighbors, affichage.SCREEN_WIDTH, affichage.SCREEN_HEIGHT) 

        # --- C. Rendu Graphique (Draw) ---
        screen.fill(affichage.BLACK) 
        
        for boid in boids:
            boid.draw(screen, affichage.WHITE) 
            
        pygame.display.flip() 
        clock.tick(affichage.FPS) 

    pygame.quit()

if __name__ == '__main__':
    patched_main()