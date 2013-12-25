window.App.views.MeetingPanelView = Backbone.View.extend({
    el: "#meetings-panel",

    events: {
        "click #add-meeting-modal-button": "openMeetingModal"
    },

    initialize: function() {
        this.meetingsListSubView = new App.views.MeetingListView();
        this.calendarSubView = new App.views.CalendarView();

        $(document).on("didFinishRenderingMeetings_global", function() {
            this.calendarSubView.render(this.meetingsListSubView.meetingCollection.getMeetingsForCalendar);
        }.bind(this));
    },

    openMeetingModal: function() {
        var template = Handlebars.compile( $("#template-meetings-add-modal").html() );
        $("#add-meeting-modal-container").html(template);

        var $meetingAddModal = $("#meeting-add-modal");

        $meetingAddModal.find("#meeting-add-save-button").click(function(e) {
            // Called if Save in modal dialog was clicked
            this.meetingsListSubView.addMeeting();
            $meetingAddModal.modal('hide');
        }.bind(this));

        $meetingAddModal.modal('show');
    }
});
