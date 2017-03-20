'use strict';

angular.module('myApp.profile', ['ngRoute', 'ngCookies'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/user/me', {
            templateUrl: 'profile/profile.html',
            controller: 'MyProfileCtrl'
        });
        $routeProvider.when('/user/:userId', {
            templateUrl: 'profile/profile.html',
            controller: 'UserProfileCtrl'
        });
    }])

    .controller('MyProfileCtrl', ['$location', '$scope', '$http', '$cookies', function ($location, $scope, $http, $cookies) {

        /* ------ BEGIN INIT ------ */

        $scope.request = {};
        $scope.nbChallengesAvailable = 0;
        $scope.totalScoreChallenges = 0;
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
                $scope.currentUser = true;
                $scope.user.ID = me.ID;
                $scope.user.score = 0;
                $scope.user.validatedChallenges = [];
                $http.get('/v1.0/user/' + me.ID + '/validatedChallenges').then(function (response) {
                    var validatedChallenges = response.data;
                    $scope.user.validatedChallenges = validatedChallenges;
                    for (var challIt = 0; challIt < validatedChallenges.length; ++challIt) {
                        $scope.user.score += validatedChallenges[challIt].points;
                    }
                }, function (response) {
                    var error = response.data;
                    $.snackbar({
                        content: "An error occured while processing request : " + error.message,
                        timeout: 3000 + error.message.length * 25
                    });
                });
            }, function (response) {
                var error = response.data;
                $.snackbar({
                    content: "An error occured while processing request : " + error.message,
                    timeout: 3000 + error.message.length * 25
                });
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
    }])
    
    .controller('UserProfileCtrl', ['$routeParams', '$location', '$scope', '$http', '$cookies', function ($routeParams, $location, $scope, $http, $cookies) {
        
	$scope.request = {};
        $scope.nbChallengesAvailable = 0;
        $scope.totalScoreChallenges = 0;
	$scope.user = {};
	$http.get('/v1.0/user/' + $routeParams.userId).then(function (response) {
            var user = response.data;
            $scope.currentUser = false;
            $scope.user = user;
            $scope.user.score = 0;
            $scope.user.validatedChallenges = [];
            $http.get('/v1.0/user/' + user.ID + '/validatedChallenges').then(function (response) {
                var validatedChallenges = response.data;
                $scope.user.validatedChallenges = validatedChallenges;
                for (var challIt = 0; challIt < validatedChallenges.length; ++challIt) {
                    $scope.user.score += validatedChallenges[challIt].points;
                }
            }, function (response) {
                var error = response.data;
                $.snackbar({
                    content: "An error occured while processing request : " + error.message,
                    timeout: 3000 + error.message.length * 25
                });
            });
        }, function (response) {
            var error = response.data;
            $.snackbar({
                content: "An error occured while processing request : " + error.message,
                timeout: 3000 + error.message.length * 25
            });
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
    }]);
