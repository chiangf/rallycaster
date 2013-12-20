window.App.views.MeetingListView = Backbone.View.extend({
    el: "#meetings-list",

    events: {},

    initialize: function() {
        this.meetings = new App.collections.Meetings();

        this.getMeetings();
    },

    getMeetings: function() {
        this.meetings
            .fetch()
            .done( this.render.bind(this) );
    },

    render: function() {
        var template = Handlebars.compile( $("#template-meetings-list").html() );
        this.$el.html(template({
            meetings: this.meetings.toJSON()
        }));
    },

    addMeeting: function() {
        var meeting = new App.models.Meeting();
        meeting.save({
            name: $("#meeting-name").val(),
            invited_people: $("#invited-people").val(),
            description: $("#meeting-description").val(),
            date: $("#meeting-date-text").val(),
            location: $("#meeting-location").val()
        });

        this.meetings.add(meeting);
    }
});
