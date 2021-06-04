var socket = io();

socket.emit("requestETA", {"referrer": document.referrer});

socket.on("postETA", data => {
    if (data["eta"] == null) {
        document.getElementById().textContent = "unknown.";
    }
    else {
        document.getElementById().textContent = data["eta"] + " seconds.";
    }
});

socket.on("revealFate", data => {
    if (data["url"] == document.referrer) {
        if (data["fate"] == true) {
            window.location.replace(document.referrer);
        }
        else {
            document.getElementById("wait-message").style.display = "none";
            document.getElementById("error-message").style.display = "initial";
        }
    }
});