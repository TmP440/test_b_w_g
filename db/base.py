# Import all the models, so that Base has them before being
# imported by Alembic
from core.database import Base
from models.pairs import Pairs
