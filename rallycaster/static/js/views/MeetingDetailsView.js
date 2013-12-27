window.App.views.MeetingDetailsView = Backbone.View.extend({
    el: "#meeting-details-container",

    render: function () {
        var template = Handlebars.compile($("#template-meeting-details").html());

        this.$el.html(template(this.model.toJSON()));
    }
});
