# Projet-Diagramme-Bode
Projet d'Acquisition des données 2, M1 Physique Numérique. 

Références de machines utilisées :
Pour l'oscilloscope : GDS-1000B Series Digital Storage Oscilloscopes de Gwinstek
Pour le générateur : GDS-1000B Series Digital Storage Oscilloscopes de RIGOL

## Paramètres que vous pouvez choisir

Voici une présentation des paramètres utilisés dans ce programme, de leur signification et des conditions qu'ils doivent remplir.

**freq_dep** = Correspond à la fréquence de départ par laquelle vous voulez commencer le balayage des fréquences pour le diagramme de Bode. Elle est exprimée en Hz. 

**freq_fin** = Correspond à la fréquence de fin par laquelle vous voulez finir le balayage des fréquences pour le diagramme de Bode. Elle est exprimée en Hz.

**nb_points** = Correspond au nombre de points voulu sur le diagramme de Bode. Plus le nombre (sans dimension) choisi est grand plus le diagramme de Bode est précis mais aussi plus il est long à tracer.

**voie_entree** = Correspond à la voie de l'oscilloscope sur laquelle arrive le signal d'entrée de votre circuit quelconque. Cela peut être 1 ou 2.

**amplitude_entree** = L'amplitude désirée pour votre signal d'entrée. Elle est exprimée en V.

**moyenne_echantillon** = Le nombre d'échantillons que vous choisissez pour mesurer le signal. Il y a plusieurs puissances de 2 au choix. 

**echelle** = Correspond à l'échelle du graphique vous choisissez. Ou bien vous aurez un graphe final en échelle linéaire ou bien en échelle semi-logarithmique avec l'échelle des fréquences en échelle logarithmique sur le diagramme du gain. Il est conseillé de choisir l'échelle semi-logarithmique pour une meilleure practicité de lecture mais le choix est laissé à l'utilisateur.

**frequence_coupure_case** = L'utilisateur peut choisir ou non d'afficher une droite à -3dB sur le graphe final du gain. Cela peut aider à évaluer la fréquence de coupure dans le cas de circuits simples. Attention cela ne vous aidra pas dans le cas de filtres d'ordre élevé, de filtres résonants, de filtres non linéaires ou bien de filtres spéciaux (Butterworth, Chevyshev, etc...).

## Paramètres imposés

**voie_sortie** = Correspond à la voie de l'oscilloscope sur laquelle arrive le signal de sortie de votre circuit quelconque. Par défaut si votre **voie_entree** est 1 ce sera 2 et vice-versa.

**amplitude_max** = Correspond à l'amplitude maximale que le GBF peut produire. Elle est exprimée en V. 


