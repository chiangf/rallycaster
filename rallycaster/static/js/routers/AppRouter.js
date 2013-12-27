window.App.routers.AppRouter = Backbone.Router.extend({
    routes: {
    },

    views: {},
    collections: {},

    initialize: function () {
        console.log("initialize user menu");
        this.views.userMenuView = new App.views.UserMenuView();
    },

    goLogin: function () {
        console.log("login route");
        this.views.loginView = new App.views.LoginView();
    },

    goBegin: function () {
        console.log("begin route");
        this.views.meetingPanelView = new App.views.MeetingPanelView();
    }
});
