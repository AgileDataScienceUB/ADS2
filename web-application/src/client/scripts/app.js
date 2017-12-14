'use strict';

/**
 * @ngdoc overview
 * @name ADS_Group2_Application
 * @description
 * # ADS_Group2_Application
 *
 * Main module of the application.
 */
 var app = angular
  .module('ADS_Group2_Application', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'duScroll',
    'rzModule'
  ])
  .config(function ($routeProvider,$locationProvider) {
    $locationProvider.hashPrefix('');
    $routeProvider
      // .when('/', {
      //   templateUrl: 'views/main.html',
      //   controller: 'MainCtrl',
      //   controllerAs: 'main'
      // })

        .when('/welcome', {
            templateUrl: 'views/welcome.html',
            controller: 'WelcomeCtrl',
            controllerAs: 'welcome'
        })

      .when('/map-explore', {
        templateUrl: 'views/map-explore.html',
        controller: 'MapCtrl-Exp',
        controllerAs: 'map'
      })

        .when('/map-recommend', {
            templateUrl: 'views/map-recommend.html',
            controller: 'MapCtrl-Rec',
            controllerAs: 'map'
        })

      .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl',
        controllerAs: 'about'
      })


      .otherwise({
        redirectTo: '/welcome'
      });
  });
