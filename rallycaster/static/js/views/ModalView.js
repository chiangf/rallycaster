// Usage:
//  var view = new ModalView({template: "#template-meeting-add"})
window.App.views.ModalView = Backbone.View.extend({
    initialize: function(options) {
        this.caller = options.caller;
        this.template = $(options.template).html();
    },

    render: function() {
        this.$el.html(this.template);
        return this;
    }
});
