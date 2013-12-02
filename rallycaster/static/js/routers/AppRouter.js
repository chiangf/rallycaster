window.App.routers.AppRouter = Backbone.Router.extend({
    routes: {
        "": "goIndex",
        "login": "goLogin"
    },

    goIndex: function() {
        console.log("index route");
        new App.views.MeetingContainerView();
    },

    goLogin: function() {
        // TODO: Fill this out
        console.log("login route");
    }
});

$(document).on('ready', function() {
    App.router = new App.routers.AppRouter();
    App.router.goIndex();
});
