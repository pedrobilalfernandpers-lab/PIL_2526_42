# services/matching_service.py
# Algorithme de calcul du score de compatibilité mentor ↔ mentoré

from typing import List, Dict
from sqlalchemy.orm import Session

from models.user import User, UserSkill, UserAvailability
from models.mentorship_post import MentorshipPost
from models.match import Match


# Filières considérées comme proches (pour le critère 3)
RELATED_FIELDS = {
    "IA":    ["IM", "GL"],
    "IM":    ["IA", "GL"],
    "GL":    ["IA", "IM", "SI"],
    "SI":    ["GL"],
    "SE&IoT": ["IA", "IM"],
}


def _get_common_slots(availabilities_a, availabilities_b) -> int:
    """
    Compte le nombre de créneaux horaires qui se chevauchent
    entre deux listes de disponibilités.
    Deux créneaux se chevauchent si : même jour ET les heures se croisent.
    """
    count = 0
    for a in availabilities_a:
        for b in availabilities_b:
            if (a.day_of_week == b.day_of_week
                    and a.start_time < b.end_time
                    and b.start_time < a.end_time):
                count += 1
    return count


def calculate_score(mentor: User, mentee: User, skill_id: int) -> float:
    """
    Calcule le score de compatibilité entre un mentor et un mentoré
    pour une compétence donnée. Score sur 100 points :

    Critère 1 — Compétences (40 pts max) :
        Le mentor maîtrise la compétence (strong)
        ET le mentoré en a besoin (weak) → +40 pts

    Critère 2 — Disponibilités (30 pts max) :
        +10 pts par créneau commun, max 30 pts

    Critère 3 — Filière/Niveau (30 pts max) :
        Même filière → +30 pts
        Filières proches → +15 pts
        Filières différentes → +0 pt
    """
    score = 0.0

    # ── Critère 1 : Compétences ──────────────────────────────
    mentor_strong = {us.skill_id for us in mentor.skills if us.proficiency == "strong"}
    mentee_weak   = {us.skill_id for us in mentee.skills  if us.proficiency == "weak"}

    if skill_id in mentor_strong and skill_id in mentee_weak:
        score += 40

    # ── Critère 2 : Disponibilités communes ─────────────────
    common = _get_common_slots(mentor.availabilities, mentee.availabilities)
    score += min(30, common * 10)

    # ── Critère 3 : Proximité de filière ────────────────────
    if mentor.field_of_study == mentee.field_of_study:
        score += 30
    elif mentee.field_of_study in RELATED_FIELDS.get(mentor.field_of_study, []):
        score += 15

    return round(score, 2)


def compute_matches_for_user(db: Session, current_user: User) -> List[Dict]:
    """
    Calcule tous les matches possibles pour un utilisateur :
    1. Trouve les compétences où il a besoin d'aide (weak)
    2. Pour chaque compétence, trouve les utilisateurs qui la maîtrisent (strong)
    3. Calcule le score pour chaque paire
    4. Sauvegarde les nouveaux matches en BDD (si pas déjà existants)
    5. Retourne tous les matches triés par score décroissant
    """
    # Compétences où l'utilisateur courant a besoin d'aide
    my_weak_skill_ids = {
        us.skill_id for us in current_user.skills if us.proficiency == "weak"
    }

    if not my_weak_skill_ids:
        return []  # Pas de lacunes déclarées → pas de matches possibles

    results = []

    # Cherche les utilisateurs potentiels mentors (qui ont des compétences strong)
    potential_mentors = (
        db.query(User)
        .join(UserSkill)
        .filter(
            UserSkill.proficiency == "strong",
            UserSkill.skill_id.in_(my_weak_skill_ids),
            User.id != current_user.id
        )
        .distinct()
        .all()
    )

    for mentor in potential_mentors:
        mentor_strong_ids = {us.skill_id for us in mentor.skills if us.proficiency == "strong"}
        common_skills = my_weak_skill_ids & mentor_strong_ids

        for skill_id in common_skills:
            # Vérifie si ce match existe déjà
            existing = db.query(Match).filter(
                Match.mentor_id == mentor.id,
                Match.mentee_id == current_user.id,
                Match.skill_id  == skill_id
            ).first()

            score = calculate_score(mentor, current_user, skill_id)

            if score < 40:
                continue  # Score trop bas, pas pertinent

            if not existing:
                # Crée le match en BDD
                new_match = Match(
                    mentor_id = mentor.id,
                    mentee_id = current_user.id,
                    skill_id  = skill_id,
                    score     = score,
                    status    = "pending"
                )
                db.add(new_match)
                db.commit()
                db.refresh(new_match)
                results.append(new_match)
            else:
                # Met à jour le score si le profil a changé
                existing.score = score
                db.commit()
                results.append(existing)

    # Tri par score décroissant
    results.sort(key=lambda m: float(m.score), reverse=True)
    return results