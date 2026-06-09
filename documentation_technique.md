# 📘 Documentation Complète : IFRI MentorLink (Code & Base de Données)

Ce document explique le projet **fichier par fichier**, et détaille le fonctionnement de la base de données à travers un **parcours utilisateur**. Idéal pour comprendre et présenter le projet !

---

## 🚀 1. Le Parcours Utilisateur (Comment la Base de Données s'anime)

Imaginons un étudiant nommé **Ali** (Licence 1) qui cherche de l'aide en Python, et une étudiante nommée **Fatou** (Master 1) qui veut aider en Python. Voici comment la base de données (Supabase) réagit à chaque étape :

### Étape 1 : L'Inscription (`table users`)
*   **Ali** remplit le formulaire. 
*   L'API chiffre son mot de passe pour qu'il soit illisible (grâce à `bcrypt`).
*   **BDD :** L'API fait un `INSERT INTO users`. Ali devient l'utilisateur ID: 1. Fatou s'inscrit et devient l'utilisateur ID: 2.

### Étape 2 : L'Ajout de compétences (`table user_skills` & `table skills`)
*   L'API récupère les compétences depuis la table `skills` (où "Python" est l'ID 3).
*   **Fatou** indique qu'elle est "Forte" en Python. **Ali** indique qu'il est "Faible".
*   **BDD :** Deux lignes sont créées dans la table pivot `user_skills` : 
    *   `[user_id: 2, skill_id: 3, proficiency: "strong"]` (Pour Fatou)
    *   `[user_id: 1, skill_id: 3, proficiency: "weak"]` (Pour Ali)

### Étape 3 : Création d'une Demande/Offre (`table mentorship_posts`)
*   **Fatou** crée une "Offre" de mentorat en Python.
*   **Ali** crée une "Demande" d'aide en Python.
*   **BDD :** Création de deux lignes dans `mentorship_posts` :
    *   Une ligne `type="offer"` liée à Fatou.
    *   Une ligne `type="request"` liée à Ali.

### Étape 4 : L'Algorithme de Matching (`table matches`)
*   Ali clique sur "Voir mes mentors recommandés".
*   L'API (le `matching_service.py`) regarde toutes les "offres" qui correspondent à la "demande" d'Ali. Il voit que Fatou propose du Python !
*   **BDD :** L'API insère une recommandation : `INSERT INTO matches (mentor_id: 2, mentee_id: 1, score: 90, status: 'pending')`. Ali voit la carte de Fatou avec un score de 90%.

### Étape 5 : L'Acceptation et la Discussion (`table conversations` & `table messages`)
*   Ali accepte Fatou comme mentor.
*   **BDD :** Le statut dans `matches` passe à `'accepted'`. Aussitôt, l'API crée une ligne dans la table `conversations`.
*   Ali envoie "Bonjour Fatou !".
*   **BDD :** L'API crée une ligne dans la table `messages` avec le contenu "Bonjour Fatou !", liée à leur conversation. 

---

## 📂 2. Explication de TOUT le code (Dossier par Dossier)

Voici l'explication de ce que fait chaque fichier de ton projet Python.

### 🌟 La Racine du projet
*   `main.py` : C'est le chef d'orchestre. Il initialise **FastAPI** (le framework de notre serveur). C'est lui qui configure le "CORS" (pour autoriser le frontend Vue.js à lui parler) et qui importe toutes les "routes" (les URLs) pour les rendre accessibles sur Internet.
*   `database.py` : Il crée le "moteur" (engine) qui se connecte à **Supabase**. C'est ici qu'on crée la fonction `get_db()` : elle ouvre une connexion à la base de données à chaque requête de l'utilisateur, et la ferme quand la requête est terminée (pour ne pas saturer le serveur).
*   `config.py` : Il va lire le fichier `.env` pour récupérer les mots de passe de la base de données de façon sécurisée (sans que le mot de passe ne soit écrit directement dans le code).

