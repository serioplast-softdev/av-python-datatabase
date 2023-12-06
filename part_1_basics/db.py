from sqlmodel import Session, SQLModel, create_engine, or_, select

from model import Hero

_DUMMY_HEROES_DATA = [
    {"name": "Deadpond", "secret_name": "Dive Wilson"},
    {"name": "Spider-Boy", "secret_name": "Pedro Parqueador"},
    {"name": "Rusty-Man", "secret_name": "Tommy Sharp", "age": 48},
    {"name": "Tarantula", "secret_name": "Natalia Roman-on", "age": 32},
    {"name": "Black Lion", "secret_name": "Trevor Challa", "age": 35},
    {"name": "Dr. Weird", "secret_name": "Steve Weird", "age": 36},
    {"name": "Captain North America", "secret_name": "Esteban Rogelios", "age": 93}
]

_engine = None

def setup(db_file_path=None, echo=False):
    global _engine
    if db_file_path is None:
        sqlite_url = "sqlite://" # Use in memory database
    else:
        sqlite_url = f"sqlite:///{db_file_path}"
    _engine = create_engine(sqlite_url, echo=echo)
    SQLModel.metadata.create_all(_engine)

def create_heroes():
    heroes = [Hero(**hero_data) for hero_data in _DUMMY_HEROES_DATA]
    with Session(_engine) as session:
        for hero in heroes:
            session.add(hero)
        session.commit()
        for hero in heroes:
            # session.refresh(hero)
            print(f"Newly added hero \"{hero.name}\" has ID {hero.id}")

def update_heroes():
    with(Session(_engine)) as session:
        hero_1 = session.exec(select(Hero).where(Hero.name == "Spider-Boy")).one()
        hero_2 = session.exec(select(Hero).where(Hero.name == "Captain North America")).one()

        hero_1.name = "Spider-Youngster"
        hero_1.age = 16
        hero_2.name = "Captain North America Except Canada"
        hero_2.age = 110

        heroes = [hero_1, hero_2]
        for hero in heroes:
            session.add(hero)
        session.commit()
        for hero in heroes:
            # session.refresh(hero)
            print(f"Updated hero: \"{hero.name}\", age {hero.age}")

def delete_heroes():
    hero_name = "Spider-Youngster"
    with(Session(_engine)) as session:
        hero = session.exec(select(Hero).where(Hero.name == hero_name)).one()
        session.delete(hero)
        session.commit()
        if session.exec(select(Hero).where(Hero.name == hero_name)).first() is None:
            print(f"Hero \"{hero_name}\" has been deleted.")

def get_all_heroes():
    with Session(_engine) as session:
        return session.exec(select(Hero)).all()

def get_hero_by_name(name: str):
    with Session(_engine) as session:
        statement = select(Hero).where(Hero.name == name)
        return session.exec(statement).first()

def get_heroes_older_than(age: int):
    with Session(_engine) as session:
        statement = select(Hero).where(Hero.age > age)
        return session.exec(statement).all()

def get_heroes_between_age(from_age: int, to_age: int):
    with Session(_engine) as session:
        statement = select(Hero) \
            .where(Hero.age >= from_age) \
            .where(Hero.age <= to_age)
        return session.exec(statement).all()

def get_heroes_younger_or_older_than(under_age: int, over_age: int):
    with(Session(_engine)) as session:
        statement = select(Hero).where(or_(Hero.age < under_age, Hero.age > over_age))
        return session.exec(statement).all()

def get_deadpond():
    # "Deadpond" is expected to be present and unique in the "name" column
    with(Session(_engine)) as session:
        return session.exec(select(Hero).where(Hero.name == "Deadpond")).one()

def get_hero_by_id(id_: int):
    with(Session(_engine)) as session:
        return session.get(Hero, id_)

def get_heroes_page(page_number: int, heroes_per_page: int):
    # Page numbering starts from 1
    page_number -= 1;
    with(Session(_engine)) as session:
        statement = select(Hero) \
            .offset(page_number * heroes_per_page) \
            .limit(heroes_per_page)
        return session.exec(statement).all()
