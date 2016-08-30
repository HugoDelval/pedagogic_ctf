'use strict';

angular.module('myApp.login', ['ngRoute', 'ngCookies'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/user/login', {
    templateUrl: 'login/login.html',
    controller: 'LoginCtrl'
  });
}])

.controller('LoginCtrl', ['$location', '$scope', '$http', '$cookies', function($location, $scope, $http, $cookies) {

	/* ------ BEGIN INIT ------ */
	$scope.request = {};
	$scope.user = $cookies.getObject('user') || {};
	if(!$scope.user.nick){
		$scope.user = {}
	}
	if($scope.user && $scope.user.isLoggedIn){
		alert('You are already logged in');
		$location.path('/user/me');
	}
	/* ------ END INIT ------ */


	/* ------ BEGIN SERVER INTERACTION ------ */
	$scope.login = function(){
		$http.post('/v1.0/user/login', $scope.request).success(function(data){
			$scope.user.token = data;
			$scope.user.isLoggedIn = true;
			$scope.user.nick = $scope.request.nick;
			$cookies.putObject('user', $scope.user);
			$location.path('/user/me');
		}).error(function(error){
			$.snackbar({
		        content: error.message,
		        timeout: 5000
		    });
			$location.path('/');
		});
	}

	/* ------ END SERVER INTERACTION ------ */
}]);
