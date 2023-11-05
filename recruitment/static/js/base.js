function createNotification(type, text) {
    const notifications = document.querySelector(".position-fixed");
    const newDiv = document.createElement("div");
    if (type === "error") type = "danger";
    newDiv.classList.add("alert", "alert-" + type, "rounded", "p-3", "mb-3", "w-100");
    newDiv.setAttribute("role", "alert");
    newDiv.onclick = function () {
        newDiv.style.display = 'none';
    }

    const closeButton = document.createElement("button");
    closeButton.type = "button";
    closeButton.classList.add("btn-close", "float-end");
    closeButton.setAttribute("aria-label", "Close");
    closeButton.onclick = function () {
        newDiv.style.display = 'none';
    }
    const messageText = document.createTextNode(text);
    newDiv.appendChild(closeButton);
    newDiv.appendChild(messageText);

    notifications.appendChild(newDiv);
}

function removeNotification() {
    const notifications = document.getElementById("notificationContainer");
    const topNotification = notifications.firstElementChild;
    if (topNotification !== null) {
        topNotification.remove();
    }
}

function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length === 2) {
        return parts.pop().split(";").shift();
    }
}

document.getElementById('theme-switch').addEventListener('change', function(event) {
    document.body.classList.toggle('dark-mode', event.target.checked);
});

setInterval(removeNotification, 2000);
