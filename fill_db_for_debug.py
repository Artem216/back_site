from sqlalchemy import URL, create_engine, select
from sqlalchemy.orm import Session

from config.settings import settings
from src.db.models import Base, Deal, Instrument, User, DealType

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


inst1 = Instrument(
    code="AIG-RM", title="American International ORD SHS", group="stock_shares"
)
inst2 = Instrument(code="AMEZ", title="Ашинский метзавод ПАО ао", group="stock_shares")
inst3 = Instrument(
    code="MAGEP", title="&quot;Магаданэнерго&quot; ПАО ап", group="stock_shares"
)
inst4 = Instrument(code="GAZA", title="ГАЗ ПАО ао", group="stock_shares")
inst5 = Instrument(code="GAZAP", title="ГАЗ ПАО ап", group="stock_shares")


deal1 = Deal(
    instrument = inst1,
    deal_type=DealType.buy,
    price=200.0,
    quantity=11,
)

deal2 = Deal(
    instrument = inst1,
    deal_type=DealType.sell,
    price=210.0,
    quantity=11,
)

deal3 = Deal(
    instrument = inst2,
    deal_type=DealType.buy,
    price=10.0,
    quantity=1,
)
deal4 = Deal(
    instrument = inst2,
    deal_type=DealType.sell,
    price=5.0,
    quantity=1,
)
deal5 = Deal(
    instrument = inst3,
    deal_type=DealType.buy,
    price=1000.0,
    quantity=13,
)
deal6 = Deal(
    instrument = inst3,
    deal_type=DealType.sell,
    price=1080.0,
    quantity=13,
)


with Session(engine, autoflush=False) as session:
    user1 = session.scalar(select(User).where(User.email == "test1@example.com"))
    user2 = session.scalar(select(User).where(User.email == "test2@example.com"))
    # for instr in (inst1, inst2, inst3, inst4, inst5):
    #     session.merge(instr)
    for deal in (deal1, deal2, deal3, deal4, deal5, deal6):
        deal.user = user1
        session.merge(deal)
    # user1.deals.extend([deal1, deal2, deal3, deal4, deal5, deal6])
    # session.merge(user1)
    
    session.commit()

