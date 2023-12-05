from sqlalchemy.orm import Session
from src.db.models import Instrument
from config.settings import settings
from src.db.models import Base

from sqlalchemy import URL, create_engine


engine_url = URL.create(
    "postgresql+psycopg2",
    username=settings.postgres_user,
    password=settings.postgres_password,
    host=settings.postgres_host,
    port=settings.postgres_port_number,
    database=settings.postgres_db,
)

engine = create_engine(engine_url)

Base.metadata.create_all(engine)

instruments = (
        Instrument(code="AIG-RM", title="American International ORD SHS", group="stock_shares"),
        Instrument(code="AMEZ", title="Ашинский метзавод ПАО ао", group="stock_shares"),
        Instrument(code="MAGEP", title="&quot;Магаданэнерго&quot; ПАО ап", group="stock_shares"),
        )

with Session(engine) as session:
    session.add_all(instruments)
    session.commit()






