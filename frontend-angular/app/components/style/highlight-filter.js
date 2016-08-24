'use strict';

angular.module('myApp.style.highlight-filter', [])

.filter('highlight', function($sce) {
  return function(input, lang) {
    if (lang && input) return hljs.highlight(lang, input).value;
    return input;
  }
}).filter('unsafe', function($sce) { return $sce.trustAsHtml; })
