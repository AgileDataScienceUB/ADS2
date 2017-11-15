/**
 * Created by dsolans on 24/05/2017.
 */


angular.module('ADS_Group2_Application').factory('RestService', function ($http) {
    var restService = {};

    restService.doPost = function (url, json) {

        console.log("POST to: "+url);
        return $http.post(url, json);

    };

    restService.doPostWithFile = function (url, json) {
        console.log("POST with file to: "+url);


        return $http.post(url, json, {
            transformRequest: angular.identity,
            headers: {'Content-Type': undefined}
        });
    };

    restService.doGet = function (url) {
        console.log("GET to: "+url);

        return $http.get(url);
    };

    return restService;
});
