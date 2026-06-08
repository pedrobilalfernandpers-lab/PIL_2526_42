# models/__init__.py
# Ce fichier dit à SQLAlchemy : "voici tous mes models, enregistre-les tous"

from .user import User, UserSkill, UserAvailability
from .skill import Skill
from .mentorship_post import MentorshipPost, PostAvailability
from .match import Match
from .conversation import Conversation
from .message import Message