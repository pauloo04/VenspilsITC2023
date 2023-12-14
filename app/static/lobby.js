var socket = io.connect()

let gtg = false;
let onwPlaceID;

window.onload = function() {
    document.getElementById("lobbyCode").innerHTML = lobbyCode
    socket.emit("lobbyConnect", lobbyCode)
    document.getElementById("ready").addEventListener("click", function() {
        var button = document.getElementById("ready")
        if (button.innerHTML == "READY"){
            document.getElementById("p" + onwPlaceID + "_indicator").style.backgroundColor = "limegreen"
            button.innerHTML = "NOT READY"
            socket.emit("playerReady", lobbyCode, playerID)
        }
        else if (button.innerHTML == "NOT READY") {
            document.getElementById("p" + onwPlaceID + "_indicator").style.backgroundColor = "#ffe433"
            button.innerHTML = "READY"
            socket.emit("playerNotReady", lobbyCode, playerID)
        }
    })

    document.getElementById('start').addEventListener("click", async function() {
        await new Promise(resolve => {
            socket.emit("checkPlayerCount", lobbyCode, (bool) => {
                if (bool){
                    gtg = true;
                }
                    resolve(bool)
            })
        })
        if (gtg) {
            socket.emit("redirectToSketch", lobbyCode)
        }
        else {
            alert("Not enough players! There needs to be at least 3 players in the lobby!")
        }
    })
}

socket.on("redirect", function(url){
    window.location.href = url["url"] + "?lobbyCode=" + lobbyCode + "&playerID=" + playerID
})

socket.on("playerReadyID", async function(readyPlayerID){
    await new Promise(resolve => {
        socket.emit("returnPlayerData", readyPlayerID, (username) => {
            for(i=2; i<=8; i++){
                if (document.getElementById("p" + i.toString() + "name").innerHTML == username) {
                    document.getElementById("p" + i + "_indicator").style.backgroundColor = "limegreen"
                    break
                }
            }
            resolve(true)
        })
    })
})

socket.on("playerNotReadyID", async function(notReadyPlayerID){
    await new Promise(resolve => {
        socket.emit("returnPlayerData", notReadyPlayerID, (username) => {
            for(i=2; i<=8; i++){
                if (document.getElementById("p" + i.toString() + "name").innerHTML == username) {
                    document.getElementById("p" + i + "_indicator").style.backgroundColor = "#ffe433"
                    resolve(username)
                }
            }
        })
    })
})

socket.on("sendLobbyData", async function(data) {
    players = JSON.parse(data.Players)
    document.getElementById("ready").innerHTML = "READY"
    for (let [key, value] of Object.entries(players)) {
        if (value != null) {
            placeID = key.split("")[6]
            _playerID = value.toString()
            if (_playerID == playerID) {
                onwPlaceID = placeID
            }
            if (placeID == "1" && playerID == _playerID){
                document.getElementById('start').hidden = false
                document.getElementById("ready").hidden = true
            }
            else if (placeID != "1" && playerID == _playerID) {
                document.getElementById("ready").hidden = false
            }
            await new Promise(resolve => {
                socket.emit("returnPlayerData", _playerID, (username) => {
                    document.getElementById("p" + placeID + "name").innerHTML = username
                    indicator = document.getElementById("p" + placeID + "_indicator")
                    if (placeID == 1){
                        indicator.style.backgroundColor = "limegreen"
                    }
                    else {
                        indicator.style.backgroundColor = "#ffe433"
                    }
                    resolve(username)
                })
            })
        }
    }
})

