🐦 Simulation de Boids en Python (Pygame)

Ce projet est une implémentation en Python de l’algorithme Boids, créé par Craig Reynolds en 1986.
L’objectif est de simuler un comportement collectif réaliste — appelé flocking — en utilisant uniquement trois règles simples appliquées par chaque agent (boid) :

Séparation : éviter les collisions avec les voisins proches.

Alignement : s’aligner sur la direction et la vitesse des autres boids à proximité.

Cohésion : se diriger vers le centre de masse local du groupe.

L’affichage et les animations sont entièrement gérés avec Pygame.

📸 Aperçu du projet

Le programme affiche un groupe de boids se déplaçant de manière fluide et naturelle à l’écran.
Chaque boid analyse son environnement et modifie sa direction en fonction des trois règles fondamentales.

Ce projet permet d’observer en temps réel des comportements collectifs complexes émerger de règles très simples.

🚀 Fonctionnalités

Simulation réaliste du comportement de flocking

Séparation, alignement et cohésion ajustables

Déplacement fluide avec vecteurs

Affichage graphique en temps réel via Pygame

Paramètres de la simulation facilement modifiables (vitesse, nombre de boids, rayon de vision, force des règles…)

Animation fluide même avec un grand nombre de boids

🛠️ Technologies utilisées

Python 3.x

Pygame pour l’affichage graphique

Math vectorielle (calculs 2D, normalisation, distances)

📦 Installation
1. Cloner le projet
git clone ttps://github.com/AlexAdowin/simulation-de-Boids.git 
cd boids-simulation

2. Installer les dépendances
pip install pygame

▶️ Lancer la simulation
python main.py

📁 Structure du projet
boids-simulation/
├── main.py           # Point d'entrée de la simulation
├── boid.py           # Classe Boid avec les règles (séparation, alignement, cohésion)
├── settings.py       # Paramètres modifiables (nombre de boids, vitesse, rayon, etc.)
├── utils.py          # Fonctions utilitaires (vecteurs, distance…)
└── README.md         # Documentation du projet

⚙️ Paramétrage

Vous pouvez ajuster :

le nombre de boids

la vitesse maximale

le rayon de vision

les forces appliquées (cohésion, alignement, séparation)

la taille de la fenêtre

la couleur et taille des boids

Toutes les options sont centralisées dans settings.py.

🎯 Objectifs du projet

Comprendre l’émergence de comportements complexes via des règles simples

Manipuler Pygame pour l’affichage d’un système dynamique

Approfondir l’utilisation des vecteurs et transformations en 2D

Reproduire un algorithme classique d’intelligence artificielle

📚 Référence

Craig Reynolds — Flocks, Herds, and Schools: A Distributed Behavioral Model (1986)