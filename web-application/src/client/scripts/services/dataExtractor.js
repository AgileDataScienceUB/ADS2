/**
 * Created by dsolans on 24/05/2017.
 */

angular.module('ADS_Group2_Application').factory('DataExtractorService', function(RestService, $http, CA_API_BASE_URL) {
    var dataExtractionService = {};

    dataExtractionService.getGraphData = function() {

        return $http.get(CA_API_BASE_URL+'graph/software_stream_01/ts/4').then(function (d) {
            angular.copy(d.data, dataExtractionService.graph_data);

            angular.copy(true, dataExtractionService.dataHasBeenExtracted);

            console.log("SUBGRAPHS DATA ON SERVICE --> ", d.data);
            return d.data;
        });
    };



    return dataExtractionService;
});
