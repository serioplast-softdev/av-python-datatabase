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

def create_heroes_1(): # Defines relations using IDs

    with Session(_engine) as session:

        # Teams creation
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")
        teams = [team_preventers, team_z_force]
        for team in teams:
            session.add(team)
        session.commit()
        for team in teams:
            session.refresh(team)
            print(f"Team added: {team}")

        # Heroes creation
        hero_deadpond = Hero(name="Deadpond", secret_name="Dive Wilson", team_id=team_z_force.id)
        hero_rusty_man = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48, team_id=team_preventers.id)
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
        heroes = [hero_deadpond, hero_rusty_man, hero_spider_boy]
        for hero in heroes:
            session.add(hero)

        # Commit changes and show heroes
        session.commit()
        for hero in heroes:
            session.refresh(hero)
            print(f"Hero added: {hero}")

def create_heroes_2(): # Defines relations using relationship attributes

    with Session(_engine) as session:

        # Heroes and teams creation
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")
        hero_deadpond = Hero(name="Deadpond", secret_name="Dive Wilson", team=team_z_force)
        hero_rusty_man = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48, team=team_preventers)
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
        heroes = [hero_deadpond, hero_rusty_man, hero_spider_boy]
        for hero in heroes:
            session.add(hero)

        # Commit changes and show heroes
        session.commit()
        for hero in heroes:
            session.refresh(hero)
            print(f"Hero added: {hero}")

def update_relations_1(): # Updates relations via IDs

    with Session(_engine) as session:

        # Query needed objects
        hero_spider_boy = session.exec(select(Hero).where(Hero.name == "Spider-Boy")).one()
        team_preventers = session.exec(select(Team).where(Team.name == "Preventers")).one()

        # Assign Spider-Boy to team Preventers after creation
        hero_spider_boy.team_id = team_preventers.id
        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        print(f"Hero updated: {hero_spider_boy}")

        # Remove Spider-Boy from team Preventers
        hero_spider_boy.team_id = None
        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        print(f"Hero updated: {hero_spider_boy}")

def update_relations_2(): # Updates relations via relationship attributes

    with Session(_engine) as session:

        # Query needed objects
        hero_spider_boy = session.exec(select(Hero).where(Hero.name == "Spider-Boy")).one()
        team_preventers = session.exec(select(Team).where(Team.name == "Preventers")).one()

        # Assign Spider-Boy to team Preventers after creation
        hero_spider_boy.team = team_preventers
        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        print(f"Hero updated: {hero_spider_boy}")

        # Remove Spider-Boy from team Preventers
        hero_spider_boy.team = None
        session.add(hero_spider_boy)
        session.commit()
        session.refresh(hero_spider_boy)
        print(f"Hero updated: {hero_spider_boy}")

def create_more_heroes():

    with Session(_engine) as session:

        hero_black_lion = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
        hero_princess_sure_e = Hero(name="Princess Sure-E", secret_name="Sure-E")
        team_wakaland = Team(
            name="Wakaland",
            headquarters="Wakaland Capital City",
            heroes=[hero_black_lion, hero_princess_sure_e],
        )
        session.add(team_wakaland)
        session.commit()
        session.refresh(team_wakaland)
        print(f"Created new team: \"{team_wakaland.name}\" with heroes: " + ", ".join([f"\"{hero.name}\"" for hero in team_wakaland.heroes]))

        team_preventers = session.exec(select(Team).where(Team.name == "Preventers")).one()
        new_preventers_heroes = [
            Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32),
            Hero(name="Dr. Weird", secret_name="Steve Weird", age=36),
            Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93)
        ]
        for new_preventers_hero in new_preventers_heroes:
            team_preventers.heroes.append(new_preventers_hero)
        session.add(team_preventers)
        session.commit()
        for new_preventers_hero in new_preventers_heroes:
            print(f"New Preventers hero: \"{new_preventers_hero.name}\"")

def print_result(select_function):
    def decorated():
        result = select_function()
        for hero, team in result:
            print("Hero: \"{}\" - Team: \"{}\"".format(
                hero.name if hero is not None else "NULL",
                team.name if team is not None else "NULL"
            ))
        return result
    return decorated

@print_result
def select_heroes_1(): # Version with where
    with Session(_engine) as session:
        return session.exec(select(Hero, Team).where(Hero.team_id == Team.id)).all()

@print_result
def select_heroes_2(): # Version with join
    with Session(_engine) as session:
        return session.exec(select(Hero, Team).join(Team)).all()

@print_result
def select_heroes_3(): # Version with outer join
    with Session(_engine) as session:
        return session.exec(select(Hero, Team).join(Team, isouter=True)).all()

@print_result
def select_heroes_4(): # Print heroes who are part of the Preventers team
    with Session(_engine) as session:
        return session.exec(select(Hero, Team).join(Team).where(Team.name == "Preventers")).all()

def select_heroes_5():
    with Session(_engine) as session:
        hero_spider_boy = session.exec(select(Hero).where(Hero.name == "Spider-Boy")).one()
        print("Hero \"{}\" belongs to {}".format(
            hero_spider_boy.name,
            f"team \"{hero_spider_boy.team.name}\"" if hero_spider_boy.team is not None else "no team"
        ))
        team_preventers = session.exec(select(Team).where(Team.name == "Preventers")).one()
        print(f"Team \"{team_preventers.name}\" has heroes: " + ", ".join([f"\"{hero.name}\"" for hero in team_preventers.heroes]))
