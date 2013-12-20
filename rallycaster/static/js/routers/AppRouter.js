window.App.routers.AppRouter = Backbone.Router.extend({
    routes: {
        "": "goBegin"
    },

    initialize: function() {
        console.log("initialize user menu");
        new App.views.UserMenuView();
    },

    goLogin: function() {
        console.log("login route");
        new App.views.LoginView();
    },

    goBegin: function() {
        console.log("begin route");
        new App.views.MeetingContainerView();
    }
});
