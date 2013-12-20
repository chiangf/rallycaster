window.App.views.MeetingContainerView = Backbone.View.extend({
    el: "#meetings-container",

    events: {
        "click #open-meeting-modal": "openMeetingModal"
    },

    initialize: function() {
        this.meetingsListSubView = new App.views.MeetingListView();
    },

    openMeetingModal: function() {
        var template = Handlebars.compile( $("#template-meetings-add-modal").html() );
        $("#meeting-add-modal-container").html(template);

        var $meetingAddModal = $("#meeting-add-modal");

        $meetingAddModal.find("#meeting-add-save-button").click(function(e) {
            // Called if Save in modal dialog was clicked
            this.meetingsListSubView.addMeeting();
            $meetingAddModal.modal('hide');
        }.bind(this));

        $meetingAddModal.modal('show');
    }
});
