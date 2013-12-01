window.Application.models.MeetingModel = Backbone.Model.extend({
    idAttribute: "_id",

    url: function() {
        if (this.id) {
            return "/meetings/" + this.id;
        } else {
            return "/meetings"
        }
    }
});
