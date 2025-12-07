# Fichier: logique.py
import pygame
import random
import math
from utils import Vector # Importe la classe Vector de utils.py

class Boid:
    """Classe Boid avec les trois règles de flocage, utilisant des objets Vector."""
    
    def __init__(self, x, y):
        # Utilisation de Vector pour position, velocity et acceleration
        self.position = Vector(x, y) 
        self.velocity = Vector(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = Vector(0, 0)
        self.max_speed = 4.0
        self.size = 5

        # Constantes de Flocage (Tuning)
        self.separation_radius = 25.0 
        self.separation_weight = 1.5
        self.alignment_radius = 50.0  
        self.alignment_weight = 1.0
        self.cohesion_radius = 50.0 
        self.cohesion_weight = 1.0

    # ------------------------------------------------------------------
    # --- CONTRÔLE DE MOUVEMENT ---
    # ------------------------------------------------------------------

    def limit_speed(self):
        mag = self.velocity.magnitude()
        if mag > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed 

    def check_edges(self, width, height):
        """Gestion des bords (Wrapping/Tore) en utilisant les composants x et y de Vector."""
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
    # (separation, alignment, cohesion - fonctions inchangées par rapport à la dernière version)
    # ------------------------------------------------------------------

    def separation(self, all_boids):
        steering_force = Vector(0, 0)
        count = 0                    
        for neighbor in all_boids:
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
        
    def alignment(self, all_boids):
        average_velocity = Vector(0, 0)
        count = 0 
        radius = self.alignment_radius
        for neighbor in all_boids:
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

    def cohesion(self, all_boids):
        center_of_mass = Vector(0, 0)
        count = 0 
        radius = self.cohesion_radius
        for neighbor in all_boids:
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
    # --- MÉTHODES UTILISÉES PAR LA BOUCLE PRINCIPALE ---
    # ------------------------------------------------------------------
    
    def update(self, all_boids, width, height):
        """Méthode de mise à jour complète (appelée par la boucle de jeu)."""
        separation_force = self.separation(all_boids)
        alignment_force = self.alignment(all_boids)
        cohesion_force = self.cohesion(all_boids)

        self.acceleration += separation_force 
        self.acceleration += alignment_force 
        self.acceleration += cohesion_force
        
        self.velocity += self.acceleration
        self.limit_speed()
        self.position += self.velocity
        
        self.check_edges(width, height) # Utilise width/height
        self.acceleration = Vector(0, 0)
        
    def draw(self, screen, color=(255, 255, 255)):
        """Dessine le Boid comme un triangle pour indiquer la direction."""
        
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