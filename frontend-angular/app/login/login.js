'use strict';

angular.module('myApp.login', ['ngRoute', 'ngCookies'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/user/login', {
            templateUrl: 'login/login.html',
            controller: 'LoginCtrl'
        });
    }])

    .controller('LoginCtrl', ['$location', '$scope', '$http', '$cookies', function ($location, $scope, $http, $cookies) {

        /* ------ BEGIN INIT ------ */
        $scope.request = {};
        $scope.user = $cookies.getObject('user') || {};
        if (!$scope.user.email) {
            $scope.user = {}
        }
        if ($scope.user && $scope.user.isLoggedIn) {
            $.snackbar({
                content: "You are already logged in.",
                timeout: 3000
            });
            $location.path('/user/me');
        }
        /* ------ END INIT ------ */


        /* ------ BEGIN SERVER INTERACTION ------ */
        $scope.login = function () {
            $http.post('/v1.0/user/login', $scope.request).then(function (response) {
                var data = response.data;
                $scope.user.token = data;
                $scope.user.isLoggedIn = true;
                $scope.user.email = $scope.request.email;
                $cookies.putObject('user', $scope.user);
                $location.path('/user/me');
            }, function (response) {
                var error = response.data;
                $.snackbar({
                    content: error.message,
                    timeout: 3000
                });
            });
        };

        /* ------ END SERVER INTERACTION ------ */
    }]);
