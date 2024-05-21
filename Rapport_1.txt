# Rapport 1
Membres de l'équipe
Ahmed Sadek, Erick R Delgado Garcia, Paul Agudze et Thomas Garneau

## Proximité aux Niveaux de Conception

- **Niveau 1** - Pourcentage de la proximité: 100 %
- **Niveau 2** - Pourcentage de la proximité: 100 %
- **Niveau 3** - Pourcentage de la proximité: 100 %
  Étant donné que les méthodes wink sont optionnelles, elles ne sont pas prises en compte. Nous considérons que la structure est respectée à la lettre pour le reste.

## Courte Description de l'Infrastructure Réalisée

### Classe Robot

- **Validation de l'intégrité du robot**:
  Lorsque le robot est initialisé, on initialise les senseurs pour la manette, les servomoteurs et le télémètre. Dans C64, l’état qui vérifie l’intégrité du robot appelle la propriété `has_integrity` de la classe `Robot`. Cette dernière retourne un booléen qui retourne `true` si tous les senseurs sont instanciés.

- **Gestion de la télécommande**:
  Nous avons un Enum nommé `KeyCodes` qui permet de transformer les inputs de la télécommande en noms plus significatifs. Nous avons une méthode nommée `read_input` qui gère la lecture de la télécommande. Elle accepte un argument optionnel, `read_once`, qui par défaut est faux. Lorsque cet attribut est vrai, la méthode retourne une seule fois la valeur de la touche appuyée. Sinon, la valeur est constamment retournée. Ces deux cas sont utiles pour gérer le déplacement entre les tâches et pour gérer les déplacements du robot.

- **Gestion du télémètre et de son servo moteur**:
  Le télémètre est initialisé lors de l’initialisation du robot et sa position est centrée à chaque initialisation.

- **Gestion des moteurs**:
  Nous avons une méthode qui encapsule la logique pour contrôler les mouvements du robot, y compris avancer, reculer, tourner à gauche, tourner à droite, s'arrêter et effectuer une rotation sur place.

- **Gestion de la couleur pour les yeux (la classe Eye Blinkers)**:
  Nous avons une variable de classe de type dictionnaire qui contient les noms des couleurs et leurs valeurs RGB. Nous avons implémenté des méthodes pour ouvrir et fermer chaque œil individuellement et par paire. Nous avons utilisé la même mécanique pour changer la couleur des yeux, soit individuellement ou par paire.

### Structure Générale du Logiciel

- **Infrastructure générale du logiciel**:
  C64 est une `FiniteStateMachine` (FSM) qui contient une instance de la classe `Robot`. Cette instance permet à C64 d'appeler des fonctions pour permettre d’accéder aux fonctionnalités matérielles du robot et ainsi effectuer les tâches demandées par l’utilisateur. Toutes ces tâches sont programmées et on peut se déplacer entre le menu home et ces dernières.

- **Capacité modulaire d'insertion d'une nouvelle tâche**:
  Notre programme permet aux développeurs d’ajouter une nouvelle tâche avec facilité. L’utilisation de la FSM facilite ceci puisque nous avons simplement besoin d’ajouter un état et les transitions nécessaires pour appeler la nouvelle tâche lorsque requis. Une fois la tâche créée, il suffit de l’importer dans C64, de l’attribuer à un `MonitoredState`, de créer une transition de l’état home vers la tâche et inversement. Les conditions pour ces transitions doivent être des `ManualControlCondition` qui prennent pour argument la touche requise pour accéder à la tâche ou au home (`expected_value`). Il faut absolument, dans la liste des actions à effectuer dans l'état de la tâche, faire le suivi de la FSM qu’il contient, à l’aide de la fonction `track()`.

## Patrons de Conception

- **State Machine**: Le projet, C64, est une instance de notre classe `FiniteStateMachine` et sera utilisé tout au long du programme pour gérer la logique.
- **Strategy**: Les différentes conditions encapsulent la logique qui sera utilisée pour savoir si on doit transitionner d’un état à l’autre.
- **Factory**: La classe C64 utilise une méthode nommée `__create_state` qui contient une série d'instructions permettant de créer et initialiser un état lorsqu’elle est appelée.
- **Observer**: Les `MonitoredState` et les `MonitoredStateCondition` sont des classes qui observent les changements de certains attributs internes et qui indiquent au FSM de transitionner au besoin.
- **Decorator**: Dans la classe `Transition`, nous utilisons le décorateur `@property` pour la méthode `valid` et nous utilisons le décorateur `@abstractmethod` pour la méthode abstraite `transiting`.

## Impact de l'Utilisation du Patron de Conception Machine d'État (State Pattern)

### Avantages

1. **Séparation claire des responsabilités**:
   - **Encapsulation**: Chaque état est représenté par une classe distincte qui encapsule le comportement spécifique de cet état. Cela permet une séparation claire des responsabilités, rendant le code plus modulaire et plus facile à maintenir.
   - **Facilité d'extension**: Ajouter de nouveaux états ou modifier des états existants devient plus simple. Il suffit de créer une nouvelle classe ou de modifier une classe existante sans impacter les autres parties du système.

