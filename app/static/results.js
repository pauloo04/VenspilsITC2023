var socket = io.connect()
socket.emit("joinRoom", lobbyCode)

let results;

window.onload = function() {
    document.getElementById("backHome").addEventListener("click", function() {
        window.location.href = "/"
    })
    socket.emit("getPrompt", lobbyCode, (prompt) => {
        document.getElementById("prompt").innerHTML = prompt
    })
    socket.emit("requestResults", lobbyCode, (results) => {
        for (const [key, value] of Object.entries(results)) {
            if (key == "paintingImage") {
                document.getElementById(key).src = value
                document.getElementById("finalImage").src = value
            }
            else if (key == "sketch1Image" || key == "sketch2Image") {
                document.getElementById(key).src = value
            }
            else {
                document.getElementById(key).innerHTML = value
            }
        }
    })
}