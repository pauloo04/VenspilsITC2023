from flask import render_template, flash, redirect, url_for, flash, send_from_directory, request
from app import f_app, db
from app.forms import JoinForm, PlayForm
from app.models import Lobby, Player
from sqlalchemy import func
import string
import random
import json

prompts = [
            "Combine an elephant with a bike",
            "Huston, we have a problem",
            "Combine a couch with a surf board",
            "A vegetable house",
            "A clock made from glasses",
            "What would make finding a tv remote easier?",
            "Happiness",
            "Sadness",
            "A magnetic book",
            "A dollar tree",
            "A reusable fruit straw",
            "Bigger is better",
            "What is useless?",
            "Add a bar stand to a fruit",
            "Empire state of mind",
            "Fyling conversation",
            "How does the future of north pole look like?",
            "Reverse a flower vase",
            "A chopstick spoon",
            "A pencilpen",
            "Reuse a shelf",
            "Breathing icon",
            "A butter glue",
            "Upside down beer bottle",
            "I'm the king of the world!",
            "There's no place like home.",
            "Upside down Birthday cake",
            "Cactus with a cowboy hat",
            "A House with a round roof",
            "A banana in a boat",
            "A Cucumber playing a Guitar",
            "A Flower with candy inside",
            "A Racing car",
            "A Spider swimming in the river",
            "A crab building a sand castle",
            "A table in the sea",
            "Kangaroos getting married",
            "An Orange throwing a ball",
            "Framed Christmas Tree",
            "A Frog with glasses",
            "A Lemon on top of Mount Everest",
            "A Butterfly flying to the Sun",
            "A Mannequin head on fire",
            "A Goat playing video games",
            "A pen as a foot",
            "A polar bear harvesting coconuts",
            "A Giraffe drinking wine",
            "Hot air baloon as a light bulb",
            "A Scarecrow in a dress",
            "A Pineapple driving a car"
]

@f_app.after_request
def add_security_headers(resp):
    resp.headers['Access-Control-Allow-Private-Network'] = 'true'
    return resp

# Home page links
@f_app.route("/", methods=['GET', 'POST'])
def home():
    form = PlayForm()
    if form.validate_on_submit():
        playerData = Player(Username=form.username.data)
        db.session.add(playerData)
        db.session.commit()
        lobbyCode = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        while (Lobby.query.filter(Lobby.LobbyCode == lobbyCode).first() is not None):
            lobbyCode = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        if (Lobby.query.filter(Lobby.LobbyCode == lobbyCode).first() is None):
            Players = {"Player1ID":playerData.PlayerID,
            "Player2ID":None,
            "Player3ID":None,
            "Player4ID":None,
            "Player5ID":None,
            "Player6ID":None,
            "Player7ID":None,
            "Player8ID":None,
            }
            Players = json.dumps(Players)
            lobbyData = Lobby(Players=Players, LobbyCode=lobbyCode, RoundLength=form.roundLength.data, Prompt=random.choice(prompts))
            db.session.add(lobbyData)
            db.session.commit()
        return redirect(url_for("lobby", lobbyCode=lobbyCode, playerID=playerData.PlayerID))
    return render_template("home.html", form=form)


@f_app.route("/join", methods=['GET', 'POST'])
def join():
    form = JoinForm()
    if form.validate_on_submit():
        playerData = Player(Username=form.username.data)
        db.session.add(playerData)
        db.session.commit()
        lobbyCode = form.lobby.data
        if Lobby.query.filter(Lobby.LobbyCode == lobbyCode).first():
            row = db.session.query(Lobby.Players).filter(Lobby.LobbyCode == lobbyCode).first()
            x = json.loads(row[0])
            print(x, flush=True)
            for key in x:
                if x[key] == None:
                    x[key] = playerData.PlayerID
                    break
            else:
                flash("Lobby is full! Please try to join another lobby!", category='danger')
                return render_template("home.html", form=form)
            db.session.query(Lobby).filter(Lobby.LobbyCode == lobbyCode).update({"Players": json.dumps(x)})
            db.session.commit()
            return redirect(url_for("lobby", lobbyCode=lobbyCode, playerID=playerData.PlayerID))
        else:
            flash("Lobby code is not valid! Try to join again or create your own lobby!", category='danger')
    return render_template("join.html", form=form)


@f_app.route("/lobby", methods=['GET', 'POST'])
def lobby():
    lobbyCode = request.args["lobbyCode"]
    playerID = request.args["playerID"]
    return render_template("lobby.html", lobbyCode=lobbyCode, playerID=playerID)


# Drawing links
@f_app.route("/draw/sketch", methods=['GET', 'POST'])
def sketch():
    playerID = request.args['playerID']
    lobbyCode= request.args["lobbyCode"]
    if db.session.query(Lobby.Sketch1StartTime).filter(Lobby.LobbyCode == lobbyCode).first()[0] is None:
        db.session.query(Lobby).filter(Lobby.LobbyCode == lobbyCode).update({"Sketch1StartTime": func.now()})
        db.session.commit()
    return render_template("sketch.html", playerID=playerID, lobbyCode=lobbyCode)


@f_app.route("/draw/improve", methods=['GET', 'POST'])
def improve():
    playerID = request.args['playerID']
    lobbyCode= request.args["lobbyCode"]
    if db.session.query(Lobby.Sketch2StartTime).filter(Lobby.LobbyCode == lobbyCode).first()[0] is None:
        db.session.query(Lobby).filter(Lobby.LobbyCode == lobbyCode).update({"Sketch2StartTime": func.now()})
        db.session.commit()
    return render_template("improve.html", playerID=playerID, lobbyCode=lobbyCode)


@f_app.route("/draw/paint", methods=['GET', 'POST'])
def paint():
    playerID = request.args['playerID']
    lobbyCode= request.args["lobbyCode"]
    if db.session.query(Lobby.PaintingStartTime).filter(Lobby.LobbyCode == lobbyCode).first()[0] is None:
        db.session.query(Lobby).filter(Lobby.LobbyCode == lobbyCode).update({"PaintingStartTime": func.now()})
        db.session.commit()
    return render_template("paint.html", playerID=playerID, lobbyCode=lobbyCode)


# Voting links
@f_app.route("/vote/sketch", methods=['GET', 'POST'])
def voteSketch():
    playerID = request.args['playerID']
    lobbyCode= request.args["lobbyCode"]
    return render_template("voting.html", playerID=playerID, lobbyCode=lobbyCode)


@f_app.route("/vote/improvement", methods=['GET', 'POST'])
def voteSketch2():
    playerID = request.args['playerID']
    lobbyCode= request.args["lobbyCode"]
    return render_template("voting.html", playerID=playerID, lobbyCode=lobbyCode)


@f_app.route("/vote/painting", methods=['GET', 'POST'])
def votePainting():
    playerID = request.args['playerID']
    lobbyCode= request.args["lobbyCode"]
    return render_template("voting.html", playerID=playerID, lobbyCode=lobbyCode)


# Result links
@f_app.route("/results", methods=['GET', 'POST'])
def results():
    lobbyCode= request.args["lobbyCode"]
    return render_template("results.html", lobbyCode=lobbyCode)


# Static folder link
@f_app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)