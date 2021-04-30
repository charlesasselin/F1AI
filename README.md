# F1AI
Requirements:
* amplpy
* f1-2020-telemetry-master

# LISEZ-MOI #
 ce prototype SIAD a été développé par :
* Charles Asselin

En collaboration:
* Xavier Gagnon-Bergeron
* Freddy Constant Mojuye Njike
* Kimberly Larêche
* Victor Leboutillier
# Description du prototype #
Le prototype de SIAD a été développé dans le cadre du cours MQT-2100. C'est un programme linéaire qui permet de calculer et planifier  les moments et la fréquence auxquels les bolides s'arrês afin de maximiser la qualité du matériel fourni lors d'une cours de formule 1

# Installation #
Ce SIAD est disponible sur github: https://github.com/charlesasselin/F1AI/
Voici les /tapes pour l'installation
1. Installer AMPL
2. Ajouter AMPL au PATH de votre environnement de travail
3. Installer la librairie amplpy sur l'environnement python (pip install amplpy)
4. Installer la librairie f1 2020 telemetrie (pip install f1-2020-telemetry)

# Faire rouler l'application #
Pour l'instant, l'application n'a pas encore été construite. Il faut donc rouler un fichier python.
C'est le fichier F1AI.py qu'il faut rouler. Il est possible de le faire à partir du terminal dans le directory .src.
1. Tapper "python FIA1.py" (sans les guillemets) dans le terminal
2. Une fenêtre python apparaîtra, il suffit de cliquer dessus

# Analyse #
Ces étapes sont à réaliser dans l'interface logiciel
1. Choisir le fichier à analyser
2. Choisir le solveur
3. Appuyer sur le bouton Run Solver

# Record #
Ces étapes sont à réaliser dans l'interface logiciel
1. Dans le fichier record.py, il faut changer l'adresse IP pour celle de votre ordinateur.
2. Dans le jeu f1 2020, il faut s'assurer que le port est bel et bien celui dans le code. Par défaut: 20777
3. Appuyer sur le bouton Record
Note: La fonction record ne fonctionne pas si votre ordinateur n'est pas connecté à un simulateur.

## Bonne course! ##
