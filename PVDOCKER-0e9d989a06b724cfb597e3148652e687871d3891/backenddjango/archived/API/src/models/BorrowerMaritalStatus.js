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
import BlankEnum from './BlankEnum';
import MaritalStatusEnum from './MaritalStatusEnum';

/**
 * The BorrowerMaritalStatus model module.
 * @module models/BorrowerMaritalStatus
 * @version 1.0.0
 */
class BorrowerMaritalStatus {
    /**
     * Constructs a new <code>BorrowerMaritalStatus</code>.
     * @alias module:models/BorrowerMaritalStatus
     * @param {(module:models/BlankEnum|module:models/MaritalStatusEnum)} instance The actual instance to initialize BorrowerMaritalStatus.
     */
    constructor(instance = null) {
        if (instance === null) {
            this.actualInstance = null;
            return;
        }
        var match = 0;
        var errorMessages = [];
        try {
            if (typeof instance === "MaritalStatusEnum") {
                this.actualInstance = instance;
            } else {
                // plain JS object
                // validate the object
                MaritalStatusEnum.validateJSON(instance); // throw an exception if no match
                // create MaritalStatusEnum from JS object
                this.actualInstance = MaritalStatusEnum.constructFromObject(instance);
            }
            match++;
        } catch(err) {
            // json data failed to deserialize into MaritalStatusEnum
            errorMessages.push("Failed to construct MaritalStatusEnum: " + err)
        }

        try {
            if (typeof instance === "BlankEnum") {
                this.actualInstance = instance;
            } else {
                // plain JS object
                // validate the object
                BlankEnum.validateJSON(instance); // throw an exception if no match
                // create BlankEnum from JS object
                this.actualInstance = BlankEnum.constructFromObject(instance);
            }
            match++;
        } catch(err) {
            // json data failed to deserialize into BlankEnum
            errorMessages.push("Failed to construct BlankEnum: " + err)
        }

        if (match > 1) {
            throw new Error("Multiple matches found constructing `BorrowerMaritalStatus` with oneOf schemas BlankEnum, MaritalStatusEnum. Input: " + JSON.stringify(instance));
        } else if (match === 0) {
            this.actualInstance = null; // clear the actual instance in case there are multiple matches
            throw new Error("No match found constructing `BorrowerMaritalStatus` with oneOf schemas BlankEnum, MaritalStatusEnum. Details: " +
                            errorMessages.join(", "));
        } else { // only 1 match
            // the input is valid
        }
    }

    /**
     * Constructs a <code>BorrowerMaritalStatus</code> from a plain JavaScript object, optionally creating a new instance.
     * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @param {module:models/BorrowerMaritalStatus} obj Optional instance to populate.
     * @return {module:models/BorrowerMaritalStatus} The populated <code>BorrowerMaritalStatus</code> instance.
     */
    static constructFromObject(data, obj) {
        return new BorrowerMaritalStatus(data);
    }

    /**
     * Gets the actual instance, which can be <code>BlankEnum</code>, <code>MaritalStatusEnum</code>.
     * @return {(module:models/BlankEnum|module:models/MaritalStatusEnum)} The actual instance.
     */
    getActualInstance() {
        return this.actualInstance;
    }

    /**
     * Sets the actual instance, which can be <code>BlankEnum</code>, <code>MaritalStatusEnum</code>.
     * @param {(module:models/BlankEnum|module:models/MaritalStatusEnum)} obj The actual instance.
     */
    setActualInstance(obj) {
       this.actualInstance = BorrowerMaritalStatus.constructFromObject(obj).getActualInstance();
    }

    /**
     * Returns the JSON representation of the actual instance.
     * @return {string}
     */
    toJSON = function(){
        return this.getActualInstance();
    }

    /**
     * Create an instance of BorrowerMaritalStatus from a JSON string.
     * @param {string} json_string JSON string.
     * @return {module:models/BorrowerMaritalStatus} An instance of BorrowerMaritalStatus.
     */
    static fromJSON = function(json_string){
        return BorrowerMaritalStatus.constructFromObject(JSON.parse(json_string));
    }
}


BorrowerMaritalStatus.OneOf = ["BlankEnum", "MaritalStatusEnum"];

export default BorrowerMaritalStatus;

