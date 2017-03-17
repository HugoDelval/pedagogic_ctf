'use strict';

angular.module('myApp.index', ['ngRoute', 'ui.ace', 'angularModalService'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/', {
            templateUrl: 'index/index.html',
            controller: 'IndexCtrl'
        });
    }])

    .controller('IndexCtrl', ['$cookies', '$sce', '$scope', '$http', '$location', '$anchorScroll', 'ModalService', function ($cookies, $sce, $scope, $http, $location, $anchorScroll, ModalService) {

        /* ------ BEGIN INIT ------ */
        $.fn.extend({
            qcss: function (css) {
                return $(this).queue(function (next) {
                    $(this).css(css);
                    next();
                });
            }
        });

	$scope.executeButtonText = "Execute";
	$scope.correctButtonText = "Check if your code is better than mine!";

        $scope.isShownHash = {};
        $scope.requestExecute = {};
        $scope.requestValidate = {};
        $scope.challengeResults = {};
        $scope.requestCorrect = {};
        $scope.challenge = {};
        $scope.language = {};
        $http.get('/v1.0').then(function (response) {
            var challenges = response.data;
            $scope.challenges = challenges;
            for (var challIt = 0; challIt < $scope.challenges.length; ++challIt) {
                $scope.requestCorrect[$scope.challenges[challIt].challenge_id] = {};
            }
            $scope.showChallenge($scope.challenges[0].challenge_id, 0);
            $(".search-details-form").hide();
        }, function (response) {
            var error = response.data;
            $.snackbar({
                content: "An error occured while processing request : " + error.message,
                timeout: 3000 + error.message.length * 25
            });
        });
        $scope.user = $cookies.getObject('user') || {};
        if (!$scope.user.email) {
            $scope.user = {}
        }
        /* ------ END INIT ------ */


        /* ------ BEGIN SERVER INTERACTION ------ */
        $scope.showChallenge = function (challengeId, challIndex) {
            $scope.isShownHash = {};
            $scope.aceLoaded = {};
            $scope.editors = {};
            $http.get('/v1.0/challenge/' + challengeId).then(function (response) {
                $scope.challenge = response.data;
                $scope.challenge.challenge_id = challengeId;
                var challenge = $scope.challenge;
                $scope.challenges[challIndex].languages = challenge.languages;
                $scope.aceLoaded[challengeId] = {};
                $scope.editors[challengeId] = {};
                for (var languageIt = 0; languageIt < challenge.languages.length; ++languageIt) {
                    var language = challenge.languages[languageIt];
                    $scope.requestCorrect[challengeId][language.extension] = {
                        "content_script": language.file_content
                    };
                    $scope.aceLoaded[challengeId][language.extension] = (function (challId, ext) {
                        return function (_editor) {
                            $scope.editors[challId][ext] = _editor;
                            $scope.editors[challId][ext].renderer.updateFull();
                        };
                    })(challengeId, language.extension);
                }
                $scope.language = challenge.languages[0];
            }, function (response) {
                var error = response.data;
                $.snackbar({
                    content: "An error occured while processing request : " + error.message,
                    timeout: 3000 + error.message.length * 25
                });
            });
        };
        $scope.execute = function (challengeId, path, extension) {
            $http.defaults.headers.common['X-CTF-AUTH'] = $scope.user.token;
            var title = "";
            var message = "";
            var req = {};
            if (path.indexOf("execute") !== -1) {
		var previousButtonText = $scope.executeButtonText;
                $scope.executeButtonText = "Processing";
                $http.post('/v1.0/challenge/' + challengeId + path, $scope.requestExecute[challengeId]).then(function (response) {
                    var challOutput = response.data;
                    $anchorScroll("output_" + challengeId);
                    $("#output_" + challengeId, function() {
                        $("#output_" + challengeId).html(challOutput.message); // To generate XSS !!
                    })
                    $("#output_" + challengeId).delay(750).qcss({ backgroundColor: '#FFFF70' }).delay(750).qcss({ backgroundColor: 'white' }).delay(750).qcss({ backgroundColor: '#FFFF70' }).delay(750).qcss({ backgroundColor: 'white' }).delay(750);
		    $scope.executeButtonText = previousButtonText;
                }, function (response) {
                    title = "Execution error";
                    message = response.data.message;
		    $scope.executeButtonText = previousButtonText;
	            showModal(title, message);
                });
            }
            else if (path.indexOf("validate") !== -1) {
                // validate
                $http.post('/v1.0/challenge/' + challengeId + path, $scope.requestValidate[challengeId]).then(function (response) {
                    title = "Success";
                    message = response.data.message;
	            showModal(title, message);
                }, function (response) {
                    title = "Validation error";
                    message = response.data.message;
	            showModal(title, message);
                });
            } else if (path.indexOf("correct") !== -1) {
                // correct
		var previousButtonText = $scope.correctButtonText;
                $scope.correctButtonText = "Checking";
                $scope.requestCorrect[challengeId][extension].language_extension = extension;
                $http.post('/v1.0/challenge/' + challengeId + path, $scope.requestCorrect[challengeId][extension]).then(function (response) {
                    title = "Success";
                    message = response.data.message;
		    $scope.correctButtonText = previousButtonText;
	            showModal(title, message);
                }, function (response) {
                    title = "Correction error";
                    message = response.data.message;
		    $scope.correctButtonText = previousButtonText;
	            showModal(title, message);
                });
            }
        };
        $scope.reset = function (challengeId) {
            $scope.requestExecute = {};
            $scope.requestValidate = {};
            $scope.execute(challengeId, '/execute');
        };
        /* ------ END SERVER INTERACTION ------ */


        /* ------ BEGIN UTILS ------ */
        $scope.isChallengeSelected = function (challenge) {
            return challenge.challenge_id == $scope.challenge.challenge_id;
        }
        $scope.isLanguageSelected = function (language) {
            return language == $scope.language;
        }
        $scope.areLanguageAndChallengeSelected = function (language, challenge) {
            return $scope.isChallengeSelected(challenge) && $scope.isLanguageSelected(language);
        }
        $scope.selectLanguage = function (language) {
            $scope.language = language;
        }
        /* ------ END UTILS ------ */

        function showModal(title, message) {
	    ModalService.showModal({
	      templateUrl: "partials/modal.html",
	      controller: function() {
	        this.title = title;
	        this.message = message;
	      },
	      controllerAs : "modal"
	    }).then(function(modal) {
		modal.element.modal();
	    });
	}

    }]);
