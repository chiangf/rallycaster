function Services() {
    var self = this;

    //TODO: hardcode
    var SERVICES_BASE_URL = "http://localhost:5000/";

//    this.authenticate = function() {
//        self.call({
//            type: "POST",
//            url: SERVICES_BASE_URL + "login",
//            dataType: "json",
//            success: function(settings) {
//                alert('authenticate success!');
//            },
//            error: function(settings) {
//                alert('authenticate error');
//            }
//        });
//    };

    this.authenticate = function() {

    };

    this.call = function(settings) {
        var sessionTokenCookie = getSessionTokenCookie();

        // If session token does not exist, redirect to login page
        if (sessionTokenCookie === null) {
            alert('session token cookie does not exist');
            window.location.replace("/login");
        }

        settings['url'] = SERVICES_BASE_URL + settings['url'];
        settings['dataType'] = 'json';
        settings['headers'] = {
            'X-TOKEN': sessionTokenCookie
        }
        $.ajax(settings);
    };

    var getSessionTokenCookie = function() {
        return $.cookie("session-token");
    };
};

var services = new Services();