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
import BorrowerMaritalStatus from './BorrowerMaritalStatus';
import BorrowerResidencyStatus from './BorrowerResidencyStatus';

/**
 * The Borrower model module.
 * @module models/Borrower
 * @version 1.0.0
 */
class Borrower {
    /**
     * Constructs a new <code>Borrower</code>.
     * @alias module:models/Borrower
     * @param id {Number} 
     * @param address {Object.<String, Object>} 
     * @param employmentInfo {Object.<String, Object>} 
     */
    constructor(id, address, employmentInfo) { 
        
        Borrower.initialize(this, id, address, employmentInfo);
    }

    /**
     * Initializes the fields of this object.
     * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
     * Only for internal use.
     */
    static initialize(obj, id, address, employmentInfo) { 
        obj['id'] = id;
        obj['address'] = address;
        obj['employment_info'] = employmentInfo;
    }

    /**
     * Constructs a <code>Borrower</code> from a plain JavaScript object, optionally creating a new instance.
     * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @param {module:models/Borrower} obj Optional instance to populate.
     * @return {module:models/Borrower} The populated <code>Borrower</code> instance.
     */
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new Borrower();

            if (data.hasOwnProperty('id')) {
                obj['id'] = ApiClient.convertToType(data['id'], 'Number');
            }
            if (data.hasOwnProperty('first_name')) {
                obj['first_name'] = ApiClient.convertToType(data['first_name'], 'String');
            }
            if (data.hasOwnProperty('last_name')) {
                obj['last_name'] = ApiClient.convertToType(data['last_name'], 'String');
            }
            if (data.hasOwnProperty('email')) {
                obj['email'] = ApiClient.convertToType(data['email'], 'String');
            }
            if (data.hasOwnProperty('phone')) {
                obj['phone'] = ApiClient.convertToType(data['phone'], 'String');
            }
            if (data.hasOwnProperty('date_of_birth')) {
                obj['date_of_birth'] = ApiClient.convertToType(data['date_of_birth'], 'Date');
            }
            if (data.hasOwnProperty('address')) {
                obj['address'] = ApiClient.convertToType(data['address'], {'String': Object});
            }
            if (data.hasOwnProperty('employment_info')) {
                obj['employment_info'] = ApiClient.convertToType(data['employment_info'], {'String': Object});
            }
            if (data.hasOwnProperty('tax_id')) {
                obj['tax_id'] = ApiClient.convertToType(data['tax_id'], 'String');
            }
            if (data.hasOwnProperty('marital_status')) {
                obj['marital_status'] = BorrowerMaritalStatus.constructFromObject(data['marital_status']);
            }
            if (data.hasOwnProperty('residency_status')) {
                obj['residency_status'] = BorrowerResidencyStatus.constructFromObject(data['residency_status']);
            }
            if (data.hasOwnProperty('referral_source')) {
                obj['referral_source'] = ApiClient.convertToType(data['referral_source'], 'String');
            }
            if (data.hasOwnProperty('tags')) {
                obj['tags'] = ApiClient.convertToType(data['tags'], 'String');
            }
        }
        return obj;
    }

    /**
     * Validates the JSON data with respect to <code>Borrower</code>.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @return {boolean} to indicate whether the JSON data is valid with respect to <code>Borrower</code>.
     */
    static validateJSON(data) {
        // check to make sure all required properties are present in the JSON string
        for (const property of Borrower.RequiredProperties) {
            if (!data.hasOwnProperty(property)) {
                throw new Error("The required field `" + property + "` is not found in the JSON data: " + JSON.stringify(data));
            }
        }
        // ensure the json data is a string
        if (data['first_name'] && !(typeof data['first_name'] === 'string' || data['first_name'] instanceof String)) {
            throw new Error("Expected the field `first_name` to be a primitive type in the JSON string but got " + data['first_name']);
        }
        // ensure the json data is a string
        if (data['last_name'] && !(typeof data['last_name'] === 'string' || data['last_name'] instanceof String)) {
            throw new Error("Expected the field `last_name` to be a primitive type in the JSON string but got " + data['last_name']);
        }
        // ensure the json data is a string
        if (data['email'] && !(typeof data['email'] === 'string' || data['email'] instanceof String)) {
            throw new Error("Expected the field `email` to be a primitive type in the JSON string but got " + data['email']);
        }
        // ensure the json data is a string
        if (data['phone'] && !(typeof data['phone'] === 'string' || data['phone'] instanceof String)) {
            throw new Error("Expected the field `phone` to be a primitive type in the JSON string but got " + data['phone']);
        }
        // ensure the json data is a string
        if (data['tax_id'] && !(typeof data['tax_id'] === 'string' || data['tax_id'] instanceof String)) {
            throw new Error("Expected the field `tax_id` to be a primitive type in the JSON string but got " + data['tax_id']);
        }
        // validate the optional field `marital_status`
        if (data['marital_status']) { // data not null
          BorrowerMaritalStatus.validateJSON(data['marital_status']);
        }
        // validate the optional field `residency_status`
        if (data['residency_status']) { // data not null
          BorrowerResidencyStatus.validateJSON(data['residency_status']);
        }
        // ensure the json data is a string
        if (data['referral_source'] && !(typeof data['referral_source'] === 'string' || data['referral_source'] instanceof String)) {
            throw new Error("Expected the field `referral_source` to be a primitive type in the JSON string but got " + data['referral_source']);
        }
        // ensure the json data is a string
        if (data['tags'] && !(typeof data['tags'] === 'string' || data['tags'] instanceof String)) {
            throw new Error("Expected the field `tags` to be a primitive type in the JSON string but got " + data['tags']);
        }

        return true;
    }


}

Borrower.RequiredProperties = ["id", "address", "employment_info"];

/**
 * @member {Number} id
 */
Borrower.prototype['id'] = undefined;

/**
 * @member {String} first_name
 */
Borrower.prototype['first_name'] = undefined;

/**
 * @member {String} last_name
 */
Borrower.prototype['last_name'] = undefined;

/**
 * @member {String} email
 */
Borrower.prototype['email'] = undefined;

/**
 * @member {String} phone
 */
Borrower.prototype['phone'] = undefined;

/**
 * @member {Date} date_of_birth
 */
Borrower.prototype['date_of_birth'] = undefined;

/**
 * @member {Object.<String, Object>} address
 */
Borrower.prototype['address'] = undefined;

/**
 * @member {Object.<String, Object>} employment_info
 */
Borrower.prototype['employment_info'] = undefined;

/**
 * Tax File Number or equivalent
 * @member {String} tax_id
 */
Borrower.prototype['tax_id'] = undefined;

/**
 * @member {module:models/BorrowerMaritalStatus} marital_status
 */
Borrower.prototype['marital_status'] = undefined;

/**
 * @member {module:models/BorrowerResidencyStatus} residency_status
 */
Borrower.prototype['residency_status'] = undefined;

/**
 * @member {String} referral_source
 */
Borrower.prototype['referral_source'] = undefined;

/**
 * @member {String} tags
 */
Borrower.prototype['tags'] = undefined;






export default Borrower;

