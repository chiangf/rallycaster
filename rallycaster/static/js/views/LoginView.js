window.App.views.LoginView = Backbone.View.extend({
    el: "#login-modal-container",

    events: {
        "click #login-facebook": "loginFacebook"
    },

    initialize: function () {
        this.render();
    },

    render: function () {
        var template = Handlebars.compile($("#template-login-chooser-modal").html());
        this.$el.html(template);

        var $loginModal = $("#login-modal");
        $loginModal.modal('show');
    },

    loginFacebook: function () {
        $.ajax({
            url: "/api/login/facebook/",
            type: "POST"
        });
    }
});
