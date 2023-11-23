const baseURL = window.location.origin;
const notificationQueue = [];


let headers = new Headers();
headers.append('Content-Type', 'application/json');

function createNotification(type, text) {
    const notifications = $(".position-fixed");
    if (type === "error") type = "danger";
    const newDiv = $("<div>").addClass(["alert", "alert-" + type, "rounded", "p-3", "mb-3", "w-100"]).attr("role", "alert");


    newDiv.click(function () {
        newDiv.hide();
    });

    const closeButton = $("<button>").attr({
        type: "button",
        "aria-label": "Close"
    }).addClass("btn-close float-end").click(function () {
        newDiv.hide();
    });

    const messageText = $("<div>").text(text);

    newDiv.append(closeButton, messageText);

    notifications.append(newDiv);
    notificationQueue.push(newDiv.get(0));

    if (notificationQueue.length > 0) {
        setTimeout(removeNextNotification, 2000);
    }
}


function removeNextNotification() {
    const firstUnexpected = $(".position-fixed").children().first().get(0);
    const topNotification = notificationQueue.shift();

    if (topNotification !== null) {
        $(topNotification).remove();
    }

    if (notificationQueue.length > 0) {
        setTimeout(removeNextNotification, 2000);
    }
}


function getCookie(name) {
    var value = "; " + document.cookie;
    console.log(value);
    var parts = value.split("; " + name + "=");
    if (parts.length === 2) {
        return parts.pop().split(";").shift();
    }
}

function appendCookie(name, value) {
    document.cookie = name + "=" + value + ";";
}

let userTypeSwitcher = $("#flexSwitchCheckDefault");
if (userTypeSwitcher !== null) {
    userTypeSwitcher.on("change", function (event) {
        $('#switchTypeLabel').text(this.checked ? 'I am Employer' : 'I am Worker');

        $.ajax({
            url: "/api/switch_user_profile",
            type: "POST",
            headers: headers,
            data: JSON.stringify({"type": userTypeSwitcher.prop('checked')}),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                if (data.type) {
                    userTypeSwitcher.prop('checked', true);
                    document.cookie = "type=1";
                    setTimeout(function () {
                        window.location.href = "/employer"
                    }, 500);
                } else {
                    userTypeSwitcher.prop('checked', false);
                    document.cookie = "type=0";
                    setTimeout(function () {
                        window.location.href = "/"
                    }, 500);
                }
            },
            error: function (error) {
                createNotification("alert", "Error while switching profile.");
            }
        });
    });
}


document.getElementById('theme-switch').addEventListener('change', function (event) {
    document.body.classList.toggle('dark-mode', event.target.checked);
});


$(document).ready(function() {

    $('#notificationContainer .alert').each(function() {
        notificationQueue.push(this);
    });


    if (notificationQueue.length > 0) {
        setTimeout(removeNextNotification, 2000);
    }
});
