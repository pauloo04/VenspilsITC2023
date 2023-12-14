from app import f_app
from app import socketio, join_room
from app import db
from app import f_app
from flask import url_for
from app.models import Sketch1, Lobby, Player, Sketch2, Painting
import sqlite3
import json
from sqlalchemy import desc
from datetime import timedelta

# Saves first sketch to database
@socketio.on('sketch1')
def sketchSave(arg1, arg2, arg3):
    PlayerID = int(arg1)
    LobbyCode = arg2
    DrawingBlob = arg3
    sketchData = Sketch1(LobbyCode=LobbyCode, PlayerID=PlayerID, DrawingBlob=DrawingBlob)
    db.session.add(sketchData)
    db.session.commit()
    sketchCount = db.session.query(Sketch1.Sketch1ID).filter(Sketch1.LobbyCode == LobbyCode).count()
    players = db.session.query(Lobby.Players).filter(Lobby.LobbyCode == LobbyCode).first()
    players = json.loads(players[0])
    counter = 0
    for key in players:
        if players[key] != None:
            counter += 1
    if counter <= sketchCount:
        return True
    return False


@socketio.on('improve')
def improvementSave(arg1, arg2, arg3):
    PlayerID = int(arg1)
    LobbyCode = arg2
    DrawingBlob = arg3
    sketchData = Sketch2(LobbyCode=LobbyCode, PlayerID=PlayerID, DrawingBlob=DrawingBlob)
    db.session.add(sketchData)
    db.session.commit()
    sketchCount = db.session.query(Sketch2.Sketch2ID).filter(Sketch2.LobbyCode == LobbyCode).count()
    players = db.session.query(Lobby.Players).filter(Lobby.LobbyCode == LobbyCode).first()
    players = json.loads(players[0])
    counter = 0
    for key in players:
        if players[key] != None:
            counter += 1
    if counter <= sketchCount:
        return True
    return False


@socketio.on('painting')
def paintingSave(arg1, arg2, arg3):
    PlayerID = int(arg1)
    LobbyCode = arg2
    DrawingBlob = arg3
    sketchData = Painting(LobbyCode=LobbyCode, PlayerID=PlayerID, DrawingBlob=DrawingBlob)
    db.session.add(sketchData)
    db.session.commit()
    sketchCount = db.session.query(Painting.PaintingID).filter(Painting.LobbyCode == LobbyCode).count()
    players = db.session.query(Lobby.Players).filter(Lobby.LobbyCode == LobbyCode).first()
    players = json.loads(players[0])
    counter = 0
    for key in players:
        if players[key] != None:
            counter += 1
    if counter <= sketchCount:
        return True
    return False


@socketio.on("redirectToVote1")
def redirectToVote(lobbyCode):
    socketio.emit('redirect', {'url': url_for("voteSketch")}, to=lobbyCode)    


@socketio.on("redirectToVote2")
def redirectToVote2(lobbyCode):
    socketio.emit('redirect', {'url': url_for("voteSketch2")}, to=lobbyCode)   


@socketio.on("redirectToVote3")
def redirectToVote3(lobbyCode):
    socketio.emit('redirect', {'url': url_for("votePainting")}, to=lobbyCode)   


