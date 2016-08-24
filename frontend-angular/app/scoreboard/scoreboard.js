'use strict';

angular.module('myApp.scoreboard', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/user', {
    templateUrl: 'scoreboard/scoreboard.html',
    controller: 'ScoreboardCtrl'
  });
}])

.controller('ScoreboardCtrl', ['$sce', '$scope', '$http', 'UserService', function($sce, $scope, $http, UserService) {

	/* ------ BEGIN INIT ------ */
	$scope.request = {};
	$http.get('/v1.0/user').success( function ( data ) {
		$scope.users = data;
	}).error(function(data){
		alert("An error occured while processing request : " + data.message);
	});
	/* ------ END INIT ------ */
}]);
