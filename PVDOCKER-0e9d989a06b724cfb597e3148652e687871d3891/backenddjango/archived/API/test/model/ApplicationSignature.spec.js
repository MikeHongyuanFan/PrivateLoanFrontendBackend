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
    instance = new CrmClientJs.ApplicationSignature();
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

  describe('ApplicationSignature', function() {
    it('should create an instance of ApplicationSignature', function() {
      // uncomment below and update the code to test ApplicationSignature
      //var instance = new CrmClientJs.ApplicationSignature();
      //expect(instance).to.be.a(CrmClientJs.ApplicationSignature);
    });

    it('should have the property signature (base name: "signature")', function() {
      // uncomment below and update the code to test the property signature
      //var instance = new CrmClientJs.ApplicationSignature();
      //expect(instance).to.be();
    });

    it('should have the property name (base name: "name")', function() {
      // uncomment below and update the code to test the property name
      //var instance = new CrmClientJs.ApplicationSignature();
      //expect(instance).to.be();
    });

    it('should have the property signatureDate (base name: "signature_date")', function() {
      // uncomment below and update the code to test the property signatureDate
      //var instance = new CrmClientJs.ApplicationSignature();
      //expect(instance).to.be();
    });

    it('should have the property notes (base name: "notes")', function() {
      // uncomment below and update the code to test the property notes
      //var instance = new CrmClientJs.ApplicationSignature();
      //expect(instance).to.be();
    });

  });

}));