@socketio.on("requestPNG")
def send_png(arg1, arg2, arg3):
    images = None
    if arg3 == "VoteSketch":
        with sqlite3.connect("C:\\Users\\matis\\Documents\\VSC Projects\\vitc2023\\Vitc2023\\instance\\idedraw.db") as con:
            images = {}
            for x in con.execute(f"""SELECT Sketch1ID, DrawingBlob FROM Sketch1 WHERE LobbyCode == '{arg1}' AND PlayerID != {str(arg2)}"""):
                images[str(x[0])] = x[1]
    elif arg3 == "VoteImprovement":
        with sqlite3.connect("C:\\Users\\matis\\Documents\\VSC Projects\\vitc2023\\Vitc2023\\instance\\idedraw.db") as con:
            images = {}
            for x in con.execute(f"""SELECT Sketch2ID, DrawingBlob FROM Sketch2 WHERE LobbyCode == '{arg1}' AND PlayerID != {str(arg2)}"""):
                images[str(x[0])] = x[1]
    elif arg3 == "VotePainting":
        with sqlite3.connect("C:\\Users\\matis\\Documents\\VSC Projects\\vitc2023\\Vitc2023\\instance\\idedraw.db") as con:
            images = {}
            for x in con.execute(f"""SELECT PaintingID, DrawingBlob FROM Painting WHERE LobbyCode == '{arg1}' AND PlayerID != {str(arg2)}"""):
                images[str(x[0])] = x[1]
    elif arg3 == "Improvement":
        with sqlite3.connect("C:\\Users\\matis\\Documents\\VSC Projects\\vitc2023\\Vitc2023\\instance\\idedraw.db") as con:
            for x in con.execute(f"""SELECT DrawingBlob FROM Sketch1 WHERE LobbyCode == '{arg1}' ORDER BY AvgVote DESC LIMIT 1"""):
                images = x[0]
                break
    elif arg3 == "Painting":
        with sqlite3.connect("C:\\Users\\matis\\Documents\\VSC Projects\\vitc2023\\Vitc2023\\instance\\idedraw.db") as con:
            for x in con.execute(f"""SELECT DrawingBlob FROM Sketch2 WHERE LobbyCode == '{arg1}' ORDER BY AvgVote DESC LIMIT 1"""):
                images = x[0]
                break
    return images
    

# When player has voted on a certain sketch, record this event to DB
@socketio.on('vote1')
def record_vote1(arg1, arg2):
    id = int(arg1)
    vote = int(arg2)
    db.session.query(Sketch1).filter(Sketch1.Sketch1ID == id).update({"VoteTotal": Sketch1.VoteTotal + vote})
    db.session.query(Sketch1).filter(Sketch1.Sketch1ID == id).update({"Voters": Sketch1.Voters + 1})
    db.session.commit()


@socketio.on('vote2')
def record_vote2(arg1, arg2):
    id = int(arg1)
    vote = int(arg2)
    db.session.query(Sketch2).filter(Sketch2.Sketch2ID == id).update({"VoteTotal": Sketch2.VoteTotal + vote})
    db.session.query(Sketch2).filter(Sketch2.Sketch2ID == id).update({"Voters": Sketch2.Voters + 1})
    db.session.commit()


@socketio.on('vote3')
def record_vote3(arg1, arg2):
    id = int(arg1)
    vote = int(arg2)
    db.session.query(Painting).filter(Painting.PaintingID == id).update({"VoteTotal": Painting.VoteTotal + vote})
    db.session.query(Painting).filter(Painting.PaintingID == id).update({"Voters": Painting.Voters + 1})
    db.session.commit()


@socketio.on('lobbyConnect')
def lobbyConnect(arg1):
    lobbyCode = str(arg1)
    join_room(lobbyCode)
    lobbyData = Lobby.query.filter(Lobby.LobbyCode == lobbyCode).first()
    lobbyData = lobbyData.to_dict()
    socketio.emit("sendLobbyData", lobbyData, to=lobbyCode)


@socketio.on('lobbyData')
def lobbyData(lobbyCode):
    lobbyData = Lobby.query.filter(Lobby.LobbyCode == lobbyCode).first()
    lobbyData = lobbyData.to_dict()
    socketio.emit("sendLobbyData", lobbyData, to=lobbyCode)

@socketio.on("joinRoom")
def joinRoom(lobbyCode):
    join_room(lobbyCode)


@socketio.on("returnPlayerData")
def returnPlayerData(arg1):
    result = (Player.query.filter(Player.PlayerID == int(arg1)).first()).to_dict()
    return result["Username"]


@socketio.on("checkPlayerCount")
def checkPlayerCount(arg1):
    if Lobby.query.filter(Lobby.LobbyCode == arg1).first():
        row = db.session.query(Lobby.Players).filter(Lobby.LobbyCode == arg1).first()
        x = json.loads(row[0])
        count = 0
        for key in x:
            if count >= 3:
                return True
            if x[key] != None:
                count += 1
        else:
            return False


@socketio.on("checkVotes1")
def checkVotes1(arg1):
    count = -1
    if Lobby.query.filter(Lobby.LobbyCode == str(arg1)).first():
        row = db.session.query(Lobby.Players).filter(Lobby.LobbyCode == str(arg1)).first()
        x = json.loads(row[0])
        for key in x:
            if x[key] != None:
                count += 1
    rows = db.session.query(Sketch1.Voters).filter(Sketch1.LobbyCode == str(arg1)).all()
    for row in rows:
        if row[0] < count:
            return False
    else:
        return True


