'use strict';

angular.module('myApp.profile', ['ngRoute', 'ngCookies'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/user/me', {
            templateUrl: 'profile/profile.html',
            controller: 'ProfileCtrl'
        });
    }])

    .controller('ProfileCtrl', ['$location', '$scope', '$http', '$cookies', function ($location, $scope, $http, $cookies) {

        /* ------ BEGIN INIT ------ */
        $scope.request = {};
        $scope.nbChallengesAvailable = 0;
        $scope.totalScoreChallenges = 0;
        $scope.nbUsers = 0;
        $scope.user = $cookies.getObject('user') || {};
        if (!$scope.user.email) {
            $scope.user = {}
        }
        if (!$scope.user || !$scope.user.isLoggedIn) {
            $.snackbar({
                content: "You must login to access this page.",
                timeout: 3000
            });
            $location.path("/user/login");
        } else {
            $http.defaults.headers.common['X-CTF-AUTH'] = $scope.user.token;
            $http.get('/v1.0/user/me').then(function (response) {
                var me = response.data;
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
                                            timeout: 3000 + error.message.length * 25
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
                                timeout: 3000 + error.message.length * 25
                            });
                        });
                    }
                }, function (response) {
                    var error = response.data;
                    $.snackbar({
                        content: "An error occured while processing request : " + error.message,
                        timeout: 3000 + error.message.length * 25
                    });
                });
                // END users scores -> rank + nbUsers

            }, function () {
                $scope.user.token = "";
                $scope.user.isLoggedIn = false;
                $scope.user.email = "anonymous";
                $cookies.putObject('user', $scope.user);
                $.snackbar({
                    content: "You must login to access this page.",
                    timeout: 3000
                });
                $location.path("/user/login");
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
                    timeout: 3000 + error.message.length * 25
                });
            });
        }
        /* ------ END INIT ------ */


        /* ------ BEGIN USER-SERVER INTERACTION ------ */
        $scope.changePassword = function () {
            if ($scope.request.password !== $scope.request.passwordConfirm) {
                $.snackbar({
                    content: "Password mismatch.",
                    timeout: 3000
                });
            } else {
                $http.put('/v1.0/user/me/changePassword', $scope.request).then(function (response) {
                    $location.path("/user/login");
                    $.snackbar({
                        content: response.data,
                        timeout: 3000 + response.data.length * 25
                    });
                }, function (response) {
                    var error = response.data;
                    $.snackbar({
                        content: "An error occured while processing request : " + error.message,
                        timeout: 3000 + error.message.length * 25
                    });
                });
            }
        };
        $scope.deleteAccount = function () {
            var ask = confirm("Are you sure?");
            if (ask) {
                $http.delete('/v1.0/user/me/unregister').then(function (response) {
                    $.snackbar({
                        content: response.data.message,
                        timeout: 3000
                    });
                    $location.path("/");
                }, function (response) {
                    var error = response.data;
                    $.snackbar({
                        content: "An error occured while processing request : " + error.message,
                        timeout: 3000 + error.message.length * 25
                    });
                });
            }
        };
        /* ------ END USER-SERVER INTERACTION ------ */
    }]);
