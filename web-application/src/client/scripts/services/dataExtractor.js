/**
 * Created by dsolans on 24/05/2017.
 */

angular.module('ADS_Group2_Application').factory('DataExtractorService', function(RestService, $http, API_BASE_URL) {
    var dataExtractionService = {};


    /*
    Twitter related endpoints
     */

    dataExtractionService.startTweetsGathering = function() {

        return $http.get(API_BASE_URL+'twitter/gather/start/').then(function (d) {
            return d;
        });
    };

    dataExtractionService.stopTweetsGathering = function() {

        return $http.get(API_BASE_URL+'twitter/tweets/get/').then(function (d) {
            return d;
        });
    };


    dataExtractionService.getTweetsData = function() {

        return $http.get(API_BASE_URL+'twitter/gather/stop/').then(function (d) {
            return d;
        });
    };


    /*
    Flats renting price related
     */

    dataExtractionService.getRentalPrice = function() {

        return $http.get(API_BASE_URL+'flats_rental/').then(function (d) {
            return d;
        });
    };

    /*
    Recomendation
     */
    dataExtractionService.getRecommendation = function(favourite_point,max_transport_time,min_transport_time, max_rental_price, min_rental_price, night_live) {

        var body = {};
        body.lat = favourite_point[0];
        body.lng = favourite_point[0];
        body.metro=1;
        body.bus=0;
        body.max_transport_time=max_transport_time;
        body.min_transport_time=min_transport_time;
        body.max_rental_price=max_rental_price;
        body.min_rental_price=min_rental_price;
        body.night_live=night_live;

        console.log("Executing recommendation for: ", body);

        return $http.post(API_BASE_URL+'recommendation/scores', body).then(function (d) {
            console.log("Obtained recommendation: ", d);
            return d;
        });
    };


    return dataExtractionService;
});
