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
import StageEnum from './StageEnum';

/**
 * The ApplicationStageUpdateRequest model module.
 * @module models/ApplicationStageUpdateRequest
 * @version 1.0.0
 */
class ApplicationStageUpdateRequest {
    /**
     * Constructs a new <code>ApplicationStageUpdateRequest</code>.
     * @alias module:models/ApplicationStageUpdateRequest
     * @param stage {module:models/StageEnum} 
     */
    constructor(stage) { 
        
        ApplicationStageUpdateRequest.initialize(this, stage);
    }

    /**
     * Initializes the fields of this object.
     * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
     * Only for internal use.
     */
    static initialize(obj, stage) { 
        obj['stage'] = stage;
    }

    /**
     * Constructs a <code>ApplicationStageUpdateRequest</code> from a plain JavaScript object, optionally creating a new instance.
     * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @param {module:models/ApplicationStageUpdateRequest} obj Optional instance to populate.
     * @return {module:models/ApplicationStageUpdateRequest} The populated <code>ApplicationStageUpdateRequest</code> instance.
     */
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new ApplicationStageUpdateRequest();

            if (data.hasOwnProperty('stage')) {
                obj['stage'] = StageEnum.constructFromObject(data['stage']);
            }
            if (data.hasOwnProperty('notes')) {
                obj['notes'] = ApiClient.convertToType(data['notes'], 'String');
            }
        }
        return obj;
    }

    /**
     * Validates the JSON data with respect to <code>ApplicationStageUpdateRequest</code>.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @return {boolean} to indicate whether the JSON data is valid with respect to <code>ApplicationStageUpdateRequest</code>.
     */
    static validateJSON(data) {
        // check to make sure all required properties are present in the JSON string
        for (const property of ApplicationStageUpdateRequest.RequiredProperties) {
            if (!data.hasOwnProperty(property)) {
                throw new Error("The required field `" + property + "` is not found in the JSON data: " + JSON.stringify(data));
            }
        }
        // ensure the json data is a string
        if (data['notes'] && !(typeof data['notes'] === 'string' || data['notes'] instanceof String)) {
            throw new Error("Expected the field `notes` to be a primitive type in the JSON string but got " + data['notes']);
        }

        return true;
    }


}

ApplicationStageUpdateRequest.RequiredProperties = ["stage"];

/**
 * @member {module:models/StageEnum} stage
 */
ApplicationStageUpdateRequest.prototype['stage'] = undefined;

/**
 * @member {String} notes
 */
ApplicationStageUpdateRequest.prototype['notes'] = undefined;






export default ApplicationStageUpdateRequest;

