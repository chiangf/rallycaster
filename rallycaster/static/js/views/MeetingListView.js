window.Application.views.MeetingListView = Backbone.View.extend({
    $el: $("#meetings-list"),

    events: {
    },

    initialize: function() {
        this.meetings = new Application.collections.MeetingCollection();

//        $("button#meeting-button-save").click(function(event) {
//            this.addMeeting(event);
//        }).bind(this);

        this.getMeetings();
    },

    getMeetings: function() {
        this.meetings
            .fetch()
            .done( this.renderMeetings.bind(this) );
    },

    renderMeetings: function() {debugger;
        var template = Handlebars.compile( $("#template-meetings-list").html() );
        this.$el.html(template);
    },

    addMeeting: function(meeting_info) {debugger;
        this.meetings.create(meeting_info);
    }
});

$(document).ready(function() {
    view = new Application.views.MeetingListView();
});
