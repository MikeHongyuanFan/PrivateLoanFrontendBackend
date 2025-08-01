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

import ApiClient from '../ApiClient';

/**
 * The BranchRequest model module.
 * @module models/BranchRequest
 * @version 1.0.0
 */
class BranchRequest {
    /**
     * Constructs a new <code>BranchRequest</code>.
     * Serializer for branch information
     * @alias module:models/BranchRequest
     * @param name {String} 
     */
    constructor(name) { 
        
        BranchRequest.initialize(this, name);
    }

    /**
     * Initializes the fields of this object.
     * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
     * Only for internal use.
     */
    static initialize(obj, name) { 
        obj['name'] = name;
    }

    /**
     * Constructs a <code>BranchRequest</code> from a plain JavaScript object, optionally creating a new instance.
     * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @param {module:models/BranchRequest} obj Optional instance to populate.
     * @return {module:models/BranchRequest} The populated <code>BranchRequest</code> instance.
     */
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new BranchRequest();

            if (data.hasOwnProperty('name')) {
                obj['name'] = ApiClient.convertToType(data['name'], 'String');
            }
            if (data.hasOwnProperty('address')) {
                obj['address'] = ApiClient.convertToType(data['address'], 'String');
            }
            if (data.hasOwnProperty('phone')) {
                obj['phone'] = ApiClient.convertToType(data['phone'], 'String');
            }
            if (data.hasOwnProperty('email')) {
                obj['email'] = ApiClient.convertToType(data['email'], 'String');
            }
        }
        return obj;
    }

    /**
     * Validates the JSON data with respect to <code>BranchRequest</code>.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @return {boolean} to indicate whether the JSON data is valid with respect to <code>BranchRequest</code>.
     */
    static validateJSON(data) {
        // check to make sure all required properties are present in the JSON string
        for (const property of BranchRequest.RequiredProperties) {
            if (!data.hasOwnProperty(property)) {
                throw new Error("The required field `" + property + "` is not found in the JSON data: " + JSON.stringify(data));
            }
        }
        // ensure the json data is a string
        if (data['name'] && !(typeof data['name'] === 'string' || data['name'] instanceof String)) {
            throw new Error("Expected the field `name` to be a primitive type in the JSON string but got " + data['name']);
        }
        // ensure the json data is a string
        if (data['address'] && !(typeof data['address'] === 'string' || data['address'] instanceof String)) {
            throw new Error("Expected the field `address` to be a primitive type in the JSON string but got " + data['address']);
        }
        // ensure the json data is a string
        if (data['phone'] && !(typeof data['phone'] === 'string' || data['phone'] instanceof String)) {
            throw new Error("Expected the field `phone` to be a primitive type in the JSON string but got " + data['phone']);
        }
        // ensure the json data is a string
        if (data['email'] && !(typeof data['email'] === 'string' || data['email'] instanceof String)) {
            throw new Error("Expected the field `email` to be a primitive type in the JSON string but got " + data['email']);
        }

        return true;
    }


}

BranchRequest.RequiredProperties = ["name"];

/**
 * @member {String} name
 */
BranchRequest.prototype['name'] = undefined;

/**
 * @member {String} address
 */
BranchRequest.prototype['address'] = undefined;

/**
 * @member {String} phone
 */
BranchRequest.prototype['phone'] = undefined;

/**
 * @member {String} email
 */
BranchRequest.prototype['email'] = undefined;






export default BranchRequest;

