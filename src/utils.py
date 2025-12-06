import math

class Vector:
    
    def __init__(self, x=0.0, y=0.0):
        # On stocke les composantes
        self.x = float(x)
        self.y = float(y)
        
    # Decoiverte de la Méthodes Magiques (Surcharge d'Opérateur) ---
    
    # Permet de faire : v1 + v2
    def __add__(self, other):
        """Additionne deux vecteurs (Vector + Vector)"""
        # On retourne un NOUVEL objet Vector, résultat de l'addition
        return Vector(self.x + other.x, self.y + other.y)

    # Permet de faire : v1 - v2
    def __sub__(self, other):
        """Soustrait un vecteur à un autre (Vector - Vector)"""
        return Vector(self.x - other.x, self.y - other.y)

    # Permet de faire : v1 * 5 (multiplication scalaire)
    def __mul__(self, scalar):
        """Multiplie par un scalaire (Vector * nombre)"""
        return Vector(self.x * scalar, self.y * scalar)

    # Pour que print(v) affiche un résultat lisible
    def __repr__(self):
        return f"Vector({self.x:.2f}, {self.y:.2f})"
    
    # --- Méthodes Mathématiques Utilitaires ---
    
    def magnitude(self):
        """Calcule la longueur du vecteur"""
        return math.sqrt(self.x**2 + self.y**2) # pythagore

    def normalize(self):
        """Retourne un nouveau vecteur de même direction mais de longueur 1"""
        mag = self.magnitude()
        if mag == 0:
            return Vector(0, 0)
        return Vector(self.x / mag, self.y / mag)