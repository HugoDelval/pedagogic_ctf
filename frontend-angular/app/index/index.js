'use strict';

angular.module('myApp.index', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/', {
    templateUrl: 'index/index.html',
    controller: 'IndexCtrl'
  });
}])

.controller('IndexCtrl', ['$cookies', '$sce', '$scope', '$http', function($cookies, $sce, $scope, $http) {

	/* ------ BEGIN INIT ------ */
	$scope.isShownHash = {};
	$scope.request_execute = {};
	$scope.request_validate = {};
	$http.get('/v1.0').success( function ( data ) {
		$scope.challenges = data;
	}).error(function(data){
		alert("An error occured while processing request : " + data.message);
	});
	$scope.user = $cookies.getObject('user') || {};
	if(!$scope.user.nick){
		$scope.user = {}
	}
	/* ------ END INIT ------ */


	/* ------ BEGIN SERVER INTERACTION ------ */
	$scope.showChallenge = function(challengeId, extension, challIndex){
		if(! $scope.challenges[challIndex].languages[0].file_content){
			$http.get('/v1.0/challenge/' + challengeId).success( function ( data ) {
				$scope.challenges[challIndex].languages = data.languages;
			    $scope.isShownHash[challengeId + extension] = !$scope.isShownHash[challengeId + extension];
			    $scope.execute(challengeId, '/execute');
			}).error(function(data){
				alert("An error occured while processing request : " + data.message);
			})
		}else{
			$scope.isShownHash[challengeId + extension] = !$scope.isShownHash[challengeId + extension];
		}
	}
	$scope.execute = function(challengeId, path){
		$http.defaults.headers.common['X-CTF-AUTH'] = $scope.user.token;
		var req = {};
		if(path.indexOf("execute") !== -1)
			req = $scope.request_execute[challengeId];
		else
			req = $scope.request_validate[challengeId];
		$http.post('/v1.0/challenge/' + challengeId + path, req).success( function ( data ) {
				$scope.challengeResults = data;
		}).error( function ( data ) {
				$scope.challengeResults = "An error occured while processing request : " + data.message;
		});
	}
	$scope.reset = function(challengeId){
		$scope.request_execute = {};
		$scope.request_validate = {};
		$scope.execute(challengeId, '/execute');
	}
	/* ------ END SERVER INTERACTION ------ */


	/* ------ BEGIN UTILS ------ */
	$scope.isShown = function(challengeId, extension){
		return $scope.isShownHash[challengeId + extension];
	}
	$scope.buttonText = function(challengeId, extension, languageName){
		if($scope.isShown(challengeId, extension))
			return "Reduce";
		else
			return "Try the " +  languageName + " version of this challenge";
	}
	/* ------ END UTILS ------ */

}]);
