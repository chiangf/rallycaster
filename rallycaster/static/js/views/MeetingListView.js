window.App.views.MeetingListView = Backbone.View.extend({
    el: "#meetings-list",

    events: {},

    initialize: function() {
        this.meetingCollection = new App.collections.MeetingCollection();

        // Re-render the meetings list when the collection changes
        this.listenTo( this.meetingCollection, 'add', this.render );

        this.getMeetings();
    },

    getMeetings: function() {
        this.meetingCollection
            .fetch()
            .done( this.render.bind(this) );
    },

    render: function() {
        var template = Handlebars.compile( $("#template-meetings-list").html() );
        this.$el.html(template({
            meetings: this.meetingCollection.toJSON()
        }));

        // Render in the calendar view
        $(document).trigger( "didFinishRenderingMeetings_global" );
    },

    addMeeting: function() {
        var meeting = new App.models.MeetingModel();
        meeting.save({
            name: $("#meeting-name").val(),
            invited_people: $("#invited-people").val(),
            description: $("#meeting-description").val(),
            date: $("#meeting-date-text").val(),
            location: $("#meeting-location").val()
        });

        this.meetingCollection.add(meeting);


    }
});
