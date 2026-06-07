# IFRI_MentorLink — Projet Intégrateur PIL1 2025-2026

## Vue d'ensemble du projet
**IFRI_MentorLink** est une plateforme web de mise en relation entre étudiants de l'IFRI. L'objectif est de permettre à un étudiant compétent dans une matière (mentor) d’aider un autre étudiant (mentoré) de façon structurée via une plateforme numérique. Ce projet intégrateur mobilise toutes les compétences de première année : algorithmique, développement web, bases de données relationnelles, Python, et travail collaboratif avec Git.

---

## 1. Parcours utilisateur

1. **Découverte et inscription** : L’utilisateur accède à la landing page, clique sur « S’inscrire », renseigne ses informations personnelles, ses compétences, ses points faibles et ses disponibilités.
2. **Connexion** : L’utilisateur se connecte via email/téléphone + mot de passe, reçoit un token JWT et accède à son dashboard.
3. **Gestion des posts** : L’utilisateur peut créer des posts de mentorat (offre ou demande), consulter les posts des autres étudiants et répondre à ceux correspondant à ses besoins.
4. **Matching** : L’algorithme calcule un score de compatibilité pour chaque paire mentor-mentoré et affiche les résultats avec compétence commune, disponibilité partagée et score.
5. **Messagerie** : Une conversation est créée automatiquement pour chaque match accepté. Les messages sont échangés en temps réel via Supabase Realtime.
6. **Mise à jour continue** : L’utilisateur peut modifier son profil, mettre à jour ses compétences et disponibilités, gérer ses posts, et suivre ses matches et conversations.

> ⚠️ Remarque : La messagerie n’est disponible qu’entre utilisateurs ayant un match accepté.

---

## 2. Choix technologiques

| Côté | Technologie | Pourquoi |
|------|------------|----------|
| Frontend | Vue.js 3 + Vite | Syntaxe simple, composants réutilisables, intégration facile avec API REST |
| Backend | FastAPI (Python) | Documentation automatique, validation Pydantic, gestion JWT simple |
| Base de données | Supabase/PostgreSQL | SQL relationnel, hébergé, support Realtime pour chat, export SQL facile |

**Flux global :**

```
Navigateur (Vue.js)
      ↓ HTTP REST JSON (axios)
Backend (FastAPI)
      ↓ SQL / ORM (SQLAlchemy)
Base de données (Supabase/PostgreSQL)
      ↕ Realtime pour chat
```

---

## 3. Base de données

### Tables principales
1. **users** : informations personnelles, filière, niveau, bio, photo
2. **skills** : compétences disponibles sur la plateforme
3. **user_skills** : relation many-to-many entre utilisateurs et compétences avec `proficiency` (strong/weak)
4. **user_availabilities** : créneaux disponibles de chaque utilisateur
5. **mentorship_posts** : offres ou demandes de mentorat
6. **post_availabilities** : disponibilités spécifiques à un post
7. **matches** : correspondances mentor-mentoré avec score et statut (pending, accepted, rejected)
8. **conversations** : conversation unique par match accepté
9. **messages** : messages échangés dans une conversation

> Script SQL complet disponible dans `database.sql`.

---

## 4. Architecture projet

### Frontend Vue.js
- **Components** :
  - Layout : `Navbar.vue`, `Footer.vue`
  - Auth : `LoginForm.vue`, `RegisterForm.vue`
  - Profile : `UserProfile.vue`, `SkillSelector.vue`, `AvailabilityPicker.vue`
  - Mentorship : `PostCard.vue`, `PostForm.vue`, `MatchCard.vue`
  - Chat : `ConversationList.vue`, `ChatBox.vue`
- **Views** :
  - `LandingPage.vue`, `LoginPage.vue`, `RegisterPage.vue`, `DashboardPage.vue`
- **Stores** : Pinia pour l’état global (authentification, notifications)
- **Services** : appels API (auth, user, mentorship, chat)

### Backend FastAPI
- **Routers** : auth, users, skills, posts, matches, chat
- **Models SQLAlchemy** : correspondance avec les tables SQL
- **Schemas Pydantic** : validation des requêtes et réponses
- **Services** : logique métier séparée (auth_service, matching_service, chat_service)
- **Authentification** : JWT + hashing bcrypt
- **Realtime** : Supabase pour messagerie instantanée

---

## 5. Workflow GitHub

- **Branches** :
  - `main` : code stable
  - `develop` : intégration
  - `feature/landing-auth` : Frontend 1
  - `feature/dashboard` : Frontend 2
  - `feature/auth-backend` : Backend 1
  - `feature/users-skills` : Backend 2
  - `feature/posts-matching` : Backend 3
  - `feature/chat` : Backend 4

- **Règles** :
  - Ne jamais commit directement sur main ou develop
  - Puller develop avant de merger sa feature
  - Committer souvent avec conventions : `feat:`, `fix:`, `docs:`, etc.
  - PR vers `develop` après avoir terminé la feature

---

## 6. Installation

### Frontend
```bash
# Aller dans le dossier frontend
cd frontend

# Installer les dépendances
npm install

# Lancer le serveur de dev
npm run dev
```

### Backend
```bash
# Aller dans le dossier backend
cd backend

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer FastAPI
uvicorn main:app --reload
```

### Base de données
1. Créer un projet Supabase et configurer PostgreSQL
2. Exécuter le script `database.sql`
3. Remplir `.env` avec :
```text
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<dbname>
SECRET_KEY=<votre_secret_jwt>
VITE_SUPABASE_URL=<url_supabase>
VITE_SUPABASE_ANON_KEY=<anon_key>
```

---

## 7. Tests
- Swagger UI backend : `http://localhost:8000/docs`
- Vue.js frontend : `http://localhost:5173/`
- Vérifier parcours utilisateur complet : inscription → login → dashboard → posts → matching → chat

---

## 8. Livrables
- `frontend/` et `backend/`
- `.env.example`
- `README.md`
- `database.sql`
- Rapport HTML avec description BDD, architecture, workflow, manuel utilisateur
