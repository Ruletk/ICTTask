switcher = document.getElementById("flexSwitchCheckDefault");

headers = new Headers();

switcher.addEventListener("change", function (event) {
    document.getElementById('switchTypeLabel').textContent = this.checked ? 'I am Employer' : 'I am Worker';

    const request = new Request("/api/switch_user_profile", {
        method: "POST",
        headers: headers,
        body: JSON.stringify({"token": userToken, "type": switcher.checked})
    });

    fetch(request).then(function (response) {
        if (response.status === 200) {
            return response.json();
        } else {
            throw new Error('Request failed');
        }
    }).then(function (data) {
        if (data.type) {
            switcher.checked = true;
            document.cookie = "type=1";
            setTimeout(function () {
                window.location.href = "/employer"
            }, 500);
        } else {
            switcher.checked = false;
            document.cookie = "type=0";
            setTimeout(function () {
                window.location.href = "/"
            }, 500);
        }

    }).catch(function (error) {
        createNotification("alert", "Error while switching profile.");
    });

});
