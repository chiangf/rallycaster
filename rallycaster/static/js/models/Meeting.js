window.App.models.Meeting = Backbone.Model.extend({
    idAttribute: "_id",

    defaults: {
        location_latitude: null,
        location_longitude: null
    },

    url: function() {
        if (this.id) {
            return "/meetings/" + this.id;
        } else {
            return "/meetings/"
        }
    }
});
