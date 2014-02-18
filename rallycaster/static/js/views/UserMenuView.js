window.App.views.UserMenuView = Backbone.View.extend({
    el: "#user-profile-dropdown",

    events: {
        "click #user-profile-logout": "logout"
    },

    logout: function () {
        $.ajax({
            url: "/api/logout/",
            type: "PUT"
        });
    }
});
