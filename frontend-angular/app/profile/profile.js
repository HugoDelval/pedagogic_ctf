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
	$scope.nbChallengesAvailable = 0;
	$scope.totalScoreChallenges = 0;
	$scope.nbUsers = 0;
	$scope.user = $cookies.getObject('user') || {};
	if(!$scope.user.nick){
		$scope.user = {}
	}
	if(!$scope.user || !$scope.user.isLoggedIn){
		$.snackbar({
			content: "You must login to access this page.",
			timeout: 3000
		});
		$location.path("/user/login");
	}else{
		$http.defaults.headers.common['X-CTF-AUTH'] = $scope.user.token;
		$http.get('/v1.0/user/me').success(function(me){

			$scope.user.score = 0;
			$scope.user.rank = 0;
			$scope.user.validatedChallenges = [];
			// users scores -> rank + nbUsers
			$http.get('/v1.0/user').success( function ( users ) {

				$scope.nbUsers = users.length;
				var scores = new Array($scope.nbUsers);
				var nbUsersDone = 0.00001; // float precision.. We never know.
				var calculateRank = function(increment){
					nbUsersDone += increment;
					if($scope.nbUsers <= nbUsersDone){
						scores.sort().reverse();
						$scope.user.rank = scores.indexOf($scope.user.score) + 1;
					}
				}
				for(var userIt=0 ; userIt<$scope.nbUsers ; ++userIt){
					scores[userIt] = 0;
					$http.get('/v1.0/user/'+users[userIt].ID+'/validatedChallenges').success((function(userIterator){
						return function(validatedChalls){
							for (var challIt=0; challIt < validatedChalls.length ; ++challIt){
								$http.get('/v1.0/challenge/' + validatedChalls[challIt].ChallengeID).success((function(userIter, currId, validatedChallLink) {
								    return function(validatedChall) {
										scores[userIter] += validatedChall.points;
										if(me.ID == currId){
											// user score + validated challenges
											validatedChall.date_validated = validatedChallLink.date_validated;
											$scope.user.validatedChallenges.push(validatedChall);
											$scope.user.score += validatedChall.points;
										}
										calculateRank(1.0/validatedChalls.length);
								    }
								})(userIterator, users[userIterator].ID, validatedChalls[challIt])).error(function(error){
                                    $.snackbar({
                                        content: "An error occured while processing request : " + error.message,
                                        timeout: 3000 + error.message.length * 25
                                    });
								});
							}
							if (validatedChalls.length == 0){
								calculateRank(1);
							}
						}
					})(userIt)).error(function(error){
                        $.snackbar({
                            content: "An error occured while processing request : " + error.message,
                            timeout: 3000 + error.message.length * 25
                        });
					});
				}
			}).error(function(error){
                $.snackbar({
                    content: "An error occured while processing request : " + error.message,
                    timeout: 3000 + error.message.length * 25
                });
			});
			// END users scores -> rank + nbUsers

		}).error(function(){
			$scope.user.token = "";
			$scope.user.isLoggedIn = false;
			$scope.user.nick = "anonymous";
			$cookies.putObject('user', $scope.user);
            $.snackbar({
                content: "You must login to access this page.",
                timeout: 3000
            });
			$location.path("/user/login");
		});
		$http.get('/v1.0/challenge').success(function(challenges){
			$scope.nbChallengesAvailable = challenges.length;
			for(var challIt=0 ; challIt<challenges.length ; ++challIt){
				$scope.totalScoreChallenges += challenges[challIt].points;
			}
		}).error(function(error){
            $.snackbar({
                content: "An error occured while processing request : " + error.message,
                timeout: 3000 + error.message.length * 25
            });
		});
	}
	/* ------ END INIT ------ */


	/* ------ BEGIN USER-SERVER INTERACTION ------ */
	$scope.changePassword = function(){
		if($scope.request.password !== $scope.request.passwordConfirm){
            $.snackbar({
                content: "Password mismatch.",
                timeout: 3000
            });
		}else{
			$http.put('/v1.0/user/me/changePassword', $scope.request).success(function(data){
				$scope.response = data;
			}).error(function(error){
                $.snackbar({
                    content: "An error occured while processing request : " + error.message,
                    timeout: 3000 + error.message.length * 25
                });
			});
		}
	};
	$scope.deleteAccount = function(){
		var ask = confirm("Are you sure?");
		if(ask){
			$http.delete('/v1.0/user/me/unregister').success(function(response){
                $.snackbar({
                    content: response.message,
                    timeout: 3000
                });
				$location.path("/");
			}).error(function(error){
                $.snackbar({
                    content: "An error occured while processing request : " + error.message,
                    timeout: 3000 + error.message.length * 25
                });
			});
		}
	};
	/* ------ END USER-SERVER INTERACTION ------ */
}]);
