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
        $http.get('/v1.0/scoreboard').then(function (response) {
            var users = response.data;
            $scope.users = users;
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
