# VirtualLabelsAR

## Objectif
Ce projet vise a implémenter une assistance en réalité augmenté (utilisant la première et la deuxième génération Hololens) pour des personnes ayant des troubles neurocognitifs. 

## Fonctionnalités implémentées
Actuellement, les fonctionnalités implémentées sont :
- Création d'étiquettes virtuelles en utilisant la reconnaissance vocale (avec le mot-clé "Create Label").
- Mappage spatial permettant l'interaction entre les étiquettes virtuelles et les surfaces réelles de l’environnement autour du HoloLens (affichage du maillage en utilisant la reconnaissance vocale avec les mots-clés "Mapping On/Off").
- Déplacement des étiquettes sur les surfaces d'une pièce en utilisant le geste Air Tap.
- Création d'une ancre spatiale lorsqu'une étiquette est placée, permettant ainsi aux étiquettes de conserver leur emplacement.
- Sauvegarde des coordonnées de la caméra dans le repère du worldOrigin, dont le but sera de pouvoir ajouter des étiquettes via une vidéo sur un PC.
- Mise en place d'un protocole Websocket avec un serveur python chargé d'envoyer un fichier JSON contenant les informations nécéssaires à la création d'étiquettes (position, rotation, contenu). Les étiquettes sont envoyées à la Hololens en utilisant la reconnaissance vocale (avec le mot clé "send labels").
- Création des étiquettes aux coordonnées reçues par le serveur. 

De nouvelles fonctionnalités seront implémentées (Section TODO a la fin).

## Compilation
Pour installer ce projet, commencez par cloner ce répertoire.
- Installez la dernière version de Unity (2019.4.3f1 a ce jour): https://store.unity.com/#plans-individual
- Installez Visual Studio 2019 : https://visualstudio.microsoft.com/fr/
- Ouvrez le projet dans Unity, Allez dand File > Build settings, vérifiez que la platforme sélectionnée est bien Universal Windows Platform, et que l'architecture est x86 pour la hololens 1 ou ARM pour la hololens 2, puis faites "Build".
- Dans votre menu Hierarchy (contenant les différents gameObjects de votre scène), sélectionnez MixedRealityToolkit, puis dans l'inspecteur, sélectionnez le profil correspondant au modèle de votre Hololens :
	- Hololens1ConfigurationProfil_clone pour la Hololens 1.
	- Hololens2ConfigurationProfil_clone pour la Hololens 2.
- Une fois terminé, ouvrez la solution dans Visual Studio, choisissez comme configuration "release", l'architecture doit être x86 pour la hololens 1 ou ARM pour la hololens 2, et choisissez comme debogeur "Ordinateur distant".
- Ouvrez les propriétés de déboguage, section déboguage, dans le champs "nom de l'ordinateur", placez y l'adresse IP de la Hololens (disponible dans les paramètres réseau de la Hololens).
- Il ne vous reste plus qu'a déployer la solution via le menu généré. 

## Lancement
L'application doit maintenant apparaitre dans la liste des applications installées du Hololens, il ne vous reste plus qu'a la lancer.

### TODO
Le serveur a pour objectif de recevoir les étiquettes envoyés par l'application bureau et de les renvoyer a l'applicationn Hololens. Il n'y a pour le moment aucun lien entre l'application bureau et le serveur. Actuellement, le serveur simule la réception des étiquettes par l'application bureau en créant un JSON contenant de fausses informations. C'est ce même JSON qui est envoyé à la Hololens.
