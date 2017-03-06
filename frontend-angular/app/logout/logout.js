'use strict';

angular.module('myApp.logout', ['ngRoute', 'ngCookies'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/user/logout', {
            templateUrl: 'logout/logout.html',
            controller: 'LogoutCtrl'
        });
    }])

    .controller('LogoutCtrl', ['$location', '$scope', '$http', '$cookies', function ($location, $scope, $http, $cookies) {
        $scope.user = $cookies.getObject('user') || {};
        if (!$scope.user.email) {
            $scope.user = {}
        }
        if (!$scope.user || !$scope.user.isLoggedIn) {
            $.snackbar({
                content: "You are already logged out",
                timeout: 3000
            });
            $location.path('/');
        } else {
            $http.defaults.headers.common['X-CTF-AUTH'] = $scope.user.token;
            $http.post('/v1.0/user/logout', null).then(function (response) {
                var data = response.data;
                $scope.response = data;
                $scope.user.isLoggedIn = false;
                $scope.user.token = "";
                $scope.user.email = "anonymous";
                $cookies.putObject('user', $scope.user);
                $.snackbar({
                    content: data.message,
                    timeout: 3000
                });
                $location.path('/');
            }, function (response) {
                var error = response.data;
                $.snackbar({
                    content: "An error occured while processing request : " + error.message,
                    timeout: 3000 + error.message.length * 25
                });
            });
        }
    }]);
