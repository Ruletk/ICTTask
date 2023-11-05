const container = document.getElementsByClassName('card');

var headers = new Headers();
headers.append('Content-Type', 'application/json');

for (var i = 0; i < container.length; i++) {
    (function (i) {
        var vacancy_id = container[i].querySelector(".card-header a").getAttribute("href").split("/")[2];

        var request = new Request("api/check_user_vacancy_favorite", {
            method: "POST",
            headers: headers,
            body: JSON.stringify({"token": userToken, "vacancy_id": vacancy_id})
        });
        fetch(request)
            .then(function (response) {
                if (response.status === 200) {
                    return response.json();
                } else {
                    throw new Error('Request failed');
                }
            })
            .then(function (data) {
                var img = container[i].querySelector(".card-header .btn img");
                if (data.on) {
                    img.setAttribute("src", "/static/icons/star_filled.png")
                } else {
                    img.setAttribute("src", "/static/icons/star.png");
                }
            })
            .catch(function (error) {
                createNotification("alert", "Error while checking favorite vacancies.");
                console.log(error);
            });
    })(i);
}


for (var i = 0; i < container.length; i++) {
    (function (i) {
        container[i].addEventListener('click', function (event) {
            if (event.target.classList.contains('btn') && event.target.parentElement.classList.contains('card-header')) {
                var vacancy_id = container[i].querySelector(".card-header a").getAttribute("href").split("/")[2];

                var request = new Request("api/switch_user_vacancy_favorite", {
                    method: "POST",
                    headers: headers,
                    body: JSON.stringify({"token": userToken, "vacancy_id": vacancy_id})
                });
                fetch(request)
                    .then(function (response) {
                        if (response.status === 200) {
                            return response.json();
                        } else {
                            throw new Error('Request failed');
                        }
                    })
                    .then(function (data) {
                        var img = container[i].querySelector(".card-header .btn img");
                        if (data.on) {
                            img.setAttribute("src", "/static/icons/star_filled.png");
                            createNotification("info", "Vacancy added to favorites.")
                        } else {
                            img.setAttribute("src", "/static/icons/star.png");
                            createNotification("info", "Vacancy removed from favorites.")
                        }
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
            }
        });
    })(i);
}
