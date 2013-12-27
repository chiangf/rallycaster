window.App.views.MeetingPanelView = Backbone.View.extend({
    el: "#meetings-panel",

    events: {
        "click #add-meeting-modal-button": "addMeetingModal",
        "click .meeting-details-link": "editMeetingModal"
    },

    initialize: function () {
        this.meetingsListSubView = new App.views.MeetingListView();
        this.calendarSubView = new App.views.CalendarView();

        $(document).on("didFinishRenderingMeetings_global", function () {
            this.showCalendarSubView();
        }.bind(this));
    },

    addMeetingModal: function (e) {
        this.openMeetingModal(null);
    },
    editMeetingModal: function (e) {
        var $target = $(e.target),
            meetingId = $(e.currentTarget).data("meetingId"),
            meeting = App.router.collections.meetingCollection.get(meetingId);

        this.openMeetingModal(meeting);
    },
    openMeetingModal: function (meeting) {
        var template = Handlebars.compile($("#template-meetings-add-modal").html());

        var renderedTemplate;
        if (meeting) {
            renderedTemplate = template(meeting.toJSON());
        } else {
            renderedTemplate = template();
            meeting = null;
        }

        $("#add-meeting-modal-container").html(renderedTemplate);

        var $meetingAddModal = $("#meeting-add-modal");
        $meetingAddModal.find("#meeting-add-save-button").click(function (e) {
            // Called if Save in modal dialog was clicked
            this.meetingsListSubView.saveMeeting(meeting);
            $meetingAddModal.modal('hide');
        }.bind(this));

        $meetingAddModal.modal('show');
    },

    showCalendarSubView: function () {
        this.calendarSubView.render(App.router.collections.meetingCollection.getMeetingsForCalendar);
    },
    hideCalendarSubView: function () {
        this.calendarSubView.$el.fadeOut();
    }

//    showMeetingDetails: function( e ) {
//        var $target = $( e.target ),
//            meetingId = $( e.currentTarget ).data( "meetingId" );
//
//        this.hideCalendarSubView();
//
//        this.meetingDetailsView = new App.views.MeetingDetailsView({
////            appModel: this.meetingCollection.get( meetingId ),
////            backUrlFragment: Backbone.history.fragment
//            model: App.router.collections.meetingCollection.get( meetingId )
//        }).render();
//    }
});
