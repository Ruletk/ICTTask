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

function respondButton(vacancy_id) {
    $.ajax({
        url: baseURL + "/vacancy/respond/" + vacancy_id,
        type: "post",
        headers: headers,
        beforeSend: function () {
            $("#respondButton").prop("disabled", true);
        }
    })
        .done(function (data) {
            $("#respondButton").prop("disabled", false);
            createNotification("success", "You have successfully responded to the vacancy.");
            $("#respondButton").hide();
        })
        .fail(function (jqXHR, ajaxOptions, thrownError) {
            $("#respondButton").prop("disabled", false);
            createNotification("error", "Error while responding to the vacancy.");
        });
}


$(document).ready(function() {

    $('#notificationContainer .alert').each(function() {
        notificationQueue.push(this);
    });


    if (notificationQueue.length > 0) {
        setTimeout(removeNextNotification, 2000);
    }
});
