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
* Enum class MaritalStatusEnum.
* @enum {}
* @readonly
*/
export default class MaritalStatusEnum {
    
        /**
         * value: "single"
         * @const
         */
        "single" = "single";

    
        /**
         * value: "married"
         * @const
         */
        "married" = "married";

    
        /**
         * value: "de_facto"
         * @const
         */
        "de_facto" = "de_facto";

    
        /**
         * value: "divorced"
         * @const
         */
        "divorced" = "divorced";

    
        /**
         * value: "widowed"
         * @const
         */
        "widowed" = "widowed";

    

    /**
    * Returns a <code>MaritalStatusEnum</code> enum value from a Javascript object name.
    * @param {Object} data The plain JavaScript object containing the name of the enum value.
    * @return {module:models/MaritalStatusEnum} The enum <code>MaritalStatusEnum</code> value.
    */
    static constructFromObject(object) {
        return object;
    }
}