2. **Gestion explicite des transitions**:
   - **Transitions définies**: Les transitions entre états sont explicitement définies, ce qui rend le flux de contrôle du système plus prévisible et plus facile à comprendre.
   - **Conditions de transition**: Les conditions de transition peuvent être encapsulées dans des objets, permettant une gestion flexible et réutilisable des règles de transition.

3. **Modularité**:
   - **Réutilisabilité**: Les états et les transitions peuvent être réutilisés dans différentes parties de l'application ou dans différents projets, ce qui améliore la réutilisabilité du code.
   - **Tests unitaires**: Chaque état et chaque transition peuvent être testés de manière isolée, ce qui simplifie les tests unitaires et améliore la fiabilité du système.

4. **Scalabilité**:
   - **Ajout de nouvelles fonctionnalités**: Le modèle facilite l'ajout de nouvelles fonctionnalités sans affecter le comportement existant, ce qui est essentiel pour des projets évolutifs.

### Inconvénients

1. **Complexité initiale**:
   - **Surcharge de conception**: La mise en place initiale d'un FSM peut être complexe et demande un effort de conception important. Il faut définir les états, les transitions et les conditions de manière exhaustive.
   - **Courbe d'apprentissage**: Les développeurs doivent comprendre les concepts de la machine d'état et les patrons de conception associés, ce qui peut nécessiter une formation supplémentaire.

2. **Fragmentation du code**:
   - **Multiplication des classes**: L'utilisation du patron de conception peut entraîner une fragmentation du code en de nombreuses petites classes, ce qui peut rendre la navigation et la gestion du code plus complexe, surtout pour les projets de grande envergure.

### Comparaison avec une Approche sans FSM

#### Sans FSM

1. **Code monolithique**:
   - **Regroupement du comportement**: Toutes les logiques de contrôle et de gestion des états seraient regroupées dans quelques classes ou méthodes, rendant le code monolithique et difficile à comprendre.
   - **Maintenance difficile**: Ajouter ou modifier des fonctionnalités nécessiterait de parcourir et de modifier du code spaghetti, ce qui augmente le risque d'introduire des bugs et rend la maintenance difficile.

2. **Transitions implicites**:
   - **Transitions non explicites**: Les transitions entre états seraient gérées de manière implicite par des conditions `if-else` ou des `switch` statements, rendant le flux de contrôle moins clair et plus difficile à suivre.
   - **Gestion des conditions complexe**: La gestion des conditions de transition deviendrait rapidement complexe et difficile à maintenir, surtout si les conditions sont nombreuses et variées.

3. **Réduction de la modularité**:
   - **Réutilisabilité limitée**: Il serait plus difficile de réutiliser des parties du code, car les logiques seraient fortement couplées et dispersées dans de grandes méthodes ou classes.
   - **Tests plus compliqués**: Tester des fonctionnalités spécifiques serait plus difficile, car il faudrait mettre en place de nombreux mocks et stubs pour isoler les parties du code à tester.

4. **Scalabilité réduite**:
   - **Évolution difficile**: Ajouter de nouvelles fonctionnalités ou adapter l'application à de nouveaux besoins serait plus complexe et risqué, car cela nécessiterait des modifications importantes du code existant.

### Impact

**Avec FSM**:
- **Structure claire et maintenable**: La structure du code est claire, chaque état et transition étant bien définis et encapsulés. Cela facilite la maintenance et l'extension du système.
- **Flexibilité et réutilisabilité**: Les états et transitions peuvent être facilement réutilisés et étendus, rendant le système plus flexible.
- **Fiabilité améliorée**: Grâce à une séparation claire et à des tests unitaires faciles, la fiabilité du système est améliorée.

**Sans FSM**:
- **Complexité accrue**: Le code devient rapidement complexe et difficile à gérer, surtout pour les systèmes avec de nombreux états et transitions.
- **Maintenance et évolutivité limitées**: Les efforts de maintenance et d'extension deviennent coûteux et risqués, réduisant la capacité à évoluer facilement.
- **Moins de modularité et de réutilisabilité**: Le code est moins modulaire, ce qui limite la réutilisabilité et complique les tests unitaires.



En bref, l'utilisation du patron de conception Machine d'État apporte des avantages significatifs en termes de structure, de maintenabilité, de flexibilité, et de fiabilité, bien que cela puisse introduire une complexité initiale. Ne pas utiliser ce patron pour un système complexe conduirait à un code difficile à gérer, moins flexible, et plus sujet aux erreurs.


### Autres Éléments d'Abstraction  
-  **Gestion de la Séquence des Actions**: Dans notre projet, une attention particulière a été portée à la gestion de la séquence des actions. Pour chaque état, nous avons défini des actions spécifiques à exécuter lors de l'entrée, du maintien et de la sortie de cet état. Cette abstraction permet une meilleure organisation des comportements et assure que les actions sont exécutées dans un ordre cohérent et prévisible. En encapsulant ces actions dans des méthodes distinctes, nous avons facilité la réutilisabilité et la modification des séquences d'actions sans perturber la logique de l'état lui-même.