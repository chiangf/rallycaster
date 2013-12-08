window.App.views.LoginView = Backbone.View.extend({
    el: "#login-modal-container",

    events: {
        "click #login-facebook": "loginFacebook"
    },

    render: function() {
        var view = new window.App.views.ModalView({template: "#template-login-chooser"});
        var modal = new Backbone.BootstrapModal({
            content: view,
            title: "Login",
            animate: true
        }).open();
    },

    loginFacebook: function() {
        $.ajax({
            url: "/login/facebook/",
            type: "POST"
        });
    }
});
