#!/usr/bin/env python3

import db
import model

def main():
    db.setup()
    db.create_heroes()

if __name__ == "__main__":
    main()
