window.App.collections.MeetingCollection = Backbone.Collection.extend({
    model: App.models.MeetingModel,

    url: "/meetings/",

    initialize: function() {
        _.bindAll(this, "getMeetingsForCalendar");
    },

    parse: function(response) {
        return response.meetings;
    },

    getMeetingsForCalendar: function() {
        var meetings = [];
        _.each( this.models, function( model ) {
            meetings.push({
                "id": model.get("_id"),
                "title": model.get("name"),
                "url": "http://example.com",    // TODO: Change this!
                "class": "event-important",
                "start": Date.now(),    // TODO: Change this!
                "end": Date.now() + 10000   // TODO: Change this!
            });
        });
        return meetings;
    }
});
