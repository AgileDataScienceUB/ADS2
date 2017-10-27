'use strict';

/**
 * @ngdoc function
 * @name ADS_Group2_Application.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the ADS_Group2_Application
 */
angular.module('ADS_Group2_Application')
  .controller('AboutCtrl', function () {
    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];


    particlesJS.load('particles-js', 'data/particles.json', function() {
      console.log('callback - particles.js config loaded');
    });

  });
