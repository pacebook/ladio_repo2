(function() {
    'use strict';

    var current_url = window.location.href;
    var pattern = /^https?:\/\/127\.0\.0\.1|^https?:\/\/localhost/g.test(current_url);
    var StaticUrl = pattern ?
                    '/' :
                    'https://ladiobc.s3-ap-northeast-1.amazonaws.com/';
    var RootUrl = pattern ?
                  'http://localhost:8000/' :
                  'http://ladio-test2-dev.elasticbeanstalk.com/';

    angular.module('ladio.services', [])

    .constant('UrlBundle', {
        'StaticUrl':StaticUrl,
        'RootUrl':RootUrl
    })

})();