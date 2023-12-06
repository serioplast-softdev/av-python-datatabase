#!/usr/bin/env python3

import db
import model

def run_queries():
    db.get_all_heroes()

    deadpond = db.get_hero_by_name("Deadpond")
    assert deadpond is None or deadpond.name == "Deadpond"

    db.get_heroes_older_than(35)
    db.get_heroes_between_age(20, 40)
    db.get_heroes_younger_or_older_than(30, 70)

    deadpond = db.get_deadpond()
    assert deadpond is not None and deadpond.name == "Deadpond"

    third_hero = db.get_hero_by_id(3)
    assert third_hero is None or third_hero.id == 3

    print("Showing three heroes per page, from page 1 to page 5")
    for page_number in range(1, 6):
        page_heroes = db.get_heroes_page(page_number, 3)
        print(f"Page #{page_number}: ", end="")
        print(", ".join((hero.name for hero in page_heroes)) if page_heroes else "No heroes.")

def main():
    db.setup()
    db.create_heroes()
    db.update_heroes()
    db.delete_heroes()
    run_queries()

if __name__ == "__main__":
    main()
