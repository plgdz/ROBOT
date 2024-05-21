## Énoncé Partie 2 - Rapport

### Membres de l’équipe :

- Ahmed Sadek
- Erick R Delgado Garcia
- Paul Agudze
- Thomas Garneau

### Description de la tâche 2 :

La tâche 2 appelée Wondering a une similitude avec la tâche 1, car nous avons toujours un manual control du robot, cependant lorsque nous arrêtons de contrôler le robot, il attend 5 secondes jusqu'à ce que, comme son nom l'indique, il commence à errer. Il erre pendant 2 secondes et arrête pendant 2 secondes et recommence.

Pendant qu’il erre ou pendant qu’on contrôle le robot, si jamais il trouve un obstacle à son chemin avec un champ de vision de 300 mm, il va regarder à gauche et à droite pour vérifier s’il peut changer de direction. Il va aller par la suite à la direction ayant l’obstacle le plus loin, puis il recommence à errer.

- L’œil droit va avoir la couleur “magenta” et va blinker avec un cycle duration de 1 seconde, et qui va être ouverte la moitié du cycle. Le moment où on entre dans la tâche 2. Puis, le 2 yeux sont fermés le moment qu’on entre dans state_wonder et state_stop (dans la tâche 2). Pour les states qui restent (forward, backward, left, right) les yeux et les LED ont les mêmes configs que la tâche 1.

- Dans state_wonder et state_stop, les phares ne s’allument pas et pour les states qui restent (forward, backward, left, right) les yeux et les LED ont les mêmes configs que la tâche 1.

- Le robot peut aller en avant, en arrière, à droite, à gauche et s'arrêter. Le wonder state va choisir au hasard une direction dans laquelle le robot va se déplacer entre les directions suivantes (Forward, Right, Left).

- La télécommande aide à bouger le robot dépendant aux flèches qui sont appuyées. Puis, la télémètre aide à détecter si on est proche d’un obstacle.

- On utilise le range sensor servo, dans le but de détecter les obstacles. Par rapport à la gestion pour la contrainte de limitation des angles, on va donner au servo une valeur fixe à tourner comme ça il ne dépasse jamais la limite.

### Abstractions à porter attention :

- Dans WonderingFSM (tâche 2), on utilise des ManualControlState encore pour gérer nos mouvements.

- Dans WonderingFSM, state_stop et state_wonder ont chacune une transition vers state_forward, state_backward, state_left, state_right et ses derniers ont tous un transition vers state_stop.

### Difficultés :

- La partie la plus difficile, dans la première partie du projet, était d’essayer de conceptualiser le projet en même temps de le coder. On avait de la misère à visualiser comment chaque partie de code interagit ensemble, mais au fur et à mesure, surtout en faisant le partie C64 et manual control tout à fait du sens.

- La partie 2 était moins difficile que la partie 1, puisqu’on utilisait des bouts de code déjà fait dans la partie 1. Cependant la partie la plus difficile était d’inventer une tâche qui respecte l’architecture de notre FiniteStateMachine et en même temps respecte l'énoncé demandé. Sinon l'implémentation après qu’on a eu l’idée était assez simple.