@socketio.on("checkVotes2")
def checkVotes2(arg1):
    count = -1
    if Lobby.query.filter(Lobby.LobbyCode == arg1).first():
        row = db.session.query(Lobby.Players).filter(Lobby.LobbyCode == arg1).first()
        x = json.loads(row[0])
        for key in x:
            if x[key] != None:
                count += 1
    rows = db.session.query(Sketch2.Voters).filter(Sketch2.LobbyCode == arg1).all()
    for row in rows:
        if row[0] < count:
            return False
    else:
        return True


@socketio.on("checkVotes3")
def checkVotes3(arg1):
    count = -1
    if Lobby.query.filter(Lobby.LobbyCode == arg1).first():
        row = db.session.query(Lobby.Players).filter(Lobby.LobbyCode == arg1).first()
        x = json.loads(row[0])
        for key in x:
            if x[key] != None:
                count += 1
    rows = db.session.query(Painting.Voters).filter(Painting.LobbyCode == arg1).all()
    for row in rows:
        if row[0] < count:
            return False
    else:
        return True


@socketio.on("redirectToSketch")
def redirectToSketch(lobbyCode):
    socketio.emit('redirect', {'url': url_for("sketch")}, to=lobbyCode)


@socketio.on("redirectToImprove")
def redirectToImprove(lobbyCode):
    print("Redirect to improve", flush=True)
    for id in db.session.query(Sketch1.Sketch1ID).filter(Sketch1.LobbyCode == lobbyCode):
        voteTotal = db.session.query(Sketch1.VoteTotal).filter(Sketch1.LobbyCode == lobbyCode, Sketch1.Sketch1ID == id[0])[0]
        voters = db.session.query(Sketch1.Voters).filter(Sketch1.LobbyCode == lobbyCode, Sketch1.Sketch1ID == id[0])[0]
        avgVote = round(voteTotal[0] / voters[0], 4)
        db.session.query(Sketch1).filter(Sketch1.LobbyCode == lobbyCode, Sketch1.Sketch1ID == id[0]).update({"AvgVote": avgVote})
    highestVoteID = db.session.query(Sketch1.Sketch1ID).filter(Sketch1.LobbyCode == lobbyCode).order_by(desc(Sketch1.AvgVote)).first()[0]
    db.session.query(Lobby).filter(Lobby.LobbyCode == lobbyCode).update({"Sketch1WinID": highestVoteID})
    db.session.commit()
    socketio.emit('redirect', {'url': url_for("improve")}, to=lobbyCode)


@socketio.on("redirectToPaint")
def redirectToPaint(lobbyCode):
    for id in db.session.query(Sketch2.Sketch2ID).filter(Sketch2.LobbyCode == lobbyCode):
        voteTotal = db.session.query(Sketch2.VoteTotal).filter(Sketch2.LobbyCode == lobbyCode, Sketch2.Sketch2ID == id[0])[0]
        voters = db.session.query(Sketch2.Voters).filter(Sketch2.LobbyCode == lobbyCode, Sketch2.Sketch2ID == id[0])[0]
        avgVote = round(voteTotal[0] / voters[0], 4)
        db.session.query(Sketch2).filter(Sketch2.LobbyCode == lobbyCode, Sketch2.Sketch2ID == id[0]).update({"AvgVote": avgVote})
    highestVoteID = db.session.query(Sketch2.Sketch2ID).filter(Sketch2.LobbyCode == lobbyCode).order_by(desc(Sketch2.AvgVote)).first()[0]
    db.session.query(Lobby).filter(Lobby.LobbyCode == lobbyCode).update({"Sketch2WinID": highestVoteID})
    db.session.commit()
    socketio.emit('redirect', {'url': url_for("paint")}, to=lobbyCode)


