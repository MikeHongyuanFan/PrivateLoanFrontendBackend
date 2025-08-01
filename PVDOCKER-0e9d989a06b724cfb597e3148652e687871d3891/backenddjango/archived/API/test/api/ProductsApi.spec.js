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
    instance = new CrmClientJs.ProductsApi();
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

  describe('ProductsApi', function() {
    describe('productsProductsCreate', function() {
      it('should call productsProductsCreate successfully', function(done) {
        //uncomment below and update the code to test productsProductsCreate
        //instance.productsProductsCreate(function(error) {
        //  if (error) throw error;
        //expect().to.be();
        //});
        done();
      });
    });
    describe('productsProductsDestroy', function() {
      it('should call productsProductsDestroy successfully', function(done) {
        //uncomment below and update the code to test productsProductsDestroy
        //instance.productsProductsDestroy(function(error) {
        //  if (error) throw error;
        //expect().to.be();
        //});
        done();
      });
    });
    describe('productsProductsList', function() {
      it('should call productsProductsList successfully', function(done) {
        //uncomment below and update the code to test productsProductsList
        //instance.productsProductsList(function(error) {
        //  if (error) throw error;
        //expect().to.be();
        //});
        done();
      });
    });
    describe('productsProductsPartialUpdate', function() {
      it('should call productsProductsPartialUpdate successfully', function(done) {
        //uncomment below and update the code to test productsProductsPartialUpdate
        //instance.productsProductsPartialUpdate(function(error) {
        //  if (error) throw error;
        //expect().to.be();
        //});
        done();
      });
    });
    describe('productsProductsRetrieve', function() {
      it('should call productsProductsRetrieve successfully', function(done) {
        //uncomment below and update the code to test productsProductsRetrieve
        //instance.productsProductsRetrieve(function(error) {
        //  if (error) throw error;
        //expect().to.be();
        //});
        done();
      });
    });
    describe('productsProductsUpdate', function() {
      it('should call productsProductsUpdate successfully', function(done) {
        //uncomment below and update the code to test productsProductsUpdate
        //instance.productsProductsUpdate(function(error) {
        //  if (error) throw error;
        //expect().to.be();
        //});
        done();
      });
    });
  });

}));
