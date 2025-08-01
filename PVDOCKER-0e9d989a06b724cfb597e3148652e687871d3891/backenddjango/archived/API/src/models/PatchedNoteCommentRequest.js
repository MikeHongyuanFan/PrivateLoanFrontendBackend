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
 * The PatchedNoteCommentRequest model module.
 * @module models/PatchedNoteCommentRequest
 * @version 1.0.0
 */
class PatchedNoteCommentRequest {
    /**
     * Constructs a new <code>PatchedNoteCommentRequest</code>.
     * Serializer for note comments
     * @alias module:models/PatchedNoteCommentRequest
     */
    constructor() { 
        
        PatchedNoteCommentRequest.initialize(this);
    }

    /**
     * Initializes the fields of this object.
     * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
     * Only for internal use.
     */
    static initialize(obj) { 
    }

    /**
     * Constructs a <code>PatchedNoteCommentRequest</code> from a plain JavaScript object, optionally creating a new instance.
     * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @param {module:models/PatchedNoteCommentRequest} obj Optional instance to populate.
     * @return {module:models/PatchedNoteCommentRequest} The populated <code>PatchedNoteCommentRequest</code> instance.
     */
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new PatchedNoteCommentRequest();

            if (data.hasOwnProperty('note')) {
                obj['note'] = ApiClient.convertToType(data['note'], 'Number');
            }
            if (data.hasOwnProperty('content')) {
                obj['content'] = ApiClient.convertToType(data['content'], 'String');
            }
        }
        return obj;
    }

    /**
     * Validates the JSON data with respect to <code>PatchedNoteCommentRequest</code>.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @return {boolean} to indicate whether the JSON data is valid with respect to <code>PatchedNoteCommentRequest</code>.
     */
    static validateJSON(data) {
        // ensure the json data is a string
        if (data['content'] && !(typeof data['content'] === 'string' || data['content'] instanceof String)) {
            throw new Error("Expected the field `content` to be a primitive type in the JSON string but got " + data['content']);
        }

        return true;
    }


}



/**
 * @member {Number} note
 */
PatchedNoteCommentRequest.prototype['note'] = undefined;

/**
 * @member {String} content
 */
PatchedNoteCommentRequest.prototype['content'] = undefined;






export default PatchedNoteCommentRequest;

