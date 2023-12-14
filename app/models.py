from sqlalchemy import DateTime
from app import db
from sqlalchemy_serializer import SerializerMixin


class Sketch1(db.Model):
    __tablename__ = 'Sketch1'
    Sketch1ID = db.Column("Sketch1ID", db.Integer(), primary_key=True)
    LobbyCode = db.Column("LobbyCode", db.Text(), nullable=False)
    PlayerID = db.Column("PlayerID", db.Integer(), nullable=False)
    VoteTotal = db.Column("VoteTotal", db.Float(), nullable=True)
    Voters = db.Column("Voters", db.Integer(), nullable=True)
    AvgVote = db.Column("AvgVote", db.Float(), nullable=True)
    DrawingBlob = db.Column("DrawingBlob", db.Text(), nullable=False)
    
    def __init__(self, LobbyCode, PlayerID, DrawingBlob, AvgVote=0, VoteTotal=0, Voters=0):
        self.LobbyCode = LobbyCode
        self.PlayerID = PlayerID
        self.AvgVote = AvgVote
        self.VoteTotal = VoteTotal
        self.Voters = Voters
        self.DrawingBlob = DrawingBlob


class Sketch2(db.Model):
    __tablename__ = 'Sketch2'
    Sketch2ID = db.Column("Sketch2ID", db.Integer(), primary_key=True)
    LobbyCode = db.Column("LobbyCode", db.Text(), nullable=False)
    PlayerID = db.Column("PlayerID", db.Integer(), nullable=False)
    VoteTotal = db.Column("VoteTotal", db.Float(), nullable=True)
    Voters = db.Column("Voters", db.Integer(), nullable=True)
    AvgVote = db.Column("AvgVote", db.Float(), nullable=True)
    DrawingBlob = db.Column("DrawingBlob", db.Text(), nullable=False)
    
    def __init__(self, LobbyCode, PlayerID, DrawingBlob, AvgVote=0, VoteTotal=0, Voters=0):
        self.LobbyCode = LobbyCode
        self.PlayerID = PlayerID
        self.AvgVote = AvgVote
        self.VoteTotal = VoteTotal
        self.Voters = Voters
        self.DrawingBlob = DrawingBlob


class Painting(db.Model):
    __tablename__ = 'Painting'
    PaintingID = db.Column("PaintingID", db.Integer(), primary_key=True)
    LobbyCode = db.Column("LobbyCode", db.Text(), nullable=False)
    PlayerID = db.Column("PlayerID", db.Integer(), nullable=False)
    VoteTotal = db.Column("VoteTotal", db.Float(), nullable=True)
    Voters = db.Column("Voters", db.Integer(), nullable=True)
    AvgVote = db.Column("AvgVote", db.Float(), nullable=True)
    DrawingBlob = db.Column("DrawingBlob", db.Text(), nullable=False)
    
    def __init__(self, LobbyCode, PlayerID, DrawingBlob, AvgVote=0, VoteTotal=0, Voters=0):
        self.LobbyCode = LobbyCode
        self.PlayerID = PlayerID
        self.AvgVote = AvgVote
        self.VoteTotal = VoteTotal
        self.Voters = Voters
        self.DrawingBlob = DrawingBlob


class Lobby(db.Model, SerializerMixin):
    __tablename__ = 'Lobby'
    LobbyID = db.Column("LobbyID", db.Integer(), primary_key=True)
    LobbyCode = db.Column("LobbyCode", db.Text(), nullable=False, unique=True)
    RoundLength = db.Column("RoundLength", db.Text(), nullable=False)
    Prompt = db.Column("Prompt", db.Text(), nullable=False)
    Sketch1StartTime = db.Column("Sketch1StartTime", DateTime, nullable=True)
    Sketch2StartTime = db.Column("Sketch2StartTime", DateTime, nullable=True)
    PaintingStartTime = db.Column("PaintingStartTime", DateTime, nullable=True)
    Sketch1WinID = db.Column("Sketch1WinID", db.Integer(), nullable=True)
    Sketch2WinID = db.Column("Sketch2WinID", db.Integer(), nullable=True)
    PaintingWinID = db.Column("PaintingWinID", db.Integer(), nullable=True)
    Players= db.Column("Players", db.Text(), nullable=False)

    def __init__(self, LobbyCode, Players, RoundLength, Prompt):
        self.LobbyCode = LobbyCode
        self.Players = Players
        self.RoundLength = RoundLength
        self.Prompt = Prompt

    def return_all_players():
        return Lobby.Players


class Player(db.Model, SerializerMixin):
    __tablename__ = 'Player'
    PlayerID = db.Column("PlayerID", db.Integer(), primary_key=True)
    Username = db.Column("Username", db.Text(), nullable=False)
    
    def __init__(self, Username):
        self.Username = Username