@socketio.on("redirectToResults")
def redirectToResults(lobbyCode):
    for id in db.session.query(Painting.PaintingID).filter(Painting.LobbyCode == lobbyCode):
        voteTotal = db.session.query(Painting.VoteTotal).filter(Painting.LobbyCode == lobbyCode, Painting.PaintingID == id[0])[0]
        voters = db.session.query(Painting.Voters).filter(Painting.LobbyCode == lobbyCode, Painting.PaintingID == id[0])[0]
        avgVote = round(voteTotal[0] / voters[0], 4)
        db.session.query(Painting).filter(Painting.LobbyCode == lobbyCode, Painting.PaintingID == id[0]).update({"AvgVote": avgVote})
    highestVoteID = db.session.query(Painting.PaintingID).filter(Painting.LobbyCode == lobbyCode).order_by(desc(Painting.AvgVote)).first()[0]
    db.session.query(Lobby).filter(Lobby.LobbyCode == lobbyCode).update({"PaintingWinID": highestVoteID})
    db.session.commit()
    socketio.emit('redirect', {'url': url_for("results")}, to=lobbyCode)   


@socketio.on("requestResults")
def getResults(lobbyCode):
    results = {}
    ids = None
    for x in db.session.query(Lobby.Sketch1WinID, Lobby.Sketch2WinID, Lobby.PaintingWinID).filter(Lobby.LobbyCode == lobbyCode):
        ids = x
    with sqlite3.connect("C:\\Users\\matis\\Documents\\VSC Projects\\vitc2023\\Vitc2023\\instance\\idedraw.db") as con:
        for x in con.execute(f"""SELECT DrawingBlob, AvgVote FROM Sketch1 WHERE Sketch1ID == {ids[0]}"""):
            results["sketch1Image"] = x[0]
            results["sketch1Vote"] = x[1]
            break
        for x in con.execute(f"""SELECT DrawingBlob, AvgVote FROM Sketch2 WHERE Sketch2ID == {ids[1]}"""):
            results["sketch2Image"] = x[0]
            results["sketch2Vote"] = x[1]
            break
        for x in con.execute(f"""SELECT DrawingBlob, AvgVote FROM Painting WHERE PaintingID == {ids[2]}"""):
            results["paintingImage"] = x[0]
            results["paintingVote"] = x[1]
            break
        for x in con.execute(f"""SELECT Username FROM Player WHERE PlayerID == (SELECT Sketch1.PlayerID FROM Sketch1 WHERE Sketch1.Sketch1ID == {ids[0]})"""):
            results["sketch1Author"] = x[0]
            break
        for x in con.execute(f"""SELECT Username FROM Player WHERE Player.PlayerID == (SELECT Sketch2.PlayerID FROM Sketch2 WHERE Sketch2.Sketch2ID == {ids[1]})"""):
            results["sketch2Author"] = x[0]
            break
        for x in con.execute(f"""SELECT Username FROM Player WHERE Player.PlayerID == (SELECT Painting.PlayerID FROM Painting WHERE Painting.PaintingID == {ids[2]})"""):
            results["paintingAuthor"] = x[0]
            break
    return results
    

@socketio.on("playerReady")
def playerReady(lobbyCode, playerID):
    socketio.emit("playerReadyID", playerID, to=lobbyCode)


@socketio.on("playerNotReady")
def playerReady(lobbyCode, playerID):
    socketio.emit("playerNotReadyID", playerID, to=lobbyCode)


@socketio.on("getTimer")
def getTimer(stage, lobbyCode):
    if stage == "Sketch1":
        data = db.session.query(Lobby.Sketch1StartTime).filter(Lobby.LobbyCode==lobbyCode).first()[0]
    elif stage == "Sketch2":
        data = db.session.query(Lobby.Sketch2StartTime).filter(Lobby.LobbyCode==lobbyCode).first()[0]
    elif stage == "Painting":
        data = db.session.query(Lobby.PaintingStartTime).filter(Lobby.LobbyCode==lobbyCode).first()[0]
    row = db.session.query(Lobby.RoundLength).filter(Lobby.LobbyCode==lobbyCode).first()[0]
    if row[0] == "1":
        data = data + timedelta(minutes=1)
    elif row[0] == "2":
        data = data + timedelta(minutes=2)
    else:
        data = data + timedelta(minutes=3)
    return data.strftime("%Y-%m-%d %H:%M:%S")


@socketio.on("getPrompt")
def getPrompt(lobbyCode):
    return db.session.query(Lobby.Prompt).filter(Lobby.LobbyCode==lobbyCode).first()[0]


if __name__ == "__main__":
    with f_app.app_context():
        db.create_all()
    socketio.run(f_app)