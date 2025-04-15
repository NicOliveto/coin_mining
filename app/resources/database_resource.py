from sqlalchemy import create_engine, Column, VARCHAR, NUMERIC, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.dialects.postgresql import insert

# Base definition
Base = declarative_base()

# Tables models
class CurrencyData(Base):
    __tablename__ = "currency_data"
    __table_args__ = {'schema': "relational_tb"}

    base_currency_id = Column(VARCHAR, primary_key=True, nullable=False)
    target_currency_id = Column(VARCHAR, primary_key=True, nullable=False)
    date_time = Column(TIMESTAMP, primary_key=True, nullable=False)
    purchase_amt = Column(NUMERIC, nullable=True)
    sale_amt = Column(NUMERIC, nullable=True)


# Setting up database engine and create objects
class DatabaseResource:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def init_db(self):
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()


# Manage data operations from objects created in DatabaseResource
class CoinDataResource:
    def __init__(self, db_repo: DatabaseResource):
        self.db_repo = db_repo
        self.db_repo.init_db()

    def insert_bulk_coin_prices(self, records: list[dict]):
        session = self.db_repo.get_session()
        try:
            stmt = insert(CurrencyData).values(records)
            stmt = stmt.on_conflict_do_update(
                index_elements=[CurrencyData.base_currency_id, CurrencyData.target_currency_id, CurrencyData.date_time],
                set_={
                    CurrencyData.purchase_amt: stmt.excluded.purchase_amt,
                    CurrencyData.sale_amt: stmt.excluded.sale_amt
                }
            )
            session.execute(stmt)
            session.commit()
        except Exception as e:
            session.rollback()
            raise ValueError(f"Error in bulk insert/update: {e}")
        finally:
            session.close()
