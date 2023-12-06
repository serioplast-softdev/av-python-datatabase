#!/usr/bin/env python3

import db
import model

def main():
    db.setup()

    db.create_heroes_2()
    db.update_relations_2()
    db.create_more_heroes()

    db.select_heroes_1()
    db.select_heroes_2()
    db.select_heroes_3()
    db.select_heroes_4()
    db.select_heroes_5()

if __name__ == "__main__":
    main()
