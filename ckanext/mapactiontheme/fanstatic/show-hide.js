"use strict";

this.ckan.module('show-hide', function ($, _) {
  return {
    initialize: function () {
      $.proxyAll(this, /_on/);
      this.el.on('click', this._onClick);
    },

    teardown: function() {
    },

    _onClick: function(event) {
      $('.js-hide').removeClass('js-hide');

      return false;
    }
  };
});
