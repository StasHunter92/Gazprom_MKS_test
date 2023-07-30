from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create engine
# ----------------------------------------------------------------------------------------------------------------------
db_engine = create_engine("sqlite:///database/cable_journal.db", echo=True)


# Create session
# ----------------------------------------------------------------------------------------------------------------------
class DatabaseSession:
    def __init__(self, engine):
        self.engine = engine

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session
