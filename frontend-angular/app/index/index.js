'use strict';

angular.module('myApp.index', ['ngRoute', 'ui.ace'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/', {
            templateUrl: 'index/index.html',
            controller: 'IndexCtrl'
        });
    }])

    .controller('IndexCtrl', ['$cookies', '$sce', '$scope', '$http', '$location', '$anchorScroll', function ($cookies, $sce, $scope, $http, $location, $anchorScroll) {

        /* ------ BEGIN INIT ------ */
        $.fn.extend({
            qcss: function (css) {
                return $(this).queue(function (next) {
                    $(this).css(css);
                    next();
                });
            }
        });
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
            var req = {};
            if (path.indexOf("execute") !== -1) {
                $http.post('/v1.0/challenge/' + challengeId + path, $scope.requestExecute[challengeId]).then(function (response) {
                    var challOutput = response.data;
                    $scope.challengeResults[challengeId] = challOutput;
                    $anchorScroll("output_" + challengeId);
                    $("#output_" + challengeId).delay(750).qcss({ backgroundColor: '#FFFF70' }).delay(750).qcss({ backgroundColor: 'white' }).qcss({ backgroundColor: '#FFFF70' }).delay(750).qcss({ backgroundColor: 'white' }).qcss({ backgroundColor: '#FFFF70' }).delay(750).qcss({ backgroundColor: 'white' }).qcss({ backgroundColor: '#FFFF70' }).delay(750).qcss({ backgroundColor: 'white' });
                }, function (response) {
                    var error = response.data;
                    $scope.challengeResults[challengeId].message = "An error occured while processing request : " + error.message;
                    $anchorScroll("output_" + challengeId);
                    $("#output_" + challengeId).delay(750).qcss({ backgroundColor: '#FFFF70' }).delay(750).qcss({ backgroundColor: 'white' }).qcss({ backgroundColor: '#FFFF70' }).delay(750).qcss({ backgroundColor: 'white' }).qcss({ backgroundColor: '#FFFF70' }).delay(750).qcss({ backgroundColor: 'white' }).qcss({ backgroundColor: '#FFFF70' }).delay(750).qcss({ backgroundColor: 'white' });
                });
            }
            else if (path.indexOf("validate") !== -1) {
                // validate
                $http.post('/v1.0/challenge/' + challengeId + path, $scope.requestValidate[challengeId]).then(function (response) {
                    var data = response.data;
                    alert(data.message); // modal
                }, function (response) {
                    var error = response.data;
                    alert(error.message);
                });
            } else if (path.indexOf("correct") !== -1) {
                // correct
                $scope.requestCorrect[challengeId][extension].language_extension = extension;
                $http.post('/v1.0/challenge/' + challengeId + path, $scope.requestCorrect[challengeId][extension]).then(function (response) {
                    var data = response.data;
                    alert(data.message); // modal
                }, function (response) {
                    var error = response.data;
                    alert(error.message);
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

    }]);
