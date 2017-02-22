'use strict';

angular.module('myApp.userProfile', ['ngRoute', 'ngCookies'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/user/:userId', {
            templateUrl: 'user_profile/user_profile.html',
            controller: 'UserProfileCtrl'
        });
    }])

    .controller('UserProfileCtrl', ['$routeParams', '$location', '$scope', '$http', '$cookies', function ($routeParams, $location, $scope, $http, $cookies) {

        /* ------ BEGIN INIT ------ */
        $scope.request = {};
        $scope.nbChallengesAvailable = 0;
        $scope.totalScoreChallenges = 0;
        $scope.nbUsers = 0;
        $scope.user = {};
        $http.get('/v1.0/user/' + $routeParams.userId).then(function (response) {
            var me = response.data;
            $scope.user = me;
            $scope.user.score = 0;
            $scope.user.rank = 0;
            $scope.user.validatedChallenges = [];
            // users scores -> rank + nbUsers
            $http.get('/v1.0/user').then(function (response) {
                var users = response.data;
                $scope.nbUsers = users.length;
                var scores = new Array($scope.nbUsers);
                var nbUsersDone = 0.00001; // float precision.. We never know.
                var calculateRank = function (increment) {
                    nbUsersDone += increment;
                    if ($scope.nbUsers <= nbUsersDone) {
                        scores.sort().reverse();
                        $scope.user.rank = scores.indexOf($scope.user.score) + 1;
                    }
                };
                for (var userIt = 0; userIt < $scope.nbUsers; ++userIt) {
                    scores[userIt] = 0;
                    $http.get('/v1.0/user/' + users[userIt].ID + '/validatedChallenges').then((function (userIterator) {
                        return function (response) {
                            var validatedChalls = response.data;
                            for (var challIt = 0; challIt < validatedChalls.length; ++challIt) {
                                $http.get('/v1.0/challenge/' + validatedChalls[challIt].ChallengeID).then((function (userIter, currId, validatedChallLink) {
                                    return function (response) {
                                        var validatedChall = response.data;
                                        scores[userIter] += validatedChall.points;
                                        if (me.ID == currId) {
                                            // user score + validated challenges
                                            validatedChall.date_validated = validatedChallLink.date_validated;
                                            $scope.user.validatedChallenges.push(validatedChall);
                                            $scope.user.score += validatedChall.points;
                                        }
                                        calculateRank(1.0 / validatedChalls.length);
                                    }
                                })(userIterator, users[userIterator].ID, validatedChalls[challIt]), function (response) {
                                    var error = response.data;
                                    $.snackbar({
                                        content: "An error occured while processing request : " + error.message,
                                        timeout: 3000
                                    });
                                });
                            }
                            if (validatedChalls.length == 0) {
                                calculateRank(1);
                            }
                        }
                    })(userIt), function (response) {
                        var error = response.data;
                        $.snackbar({
                            content: "An error occured while processing request : " + error.message,
                            timeout: 3000
                        });
                    });
                }
            }, function (response) {
                var error = response.data;
                $.snackbar({
                    content: "An error occured while processing request : " + error.message,
                    timeout: 3000
                });
            });
            // END users scores -> rank + nbUsers

        }, function (response) {
            var error = response.data;
            $.snackbar({
                content: "User does not exists : " + error.message,
                timeout: 3000
            });
            $location.path("/user");
        });
        $http.get('/v1.0/challenge').then(function (response) {
            var challenges = response.data;
            $scope.nbChallengesAvailable = challenges.length;
            for (var challIt = 0; challIt < challenges.length; ++challIt) {
                $scope.totalScoreChallenges += challenges[challIt].points;
            }
        }, function (response) {
            var error = response.data;
            $.snackbar({
                content: "An error occured while processing request : " + error.message,
                timeout: 3000
            });
        });
        /* ------ END INIT ------ */

    }]);
