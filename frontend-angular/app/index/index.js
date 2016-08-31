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
		for(var challIt=0 ; challIt<$scope.challenges.length ; ++challIt){
			for(var paramIt=0 ; paramIt<$scope.challenges[challIt].parameters.length ; ++paramIt){
				var param = $scope.challenges[challIt].parameters[paramIt];
			}
		}
		$(".search-details-form").hide()
	}).error(function(error){
		$.snackbar({
			content: "An error occured while processing request : " + error.message,
			timeout: 3000 + error.message.length * 25
		});
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
			}).error(function(error){
                $.snackbar({
                    content: "An error occured while processing request : " + error.message,
                    timeout: 3000 + error.message.length * 25
                });
			})
		}else{
			$scope.isShownHash[challengeId + extension] = !$scope.isShownHash[challengeId + extension];
		}
	};
	$scope.execute = function(challengeId, path){
		$http.defaults.headers.common['X-CTF-AUTH'] = $scope.user.token;
		var req = {};
		if(path.indexOf("execute") !== -1){
			$http.post('/v1.0/challenge/' + challengeId + path, $scope.request_execute[challengeId]).success( function ( data ) {
				$scope.challengeResults = data;
			}).error( function ( data ) {
				$scope.challengeResults.message = "An error occured while processing request : " + data.message;
			});
		}
		else{
			// validate
			$http.post('/v1.0/challenge/' + challengeId + path, $scope.request_validate[challengeId]).success( function ( data ) {
				alert(data.message); // modal
			}).error( function (error) {
				alert(error.message);
			});
		}
	};
	$scope.reset = function(challengeId){
		$scope.request_execute = {};
		$scope.request_validate = {};
		$scope.execute(challengeId, '/execute');
	};
	/* ------ END SERVER INTERACTION ------ */


	/* ------ BEGIN UTILS ------ */
	$scope.isShown = function(challengeId, extension){
		return $scope.isShownHash[challengeId + extension];
	};
	$scope.buttonText = function(challengeId, extension, languageName){
		if($scope.isShown(challengeId, extension))
			return "Hide " + languageName;
		else
			return "Show " + languageName;
	};
	/* ------ END UTILS ------ */

}]);
