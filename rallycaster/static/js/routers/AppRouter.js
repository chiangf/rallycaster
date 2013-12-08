window.App.routers.AppRouter = Backbone.Router.extend({
    routes: {
        "": "goBegin"
    },

    initialize: function() {
        console.log("initialize user menu");
        new App.views.UserMenuView();
    },

    goBegin: function() {
        console.log("begin route");
        new App.views.MeetingContainerView();
    }
});

$(document).on('ready', function() {
    // Setup console.log for IE8
    if (typeof console === "undefined" || typeof console.log === "undefined") {
        console.log = function() {};
    }

    // Setup default ajax handlers
    $.ajaxSetup({
        error: function(xhr, status, error) {
            console.log(error);

            // If web services returned a 401, redirect to the login page.
            if (xhr.status === 401) {
                window.location.href = "/";
            }
        }.bind(this)
    });

    App.router = new App.routers.AppRouter();
    App.router.goBegin();

    Backbone.history.start();
});
