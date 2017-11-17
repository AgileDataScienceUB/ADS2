/**
 * Created by dsolans on 24/05/2017.
 */

angular.module('ADS_Group2_Application').factory('DataExtractorService', function(RestService, $http, API_BASE_URL) {
    var dataExtractionService = {};


    dataExtractionService.startTweetsGathering = function() {

        return $http.get(API_BASE_URL+'/twitter/gather/start/').then(function (d) {
            return d;
        });
    };

    dataExtractionService.stopTweetsGathering = function() {

        return $http.get(API_BASE_URL+'/twitter/tweets/get/').then(function (d) {
            return d;
        });
    };


    dataExtractionService.getTweetsData = function() {

        return $http.get(API_BASE_URL+'/twitter/gather/stop/').then(function (d) {
            return d;
        });
    };



    return dataExtractionService;
});
