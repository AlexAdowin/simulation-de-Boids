# Fichier: main.py
import pygame
import random
import affichage # Importe tout le contenu de votre fichier affichage.py
from logique import Boid # Importe notre nouvelle classe Boid complète

# ----------------------------------------------------------------------
# --- MONKEY PATCHING : Remplacer la classe Boid ---
# ----------------------------------------------------------------------

# Ceci est l'astuce : Nous remplaçons la classe 'Boid' (basée sur des listes)
# dans le module 'affichage' par notre classe 'Boid' (basée sur Vector).
affichage.Boid = Boid

# Pour que la nouvelle méthode update vectorielle fonctionne correctement, 
# nous allons aussi corriger la fonction d'update dans la boucle principale.
# Nous remplaçons la fonction 'main' de affichage.py par une version compatible
# avec la nouvelle signature boid.update(all_boids, width, height).

original_main = affichage.main

def patched_main():
    """Version modifiée de main() qui injecte les dimensions de l'écran dans l'update."""
    
    # 1. Initialisation (Identique à l'original)
    pygame.init()
    screen = pygame.display.set_mode((affichage.SCREEN_WIDTH, affichage.SCREEN_HEIGHT))
    pygame.display.set_caption("Simulation de Boids (Flocage actif)")
    clock = pygame.time.Clock()

    # 2. Création des Boids (Crée des instances de la nouvelle classe logique.Boid)
    boids = []
    for _ in range(affichage.NUMBER_OF_BOIDS):
        x = random.randint(0, affichage.SCREEN_WIDTH)
        y = random.randint(0, affichage.SCREEN_HEIGHT)
        boids.append(affichage.Boid(x, y)) # affichage.Boid est maintenant logique.Boid

    # 3. Boucle Principale du Jeu
    running = True
    while running:
        # --- A. Gérer les Entrées (Input) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- B. Mise à Jour de la Logique (Update) ---
        # *** C'EST ICI QUE NOUS MODIFIONS LE COMPORTEMENT DE L'ANCIENNE BOUCLE ***
        for boid in boids:
            # Appel la nouvelle méthode Boid.update(all_boids, width, height)
            boid.update(boids, affichage.SCREEN_WIDTH, affichage.SCREEN_HEIGHT) 

        # --- C. Rendu Graphique (Draw) ---
        screen.fill(affichage.BLACK) 
        
        for boid in boids:
            # Appel la nouvelle méthode Boid.draw(screen) avec la couleur WHITE
            boid.draw(screen, affichage.WHITE) 
            
        pygame.display.flip() 
        clock.tick(affichage.FPS) 

    pygame.quit()

# ----------------------------------------------------------------------
# --- LANCEMENT ---
# ----------------------------------------------------------------------

if __name__ == '__main__':
    # Lance la fonction principale modifiée
    patched_main()