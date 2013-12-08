window.App.views.MeetingContainerView = Backbone.View.extend({
    el: "#meetings-container",

    events: {
        "click #open-meeting-modal": "openMeetingModal"
    },

    initialize: function() {
        this.meetingsListSubView = new App.views.MeetingListView();
    },

    openMeetingModal: function() {
        var view = new window.App.views.ModalView({template: "#template-meeting-add"});
        var modal = new Backbone.BootstrapModal({
            content: view,
            title: "Add New Meeting",
            animate: true
        });

        modal.open(function() {
            // Called if OK in modal dialog was clicked
            this.meetingsListSubView.addMeeting();
        }.bind(this));
    }
});
