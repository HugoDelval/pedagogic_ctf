'use strict';

angular.module('myApp.register', ['ngRoute', 'ngCookies'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/user/register', {
            templateUrl: 'register/register.html',
            controller: 'RegisterCtrl'
        });
    }])

    .controller('RegisterCtrl', ['$location', '$scope', '$http', '$cookies', function ($location, $scope, $http, $cookies) {

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
            $location.path("/user/me");
        }
        /* ------ END INIT ------ */


        /* ------ BEGIN SERVER INTERACTION ------ */
        $scope.register = function () {
            if ($scope.request.password !== $scope.request.passwordConfirm) {
                $.snackbar({
                    content: "Password mismatch.",
                    timeout: 3000
                });
            } else {
                $http.post('/v1.0/user/register', $scope.request).then(function (response) {
                    var data = response.data;
                    $scope.response = data;
                    $location.path("/user/me");
                }, function (response) {
                    var error = response.data;
                    $.snackbar({
                        content: "An error occured while processing request : " + error.message,
                        timeout: 3000
                    });
                });
            }
        };

        /* ------ END SERVER INTERACTION ------ */
    }]);
