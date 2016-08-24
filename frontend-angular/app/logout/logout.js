'use strict';

angular.module('myApp.logout', ['ngRoute', 'ngCookies'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/user/logout', {
    templateUrl: 'logout/logout.html',
    controller: 'LogoutCtrl'
  });
}])

.controller('LogoutCtrl', ['$location', '$scope', '$http', '$cookies', function($location, $scope, $http, $cookies) {
	$scope.user = $cookies.getObject('user') || {};
	if(!$scope.user.nick){
		$scope.user = {}
	}
	if(!$scope.user || !$scope.user.isLoggedIn){
		alert('You are already logged out');
		$location.path('/');
	}else{
		$http.defaults.headers.common['X-CTF-AUTH'] = $scope.user.token;
		$http.post('/v1.0/user/logout', null).success(function(data){
			$scope.response = data;
			$scope.user.isLoggedIn = false;
			$scope.user.token = "";
			$scope.user.nick = "anonymous";
			$cookies.putObject('user', $scope.user);
			alert(data.message);
			$location.path('/');
		}).error(function(data){
			alert("An error occured while processing request ");
		});
	}
}]);
