import math

class Vector:
    """Implémentation d'un vecteur 2D avec surcharge d'opérateurs."""
    
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)
        
    # Surcharge d'Opérateur
    def __add__(self, other):
        """Additionne deux vecteurs (Vector + Vector)"""
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Soustrait un vecteur à un autre (Vector - Vector)"""
        # CORRECTION : Cette méthode est essentielle pour les distances
        return Vector(self.x - other.x, self.y - other.y) 

    def __mul__(self, scalar):
        """Multiplie par un scalaire (Vector * nombre)"""
        return Vector(self.x * scalar, self.y * scalar)

    # Opérateurs in-place (pour les opérations += et -=)
    def __iadd__(self, other):
        """Opération in-place Vector += Vector"""
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        """Opération in-place Vector -= Vector"""
        self.x -= other.x
        self.y -= other.y
        return self
        
    def magnitude(self):
        """Calcule la longueur du vecteur."""
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        """Retourne un vecteur unitaire."""
        mag = self.magnitude()
        if mag == 0:
            return Vector(0, 0)
        return Vector(self.x / mag, self.y / mag)
    
    def __repr__(self):
        return f"Vector({self.x:.2f}, {self.y:.2f})"


class SpatialGrid:
    """Structure de grille pour la partition spatiale (optimisation O(N))."""

    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cols = math.ceil(width / cell_size)
        self.rows = math.ceil(height / cell_size)
        # La grille est un tableau 1D simulant la grille 2D
        self.grid = [[] for _ in range(self.cols * self.rows)]

    def _get_cell_index(self, pos_x, pos_y):
        """Calcule l'index 1D dans le tableau 'grid' à partir des coordonnées 2D."""
        # Utilisation de l'opérateur modulo (%) pour le 'wrapping' aux bords
        col = int(pos_x // self.cell_size) % self.cols
        row = int(pos_y // self.cell_size) % self.rows
        return row * self.cols + col

    def add_boid(self, boid):
        """Ajoute un Boid à la cellule appropriée."""
        index = self._get_cell_index(boid.position.x, boid.position.y)
        self.grid[index].append(boid)

    def reset(self):
        """Vide la grille pour la prochaine image (plus rapide que de créer une nouvelle liste)."""
        # Vider les listes sans recréer la liste externe
        for cell in self.grid:
            cell.clear() 

    def get_neighbors(self, boid):
        """Récupère les Boids voisins dans la cellule actuelle et les 8 cellules adjacentes."""
        neighbors = []
        
        col_center = int(boid.position.x // self.cell_size)
        row_center = int(boid.position.y // self.cell_size)

        # Parcourir la cellule centrale et les 8 cellules autour
        for r_offset in [-1, 0, 1]:
            for c_offset in [-1, 0, 1]:
                
                # Applique le 'wrapping' aux coordonnées de la cellule pour les bords de l'écran
                col = (col_center + c_offset) % self.cols
                row = (row_center + r_offset) % self.rows

                index = row * self.cols + col
                
                # Vérification de sécurité, bien que le modulo doive garantir un index valide
                if 0 <= index < len(self.grid):
                    neighbors.extend(self.grid[index])
                    
        return neighbors