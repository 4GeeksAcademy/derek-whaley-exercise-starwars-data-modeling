from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    UniqueConstraint,
    Table,
)
from sqlalchemy.orm import relationship, declarative_base
from eralchemy2 import render_er

# Base model definition
Base = declarative_base()

# Utility function for timestamps
def get_current_time():
    return datetime.now(timezone.utc)


# Junction Tables for Many-to-Many Relationships
film_characters = Table(
    "film_characters",
    Base.metadata,
    Column("film_id", Integer, ForeignKey("films.id"), primary_key=True),
    Column("character_id", Integer, ForeignKey("characters.id"), primary_key=True),
)

film_planets = Table(
    "film_planets",
    Base.metadata,
    Column("film_id", Integer, ForeignKey("films.id"), primary_key=True),
    Column("planet_id", Integer, ForeignKey("planets.id"), primary_key=True),
)

film_vehicles = Table(
    "film_vehicles",
    Base.metadata,
    Column("film_id", Integer, ForeignKey("films.id"), primary_key=True),
    Column("vehicle_id", Integer, ForeignKey("vehicles.id"), primary_key=True),
)


# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    name = Column(String(150), nullable=False)
    joined_at = Column(DateTime, default=get_current_time, nullable=False)

    # Relationships
    favorites = relationship("Favorite", cascade="all, delete", back_populates="user")


# Planet Model
class Planet(Base):
    __tablename__ = "planets"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    climate = Column(String(50), nullable=False)
    terrain = Column(String(50), nullable=False)
    population = Column(String(50), nullable=False)
    gravity = Column(String(50), nullable=False)
    orbital_period = Column(String(50), nullable=False)
    rotation_period = Column(String(50), nullable=False)
    surface_water = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=get_current_time, nullable=False)
    updated_at = Column(DateTime, onupdate=get_current_time)

    # Relationships
    favorites = relationship("Favorite", cascade="all, delete", back_populates="planet")
    films = relationship("Film", secondary=film_planets, back_populates="planets")


# Vehicle Model
class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    vehicle_class = Column(String(50), nullable=False)
    manufacturer = Column(String(100), nullable=False)
    length = Column(String(50), nullable=False)
    cost = Column(String(50), nullable=False)
    crew = Column(String(50), nullable=False)
    max_speed = Column(String(50), nullable=False)
    cargo_capacity = Column(String(50), nullable=False)
    consumables = Column(String(50), nullable=False)
    url = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=get_current_time, nullable=False)
    updated_at = Column(DateTime, onupdate=get_current_time)

    # Relationships
    favorites = relationship("Favorite", cascade="all, delete", back_populates="vehicle")
    films = relationship("Film", secondary=film_vehicles, back_populates="vehicles")


# Character Model
class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    gender = Column(String(50), nullable=False)
    birth_year = Column(String(50), nullable=False)
    eye_color = Column(String(50), nullable=False)
    hair_color = Column(String(50), nullable=False)
    height = Column(String(10), nullable=False)
    mass = Column(String(10), nullable=False)
    skin_color = Column(String(50), nullable=False)
    homeworld = Column(String(100), nullable=False)
    url = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=get_current_time, nullable=False)
    updated_at = Column(DateTime, onupdate=get_current_time)

    # Relationships
    favorites = relationship("Favorite", cascade="all, delete", back_populates="character")
    films = relationship("Film", secondary=film_characters, back_populates="characters")


# Film Model
class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    episode_id = Column(Integer, nullable=False)
    director = Column(String(100), nullable=False)
    producer = Column(String(200), nullable=False)
    release_date = Column(DateTime, nullable=False)
    opening_crawl = Column(String, nullable=True)

    # Relationships
    characters = relationship("Character", secondary=film_characters, back_populates="films")
    planets = relationship("Planet", secondary=film_planets, back_populates="films")
    vehicles = relationship("Vehicle", secondary=film_vehicles, back_populates="films")


# Species Model
class Species(Base):
    __tablename__ = "species"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    classification = Column(String(50), nullable=False)
    designation = Column(String(50), nullable=False)
    average_height = Column(String(50), nullable=False)
    average_lifespan = Column(String(50), nullable=False)
    language = Column(String(50), nullable=False)
    homeworld_id = Column(Integer, ForeignKey("planets.id"), nullable=True)

    # Relationships
    homeworld = relationship("Planet", backref="species")


# Droid Model
class Droid(Base):
    __tablename__ = "droids"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    model = Column(String(50), nullable=False)
    manufacturer = Column(String(100), nullable=False)
    primary_function = Column(String(50), nullable=False)
    height = Column(String(10), nullable=False)
    language = Column(String(50), nullable=False)


# Favorite Model
class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    planet_id = Column(Integer, ForeignKey("planets.id"), nullable=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=True)

    # Relationships
    user = relationship("User", back_populates="favorites")
    planet = relationship("Planet", back_populates="favorites")
    vehicle = relationship("Vehicle", back_populates="favorites")
    character = relationship("Character", back_populates="favorites")


# Generate diagram
render_er(Base, "diagram.png")