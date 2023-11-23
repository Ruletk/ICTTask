$(document).ready(function () {
    setupNavigationButtons();
});


function setupNavigationButtons() {
    $('.breadcrumb-item button').click(function () {
        $('.breadcrumb-item button').prop('disabled', false);

        $(this).prop('disabled', true);
        let wrapper = $("#profileWrapper");

        let url = "";

        switch ($(this).attr('id')) {
            case 'userProfile':
                url = '/profile/';
                break;
            case 'userSettings':
                url = '/profile/settings/';
                break;
            case 'userEducation':
                url = '/profile/education/';
                break;
            case 'userSecurity':
                url = '/profile/security/';
                break;
            case 'userResume':
                url = '/profile/resume/';
                break;
        }
        window.history.replaceState("", "", url);
        $.ajax({
            url: url,
            type: 'GET',
            success: function (data) {
                let dataWrapper = $(data).find('#profileWrapper').html();
                wrapper.html(dataWrapper);
            },
            error: function (data) {
                createNotification('error', 'Something went wrong, please try again later.')
            }
        });
    });
}
