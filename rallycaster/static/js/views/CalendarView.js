window.App.views.CalendarView = Backbone.View.extend({
    el: "#calendar-container",

    events: {
    },

    initialize: function () {
    },

    render: function (getMeetingsFunc) {
        var calendar = this.$el.calendar({
            events_source: getMeetingsFunc,
            tmpl_path: "static/lib/bower_components/bootstrap-calendar/tmpls/"
        });
    }
});
