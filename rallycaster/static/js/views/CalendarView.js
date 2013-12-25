window.App.views.CalendarView = Backbone.View.extend({
    el: null,

    events: {
    },

    initialize: function() {
    },

    render: function(getMeetingsFunc) {
        var calendar = $("#calendar-container").calendar({
            events_source: getMeetingsFunc,
            tmpl_path: "static/lib/bower_components/bootstrap-calendar/tmpls/"
        });
    }
});
