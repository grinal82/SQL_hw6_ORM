import os
from dotenv import load_dotenv
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

load_dotenv()

login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")
db_name = os.getenv("DB_NAME")


DSN = f"postgresql://{login}:{password}@localhost:5432/{db_name}"

engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


def init_data(session):
    with open("fixtures/tests_data.json", "r") as fd:
        data = json.load(fd)

    for record in data:
        model = {
            "publisher": Publisher,
            "shop": Shop,
            "book": Book,
            "stock": Stock,
            "sale": Sale,
        }[record.get("model")]
        session.add(model(id=record.get("pk"), **record.get("fields")))
    session.commit()


def find_publiher(session):
    find_publiher = int(input("Введите id издателя: "))
    result = session.query(Publisher).filter(Publisher.id == find_publiher).one()
    print(result)


init_data(session)
find_publiher(session)
