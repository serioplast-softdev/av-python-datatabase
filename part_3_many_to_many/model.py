from typing import List, Optional

from sqlmodel import SQLModel, Relationship, Field

class HeroTeamLink(SQLModel, table=True):
    team_id: Optional[int] = Field(default=None, foreign_key="team.id", primary_key=True)
    hero_id: Optional[int] = Field(default=None, foreign_key="hero.id", primary_key=True)

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str
    heroes: List["Hero"] = Relationship(back_populates="teams", link_model=HeroTeamLink)

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)
    teams: Optional[Team] = Relationship(back_populates="heroes", link_model=HeroTeamLink)
