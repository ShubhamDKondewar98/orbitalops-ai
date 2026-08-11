from dotenv import load_dotenv
load_dotenv()

import os
from sqlalchemy import create_engine
from app.db.models import Base

engine = create_engine(os.getenv("DATABASE_URL"))
Base.metadata.create_all(engine)

print("All tables created successfully")
