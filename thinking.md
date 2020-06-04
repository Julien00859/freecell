Pistes de résolution
====================

Objectifs
---------

- Monter les cartes les plus petites sur la fondation
- Construire des colonnes continues triées en partant des plus grandes

Le premier objectif est le but du jeu qui consiste à reconstituer les 4
familles de manière triée.

Le second objectif, que l'on peut considérer comme secondaire, consiste à vider
une colonne et à empiler une suite de cartes en partant du roi.

Cette stratégie permet aux cartes de plus faibles valeurs, c'est à dire celles
étant plus susceptibles d'être déplacées vers la fondation, d'être plus
facilement accessibles.

Le fait de pouvoir construire une colonne triée est en fait une conséquence des
règles du jeu.

Métriques
---------

- Freecells disponibles
- Colonnes disponibles
- Profondeur des cartes par rapport à leur valeur pour chaque colonne
- Nombre de cartes triées pour chaque colonne
- Distance entre les cartes sur la fondation par couleur

Mouvement possible
------------------

Il est possible de calculer le nombre de carte déplaçable par colonne à chaque
tour. Ce calcul est nécessaire pour déterminer l'arbre des possibilités du
coup actuel.

On peut alors simuler chaque déplacement, calculer le poids de chaque
coup et jouer réellement le coup qui semble le plus adéquoit.

/!\ comment vider les freecells ?

Poids
-----

Le poids est directement associé avec métriques avec en plus des modificateurs
qui permettent de balancer chacun d'entre eux. Par exemple, le nombre de
freecell dispo est plus important que la distance entre les cartes sur la
fondation.

Apprentissage
-------------

Peut-être un algorithme génétique qui tente de faire évoluer chacun des
modificateurs vers une solution (sub?) optimale.

Calcul de la réussite
---------------------

- Minimiser le nombre de coup totaux
- Minimiser le nombre de undo()

Calcul du hash
--------------

Afin de ne pas explorer des états qui l'ont déjà été par le passé, il est
nécessaire de retenir la liste des états explorés. Garder en mémoire l'état
complet du plateau serait très inefficace d'un point de vu de la mémoire. Une
fonction de hash qui s'applique sur le plateau est donc nécessaire.

- Chaque carte est déjà associée à un hash unique
- Les freecells sont interchangeables => Les trier par valeur ?
- Les colonnes sont interchangeables  => Les trier par somme de chaque colonne ?


Random shit
-----------

Pour le backtracking, on doit garder en mémoire la profondeur de chaque coup
évalué afin de pouvoir (for _ in range(abs(profondeur1 - profondeur2)): undo())