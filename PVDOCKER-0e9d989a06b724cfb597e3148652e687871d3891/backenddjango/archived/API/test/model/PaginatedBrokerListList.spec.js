/**
 * CRM Loan Management System API
 * A comprehensive CRM system for loan applications with fully synchronized frontend and backend development.
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 *
 */

(function(root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD.
    define(['expect.js', process.cwd()+'/src/index'], factory);
  } else if (typeof module === 'object' && module.exports) {
    // CommonJS-like environments that support module.exports, like Node.
    factory(require('expect.js'), require(process.cwd()+'/src/index'));
  } else {
    // Browser globals (root is window)
    factory(root.expect, root.CrmClientJs);
  }
}(this, function(expect, CrmClientJs) {
  'use strict';

  var instance;

  beforeEach(function() {
    instance = new CrmClientJs.PaginatedBrokerListList();
  });

  var getProperty = function(object, getter, property) {
    // Use getter method if present; otherwise, get the property directly.
    if (typeof object[getter] === 'function')
      return object[getter]();
    else
      return object[property];
  }

  var setProperty = function(object, setter, property, value) {
    // Use setter method if present; otherwise, set the property directly.
    if (typeof object[setter] === 'function')
      object[setter](value);
    else
      object[property] = value;
  }

  describe('PaginatedBrokerListList', function() {
    it('should create an instance of PaginatedBrokerListList', function() {
      // uncomment below and update the code to test PaginatedBrokerListList
      //var instance = new CrmClientJs.PaginatedBrokerListList();
      //expect(instance).to.be.a(CrmClientJs.PaginatedBrokerListList);
    });

    it('should have the property count (base name: "count")', function() {
      // uncomment below and update the code to test the property count
      //var instance = new CrmClientJs.PaginatedBrokerListList();
      //expect(instance).to.be();
    });

    it('should have the property next (base name: "next")', function() {
      // uncomment below and update the code to test the property next
      //var instance = new CrmClientJs.PaginatedBrokerListList();
      //expect(instance).to.be();
    });

    it('should have the property previous (base name: "previous")', function() {
      // uncomment below and update the code to test the property previous
      //var instance = new CrmClientJs.PaginatedBrokerListList();
      //expect(instance).to.be();
    });

    it('should have the property results (base name: "results")', function() {
      // uncomment below and update the code to test the property results
      //var instance = new CrmClientJs.PaginatedBrokerListList();
      //expect(instance).to.be();
    });

  });

}));
