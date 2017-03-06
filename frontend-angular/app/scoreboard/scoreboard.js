'use strict';

angular.module('myApp.scoreboard', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/user', {
            templateUrl: 'scoreboard/scoreboard.html',
            controller: 'ScoreboardCtrl'
        });
    }])

    .controller('ScoreboardCtrl', ['$location', '$scope', '$http', function ($location, $scope, $http) {

        /* ------ BEGIN INIT ------ */
        $scope.request = {};
        $http.get('/v1.0/user').then(function (response) {
            var users = response.data;
            $scope.users = users;
            for (var userIt = 0; userIt < users.length; ++userIt) {
                $scope.users[userIt].score = 0;
                var currId = $scope.users[userIt].ID;
                $http.get('/v1.0/user/' + currId + '/validatedChallenges').then((function (userIterator) {
                    return function (response) {
                        var validatedChalls = response.data;
                        $scope.users[userIterator].nb_validated = validatedChalls.length;
                        for (var challIt = 0; challIt < validatedChalls.length; ++challIt) {
                            $http.get('/v1.0/challenge/' + validatedChalls[challIt].ChallengeID).then((function (userIter) {
                                return function (response) {
                                    var validatedChall = response.data;
                                    $scope.users[userIter].score += validatedChall.points;
                                }
                            })(userIterator), function (response) {
                                var error = response.data;
                                $.snackbar({
                                    content: "An error occured while processing request : " + error.message,
                                    timeout: 3000
                                });
                            });
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
        /* ------ END INIT ------ */


        /* ------ BEGIN SERVER INTERACTION ------ */
        $scope.go = function (path) {
            $location.path(path);
        };
        /* ------ END SERVER INTERACTION ------ */
    }]);
