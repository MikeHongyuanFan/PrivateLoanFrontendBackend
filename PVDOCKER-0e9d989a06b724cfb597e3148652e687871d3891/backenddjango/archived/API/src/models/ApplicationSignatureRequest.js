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
 * The ApplicationSignatureRequest model module.
 * @module models/ApplicationSignatureRequest
 * @version 1.0.0
 */
class ApplicationSignatureRequest {
    /**
     * Constructs a new <code>ApplicationSignatureRequest</code>.
     * Serializer for application signature
     * @alias module:models/ApplicationSignatureRequest
     * @param signature {String} 
     * @param name {String} 
     */
    constructor(signature, name) { 
        
        ApplicationSignatureRequest.initialize(this, signature, name);
    }

    /**
     * Initializes the fields of this object.
     * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
     * Only for internal use.
     */
    static initialize(obj, signature, name) { 
        obj['signature'] = signature;
        obj['name'] = name;
    }

    /**
     * Constructs a <code>ApplicationSignatureRequest</code> from a plain JavaScript object, optionally creating a new instance.
     * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @param {module:models/ApplicationSignatureRequest} obj Optional instance to populate.
     * @return {module:models/ApplicationSignatureRequest} The populated <code>ApplicationSignatureRequest</code> instance.
     */
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new ApplicationSignatureRequest();

            if (data.hasOwnProperty('signature')) {
                obj['signature'] = ApiClient.convertToType(data['signature'], 'String');
            }
            if (data.hasOwnProperty('name')) {
                obj['name'] = ApiClient.convertToType(data['name'], 'String');
            }
            if (data.hasOwnProperty('signature_date')) {
                obj['signature_date'] = ApiClient.convertToType(data['signature_date'], 'Date');
            }
            if (data.hasOwnProperty('notes')) {
                obj['notes'] = ApiClient.convertToType(data['notes'], 'String');
            }
        }
        return obj;
    }

    /**
     * Validates the JSON data with respect to <code>ApplicationSignatureRequest</code>.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @return {boolean} to indicate whether the JSON data is valid with respect to <code>ApplicationSignatureRequest</code>.
     */
    static validateJSON(data) {
        // check to make sure all required properties are present in the JSON string
        for (const property of ApplicationSignatureRequest.RequiredProperties) {
            if (!data.hasOwnProperty(property)) {
                throw new Error("The required field `" + property + "` is not found in the JSON data: " + JSON.stringify(data));
            }
        }
        // ensure the json data is a string
        if (data['signature'] && !(typeof data['signature'] === 'string' || data['signature'] instanceof String)) {
            throw new Error("Expected the field `signature` to be a primitive type in the JSON string but got " + data['signature']);
        }
        // ensure the json data is a string
        if (data['name'] && !(typeof data['name'] === 'string' || data['name'] instanceof String)) {
            throw new Error("Expected the field `name` to be a primitive type in the JSON string but got " + data['name']);
        }
        // ensure the json data is a string
        if (data['notes'] && !(typeof data['notes'] === 'string' || data['notes'] instanceof String)) {
            throw new Error("Expected the field `notes` to be a primitive type in the JSON string but got " + data['notes']);
        }

        return true;
    }


}

ApplicationSignatureRequest.RequiredProperties = ["signature", "name"];

/**
 * @member {String} signature
 */
ApplicationSignatureRequest.prototype['signature'] = undefined;

/**
 * @member {String} name
 */
ApplicationSignatureRequest.prototype['name'] = undefined;

/**
 * @member {Date} signature_date
 */
ApplicationSignatureRequest.prototype['signature_date'] = undefined;

/**
 * @member {String} notes
 */
ApplicationSignatureRequest.prototype['notes'] = undefined;






export default ApplicationSignatureRequest;

