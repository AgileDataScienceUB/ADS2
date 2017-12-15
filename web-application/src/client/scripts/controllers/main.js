'use strict';

/**
 * @ngdoc function
 * @name ADS_Group2_Application.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the ADS_Group2_Application
 */
angular.module('ADS_Group2_Application')
  .controller('WelcomeCtrl', function ($scope) {
    this.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];

      $scope.showTutorial = function(){
          introJs().start();
      };
  });
