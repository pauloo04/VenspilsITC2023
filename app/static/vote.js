let vote
range = document.getElementById("range")

var socket = io.connect()
socket.emit("joinRoom", lobbyCode)

socket.on("redirect", function(url){
    window.location.href = url["url"] + "?lobbyCode=" + lobbyCode + "&playerID=" + playerID
})

let i = 1;
let gtg = false;

function loadImages(lobbyCode, player_id, stage) {
    socket.emit("requestPNG", lobbyCode, player_id, stage, (images) => {
        ids = {}
        for (const [key, value] of Object.entries(images)) {
            document.getElementById("drawing" + i.toString()).src = value;
            ids[i-1] = key
            i ++
          }
    })
}

document.addEventListener('DOMContentLoaded', () => {
    if (window.location.href.indexOf("sketch") > -1){
        loadImages(lobbyCode, playerID, "VoteSketch")
    }
    else if (window.location.href.indexOf("improve") > -1){
        loadImages(lobbyCode, playerID, "VoteImprovement")
    }
    else if (window.location.href.indexOf("paint") > -1){
        loadImages(lobbyCode, playerID, "VotePainting")
    }
})

$(document).ready(function(){
    $("#votingCarousel").on('slide.bs.carousel', async function (e){
        vote = parseFloat(range.value);
        if (window.location.href.indexOf("sketch") > -1){
            socket.emit("vote1", ids[e.from], vote)
        }
        else if (window.location.href.indexOf("improve") > -1){
            socket.emit("vote2", ids[e.from], vote)
        }
        else if (window.location.href.indexOf("paint") > -1){
            socket.emit("vote3", ids[e.from], vote)
        }
        range.value = 5;
        document.getElementById("num").value = 5
        if ((i-1) == e.to || e.to == 0) {
            document.getElementById("votingStage").hidden = true
            document.getElementById("waitForOthers").hidden = false
            document.getElementById("waitForOthersText").hidden = false
            if (window.location.href.indexOf("sketch") > -1){
                await new Promise(resolve => {
                    socket.emit("checkVotes1", lobbyCode, (bool) => {
                        if(bool){
                            gtg = true
                        }
                        resolve(bool)
                    })
                })
                if (gtg) {
                    socket.emit("redirectToImprove", lobbyCode)
                }
            }
            else if (window.location.href.indexOf("improve") > -1){
                await new Promise(resolve => {
                    socket.emit("checkVotes2", lobbyCode, (bool) => {
                        if(bool){
                            gtg = true
                        }
                        resolve(bool)
                    })
                })
                if (gtg) {
                    socket.emit("redirectToPaint", lobbyCode)
                }
            }
            else if (window.location.href.indexOf("paint") > -1){
                await new Promise(resolve => {
                    socket.emit("checkVotes3", lobbyCode, (bool) => {
                        if(bool){
                            gtg = true
                        }
                        resolve(bool)
                    })
                })
                if (gtg) {
                    socket.emit("redirectToResults", lobbyCode)
                }
            }
        }   
    })
})