### 📐 Le dossier `models/` (Les Tables de la BDD)
Chaque fichier représente une **table** dans PostgreSQL. On utilise SQLAlchemy pour transformer des "Classes Python" en "Tables SQL".
*   `user.py` : Définit la table `users` (email, mot de passe haché, nom, niveau d'étude).
*   `skill.py` : Définit la table `skills` et la table de liaison `user_skills` (qui lie un utilisateur à une compétence avec un niveau de maîtrise).
*   `mentorship_post.py` : Définit les offres et requêtes (`mentorship_posts`) et les disponibilités (`post_availabilities`).
*   `match.py` : Définit la table des recommandations `matches` (avec le mentor, le mentoré, et le score de compatibilité).
*   `conversation.py` & `message.py` : Gèrent le chat. Une `conversation` est liée à un match accepté, et un `message` contient le texte envoyé.

### 🛡️ Le dossier `schemas/` (Le Contrôle qualité)
Les schémas utilisent **Pydantic** pour vérifier que ce que le Frontend nous envoie est correct *avant* même de déranger la base de données.
*   `user_schema.py` : Si le frontend essaie de créer un compte sans mettre d'email, ou sans prénom, ce fichier bloque la requête et renvoie une erreur "Champ manquant". Il définit aussi la façon dont on renvoie les infos (on ne renvoie jamais le mot de passe !).
*   `post_schema.py` : Vérifie qu'un post a bien un "titre", une "description", etc.

### 🛣️ Le dossier `routers/` (Les URLs de l'API)
C'est ici qu'on définit ce qui se passe quand on tape une URL. Chaque fichier gère un thème.
*   `auth.py` (`/api/auth`) : Gère l'inscription (`/register`) et la connexion (`/login`). C'est ici qu'on génère le fameux "Token JWT" quand le mot de passe est bon.
*   `users.py` (`/api/users`) : Gère le profil de l'utilisateur. La route `GET /me` renvoie les infos de la personne connectée (grâce à son Token).
*   `skills.py` (`/api/skills`) : Renvoie simplement la liste de toutes les compétences possibles pour remplir les menus déroulants du frontend.
*   `posts.py` (`/api/posts`) : Permet de créer une annonce d'offre ou de demande de mentorat, de la modifier ou de l'archiver.
*   `matches.py` (`/api/matches`) : Contient les boutons pour "Accepter" ou "Refuser" un match.
*   `chat.py` (`/api/conversations`) : Permet de récupérer la liste de ses conversations, de lire ses messages, et d'en envoyer de nouveaux.

### 🧠 Le dossier `services/` (L'Intelligence de l'application)
C'est le code complexe, séparé des routeurs pour que ce soit plus lisible.
*   `auth_service.py` : Contient la fonction `hash_password` (qui crypte les mots de passe) et `get_current_user`. Cette dernière est vitale : elle prend le Token JWT envoyé par le frontend, le décrypte, vérifie qu'il n'est pas expiré, et retrouve l'utilisateur dans la base de données.
*   `matching_service.py` : **Le cœur de ton projet !** C'est l'algorithme intelligent. Quand on l'appelle, il prend le profil d'un étudiant, regarde toutes les offres de mentorat des autres étudiants, compare les compétences, et attribue une note (un "score"). Il sauvegarde ensuite les meilleurs profils trouvés dans la table `matches` pour que le routeur puisse les afficher à l'étudiant.

---

### 💡 Résumé du Flux Technique
1. Vue.js envoie un JSON (ex: `{"email": "ali@mail.com"}`).
2. Le `router/auth.py` reçoit la demande.
3. Le `schemas/user_schema.py` valide que c'est bien un email.
4. Le `services/auth_service.py` crypte le mot de passe.
5. Le `models/user.py` prépare l'insertion SQL.
6. Le `database.py` (SQLAlchemy) écrit dans **Supabase**.
