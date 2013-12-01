window.Application.collections.MeetingCollection = Backbone.Collection.extend({
    model: Application.models.MeetingModel,

    url: "/meetings"
});
