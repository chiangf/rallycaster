window.App.collections.Meetings = Backbone.Collection.extend({
    model: App.models.Meeting,

    url: "/meetings/",

    parse: function(response) {
        return response.meetings;
    }
});
