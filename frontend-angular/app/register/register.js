'use strict';

angular.module('myApp.register', ['ngRoute', 'ngCookies'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/user/register', {
    templateUrl: 'register/register.html',
    controller: 'RegisterCtrl'
  });
}])

.controller('RegisterCtrl', ['$location', '$scope', '$http', '$cookies', function($location, $scope, $http, $cookies) {

	/* ------ BEGIN INIT ------ */
	$scope.request = {};
	$scope.user = $cookies.getObject('user') || {};
	if(!$scope.user.nick){
		$scope.user = {}
	}
	if($scope.user && $scope.user.isLoggedIn){
		alert('You are already logged in')
		$location.path("/user/me");
	}
	/* ------ END INIT ------ */


	/* ------ BEGIN SERVER INTERACTION ------ */
	$scope.register = function(){
		if($scope.request.password !== $scope.request.passwordConfirm){
			alert("Password mismatch" )
			return;
		}else{
			$http.post('/v1.0/user/register', $scope.request).success(function(data){
				$scope.response = data;
				$location.path("/user/me");
			}).error(function(data){
				alert("An error occured while processing request ");
				$scope.response = data;
			});
		}
	}

	/* ------ END SERVER INTERACTION ------ */
}]);
