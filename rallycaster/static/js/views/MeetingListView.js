window.App.views.MeetingListView = Backbone.View.extend({
    el: "#meetings-list",

    events: {
        "click .meeting": "openMeetingDetails"
    },

    initialize: function () {
        App.router.collections.meetingCollection = new App.collections.MeetingCollection();

        this.getMeetings();
    },

    getMeetings: function () {
        App.router.collections.meetingCollection
            .fetch()
            .done(this.render.bind(this));
    },

    render: function () {
        var template = Handlebars.compile($("#template-meeting-list-item").html());

        this.$el.empty();

        App.router.collections.meetingCollection.each(function (meeting, index) {
            this.$el.append(template(meeting.toJSON()));
        }.bind(this));

        // Render in the calendar view
        $(document).trigger("didFinishRenderingMeetings_global");
    },

    saveMeeting: function (meeting) {
        if (!meeting) {
            meeting = new App.models.MeetingModel();
        }

        meeting.save({
            name: $("#meeting-name").val(),
            invited_people: $("#invited-people").val(),
            description: $("#meeting-description").val(),
            date: $("#meeting-date-text").val(),
            location: $("#meeting-location").val()
        });

        if (!meeting) {
            App.router.collections.meetingCollection.add(meeting);
        }

        // Re-render the meetings list when the collection changes
        this.getMeetings();
    }
});
