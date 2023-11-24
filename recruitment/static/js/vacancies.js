let page_num = 2;
let stop = false;


function handleToggleFavoriteVacancy(event) {
    var card = $(event.currentTarget).closest('.card');
    if (!card.length || !$(event.target).hasClass('btn') || !$(event.target).parent().hasClass('card-header')) {
        return;
    }

    var vacancy_id = card.attr("id");
    var img = card.find(".card-header .btn img");

    if (!vacancy_id || !img.length) {
        return;
    }

    $.ajax({
        url: "/api/switch_user_vacancy_favorite",
        type: "POST",
        headers: headers,
        data: JSON.stringify({"vacancy_id": vacancy_id}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            if (data.status === "error") {
                createNotification("error", "Error while adding vacancy to favorites.");
                return;
            }
            var imgSrc = data.on ? "/static/icons/star_filled.png" : "/static/icons/star.png";
            img.attr("src", imgSrc);
            var notificationText = data.on ? "Vacancy added to favorites." : "Vacancy removed from favorites.";
            createNotification("info", notificationText);
        },
        error: function (error) {
            console.log(error);
        }
    });
}


let searchTimeout;

function initSearch() {
    let urlParams = new URLSearchParams(window.location.search);
    let query = urlParams.get('query');
    let location = urlParams.get('location');
    let salary = urlParams.get('salary');
    let favorite = urlParams.get('favorite') === "true";

    let searchQuery = $("#search_query");
    let searchLocation = $("#search_location");
    let searchSalary = $("#search_salary");
    let searchFavorite = $("#search_favorite");

    if (query) searchQuery.val(decodeURIComponent(query));
    if (location) searchLocation.val(decodeURIComponent(location));
    if (salary) searchSalary.val(decodeURIComponent(salary));
    if (favorite) searchFavorite.prop('checked', favorite);

    function handleInput() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(submitForm, 300);
    }

    searchQuery.on("input", handleInput);
    searchLocation.on("input", handleInput);
    searchSalary.on("input", handleInput);
    searchFavorite.on("input", handleInput);
}

function submitForm() {
    let query = $("#search_query").val();
    let location = $("#search_location").val();
    let salary = $("#search_salary").val();
    let favorite = $("#search_favorite").is(":checked");

    if (salary !== "") {
        if (isNaN(salary) || salary < 0) {
            createNotification("error", "Salary must be a positive number.");
            return;
        }
    } else if (salary !== "") {
        createNotification("error", "Salary must be a number.");
        return;
    }

    let params = new URLSearchParams();
    if (query) params.append("query", encodeURIComponent(query));
    if (location) params.append("location", encodeURIComponent(location));
    if (salary) params.append("salary", encodeURIComponent(salary));
    if (favorite) params.append("favorite", encodeURIComponent(favorite));

    params.append("page", 1);

    let url = baseURL + "/search?" + params.toString();
    if (url[url.length - 1] === '?') url = url.slice(0, -1)

    window.history.replaceState({}, '', url);
    $.get(url)
        .done(function (data) {
            $('#vacancies').html(data);
            stop = false;
            page_num = 2;
        })
        .fail(function (error) {
            createNotification("error", "Error while searching vacancies.");
            console.log(error);
            stop = true;
        });
}

function loadMoreData() {
    if (stop) return;
    let params = new URLSearchParams();
    params.append("page", page_num);
    if ($('#searchBar').length) {
        params.append("query", $('#search_query').val());
        params.append("location", $('#search_location').val());
        params.append("salary", $('#search_salary').val());
        params.append("favorite", $('#search_favorite').is(":checked"));
    }

    let ajax_load = $('.ajax-load');

    $.ajax({
        url: "/search?" + params.toString(),
        type: "get",
        beforeSend: function () {
            ajax_load.show();
            page_num++;
        }
    })
        .done(function (data) {
            ajax_load.hide();
            if (data === "") {
                $('.ajax-load').html("No more records found");
                stop = true
            } else
                $("#vacancies").append(data);
        })
        .fail(function (jqXHR, ajaxOptions, thrownError) {

        });
}


jQuery(document).ready(function () {
    $(window).scroll(function () {
        if ($(window).scrollTop() + $(window).height() >= $(document).height()) {
            loadMoreData();
        }
    });
    initSearch();
});
