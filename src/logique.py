import math
import random
from utils import Vector

class Boid:
    def __init__(self, x, y):
        # 1. État du Boid (Utilisation des objets Vector)
        self.position = Vector(x, y) 
        # Vitesse initiale aléatoire
        self.velocity = Vector(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = Vector(0, 0)
        self.max_speed = 4.0
        self.size = 5 # Pour le dessin

        # 2. Constantes de Flocage (Rayons et Poids)
        
        # SÉPARATION (Anti-collision)
        self.separation_radius = 25.0 
        self.separation_weight = 1.5
        
        # ALIGNEMENT (Coordination)
        self.alignment_radius = 50.0  
        self.alignment_weight = 1.0
        
        # COHÉSION (Regroupement) - NOUVEAU
        self.cohesion_radius = 50.0 
        self.cohesion_weight = 1.0

    # ------------------------------------------------------------------
    # --- MÉTHODES DE CONTRÔLE DE MOUVEMENT ---
    # ------------------------------------------------------------------

    def limit_speed(self):
        """Limite la vitesse du boid à self.max_speed."""
        mag = self.velocity.magnitude()
        if mag > self.max_speed:
            # Réduit la vitesse à max_speed sans changer la direction
            self.velocity = self.velocity.normalize() * self.max_speed 

    def check_edges(self, width, height):
        """Implémente l'effet 'wrapping' (tore)."""
        if self.position.x > width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = width
            
        if self.position.y > height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = height

    # ------------------------------------------------------------------
    # --- RÈGLES DE FLOCAGE ---
    # ------------------------------------------------------------------

    def separation(self, all_boids):
        """Règle 1: Évite les voisins trop proches (force de répulsion)."""
        radius_squared = self.separation_radius * self.separation_radius
        steering_force = Vector(0, 0)
        count = 0                    
        
        for neighbor in all_boids:
            if neighbor is not self:
                # Calcul de la distance réelle (magnitude)
                distance_vector = self.position - neighbor.position
                d = distance_vector.magnitude()
                
                if d > 0 and d < self.separation_radius:
                    # Répulsion : va du voisin VERS le boid actuel
                    
                    # 1. Normaliser la direction
                    repulsion_vector = distance_vector.normalize()
                    
                    # 2. Pondérer inversement par la distance (plus proche = plus fort)
                    repulsion_vector *= (1.0 / d)

                    steering_force += repulsion_vector
                    count += 1
        
        if count > 0:
            # Calcul de la moyenne et application du poids
            steering_force *= (1.0 / count)
            steering_force *= self.separation_weight
            
        return steering_force
        
    def alignment(self, all_boids):
        """Règle 2: Essaie de correspondre à la vitesse moyenne des voisins (coordination)."""
        
        average_velocity = Vector(0, 0)
        count = 0 
        radius = self.alignment_radius
        
        for neighbor in all_boids:
            if neighbor is not self:
                # Calcul de la distance réelle
                distance_vector = neighbor.position - self.position
                d = distance_vector.magnitude() 
                
                # 1. Filtrage : Le voisin est-il dans le rayon de perception ?
                if d > 0 and d < radius:
                    
                    # 2. Accumulation : Ajouter la VITESSE du voisin
                    average_velocity += neighbor.velocity 
                    count += 1
                    
        if count > 0:
            # 3. Calcul de la moyenne
            average_velocity *= (1.0 / count)

            # 4. Calcul de la Force (Steering Force)
            # Force = Vitesse Moyenne Voulue - Vitesse Actuelle
            steering_force = average_velocity - self.velocity 
            
            # 5. Application du Poids
            steering_force *= self.alignment_weight
            
            return steering_force
        
        return Vector(0, 0) 

    # ------------------------------------------------------------------
    # --- MÉTHODE PRINCIPALE DE MISE À JOUR ---
    # ------------------------------------------------------------------

    def update(self, all_boids, width, height):
        
        # 1. Calcul des Forces
        separation_force = self.separation(all_boids)
        alignment_force = self.alignment(all_boids)
        # cohesion_force = self.cohesion(all_boids) # Sera ajouté plus tard

        # 2. Application des Forces (Accélération = Somme des Forces)
        self.acceleration += separation_force 
        self.acceleration += alignment_force 
        # self.acceleration += cohesion_force
        
        # 3. Mise à jour de la Vitesse et de la Position
        self.velocity += self.acceleration
        self.limit_speed() # Limiter la vitesse après l'ajout de l'accélération
        self.position += self.velocity
        
        # 4. Gestion des bords
        self.check_edges(width, height)

        # 5. Réinitialisation de l'accélération
        self.acceleration = Vector(0, 0)

    # ------------------------------------------------------------------
    # --- MÉTHODE DE RENDU (À COMPLÉTER DANS simulation.py) ---
    # ------------------------------------------------------------------
    
    # NOTE: Cette méthode est généralement dans le fichier de simulation pour des raisons de dépendance Pygame
    # Mais nous la laissons ici en placeholder.
    def draw(self, screen):
        pass # Utilisation de pygame.draw.circle ou autre forme