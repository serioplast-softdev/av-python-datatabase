from sqlmodel import Session, SQLModel, create_engine, or_, select

from model import Team, Hero, HeroTeamLink

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

        hero_deadpond = Hero(name="Deadpond", secret_name="Dive Wilson")
        hero_rusty_man = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")

        links = [
            HeroTeamLink(team=team_z_force, hero=hero_deadpond),
            HeroTeamLink(team=team_preventers, hero=hero_deadpond, is_training=True),
            HeroTeamLink(team=team_preventers, hero=hero_spider_boy, is_training=True),
            HeroTeamLink(team=team_preventers, hero=hero_rusty_man)
        ]
        for link in links:
            session.add(link)
        session.commit()

        for team in [team_z_force, team_preventers]:
            for link in team.hero_links:
                print("\"{}\" hero \"{}\" is {}training".format(
                    team.name,
                    link.hero.name,
                    "" if link.is_training else "not "))
