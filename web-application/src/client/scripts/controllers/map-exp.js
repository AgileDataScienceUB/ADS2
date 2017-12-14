'use strict';

/**
 * @ngdoc function
 * @name ADS_Group2_Application.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the ADS_Group2_Application
 */
angular.module('ADS_Group2_Application')
    .controller('MapCtrl-Exp', function ($scope, DataExtractorService) {
        this.awesomeThings = [
            'HTML5 Boilerplate',
            'AngularJS',
            'Karma'
        ];

        $scope.hideWelcome = false;


        $scope.heat_map_colors = ['#d7191c','#fdae61','#ffffbf','#a6d96a','#1a9641'];

        $scope.formOptions = {
            rental_council : false,
            rental_council_direction : 1,
            rental_web : false,
            rental_web_direction : 1,
            mean_size_price : false,
            mean_size_price_direction : 1,
            night : false,
            night_direction : 1,
            population : false,
            population_direction : 1,
            young : false,
            young_direction : 1,
            restaurants : false,
            restaurants_direction : 1,
            clothes_stores : false,
            clothes_stores_direction : 1,
            show_tweets :false,
            show_graph:false
        };


        $scope.getHeatMapData = function(){
            console.log("Getting heatmap data for; ", $scope.formOptions)

            if($scope.formOptions.show_tweets){
                // clearPaintedPaths();
                // if( $scope.granularitySelected == $scope.polygons1){
                //     paintDistrictsOverMap();
                // }else{
                //     paintNeighborhoodOverMap();
                // }

                removeLayers();

                gatheringTweetsOn = true;
                tweetsGatheringInterval = setInterval(function () {


                    var generateRandomTweets = function () {
                        //[[[2.0966720581,41.3507835316],[2.2281646729,41.3507835316],[2.2281646729,41.4496747477],[2.0966720581,41.4496747477],[2.0966720581,41.3507835316]]]
                        var bbox = [2.0504377635, 41.2787636541, 2.3045074059, 41.4725622346];

                        var minLng = 2.0966720581;
                        var maxLng = 2.2281646729;

                        var minLat = 41.3507835316;
                        var maxLat = 41.4496747477;

                        var maxTweets = 15;
                        var minTweets = 2;

                        var numTweetsToGenerate = Math.floor(Math.random() * (maxTweets - minTweets)) + minTweets;

                        var genatedTweets = [];
                        var lat, lng;

                        var sentiments = ['positive', 'negative', 'neutral', 'neutral', 'neutral',  'neutral'];

                        for (var i = 0; i < numTweetsToGenerate; i++) {


                            lng = Math.random() * (maxLng - minLng) + minLng;
                            lat = Math.random() * (maxLat - minLat) + minLat;
                            if ((lng - 2) / (lat - 41) < 0.5) { // Filter tweets not on water
                                genatedTweets.push({"coordinates": [lat, lng], "sentiment":sentiments[Math.floor(Math.random() * sentiments.length)]})
                            }

                        }

                        return genatedTweets;
                    };


                    var generatedTweets = generateRandomTweets();

                    generatedTweets.forEach(function (d) {
                        console.log("D: ", d);
                        paintTweet({"coordinates": d.coordinates, "sentiment":d.sentiment});

                        // /paintTweet({"coordinates":[41.387034, 2.170020]})
                    });

                    //paintTweet({"coordinates":[41.2787636541, 2.0504377635]});


                }, 750);
            }else{
                if (gatheringTweetsOn) { //Its on, should turn gathering off
                    gatheringTweetsOn = false;
                    clearInterval(tweetsGatheringInterval);
                }
            }


            if($scope.formOptions.show_graph){
                $scope.showTransportGraph();
            }else{
                removeLayers();
            }

            // if( $scope.granularitySelected == $scope.polygons1){
            //     paintDistrictsOverMap();
            // }else{
            //     paintNeighborhoodOverMap();
            // }

            DataExtractorService.getHeatMapData($scope.formOptions).then(function(response){
                console.log("Response: ", response);
            })

        }
        $scope.options = {
            "chart": {
                "type": "pieChart",
                "height": 500,
                "showLabels": true,
                "duration": 500,
                "labelThreshold": 0.01,
                "labelSunbeamLayout": true,
                "legend": {
                    "margin": {
                        "top": 5,
                        "right": 35,
                        "bottom": 5,
                        "left": 0
                    }
                }
            }
        }

        $scope.data = {

        }


        var paintedPolygons = -1;

        $scope.clickedPoint = "";
        var transport_stations = [];

        var recommendationShown=false;
        $scope.showReport = false;

        var barris;


        $scope.preferences = {};
        $scope.clickedPoint = [41.387034, 2.170020];
        $scope.preferences.maxRentalPrice =  "3500";
        $scope.preferences.minRentalPrice =  "400";
        $scope.preferences.maxTimeTravelling =  "60";
        $scope.preferences.nightLive = 0;

        $scope.changeNightLive = function(value){
            console.log("Changing night live value: ", value);
            $scope.preferences.nightLive = value;
        };



        $scope.tab = 0;

        $scope.currentDate = -1;

        $scope.STATE_STOP=1;
        $scope.STATE_PLAY=2;
        $scope.STATE_PAUSE=3;
        $scope.STATE_RESUME=4;

        $scope.time_slider_state = $scope.STATE_STOP;
        $scope.time_interval;

        $scope.displayInformation = 0;


        var gatheringTweetsOn = false;

        $scope.tweets_array = [];

        var tweetsGatheringInterval;

        var map, svg, g, tip, feature;
        var districtPolygons, choosenPolygon, colorToAssign, neighborhoodPolygons;
        var data;

        const USE_DISTRITCS_GRANULARITY = 0;
        const USE_NEIGHBORHOODS_GRANULARITY = 1;

        $scope.polygons1 = USE_DISTRITCS_GRANULARITY;
        $scope.polygons2 = USE_NEIGHBORHOODS_GRANULARITY;

        $scope.granularitySelected = $scope.polygons2;

        var map_added_elements = [];


        var heat_map_colors = ['#d73027','#fc8d59','#fee08b','#d9ef8b','#91cf60','#1a9850'];


        function projectPoint(x, y) {
            var point = map.latLngToLayerPoint(new L.LatLng(y, x));
            this.stream.point(point.x, point.y);

        }

        var clearPaintedPaths = function(){
            d3.selectAll(".polygon").remove();

            map.eachLayer(function(layer) {
                if(layer.hasOwnProperty("feature")){
                    map.removeLayer(layer);
                }

            });



        };

        var changePolygonColors = function(assigned_colors){

            if($scope.granularitySelected == $scope.polygons1){
                districtPolygons.each(function(d, i) {
                    // console.log("Polygon: ", d, i);
                    choosenPolygon = d3.select("#District_" + d.properties["C_Distri"]);


                    var selection = assigned_colors.filter(function( obj ) {
                        return obj.id == d.properties["C_Distri"];
                    });

                    colorToAssign = selection[0].color;

                    // console.log("Color to assign: ", colorToAssign);

                    d["price"] = selection[0].value;
                    //colorToAssign = "white";
                    choosenPolygon
                        .style("opacity", 1)
                        //.style("stroke", "white")
                        //.style("stroke-width", "2")
                        .style("fill", colorToAssign)
                        .attr("price", selection[0].value);

                });
            }else{

                // console.log("Assigned colors: ", assigned_colors);
                neighborhoodPolygons.each(function(d, i) {

                    colorToAssign = "white";
                    var selection = assigned_colors.filter(function( obj ) {
                        return obj.id == d.properties["C_Barri"];
                    });
                    colorToAssign = selection[0].color;
                    //console.log("Color to assign: ", colorToAssign);


                    choosenPolygon = d3.select("#Barri_"+d.properties["C_Barri"]);

                    d["price"] = selection[0].value;
                    //console.log("choosenPolygon: ", choosenPolygon);
                    choosenPolygon
                    //.style("opacity", 0.2)
                    //.style("stroke", "white")
                    //.style("stroke-width", "2")
                        .style("fill", colorToAssign)
                        .attr("price", selection[0].value);

                });
            }


        };


        var removeLayers = function(){
            // map.eachLayer(function(layer){
            //     console.log("layer: ", layer);
            //     map.removeLayer(layer);
            // });

            map_added_elements.forEach(function(d){
                map.removeLayer(d);
            });

            map_added_elements = [];

        };


        var paintDistrictsOverMap = function(){

            d3.json("data/divisiones_administrativas/districtes/districtes_geo.json", function (error, geojson) {


                // console.log("Extracted districts data: ", geojson);
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
                    .style("opacity", 1)
                    .style("z-index", 9999)
                    .attr("z-index", 9999);

                d3.selection.moveToFront(feature);

                feature.call(tip);

                feature.on('mouseover', function(d){
                    tip.show(d);
                    d3.select("#District_" + d.properties["C_Distri"]).style('opacity', 0);
                });
                feature.on('mouseout', function(d){
                    tip.hide(d);

                    d3.select("#District_" + d.properties["C_Distri"]).style('opacity', 1);
                });

                districtPolygons = feature;
                //ASDF



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

                map.on("viewreset", reset);
                reset();

            });
        }
        var paintNeighborhoodOverMap = function(){

            d3.json("data/divisiones_administrativas/barris/barris_geo.json", function (error, geojson) {


                barris = L.geoJSON(geojson, {
                    radius: 3,
                    fillColor: $scope.heat_map_colors[2],
                    color: 'black',
                    weight:1,
                    fillOpacity:0}
                ).addTo(map);

                barris.bindPopup(function(d) {
                    var result = "";

                    console.log("POPUP: ", d)
                    d = d.feature;

                    if(d.hasOwnProperty("properties")) {
                        console.log("D: ", d)

                        if (d.properties.hasOwnProperty("N_Barri")) {
                            result += "<p></p><strong>Neighborhood: </strong>" + d.properties['N_Barri'] + "</p>";
                        }

                        if (d.properties.hasOwnProperty("N_Distri")) {
                            //console.log("D: ", d);
                            result += "<p><strong>District: </strong>" + d.properties['N_Distri'] + "</p>";
                        }
                        if (d.properties.hasOwnProperty("Area")) {
                            //console.log("D: ", d);
                            result += "<p></p><strong>Area: </strong>" + d.properties['Area'] + "</p>";
                        }

                        if (d.properties.hasOwnProperty("Homes") && d.properties.hasOwnProperty("Dones")) {
                            //console.log("D: ", d);
                            result += "<p><strong>Population: </strong> </p><p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Men:&nbsp;" + d.properties['Homes'] + "</p><p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Women:&nbsp;" + d.properties['Dones'] + "</p>";
                            // result += '<nvd3 options="options" data="data"></nvd3>';

                            // $scope.data = [
                            //     {
                            //         key: "Men",
                            //         y: d.properties['Homes']
                            //     },
                            //     {
                            //         key: "Women",
                            //         y: d.properties['Dones']
                            //     }
                            //
                            // ]


                            if(!$scope.$$phase) {
                                //$digest or $apply
                                $scope.$apply()
                            }


                        }

                        if (d.properties.hasOwnProperty("WEB_1")) {
                            //console.log("D: ", d);
                            result += "<p><strong>Links: </strong> </p>"
                            result += "<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a target='_blank' href='"+d.properties['WEB_1']+"'>" + d.properties['WEB_1']+"</a></p>"
                            for(var i = 2; i< 10; i++){
                                if(d.properties.hasOwnProperty("WEB_"+i)){
                                    result += "<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a target='_blank' href='"+d.properties['WEB_'+i]+"'>" + d.properties['WEB_'+i]+"</a></p>"
                                }
                            }
                        }



                    }


                    // $('.leaflet-popup-content').css({"width":"100%"});
                    return result;
                },{
                    maxWidth : 560
                });


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

            // L.TileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            // L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', {
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
                        console.log("D: ", d)

                        if (d.properties.hasOwnProperty("N_Barri")) {
                            result += "<p></p><strong>Neighborhood: </strong>" + d.properties['N_Barri'] + "</p>";
                        }

                        if (d.properties.hasOwnProperty("N_Distri")) {
                            //console.log("D: ", d);
                            result += "<p><strong>District: </strong>" + d.properties['N_Distri'] + "</p>";
                        }

                        if (d.hasOwnProperty("price")) {
                            // console.log("D: ", d);
                            result += "<p><strong>Avg price: </strong>" + Math.floor(d['price']) + "€</p>";
                        }

                    }


                    return result;
                });


            map.on("click", function(d){
                $scope.clickedPoint = [d.latlng.lat.toFixed(5), d.latlng.lng.toFixed(5)];

                console.log("Clicked: ", d);
                if(!$scope.$$phase) {
                    //$digest or $apply
                    $scope.$apply()
                }
            })
        };

        createMap();


        $scope.changeShownPolygons = function(option){
            console.log("Changing polygons. Option: ", option);
            if (option == 0){
                clearPaintedPaths();
                paintDistrictsOverMap();

                $scope.granularitySelected = $scope.polygons1;
            }else{
                clearPaintedPaths();
                paintNeighborhoodOverMap();

                $scope.granularitySelected = $scope.polygons2;

            }
        };

        $scope.changeShownPolygons($scope.granularitySelected);


        /* Set the width of the side navigation to 250px */
        $scope.openNav = function() {

            document.getElementById("mySidenav").style.width = "25%";
        }

        /* Set the width of the side navigation to 0 */
        $scope.closeNav = function () {
            document.getElementById("mySidenav").style.width = "0";
        };


        var paintTweet = function(tweet){

            var mapBounds = map.getBounds();


            console.log("Tweet: ", tweet)
            var tweet_color = 'grey';
            if(tweet.sentiment == "positive"){
                tweet_color='green';
            }else if(tweet.sentiment == 'negative'){
                tweet_color='red';
            }
            //var marker1 = L.circle([tweet.coordinates[0]+0.15, tweet.coordinates[1]], 50);//[41.387034, 2.170020]);
            var marker1 = L.circleMarker(
                [tweet.coordinates[0],tweet.coordinates[1]], {
                    radius: 3,
                    fillColor: tweet_color,
                    color: tweet_color,
                    weight:1,
                    fillOpacity:0
                }
            );//[41.387034, 2.170020]);

            marker1.addTo(map);

            map_added_elements.push(marker1);

            setTimeout(function() { map.removeLayer(marker1); }, 2500);
        };

        /*
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
         */


//$scope.$watch("displayInformation", function(newValue, oldValue){
        $scope.displayInformationChanged = function(newValue){
            //newValue = $scope.displayInformation;
            console.log("Display information has changed: ", newValue);
            // do something

            if(newValue == 0){// Transport density
                if (gatheringTweetsOn) { //Its on, should turn gathering off
                    gatheringTweetsOn = false;
                    clearInterval(tweetsGatheringInterval);
                }
                removeLayers();
                clearPaintedPaths();
                if( $scope.granularitySelected == $scope.polygons1){
                    paintDistrictsOverMap();
                }else{
                    paintNeighborhoodOverMap();
                }



            }else if(newValue == 1){ // Rental price
                var assigned_colors = [];

                DataExtractorService.getRentalPrice().then(function(d){
                    console.log("Rental price: ", d.data);


                    var minX = Math.min.apply(Math, d.data.map(function(val) { return val.value; }));
                    var maxX = Math.max.apply(Math, d.data.map(function(val) { return val.value; }));


                    // console.log("Min value: ", minX)
                    // console.log("Max value: ", maxX)

                    var categories_range = (maxX - minX) / heat_map_colors.length;

                    // console.log("Max categories_range: ", categories_range);

                    if($scope.granularitySelected == $scope.polygons1){

                        var DISTRICTS_IDs = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"];

                        DISTRICTS_IDs.forEach(function(district_id){

                            var selection = d.data.filter(function( obj ) {
                                return obj["district"] == district_id;
                            });


                            var c = heat_map_colors[0];
                            var v = 0;
                            if(selection.length > 0 ){
                                var sum = 0;
                                selection.forEach(function(e){
                                    sum += e.value
                                });



                                var avg = sum / selection.length;

                                // console.log("AVG: ", avg);

                                v = avg;
                                c = heat_map_colors[(heat_map_colors.length-1) - Math.floor((avg - minX) / categories_range)];

                            }


                            assigned_colors.push({"id": district_id, "color": c, "value": v});


                        })


                        console.log("assigned_colors: ", assigned_colors)
                        changePolygonColors(assigned_colors)

                    }else{
                        d.data.forEach(function(polygon){
                            // console.log("For value: ", polygon.value)
                            // console.log("CAtegory is: ", ((polygon.value - minX) / categories_range));
                            var c = heat_map_colors[(heat_map_colors.length-1) - Math.floor((polygon.value - minX) / categories_range)];
                            assigned_colors.push({"id": polygon.neighborhood_id, "color": c, "value": polygon.value});
                        });

                        console.log("heat_map_colors: ", heat_map_colors)

                        changePolygonColors(assigned_colors)
                    }

                });

                if (gatheringTweetsOn) { //Its on, should turn gathering off
                    gatheringTweetsOn = false;
                    clearInterval(tweetsGatheringInterval);
                }

                //changeDistrictPolygonColors(heat_map_colors, )


            }else if(newValue == 2){  // Tweets
                gatheringTweetsOn = true;
                clearPaintedPaths();
                // if( $scope.granularitySelected == $scope.polygons1){
                //     paintDistrictsOverMap();
                // }else{
                //     paintNeighborhoodOverMap();
                // }

                removeLayers();
                tweetsGatheringInterval = setInterval(function () {


                    var generateRandomTweets = function () {
                        //[[[2.0966720581,41.3507835316],[2.2281646729,41.3507835316],[2.2281646729,41.4496747477],[2.0966720581,41.4496747477],[2.0966720581,41.3507835316]]]
                        var bbox = [2.0504377635, 41.2787636541, 2.3045074059, 41.4725622346];

                        var minLng = 2.0966720581;
                        var maxLng = 2.2281646729;

                        var minLat = 41.3507835316;
                        var maxLat = 41.4496747477;

                        var maxTweets = 15;
                        var minTweets = 2;

                        var numTweetsToGenerate = Math.floor(Math.random() * (maxTweets - minTweets)) + minTweets;

                        var genatedTweets = [];
                        var lat, lng;

                        var sentiments = ['positive', 'negative', 'neutral', 'neutral', 'neutral',  'neutral'];

                        for (var i = 0; i < numTweetsToGenerate; i++) {


                            lng = Math.random() * (maxLng - minLng) + minLng;
                            lat = Math.random() * (maxLat - minLat) + minLat;
                            if ((lng - 2) / (lat - 41) < 0.5) { // Filter tweets not on water
                                genatedTweets.push({"coordinates": [lat, lng], "sentiment":sentiments[Math.floor(Math.random() * sentiments.length)]})
                            }

                        }

                        return genatedTweets;
                    };


                    var generatedTweets = generateRandomTweets();

                    generatedTweets.forEach(function (d) {
                        console.log("D: ", d);
                        paintTweet({"coordinates": d.coordinates, "sentiment":d.sentiment});

                        // /paintTweet({"coordinates":[41.387034, 2.170020]})
                    })

                    //paintTweet({"coordinates":[41.2787636541, 2.0504377635]});


                }, 750);

            }else if(newValue == 3){  // Night live
                if (gatheringTweetsOn) { //Its on, should turn gathering off
                    gatheringTweetsOn = false;
                    clearInterval(tweetsGatheringInterval);
                }

                clearPaintedPaths();
                if( $scope.granularitySelected == $scope.polygons1){
                    paintDistrictsOverMap();
                }else{
                    paintNeighborhoodOverMap();
                }

            }else if(newValue == 4){  // Age of population
                if (gatheringTweetsOn) { //Its on, should turn gathering off
                    gatheringTweetsOn = false;
                    clearInterval(tweetsGatheringInterval);
                }
                removeLayers();
                clearPaintedPaths();
                if( $scope.granularitySelected == $scope.polygons1){
                    paintDistrictsOverMap();
                }else{
                    paintNeighborhoodOverMap();
                }


            }else if(newValue == 5){   // Studies level
                if (gatheringTweetsOn) { //Its on, should turn gathering off
                    gatheringTweetsOn = false;
                    clearInterval(tweetsGatheringInterval);
                }
                removeLayers();
                clearPaintedPaths();
                if( $scope.granularitySelected == $scope.polygons1){
                    paintDistrictsOverMap();
                }else{
                    paintNeighborhoodOverMap();
                }


            }else if(newValue == 6){  //  Mean income
                if (gatheringTweetsOn) { //Its on, should turn gathering off
                    gatheringTweetsOn = false;
                    clearInterval(tweetsGatheringInterval);
                }

                removeLayers();
                clearPaintedPaths();
                if( $scope.granularitySelected == $scope.polygons1){
                    paintDistrictsOverMap();
                }else{
                    paintNeighborhoodOverMap();
                }


            }else if(newValue == 7){  //  Mean income
                if (gatheringTweetsOn) { //Its on, should turn gathering off
                    gatheringTweetsOn = false;
                    clearInterval(tweetsGatheringInterval);
                }
                removeLayers();
                clearPaintedPaths();
                $scope.showTransportGraph();
            }


        };


        $scope.toggleTweetsGathering = function() {
            if (gatheringTweetsOn) { //Its on, should turn gathering off
                gatheringTweetsOn = false;
                clearInterval(tweetsGatheringInterval);
            } else {
                gatheringTweetsOn = true;
                tweetsGatheringInterval = setInterval(function () {


                    var generateRandomTweets = function () {
                        //[[[2.0966720581,41.3507835316],[2.2281646729,41.3507835316],[2.2281646729,41.4496747477],[2.0966720581,41.4496747477],[2.0966720581,41.3507835316]]]
                        var bbox = [2.0504377635, 41.2787636541, 2.3045074059, 41.4725622346];

                        var minLng = 2.0966720581;
                        var maxLng = 2.2281646729;

                        var minLat = 41.3507835316;
                        var maxLat = 41.4496747477;

                        var maxTweets = 10;
                        var minTweets = 2;

                        var numTweetsToGenerate = Math.floor(Math.random() * (maxTweets - minTweets)) + minTweets;

                        var genatedTweets = [];
                        var lat, lng;

                        for (var i = 0; i < numTweetsToGenerate; i++) {


                            lng = Math.random() * (maxLng - minLng) + minLng;
                            lat = Math.random() * (maxLat - minLat) + minLat;
                            if ((lng - 2) / (lat - 41) < 0.56) { // Filter tweets not on water
                                genatedTweets.push({"coordinates": [lat, lng]})
                            }

                        }

                        return genatedTweets;
                    };


                    var generatedTweets = generateRandomTweets();

                    generatedTweets.forEach(function (d) {
                        // console.log("D: ", d);
                        paintTweet({"coordinates": d.coordinates});

                        // /paintTweet({"coordinates":[41.387034, 2.170020]})
                    })

                    //paintTweet({"coordinates":[41.2787636541, 2.0504377635]});


                }, 250);
            }

        };


        $scope.calculateRecommendation = function(){

            console.log("Getting recomendation for: ");
            console.log("transport_type: ", $scope.transportOption);

            removeLayers();
            clearPaintedPaths();
            if( $scope.granularitySelected == $scope.polygons1){
                paintDistrictsOverMap();
            }else{
                paintNeighborhoodOverMap();
            }


            if($scope.granularitySelected == $scope.polygons1){

                //clearPaintedPaths();
                //paintDistrictsOverMap();

                districtPolygons.each(function(d, i) {

                    choosenPolygon = d3.select("#District_" + d.properties["C_Distri"]);

                    colorToAssign = heat_map_colors[Math.floor(Math.random() * (heat_map_colors.length ))]

                    choosenPolygon
                        .style("opacity", 1)
                        //.style("stroke", "white")
                        //.style("stroke-width", "2")
                        .style("fill", colorToAssign)

                });
            }else{

                setTimeout(function(){
                    // favourite_point,max_transport_time, max_rental_price, min_rental_price, night_live
                    DataExtractorService.getRecommendation($scope.clickedPoint, $scope.preferences.maxTimeTravelling, $scope.preferences.maxRentalPrice, $scope.preferences.minRentalPrice, $scope.preferences.nightLive).then(function(data){
                        // clearPaintedPaths();
                        // paintNeighborhoodOverMap();
                        recommendationShown = true;

                        console.log("Recomendation: ", data.data.recommendation);
                        // if(barris !== undefined){
                        //     console.log("BARRIS: ", barris)
                        //     //polygon.setStyle({fillColor: '#0000FF'});
                        // };


                        // console.log("rental_data: ", rental_data);
                        map.eachLayer(function(layer) {
                            if(layer.hasOwnProperty("feature")){
                                // map.removeLayer(layer);
                                if(data.data.recommendation.indexOf(parseInt(layer.feature.properties["C_Barri"]))>= 0) {


                                    layer.setStyle({fillColor: 'green', fillOpacity: 1});
                                }else{
                                    map.removeLayer(layer);
                                }
                            }



                            /*
                             neighborhoodPolygons.each(function(d, i) {


                             choosenPolygon = d3.select("#Barri_" + d.properties["C_Barri"]);
                             console.log("d: ")

                             if(data.data.recommendation.indexOf(parseInt(d.properties["C_Barri"]))>= 0){
                             colorToAssign = "green";

                             choosenPolygon
                             .style("opacity", 1)
                             //.style("stroke", "white")
                             //.style("stroke-width", "2")
                             .style("fill", colorToAssign)
                             }else{
                             choosenPolygon = d3.select("#Barri_" + d.properties["C_Barri"]);
                             choosenPolygon
                             .style("opacity", 0)
                             //.style("stroke", "white")
                             //.style("stroke-width", "2")
                             .style("fill", colorToAssign)
                             }




                             });
                             */
                        })


                    });
                }, 50)


            }
        }


        var paintPointOnMap = function(point_lat, point_lng, color, text){
            var circle_point = L.circleMarker(
                [point_lat,point_lng], {
                    radius: 3,
                    fillColor: color,
                    color: color,
                    weight:1,
                    fillOpacity:1
                }
            );

            circle_point.bindPopup(text);

            transport_stations.push({"marker":circle_point, "name": text});

            var popup;
            circle_point.on('mouseover', function(e) {


                // popup = L.popup()
                //     .setLatLng(e.latlng)
                //     .setContent(text)
                //     .openOn(map);

                this.openPopup();

                console.log("Pop up: ", popup);
            });

            circle_point.on('mouseout', function(e) {

                this.closePopup();
            });

            map_added_elements.push(circle_point);
            circle_point.addTo(map);
        };


        var paintLineOnMap = function(origin, target, color){

            var coords = [origin.marker.getLatLng(), target.marker.getLatLng()]
            var line = L.polyline(coords);
            line.setStyle({
                color: color
            });

            map_added_elements.push(line);

            line.addTo(map)
        };
        $scope.showTransportGraph = function(){
            d3.csv("data/transport/Lnodelist.csv", function (error, data) {

                console.log("Stations data: ", data);
                data.forEach(function(d) {
                    paintPointOnMap(d.Lat, d.Lon, "white", d.name);

                });


                d3.csv("data/transport/Ledgelist.csv", function (error, edges_data) {

                    console.log("Edges data: ", edges_data);
                    edges_data.forEach(function(edge) {

                        //console.log("Transport stations: ", transport_stations);
                        var origin = transport_stations.filter(function(station){
                            return station.name == edge.nodo1;
                        });

                        var target = transport_stations.filter(function(station){
                            return station.name == edge.nodo2;
                        });

                        if(origin.length >0 && target.length > 0){
                            paintLineOnMap(origin[0], target[0], edge.color);
                        }


                    });
                    data.forEach(function(d) {
                        paintPointOnMap(d.Lat, d.Lon, "white", d.name);

                    });



                });
            });
        }


        $scope.tabChanged = function(){
            if (gatheringTweetsOn) { //Its on, should turn gathering off
                gatheringTweetsOn = false;
                clearInterval(tweetsGatheringInterval);
            }
            removeLayers();
            clearPaintedPaths();

            if($scope.tab != 1){
                if( $scope.granularitySelected == $scope.polygons1){
                    paintDistrictsOverMap();
                }else{
                    paintNeighborhoodOverMap();
                }
            }

            recommendationShown = false;

        }


    });
