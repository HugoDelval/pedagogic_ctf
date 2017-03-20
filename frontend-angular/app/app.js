'use strict';

// Declare app level module which depends on views, and components
angular.module('myApp', [
    'ngRoute',
    'myApp.index',
    'myApp.style',
    'myApp.scoreboard',
    'myApp.register',
    'myApp.login',
    'myApp.logout',
    'myApp.profile',
]).config(['$locationProvider', '$routeProvider', function ($locationProvider, $routeProvider) {
    $locationProvider.hashPrefix('!');

    $routeProvider.otherwise({redirectTo: '/'});
}])

    .factory('UserService', function () {
        return {
            isLoggedIn: false,
            email: "anonymous",
            token: ""
        };
    });
