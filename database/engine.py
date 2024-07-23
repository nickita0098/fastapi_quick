from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'postgresql+psycopg2://nickita@localhost/test_db',
    echo=True,
)

Session = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)
