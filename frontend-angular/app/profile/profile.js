'use strict';

angular.module('myApp.profile', ['ngRoute', 'ngCookies'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/user/me', {
    templateUrl: 'profile/profile.html',
    controller: 'ProfileCtrl'
  });
}])

.controller('ProfileCtrl', ['$location', '$scope', '$http', '$cookies', function($location, $scope, $http, $cookies) {

	/* ------ BEGIN INIT ------ */
	$scope.request = {};
	$scope.validatedChallenges = [];
	$scope.nbChallengesAvailable = 0;
	$scope.score = 0;
	$scope.rank = 0;
	$scope.nbUsers = 0;
	$scope.user = $cookies.getObject('user') || {};
	if(!$scope.user.nick){
		$scope.user = {}
	}
	if(!$scope.user || !$scope.user.isLoggedIn){
		alert('You must login to access this page.');
		$location.path("/user/login");
	}else{
		$http.defaults.headers.common['X-CTF-AUTH'] = $scope.user.token;
		$http.get('/v1.0/user/me').success(function(me){

			// users scores -> rank + nbUsers
			$http.get('/v1.0/user').success( function ( users ) {
				$scope.nbUsers = users.length;
				var scores = new Array($scope.nbUsers);
				for(var userIt=0 ; userIt<$scope.nbUsers ; ++userIt){
					scores[userIt] = 0;
					$http.get('/v1.0/user/'+users[userIt].ID+'/validatedChallenges').success(function(validatedChalls){
						for (var challIt=0; challIt < validatedChalls.length ; ++challIt){
							$http.get('/v1.0/challenge/' + validatedChalls[challIt].ChallengeID).success(function(validatedChall){
								scores[userIt] += validatedChall.points;
								if(users[userIt].ID == me.ID){
									// user score + validated challenges
									$scope.validatedChallenges.push(validatedChall);
									$scope.score += validatedChall.points;
								}
							}).error(function(error){
								alert("An error occured : " + error.message);
							});
						}
					}).error(function(error){
						alert('An error occured :' + error.message);
					});
				}
				scores.sort();
				$scope.rank = scores.indexOf($scope.score) + 1;
			}).error(function(error){
				alert('An error occured :' + error.message);
			});
			// END users scores -> rank + nbUsers

		}).error(function(error){
			$scope.user.token = "";
			$scope.user.isLoggedIn = false;
			$scope.user.nick = "anonymous";
			$cookies.putObject('user', $scope.user);
			alert('You must login to access this page.');
			$location.path("/user/login");
		});

	}
	/* ------ END INIT ------ */


	/* ------ BEGIN USER-SERVER INTERACTION ------ */
	$scope.changePassword = function(){
		if($scope.request.password !== $scope.request.passwordConfirm){
			alert("Password mismatch " )
		}else{
			$http.post('/v1.0/user/me/changePassword', $scope.request).success(function(data){
				$scope.response = data;
			}).error(function(data){
				alert("An error occured while processing request ");
				$scope.response = data;
			});
		}
	}
	/* ------ END USER-SERVER INTERACTION ------ */
}]);
