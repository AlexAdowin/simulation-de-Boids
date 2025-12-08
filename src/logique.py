import random
import math
from utils import Vector, SpatialGrid 

class Boid:
    def __init__(self, x, y):
        self.position = Vector(x, y) 
        self.velocity = Vector(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = Vector(0, 0)
        self.max_speed = 4.0
        self.size = 5

        # Constantes de Flocage (Rayon de perception = Rayon max de la grille)
        self.separation_radius = 100.0 
        self.separation_weight = 50.0
        self.alignment_radius = 50.0  
        self.alignment_weight = 1.0
        self.cohesion_radius = 50.0 
        self.cohesion_weight = 1.0

    # ------------------------------------------------------------------
    # --- CONTRÔLE DE MOUVEMENT (Ajoutées pour corriger l'AttributeError) ---
    # ------------------------------------------------------------------

    def limit_speed(self):
        """Limite la vitesse du boid à self.max_speed."""
        mag = self.velocity.magnitude()
        if mag > self.max_speed:
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
    # --- RÈGLES DE FLOCAGE (separation, alignment, cohesion) ---
    # ------------------------------------------------------------------

    def separation(self, neighbors):
        """Règle 1: Répulsion des voisins trop proches (O(N) optimisé)."""
        steering_force = Vector(0, 0)
        count = 0                    
        
        for neighbor in neighbors:
            if neighbor is not self:
                distance_vector = self.position - neighbor.position
                d = distance_vector.magnitude()
                
                if d > 0 and d < self.separation_radius:
                    repulsion_vector = distance_vector.normalize()
                    repulsion_vector *= (1.0 / d)
                    steering_force += repulsion_vector
                    count += 1
        
        if count > 0:
            steering_force *= (1.0 / count)
            steering_force *= self.separation_weight
        return steering_force
        
    def alignment(self, neighbors):
        """Règle 2: Correspond à la vitesse moyenne des voisins (O(N) optimisé)."""
        average_velocity = Vector(0, 0)
        count = 0 
        radius = self.alignment_radius
        
        for neighbor in neighbors:
            if neighbor is not self:
                distance_vector = neighbor.position - self.position
                d = distance_vector.magnitude() 
                
                if d > 0 and d < radius:
                    average_velocity += neighbor.velocity 
                    count += 1
                    
        if count > 0:
            average_velocity *= (1.0 / count)
            steering_force = average_velocity - self.velocity 
            steering_force *= self.alignment_weight
            return steering_force
        return Vector(0, 0) 

    def cohesion(self, neighbors):
        """Règle 3: Se dirige vers le centre de masse (O(N) optimisé)."""
        center_of_mass = Vector(0, 0)
        count = 0 
        radius = self.cohesion_radius
        
        for neighbor in neighbors:
            if neighbor is not self:
                distance_vector = neighbor.position - self.position
                d = distance_vector.magnitude() 
                
                if d > 0 and d < radius:
                    center_of_mass += neighbor.position 
                    count += 1
                    
        if count > 0:
            center_of_mass *= (1.0 / count)
            steering_force = center_of_mass - self.position 
            if steering_force.magnitude() > 0:
                steering_force = steering_force.normalize()
                steering_force *= self.cohesion_weight
            return steering_force
        return Vector(0, 0)

    # ------------------------------------------------------------------
    # --- MÉTHODE PRINCIPALE DE MISE À JOUR (UPDATE) ---
    # ------------------------------------------------------------------

    def update(self, neighbors, width, height):
        """Calcule les forces en utilisant uniquement la liste des voisins proches."""
        
        # 1. Calcul des Forces
        separation_force = self.separation(neighbors)
        alignment_force = self.alignment(neighbors)
        cohesion_force = self.cohesion(neighbors)

        # 2. Application des Forces
        self.acceleration += separation_force 
        self.acceleration += alignment_force 
        self.acceleration += cohesion_force
        
        # 3. Mise à jour physique
        self.velocity += self.acceleration
        self.limit_speed() # <--- Appel désormais valide
        self.position += self.velocity
        
        # 4. Gestion des bords
        self.check_edges(width, height) # <--- Appel désormais valide

        # 5. Réinitialisation
        self.acceleration = Vector(0, 0)

    # ------------------------------------------------------------------
    # --- MÉTHODE DE DESSIN ---
    # ------------------------------------------------------------------
    
    def draw(self, screen, color=(255, 255, 255)):
        """Dessine le Boid comme un triangle pointant dans sa direction."""
        import pygame # Importé localement car il est utilisé ici

        if self.velocity.magnitude() > 0.1:
            angle = math.atan2(self.velocity.y, self.velocity.x)
        else:
            angle = 0 
            
        p1_x = self.position.x + self.size * math.cos(angle)
        p1_y = self.position.y + self.size * math.sin(angle)
        
        p2_x = self.position.x + self.size * math.cos(angle - 2.5) * 0.5
        p2_y = self.position.y + self.size * math.sin(angle - 2.5) * 0.5
        
        p3_x = self.position.x + self.size * math.cos(angle + 2.5) * 0.5
        p3_y = self.position.y + self.size * math.sin(angle + 2.5) * 0.5
        
        points = [(p1_x, p1_y), (p2_x, p2_y), (p3_x, p3_y)]
        pygame.draw.polygon(screen, color, points)