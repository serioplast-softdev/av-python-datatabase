from sqlmodel import Session, SQLModel, create_engine, or_, select

from model import Team, Hero

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
    with Session(_engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")
        heroes = [
            Hero(name="Deadpond", secret_name="Dive Wilson", teams=[team_z_force, team_preventers]),
            Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48, teams=[team_preventers]),
            Hero(name="Spider-Boy", secret_name="Pedro Parqueador", teams=[team_preventers])
        ]
        for hero in heroes:
            session.add(hero)
        session.commit()
        for hero in heroes:
            print("New hero \"{}\" belongs to teams: {}".format(
                hero.name,
                ", ".join([team.name for team in hero.teams])
            ))

def update_heroes():
    with Session(_engine) as session:
        hero_spider_boy = session.exec(select(Hero).where(Hero.name == "Spider-Boy")).one()
        team_z_force = session.exec(select(Team).where(Team.name == "Z-Force")).one()
        team_z_force.heroes.append(hero_spider_boy)
        session.add(team_z_force)
        session.commit()
        print("Updated Spider-Boy teams: " + ", ".join([team.name for team in hero_spider_boy.teams]))
        print("Updated Z-Force heroes: " + ", ".join([hero.name for hero in team_z_force.heroes]))

def revert_heroes():
    with Session(_engine) as session:
        hero_spider_boy = session.exec(select(Hero).where(Hero.name == "Spider-Boy")).one()
        team_z_force = session.exec(select(Team).where(Team.name == "Z-Force")).one()
        hero_spider_boy.teams.remove(team_z_force)
        session.add(team_z_force)
        session.commit()
        print("Reverted Spider-Boy teams: " + ", ".join([team.name for team in hero_spider_boy.teams]))
        print("Reverted Z-Force heroes: " + ", ".join([hero.name for hero in team_z_force.heroes]))
