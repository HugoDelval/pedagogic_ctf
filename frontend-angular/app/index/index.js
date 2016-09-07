'use strict';

angular.module('myApp.index', ['ngRoute', 'ui.ace'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/', {
    templateUrl: 'index/index.html',
    controller: 'IndexCtrl'
  });
}])

.controller('IndexCtrl', ['$cookies', '$sce', '$scope', '$http', function($cookies, $sce, $scope, $http) {

	/* ------ BEGIN INIT ------ */
	$scope.isShownHash = {};
	$scope.requestExecute = {};
	$scope.requestValidate = {};
	$scope.challengeResults = {};
	$scope.requestCorrect = {};
	$http.get('/v1.0').success( function ( challenges ) {
		$scope.challenges = challenges;
		for(var challIt=0 ; challIt<$scope.challenges.length ; ++challIt){
			$scope.requestCorrect[$scope.challenges[challIt].challenge_id] = {};
		}
		$(".search-details-form").hide();
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
			$scope.aceLoaded = {};
			$scope.editors = {};
			$http.get('/v1.0/challenge/' + challengeId).success( function ( challenge ) {
				$scope.challenges[challIndex].languages = challenge.languages;
			    $scope.isShownHash[challengeId + extension] = !$scope.isShownHash[challengeId + extension];
			    $scope.aceLoaded[challengeId] = {}
			    $scope.editors[challengeId] = {}
			    for(var languageIt=0 ; languageIt<challenge.languages.length ; ++languageIt){
					var language = challenge.languages[languageIt];
				    $scope.requestCorrect[challengeId][language.extension] = {
    					"content_script": language.file_content
    				};
    				$scope.aceLoaded[challengeId][language.extension] = (function(challId, ext){
    					return function(_editor){
    						$scope.editors[challId][ext] = _editor;
    						if (ext == extension){
								$scope.editors[challId][ext].renderer.updateFull();
    						}
    					};
    				})(challengeId, language.extension);
				}
			    $scope.execute(challengeId, '/execute');
			}).error(function(error){
                $.snackbar({
                    content: "An error occured while processing request : " + error.message,
                    timeout: 3000 + error.message.length * 25
                });
			})
		}else{
			$scope.isShownHash[challengeId + extension] = !$scope.isShownHash[challengeId + extension];
			$scope.editors[challengeId][extension].renderer.updateFull();
		}
    	
	};
	$scope.execute = function(challengeId, path, extension=null){
		$http.defaults.headers.common['X-CTF-AUTH'] = $scope.user.token;
		var req = {};
		if(path.indexOf("execute") !== -1){
			$http.post('/v1.0/challenge/' + challengeId + path, $scope.requestExecute[challengeId]).success( function ( challOutput ) {
				$scope.challengeResults[challengeId] = challOutput;
			}).error( function ( error ) {
				$scope.challengeResults[challengeId].message = "An error occured while processing request : " + error.message;
			});
		}
		else if (path.indexOf("validate") !== -1){
			// validate
			$http.post('/v1.0/challenge/' + challengeId + path, $scope.requestValidate[challengeId]).success( function ( data ) {
				alert(data.message); // modal
			}).error( function (error) {
				alert(error.message);
			});
		}else if(path.indexOf("correct") !== -1){
			// correct
			$scope.requestCorrect[challengeId][extension].language_extension = extension;
			$http.post('/v1.0/challenge/' + challengeId + path, $scope.requestCorrect[challengeId][extension]).success( function ( data ) {
				alert(data.message); // modal
			}).error( function (error) {
				alert(error.message);
			});
		}
	};
	$scope.reset = function(challengeId){
		$scope.requestExecute = {};
		$scope.requestValidate = {};
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
