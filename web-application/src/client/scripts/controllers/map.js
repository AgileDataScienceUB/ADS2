'use strict';

/**
 * @ngdoc function
 * @name ADS_Group2_Application.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the ADS_Group2_Application
 */
angular.module('ADS_Group2_Application')
    .controller('MapCtrl', function ($scope, DataExtractorService) {
        this.awesomeThings = [
            'HTML5 Boilerplate',
            'AngularJS',
            'Karma'
        ];

        $scope.tab = 0

        $scope.currentDate = -1;

        $scope.STATE_STOP=1;
        $scope.STATE_PLAY=2;
        $scope.STATE_PAUSE=3;
        $scope.STATE_RESUME=4;

        $scope.time_slider_state = $scope.STATE_STOP;
        $scope.time_interval;


        var gatheringTweetsOn = false;

        $scope.tweets_array = [];

        var tweetsGatheringInterval;

        var map, svg, g, tip;
        var districtPolygons, choosenPolygon, colorToAssign, neighborhoodPolygons;
        var data;

        const USE_DISTRICTS_GRANULARITY = 0;
        const USE_NEIGHBORHOODS_GRANULARITY = 1;


        $scope.granularitySelected = USE_DISTRICTS_GRANULARITY;


        function projectPoint(x, y) {
            var point = map.latLngToLayerPoint(new L.LatLng(y, x));
            this.stream.point(point.x, point.y);

        }

        var clearPaintedPaths = function(){
            d3.selectAll(".polygon").remove();
        };

        var changeDistrictPolygonColors = function(optionIdx){

            console.log("Changing category colors for districts with optionIdx: ", optionIdx);

            districtPolygons.each(function(d, i) {
                // console.log("Polygon: ", d, i);
                choosenPolygon = d3.select("#District_"+d.properties["N_Distri"]);

                colorToAssign = "white";
                choosenPolygon
                    .style("opacity", 0.2)
                    .style("stroke", "white")
                    .style("stroke-width", "2")
                    .style("fill", colorToAssign);

            });
        };



        var paintDistrictsOverMap = function(){

            d3.json("data/divisiones_administrativas/districtes/districtes_geo.json", function (error, geojson) {


                console.log("Extracted districts data: ", geojson);
                var transform = d3.geo.transform({point: projectPoint}),
                    path = d3.geo.path().projection(transform);

                var feature = g.selectAll("path")
                    .data(geojson.features)
                    .enter()
                    .append("path")
                    .attr("id", function (d) {

                        return "District_" + d.properties["C_Distri"];
                    })
                    .attr("class", "polygon")
                    .style("stroke", "black")
                    .style("stroke-width", "2")
                    .style("fill", function(d,i) { return "green"; } )
                    .style("opacity", 0.9);

                feature.call(tip);

                feature.on('mouseover', function(d){
                    tip.show(d);

                    console.log("d: ", d);
                    d3.select("#District_" + d.properties["C_Distri"]).style('fill', 'black');
                });
                feature.on('mouseout', function(d){
                    tip.hide(d);

                    d3.select("#District_" + d.properties["C_Distri"]).style('fill', 'green');
                });

                neighborhoodPolygons = feature;
                //ASDF

                map.on("viewreset", reset);
                reset();

                // Reposition the SVG to cover the features.
                function reset() {
                    var bounds = path.bounds(geojson),
                        topLeft = bounds[0],
                        bottomRight = bounds[1];

                    svg.attr("width", bottomRight[0] - topLeft[0])
                        .attr("height", bottomRight[1] - topLeft[1])
                        .style("left", topLeft[0] + "px")
                        .style("top", (topLeft[1]) + "px");

                    g.attr("transform", "translate(" + -topLeft[0] + "," + -topLeft[1] + ")");

                    g.selectAll("path").attr("d", path);
                }

            });
        }
        var paintNeighborhoodOverMap = function(){

            d3.json("data/divisiones_administrativas/barris/barris_geo.json", function (error, geojson) {


                // console.log("Extracted data: ", geojson);
                var transform = d3.geo.transform({point: projectPoint}),
                    path = d3.geo.path().projection(transform);

                var feature = g.selectAll("path")
                    .data(geojson.features)
                    .enter()
                    .append("path")
                    .attr("id", function (d) {


                        return "Barri_" + d.properties["C_Barri"];
                    })
                    .attr("class", "polygon")
                    .style("stroke", "black")
                    .style("stroke-width", "1")
                    .style("fill", function(d,i) { return "yellow"; } )
                    .style("opacity", 0.9);

                feature.call(tip);

                feature.on('mouseover', function(d){
                    tip.show(d);
                    console.log("d: ", d);
                    d3.select("#Barri_" + d.properties["C_Barri"]).style('fill', 'black');
                });
                feature.on('mouseout', function(d){
                    tip.hide(d);
                    console.log("d: ", d);
                    d3.select("#Barri_" + d.properties["C_Barri"]).style('fill', 'yellow');
                });

                neighborhoodPolygons = feature;


                map.on("viewreset", reset);
                reset();

                // Reposition the SVG to cover the features.
                function reset() {
                    var bounds = path.bounds(geojson),
                        topLeft = bounds[0],
                        bottomRight = bounds[1];

                    svg.attr("width", bottomRight[0] - topLeft[0])
                        .attr("height", bottomRight[1] - topLeft[1])
                        .style("left", topLeft[0] + "px")
                        .style("top", (topLeft[1]) + "px");

                    g.attr("transform", "translate(" + -topLeft[0] + "," + -topLeft[1] + ")");

                    g.selectAll("path").attr("d", path);
                }

            });
        };

        var createMap = function() {


            var width = screen.width * 0.98;
            var height = screen.height * 0.82;
            // var height = screen.height * 1;



            $("#map").css("width", width + "px");
            $("#map").css("height", height + "px");
            $("#map").css("margin-left", screen.width * 0.03 + "px");


            var legendHeight = screen.height * 0.35;

            map = new L.Map("map", {center: [41.387034, 2.170020], zoom: 12, zoomControl: false});

            // map.addLayer(new L.TileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"));
             //L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', {
             L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png', {
                maxZoom: 18, attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attribution">CARTO</a>'
            }).addTo(map);



            L.control.zoom({
                position:'topright'
            }).addTo(map);


            map.options.maxZoom = 16;
            map.options.minZoom = 10;


            svg = d3.select(map.getPanes().overlayPane)
                .append("svg");

            svg.attr('width', width)
                .attr('height', height)
                .attr("class", "clickable");

            g = svg.append("g")
                .attr("class", "leaflet-zoom-hide")
                .style("z-index", 9);
            var result;

            tip = d3.tip()
                .attr('class', 'd3-tip')
                .direction('e')
                .offset([0, 20])
                .html(function(d) {
                    var result = "";

                    if(d.hasOwnProperty("properties")) {

                        if (d.properties.hasOwnProperty("N_Barri")) {
                            result += "<p></p><strong>Neighborhood: </strong>" + d.properties['N_Barri'] + "</p>";
                        }

                        if (d.properties.hasOwnProperty("N_Distri")) {
                            console.log("D: ", d);
                            result += "<p><strong>District: </strong>" + d.properties['N_Distri'] + "</p>";
                        }
                    }


                    return result;
                });





            paintDistrictsOverMap();

            // d3.polygonContains(polygon, point)
        };

        function calculateAndPaintPointsOnMap (){
            var mapBounds = leafletMap.getBounds();

            var tmpGeoData= {
                features : geoData.features.filter(function(airbnb_listing){
                    return true; //It will return everything

                    //return ((new Date(airbnb_listing.airbnb_data.host_until).getTime() >= $scope.currentDate.getTime()) && (new Date(airbnb_listing.airbnb_data.first_review).getTime() <= $scope.currentDate.getTime()))
                })
            };

            $scope.totalListings = tmpGeoData.features.length;
            if (!$scope.$$phase) $scope.$apply();

            console.log("Filtered data: ", tmpGeoData.features.length);

            qtree = d3.geom.quadtree(tmpGeoData.features.map(function (data, i) {
                    return {
                        x: data.geometry.coordinates[0],
                        y: data.geometry.coordinates[1],
                        all: data
                    };
                }
                )
            );

            var subset = search(qtree, mapBounds.getWest(), mapBounds.getSouth(), mapBounds.getEast(), mapBounds.getNorth());
            console.log("subset: " + subset.length);

            redrawSubset(subset);
        }

        function mapmove(e) {
            calculateAndPaintPointsOnMap();

        }




        createMap();


        $scope.changeShownPolygons = function(option){
            console.log("Changing polygons. Option: ", option);
            if (option == 0){
                clearPaintedPaths();
                paintDistrictsOverMap();
            }else{
                clearPaintedPaths();
                paintNeighborhoodOverMap();

            }
        }


      /* Set the width of the side navigation to 250px */
        $scope.openNav = function() {
            document.getElementById("mySidenav").style.width = "400px";
        };

      /* Set the width of the side navigation to 0 */
        $scope.closeNav = function () {
            document.getElementById("mySidenav").style.width = "0";
        };


        var paintTweet = function(tweet){

            var mapBounds = map.getBounds();
            console.log("Map bounds: ", mapBounds)

            console.log("Adding tweet to map: ", tweet);



            //var marker1 = L.circle([tweet.coordinates[0]+0.15, tweet.coordinates[1]], 50);//[41.387034, 2.170020]);
            var marker1 = L.marker([tweet.coordinates[0],tweet.coordinates[1]]);//[41.387034, 2.170020]);

            marker1.addTo(map);

            setTimeout(function() { map.removeLayer(marker1); }, 2500);
        };

        $scope.toggleTweetsGathering = function(){
            if(gatheringTweetsOn){ //Its on, should turn gathering off
                //Stop gathering on the backend
                clearInterval(tweetsGatheringInterval);
                DataExtractorService.stopTweetsGathering().then(function(d){
                    //Remove all the tweets on the map
                    $scope.tweets_array = []


                });
            }else{//Its off, should turn gathering on
                //Start gathering on the backend
                DataExtractorService.startTweetsGathering().then(function(d){
                    //Start timer every 2 secs
                    tweetsGatheringInterval = setInterval(function(){
                        //code goes here that will be run every 5 seconds.

                        DataExtractorService.getTweetsData().then(function(d){
                            //Process tweets
                        })
                    }, 5000);

                })


            }

            gatheringTweetsOn = !gatheringTweetsOn
        }
        setInterval(function(){


             var generateRandomTweets = function(){
                 //[[[2.0966720581,41.3507835316],[2.2281646729,41.3507835316],[2.2281646729,41.4496747477],[2.0966720581,41.4496747477],[2.0966720581,41.3507835316]]]
                var bbox = [2.0504377635,41.2787636541,2.3045074059,41.4725622346];

                var minLng = 2.0966720581;
                var maxLng = 2.2281646729;

                var minLat = 41.3507835316;
                var maxLat = 41.4496747477;

                var maxTweets= 20;
                var minTweets= 2;

                var numTweetsToGenerate =   Math.floor(Math.random() * (maxTweets - minTweets)) + minTweets;

                var genatedTweets = [];
                var lat, lng;

                for(var i=0; i<numTweetsToGenerate; i++){



                    lng = Math.random() * (maxLng - minLng) + minLng;
                    lat = Math.random() * (maxLat - minLat) + minLat;
                    if((lng-2)/(lat-41) <0.56){ // Filter tweets not on water
                        genatedTweets.push({"coordinates":[lat, lng]})
                    }

                }

                return genatedTweets;
            };


            var generatedTweets = generateRandomTweets();

            generatedTweets.forEach(function(d){
                console.log("D: ", d);
                paintTweet({"coordinates":d.coordinates});

                // /paintTweet({"coordinates":[41.387034, 2.170020]})
            })

            //paintTweet({"coordinates":[41.2787636541, 2.0504377635]});


        }, 750);



        $scope.getFlatsRentalPrice = function(){
            DataExtractorService.getRentalPrice().then(function(d){
                //Process tweets
            })
        }

        $scope.getFlatsRentalPrice()


    });
