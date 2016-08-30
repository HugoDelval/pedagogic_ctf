'use strict';

angular.module('myApp.userProfile', ['ngRoute', 'ngCookies'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/user/:userId', {
    templateUrl: 'user_profile/user_profile.html',
    controller: 'UserProfileCtrl'
  });
}])

.controller('UserProfileCtrl', ['$routeParams', '$location', '$scope', '$http', '$cookies', function($routeParams, $location, $scope, $http, $cookies) {

	/* ------ BEGIN INIT ------ */
	$scope.request = {};
	$scope.nbChallengesAvailable = 0;
	$scope.totalScoreChallenges = 0;
	$scope.nbUsers = 0;
	$scope.user = {};
	$http.get('/v1.0/user/' + $routeParams.userId).success(function(me){
		$scope.user = me;
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
									timeout: 3000
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
                        timeout: 3000
                    });
				});
			}
		}).error(function(error){
            $.snackbar({
                content: "An error occured while processing request : " + error.message,
                timeout: 3000
            });
		});
		// END users scores -> rank + nbUsers

	}).error(function(error){
        $.snackbar({
            content: "User does not exists : " + error.message,
            timeout: 3000
        });
		$location.path("/user");
	});
	$http.get('/v1.0/challenge').success(function(challenges){
		$scope.nbChallengesAvailable = challenges.length;
		for(var challIt=0 ; challIt<challenges.length ; ++challIt){
			$scope.totalScoreChallenges += challenges[challIt].points;
		}
	}).error(function(error){
        $.snackbar({
            content: "An error occured while processing request : " + error.message,
            timeout: 3000
        });
	});
	/* ------ END INIT ------ */

}]);
