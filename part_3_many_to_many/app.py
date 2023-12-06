#!/usr/bin/env python3

import db
import model

def main():
    db.setup()
    db.create_heroes()
    db.update_heroes()
    db.revert_heroes()

if __name__ == "__main__":
    main()
