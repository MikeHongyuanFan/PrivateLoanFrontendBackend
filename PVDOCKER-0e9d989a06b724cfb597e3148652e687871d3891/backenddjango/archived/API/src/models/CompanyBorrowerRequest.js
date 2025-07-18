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
import AddressRequest from './AddressRequest';
import DirectorRequest from './DirectorRequest';
import FinancialInfoRequest from './FinancialInfoRequest';

/**
 * The CompanyBorrowerRequest model module.
 * @module models/CompanyBorrowerRequest
 * @version 1.0.0
 */
class CompanyBorrowerRequest {
    /**
     * Constructs a new <code>CompanyBorrowerRequest</code>.
     * @alias module:models/CompanyBorrowerRequest
     * @param registeredAddress {module:models/AddressRequest} 
     * @param directors {Array.<module:models/DirectorRequest>} 
     * @param financialInfo {module:models/FinancialInfoRequest} 
     */
    constructor(registeredAddress, directors, financialInfo) { 
        
        CompanyBorrowerRequest.initialize(this, registeredAddress, directors, financialInfo);
    }

    /**
     * Initializes the fields of this object.
     * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
     * Only for internal use.
     */
    static initialize(obj, registeredAddress, directors, financialInfo) { 
        obj['registered_address'] = registeredAddress;
        obj['directors'] = directors;
        obj['financial_info'] = financialInfo;
    }

    /**
     * Constructs a <code>CompanyBorrowerRequest</code> from a plain JavaScript object, optionally creating a new instance.
     * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @param {module:models/CompanyBorrowerRequest} obj Optional instance to populate.
     * @return {module:models/CompanyBorrowerRequest} The populated <code>CompanyBorrowerRequest</code> instance.
     */
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new CompanyBorrowerRequest();

            if (data.hasOwnProperty('company_name')) {
                obj['company_name'] = ApiClient.convertToType(data['company_name'], 'String');
            }
            if (data.hasOwnProperty('company_abn')) {
                obj['company_abn'] = ApiClient.convertToType(data['company_abn'], 'String');
            }
            if (data.hasOwnProperty('company_acn')) {
                obj['company_acn'] = ApiClient.convertToType(data['company_acn'], 'String');
            }
            if (data.hasOwnProperty('registered_address')) {
                obj['registered_address'] = AddressRequest.constructFromObject(data['registered_address']);
            }
            if (data.hasOwnProperty('directors')) {
                obj['directors'] = ApiClient.convertToType(data['directors'], [DirectorRequest]);
            }
            if (data.hasOwnProperty('financial_info')) {
                obj['financial_info'] = FinancialInfoRequest.constructFromObject(data['financial_info']);
            }
        }
        return obj;
    }

    /**
     * Validates the JSON data with respect to <code>CompanyBorrowerRequest</code>.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @return {boolean} to indicate whether the JSON data is valid with respect to <code>CompanyBorrowerRequest</code>.
     */
    static validateJSON(data) {
        // check to make sure all required properties are present in the JSON string
        for (const property of CompanyBorrowerRequest.RequiredProperties) {
            if (!data.hasOwnProperty(property)) {
                throw new Error("The required field `" + property + "` is not found in the JSON data: " + JSON.stringify(data));
            }
        }
        // ensure the json data is a string
        if (data['company_name'] && !(typeof data['company_name'] === 'string' || data['company_name'] instanceof String)) {
            throw new Error("Expected the field `company_name` to be a primitive type in the JSON string but got " + data['company_name']);
        }
        // ensure the json data is a string
        if (data['company_abn'] && !(typeof data['company_abn'] === 'string' || data['company_abn'] instanceof String)) {
            throw new Error("Expected the field `company_abn` to be a primitive type in the JSON string but got " + data['company_abn']);
        }
        // ensure the json data is a string
        if (data['company_acn'] && !(typeof data['company_acn'] === 'string' || data['company_acn'] instanceof String)) {
            throw new Error("Expected the field `company_acn` to be a primitive type in the JSON string but got " + data['company_acn']);
        }
        // validate the optional field `registered_address`
        if (data['registered_address']) { // data not null
          AddressRequest.validateJSON(data['registered_address']);
        }
        if (data['directors']) { // data not null
            // ensure the json data is an array
            if (!Array.isArray(data['directors'])) {
                throw new Error("Expected the field `directors` to be an array in the JSON data but got " + data['directors']);
            }
            // validate the optional field `directors` (array)
            for (const item of data['directors']) {
                DirectorRequest.validateJSON(item);
            };
        }
        // validate the optional field `financial_info`
        if (data['financial_info']) { // data not null
          FinancialInfoRequest.validateJSON(data['financial_info']);
        }

        return true;
    }


}

CompanyBorrowerRequest.RequiredProperties = ["registered_address", "directors", "financial_info"];

/**
 * @member {String} company_name
 */
CompanyBorrowerRequest.prototype['company_name'] = undefined;

/**
 * @member {String} company_abn
 */
CompanyBorrowerRequest.prototype['company_abn'] = undefined;

/**
 * @member {String} company_acn
 */
CompanyBorrowerRequest.prototype['company_acn'] = undefined;

/**
 * @member {module:models/AddressRequest} registered_address
 */
CompanyBorrowerRequest.prototype['registered_address'] = undefined;

/**
 * @member {Array.<module:models/DirectorRequest>} directors
 */
CompanyBorrowerRequest.prototype['directors'] = undefined;

/**
 * @member {module:models/FinancialInfoRequest} financial_info
 */
CompanyBorrowerRequest.prototype['financial_info'] = undefined;






export default CompanyBorrowerRequest;

