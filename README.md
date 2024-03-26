# Projet-Diagramme-Bode
Projet d'Acquisition des données 2, M1 Physique Numérique. 

## Références de machines à utiliser

Ce programme a été créé en se servant d'un oscilloscope et d'un GBF spécifiques. Effectivement si vous n'utilisez pas les mêmes les commandes de programmation pourront différer et mener à l'échec du programme. 

**Pour l'oscilloscope** : GDS-1000B Series Digital Storage Oscilloscopes de Gwinstek <br>
**Pour le générateur** : GDS-1000B Series Digital Storage Oscilloscopes de RIGOL

## Paramètres que vous pouvez choisir

Voici une présentation des paramètres utilisés dans ce programme, de leur signification et des conditions qu'ils doivent remplir.

**freq_dep** = Correspond à la fréquence de départ par laquelle vous voulez commencer le balayage des fréquences pour le diagramme de Bode. Elle est exprimée en Hz. 
Cette fréquence doit être comprise entre 1E-6 et 3E7 Hz pour respecter les limitations du GBF. Cela doit également être un nombre, peu importe qu'il soit entier ou non. Si ces conditions ne sont pas respectées un message d'erreur s'affichera et vous ne pourrez pas continuer avec le tracé du graphe sans changer vos valeurs.

**freq_fin** = Correspond à la fréquence de fin par laquelle vous voulez finir le balayage des fréquences pour le diagramme de Bode. Elle est exprimée en Hz.
Cette fréquence doit être strictement plus grande que **freq_dep** et inférieur à 3E7 Hz (pour les limitations du GBF). Cela doit également être un nombre, peu importe qu'il soit entier ou non. Si ces conditions ne sont pas respectées un message d'erreur s'affichera et vous ne pourrez pas continuer avec le tracé du graphe sans changer vos valeurs.

**nb_points** = Correspond au nombre de points voulu sur le diagramme de Bode. Plus le nombre (sans dimension) choisi est grand plus le diagramme de Bode est précis mais aussi plus il est long à tracer.
Cette valeur doit être un nombre entier plus grand ou égal à 1. Si cette condition n'est pas respectée un message d'erreur s'affichera et vous ne pourrez pas continuer avec le tracé du graphe sans changer vos valeurs.
Une estimation du temps maximal que peut prendre la mesure en fonction du nombre de points que vous avez renseigné vous sera donnée et il vous sera demandé si sachant cela vous voulez continuer ou non.

**voie_entree** = Correspond à la voie de l'oscilloscope sur laquelle arrive le signal d'entrée de votre circuit quelconque. Cela peut être 1 ou 2 que vous choisirez à l'aide de boutons radios.

**voie_GBF** = Correspond à la voie du GBF qui va généré l'output du signal et sur laquelle est branchée votre câble rejoignant votre circuit. Cela peut être 1 ou 2 que vous choisirez à l'aide de boutons radios.

**amplitude_entree** = L'amplitude désirée pour votre signal d'entrée. Elle est exprimée en V.
Cette amplitude doit être comprise entre 2.5E-3 V et **amplitude_max** pour respecter les limitations du GBF. Cela doit également être un nombre, peu importe qu'il soit entier ou non. Si ces conditions ne sont pas respectées un message d'erreur s'affichera et vous ne pourrez pas continuer avec le tracé du graphe sans changer vos valeurs.

**moyenne_echantillon** = Le nombre d'échantillons que vous choisissez pour faire une moyenne et mesurer le signal. Il y a plusieurs puissances de 2 au choix : 2, 4, 8, 16, 32, 64, 128 ou 256. Vous en choisirez une à l'aide d'un menu déroulant. 

**echelle** = Correspond à l'échelle du graphique vous choisissez. Ou bien vous aurez un graphe final en échelle linéaire ou bien en échelle semi-logarithmique avec l'échelle des fréquences en échelle logarithmique sur le diagramme du gain. Il est conseillé de choisir l'échelle semi-logarithmique pour une meilleure practicité de lecture mais le choix est laissé à l'utilisateur.
Vous ferez votre choix à l'aide de boutons radios. 

**frequence_coupure_case** = L'utilisateur peut choisir ou non d'afficher une droite à -3dB sur le graphe final du gain. Cela peut aider à évaluer la fréquence de coupure dans le cas de circuits simples. Attention cela ne vous aidra pas dans le cas de filtres d'ordre élevé, de filtres résonants, de filtres non linéaires ou bien de filtres spéciaux (Butterworth, Chevyshev, etc...).
Vous pouvez choisir de l'afficher grâce à une case à cocher.

Il n'est pas important que vous mettiez des points ou des virgules comme séparateurs pour les nombres, "300.7" et "300,7" par exemple fonctionneront de la même manière.

## Paramètres imposés

**voie_sortie** = Correspond à la voie de l'oscilloscope sur laquelle arrive le signal de sortie de votre circuit quelconque. Par défaut si votre **voie_entree** est 1 ce sera 2 et vice-versa.

**amplitude_max** = Correspond à l'amplitude maximale que le GBF peut produire. Elle est exprimée en V. 
Si votre fréquence de fin (**freq_fin**) est strictement inférieure à 1E7 Hz alors elle sera de 10V.
Si votre fréquence de fin (**freq_fin**) est comprise entre 1E7 Hz inclus et 3E7 Hz exclus alors elle sera de 5V.
Si votre fréquence de fin (**freq_fin**) est comprise entre 3E7 Hz inclus et 6E7Hz exclus alors elle sera de 2,5V.

## Boutons de l'interface

**Aide** : En cliquant sur ce bouton vous ouvres une nouvelle fenêtre que vous pouvez garder en parallèle et qui contient des renseignements supplémentaires sur les paramètres à choisir et qui contient le lien vers le github contenant ce README.

**Valider** : En cliquant sur ce bouton, si tous vos paramètres renseignés respectent les conditions, un pop-up s'ouvre et vous renseigne sur le temps maximal que peut prendre la mesure et vous demande si vous voulez tout de même procéder. Si c'est le cas alors l'interface pour choisir vos paramètres disparaîtra, les mesures s'effectueront et une nouvelle fenêtre contenant le graphique s'affichera. Vous pourrez alors zoomer sur ce graphe ou dézoomer à volonté ou bien même l'enregistrer.

**Quitter** : En cliquant sur ce bouton vous l'interface pour choisir vos paramètres se fermera et le programme arrêtera de s'exécuter. Si vous voulez recommencer il faudra relancer le programme.

## Aide

Si vous avez besoin d'aide ou de renseignements ou bien vous pouvez vous servir de ce README relativement complet, ou bien vous avez deux autres options.
La première est que lorsque vous lancer le programme, dans l'interface où vous devez renseigner vos paramètres il y a un bouton aide. Si vous cliquez dessus une fenêtre s'ouvrira que vous pouvez garder ouverte en parallèle et dans laquelle vous avez des renseignements concernant les paramètres et le lien vers ce github contenant ce README.
Autrement le fichier python associé à ce projet et permettant de lancer le programme est commenté de manière détaillée. 
