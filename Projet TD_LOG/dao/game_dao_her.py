from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////tmp/tdlog.db', echo=True, future=True)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)


class GameEntity(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    players = relationship("PlayerEntity", back_populates="game",
                           cascade="all, delete-orphan")


class PlayerEntity(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
    game = relationship("GameEntity", back_populates="players")
    battle_field = relationship("BattlefieldEntity",
                                back_populates="player",
                                uselist=False, cascade="all, delete-orphan")


class BattlefieldEntity(Base):
    __tablename__ = 'battlefield'
    id = Column(Integer)
    min_x = Column(Integer)
    min_y = Column(Integer)
    min_z = Column(Integer)
    max_x = Column(Integer)
    max_y = Column(Integer)
    max_z = Column(Integer)
    max_power = Column(Integer)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    player = relationship("PlayerEntity", back_populates="battlefield")
    vessel = relationship("VesselEntity",
                          back_populates="battlefield",
                          uselist=False, cascade="all, delete-orphan")


class VesselEntity(Base):
    __tablename__ = 'vessel'
    id = Column(Integer, primary_key=True)
    coord_x = Column(Integer)
    coord_y = Column(Integer)
    coord_z = Column(Integer)
    hits_to_be_destroyed = Column(Integer)
    type = Column(Integer)
    battle_field_id = Column(Integer, ForeignKey("battlefield.id"), nullable=False)
    battlefield = relationship("BattlefieldEntity", back_populates="vessel")
    weapon = relationship("WeaponEntity",
                          back_populates="vessel",
                          uselist=False, cascade="all, delete-orphan")
class WeaponEntity(Base):
    __tablename__ = 'weapon'
    id = Column(Integer, primary_key=True)
    # ammunitions = Column(Integer)
    range = Column(Integer)
    type = Column(Integer)
    vessel_id = Column(Integer, ForeignKey("vessel.id"), nullable=False)
    vessel = relationship("vessel", back_populates="weapon")

#################################################################################################################

class GameDao:
    def __init__(self):
        Base.metadata.create_all()
        self.db_session = Session()

    def create_game(self, game: Game) -> int:
        game_entity = map_to_game_entity(game)
        self.db_session.add(game_entity)
        self.db_session.commit()
        return game_entity.id

    def find_game(self, game_id: int) -> Game:
        stmt = select(GameEntity).where(GameEntity.id == game_id)
        game_entity = self.db_session.scalars(stmt).one()
        return map_to_game(game_entity)

    def create_player(self, player: Player, game_id) -> int:
        player_entity = map_to_player_entity(player, game_id)
        self.db_session.add(player_entity)
        self.db_session.commit()
        return player_entity.id

    def find_vessel(self, vessel_id: int) -> Vessel:
        stmt = select(VesselEntity).where(VesselEntity.id == vessel_id)
        vessel_entity = self.db_session.scalars(stmt).one()
        return map_to_vessel(vessel_entity)

    def find_player(self, player_id: int) -> Player:
        stmt = select(PlayerEntity).where(PlayerEntity.id == player_id)
        player_entity = self.db_session.scalars(stmt).one()
        return map_to_player(player_entity)