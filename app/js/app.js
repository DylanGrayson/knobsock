'use strict';

var KnobSock = angular.module('KnobSock', ['ngRoute']);

// KnobSock.run(function($rootScope, $location, $http) {
//     $rootScope.$on("$routeChangeStart", function(event, next, current) {
//         $http.get('/api/user/me').then(function(results) {
//             if (results.user != null) {
//                 $rootScope.authenticated = true;
//                 $rootScope.user = results;
//             } 
//             else {
//               $rootScope.user = null;
//               var nextUrl = next.$$route.originalPath;
//               if (nextUrl == '/api/user/signup' || nextUrl == '/api/user/login') {
//                 window.location = nextUrl;
//               } else {
//                 window.location = "/api/user/login";
//               }
//             }
//         });
//     });
// });

KnobSock.factory('guestService', function($rootScope, $http, $q, $log) {
  $rootScope.status = 'Retrieving data...';
  var deferred = $q.defer();
  $http.get('rest/query')
  .success(function(data, status, headers, config) {
    $rootScope.guests = data;
    deferred.resolve();
    $rootScope.status = '';
  });
  return deferred.promise;
});

KnobSock.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        templateUrl: 'partials/splash.html',
        controller: 'SplashCtrl'
      }).
      when('/dashboard/:phoneId', {
        templateUrl: 'partials/dashboard.html',
        controller: 'DashCtrl'
      }).
      otherwise({
        redirectTo: '/'
      });
  }]);

KnobSock.controller('SplashCtrl', function($scope, $rootScope, $log, $http, $routeParams, $location, $route) {

});

KnobSock.controller('DashCtrl', function($scope, $rootScope, $log, $http, $routeParams, $location, $route) {

  $scope.submitInsert = function() {
    var guest = {
      first: $scope.first,
      last: $scope.last, 
    };
    $rootScope.status = 'Creating...';
    $http.post('/rest/insert', guest)
    .success(function(data, status, headers, config) {
      $rootScope.guests.push(data);
      $rootScope.status = '';
    });
    $location.path('/');
  }
});

