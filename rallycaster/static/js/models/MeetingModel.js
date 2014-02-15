window.App.models.MeetingModel = Backbone.Model.extend({
    idAttribute: "_id",

    defaults: {
        location_latitude: 0,
        location_longitude: 0
    },

    url: function () {
        if (this.id) {
            return "/meetings/" + this.id;
        } else {
            return "/meetings/"
        }
    }
});
