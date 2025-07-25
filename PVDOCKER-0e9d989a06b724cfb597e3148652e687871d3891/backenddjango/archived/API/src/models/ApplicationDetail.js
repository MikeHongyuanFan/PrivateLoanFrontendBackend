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
import ApplicationCreateApplicationType from './ApplicationCreateApplicationType';
import BDM from './BDM';
import Borrower from './Borrower';
import Branch from './Branch';
import BrokerDetail from './BrokerDetail';
import Guarantor from './Guarantor';
import RepaymentFrequencyEnum from './RepaymentFrequencyEnum';
import StageEnum from './StageEnum';
import User from './User';

/**
 * The ApplicationDetail model module.
 * @module models/ApplicationDetail
 * @version 1.0.0
 */
class ApplicationDetail {
    /**
     * Constructs a new <code>ApplicationDetail</code>.
     * @alias module:models/ApplicationDetail
     * @param id {Number} 
     * @param stageDisplay {String} 
     * @param createdAt {Date} 
     * @param updatedAt {Date} 
     * @param borrowers {Array.<module:models/Borrower>} 
     * @param guarantors {Array.<module:models/Guarantor>} 
     * @param broker {module:models/BrokerDetail} 
     * @param bd {module:models/BDM} 
     * @param branch {module:models/Branch} 
     * @param documents {Array.<Object>} 
     * @param notes {Array.<Object>} 
     * @param fees {Array.<Object>} 
     * @param repayments {Array.<Object>} 
     * @param ledgerEntries {Array.<Object>} 
     * @param createdByDetails {module:models/User} 
     */
    constructor(id, stageDisplay, createdAt, updatedAt, borrowers, guarantors, broker, bd, branch, documents, notes, fees, repayments, ledgerEntries, createdByDetails) { 
        
        ApplicationDetail.initialize(this, id, stageDisplay, createdAt, updatedAt, borrowers, guarantors, broker, bd, branch, documents, notes, fees, repayments, ledgerEntries, createdByDetails);
    }

    /**
     * Initializes the fields of this object.
     * This method is used by the constructors of any subclasses, in order to implement multiple inheritance (mix-ins).
     * Only for internal use.
     */
    static initialize(obj, id, stageDisplay, createdAt, updatedAt, borrowers, guarantors, broker, bd, branch, documents, notes, fees, repayments, ledgerEntries, createdByDetails) { 
        obj['id'] = id;
        obj['stage_display'] = stageDisplay;
        obj['created_at'] = createdAt;
        obj['updated_at'] = updatedAt;
        obj['borrowers'] = borrowers;
        obj['guarantors'] = guarantors;
        obj['broker'] = broker;
        obj['bd'] = bd;
        obj['branch'] = branch;
        obj['documents'] = documents;
        obj['notes'] = notes;
        obj['fees'] = fees;
        obj['repayments'] = repayments;
        obj['ledger_entries'] = ledgerEntries;
        obj['created_by_details'] = createdByDetails;
    }

    /**
     * Constructs a <code>ApplicationDetail</code> from a plain JavaScript object, optionally creating a new instance.
     * Copies all relevant properties from <code>data</code> to <code>obj</code> if supplied or a new instance if not.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @param {module:models/ApplicationDetail} obj Optional instance to populate.
     * @return {module:models/ApplicationDetail} The populated <code>ApplicationDetail</code> instance.
     */
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new ApplicationDetail();

            if (data.hasOwnProperty('id')) {
                obj['id'] = ApiClient.convertToType(data['id'], 'Number');
            }
            if (data.hasOwnProperty('reference_number')) {
                obj['reference_number'] = ApiClient.convertToType(data['reference_number'], 'String');
            }
            if (data.hasOwnProperty('loan_amount')) {
                obj['loan_amount'] = ApiClient.convertToType(data['loan_amount'], 'Number');
            }
            if (data.hasOwnProperty('loan_term')) {
                obj['loan_term'] = ApiClient.convertToType(data['loan_term'], 'Number');
            }
            if (data.hasOwnProperty('interest_rate')) {
                obj['interest_rate'] = ApiClient.convertToType(data['interest_rate'], 'Number');
            }
            if (data.hasOwnProperty('purpose')) {
                obj['purpose'] = ApiClient.convertToType(data['purpose'], 'String');
            }
            if (data.hasOwnProperty('repayment_frequency')) {
                obj['repayment_frequency'] = RepaymentFrequencyEnum.constructFromObject(data['repayment_frequency']);
            }
            if (data.hasOwnProperty('application_type')) {
                obj['application_type'] = ApplicationCreateApplicationType.constructFromObject(data['application_type']);
            }
            if (data.hasOwnProperty('product_id')) {
                obj['product_id'] = ApiClient.convertToType(data['product_id'], 'String');
            }
            if (data.hasOwnProperty('estimated_settlement_date')) {
                obj['estimated_settlement_date'] = ApiClient.convertToType(data['estimated_settlement_date'], 'Date');
            }
            if (data.hasOwnProperty('stage')) {
                obj['stage'] = StageEnum.constructFromObject(data['stage']);
            }
            if (data.hasOwnProperty('stage_display')) {
                obj['stage_display'] = ApiClient.convertToType(data['stage_display'], 'String');
            }
            if (data.hasOwnProperty('created_at')) {
                obj['created_at'] = ApiClient.convertToType(data['created_at'], 'Date');
            }
            if (data.hasOwnProperty('updated_at')) {
                obj['updated_at'] = ApiClient.convertToType(data['updated_at'], 'Date');
            }
            if (data.hasOwnProperty('borrowers')) {
                obj['borrowers'] = ApiClient.convertToType(data['borrowers'], [Borrower]);
            }
            if (data.hasOwnProperty('guarantors')) {
                obj['guarantors'] = ApiClient.convertToType(data['guarantors'], [Guarantor]);
            }
            if (data.hasOwnProperty('broker')) {
                obj['broker'] = ApiClient.convertToType(data['broker'], BrokerDetail);
            }
            if (data.hasOwnProperty('bd')) {
                obj['bd'] = ApiClient.convertToType(data['bd'], BDM);
            }
            if (data.hasOwnProperty('branch')) {
                obj['branch'] = ApiClient.convertToType(data['branch'], Branch);
            }
            if (data.hasOwnProperty('documents')) {
                obj['documents'] = ApiClient.convertToType(data['documents'], [Object]);
            }
            if (data.hasOwnProperty('notes')) {
                obj['notes'] = ApiClient.convertToType(data['notes'], [Object]);
            }
            if (data.hasOwnProperty('fees')) {
                obj['fees'] = ApiClient.convertToType(data['fees'], [Object]);
            }
            if (data.hasOwnProperty('repayments')) {
                obj['repayments'] = ApiClient.convertToType(data['repayments'], [Object]);
            }
            if (data.hasOwnProperty('ledger_entries')) {
                obj['ledger_entries'] = ApiClient.convertToType(data['ledger_entries'], [Object]);
            }
            if (data.hasOwnProperty('security_address')) {
                obj['security_address'] = ApiClient.convertToType(data['security_address'], 'String');
            }
            if (data.hasOwnProperty('security_type')) {
                obj['security_type'] = ApiClient.convertToType(data['security_type'], 'String');
            }
            if (data.hasOwnProperty('security_value')) {
                obj['security_value'] = ApiClient.convertToType(data['security_value'], 'Number');
            }
            if (data.hasOwnProperty('valuer_company_name')) {
                obj['valuer_company_name'] = ApiClient.convertToType(data['valuer_company_name'], 'String');
            }
            if (data.hasOwnProperty('valuer_contact_name')) {
                obj['valuer_contact_name'] = ApiClient.convertToType(data['valuer_contact_name'], 'String');
            }
            if (data.hasOwnProperty('valuer_phone')) {
                obj['valuer_phone'] = ApiClient.convertToType(data['valuer_phone'], 'String');
            }
            if (data.hasOwnProperty('valuer_email')) {
                obj['valuer_email'] = ApiClient.convertToType(data['valuer_email'], 'String');
            }
            if (data.hasOwnProperty('valuation_date')) {
                obj['valuation_date'] = ApiClient.convertToType(data['valuation_date'], 'Date');
            }
            if (data.hasOwnProperty('valuation_amount')) {
                obj['valuation_amount'] = ApiClient.convertToType(data['valuation_amount'], 'Number');
            }
            if (data.hasOwnProperty('qs_company_name')) {
                obj['qs_company_name'] = ApiClient.convertToType(data['qs_company_name'], 'String');
            }
            if (data.hasOwnProperty('qs_contact_name')) {
                obj['qs_contact_name'] = ApiClient.convertToType(data['qs_contact_name'], 'String');
            }
            if (data.hasOwnProperty('qs_phone')) {
                obj['qs_phone'] = ApiClient.convertToType(data['qs_phone'], 'String');
            }
            if (data.hasOwnProperty('qs_email')) {
                obj['qs_email'] = ApiClient.convertToType(data['qs_email'], 'String');
            }
            if (data.hasOwnProperty('qs_report_date')) {
                obj['qs_report_date'] = ApiClient.convertToType(data['qs_report_date'], 'Date');
            }
            if (data.hasOwnProperty('signed_by')) {
                obj['signed_by'] = ApiClient.convertToType(data['signed_by'], 'String');
            }
            if (data.hasOwnProperty('signature_date')) {
                obj['signature_date'] = ApiClient.convertToType(data['signature_date'], 'Date');
            }
            if (data.hasOwnProperty('uploaded_pdf_path')) {
                obj['uploaded_pdf_path'] = ApiClient.convertToType(data['uploaded_pdf_path'], 'String');
            }
            if (data.hasOwnProperty('funding_result')) {
                obj['funding_result'] = ApiClient.convertToType(data['funding_result'], Object);
            }
            if (data.hasOwnProperty('created_by_details')) {
                obj['created_by_details'] = ApiClient.convertToType(data['created_by_details'], User);
            }
        }
        return obj;
    }

    /**
     * Validates the JSON data with respect to <code>ApplicationDetail</code>.
     * @param {Object} data The plain JavaScript object bearing properties of interest.
     * @return {boolean} to indicate whether the JSON data is valid with respect to <code>ApplicationDetail</code>.
     */
    static validateJSON(data) {
        // check to make sure all required properties are present in the JSON string
        for (const property of ApplicationDetail.RequiredProperties) {
            if (!data.hasOwnProperty(property)) {
                throw new Error("The required field `" + property + "` is not found in the JSON data: " + JSON.stringify(data));
            }
        }
        // ensure the json data is a string
        if (data['reference_number'] && !(typeof data['reference_number'] === 'string' || data['reference_number'] instanceof String)) {
            throw new Error("Expected the field `reference_number` to be a primitive type in the JSON string but got " + data['reference_number']);
        }
        // ensure the json data is a string
        if (data['loan_amount'] && !(typeof data['loan_amount'] === 'string' || data['loan_amount'] instanceof String)) {
            throw new Error("Expected the field `loan_amount` to be a primitive type in the JSON string but got " + data['loan_amount']);
        }
        // ensure the json data is a string
        if (data['interest_rate'] && !(typeof data['interest_rate'] === 'string' || data['interest_rate'] instanceof String)) {
            throw new Error("Expected the field `interest_rate` to be a primitive type in the JSON string but got " + data['interest_rate']);
        }
        // ensure the json data is a string
        if (data['purpose'] && !(typeof data['purpose'] === 'string' || data['purpose'] instanceof String)) {
            throw new Error("Expected the field `purpose` to be a primitive type in the JSON string but got " + data['purpose']);
        }
        // validate the optional field `application_type`
        if (data['application_type']) { // data not null
          ApplicationCreateApplicationType.validateJSON(data['application_type']);
        }
        // ensure the json data is a string
        if (data['product_id'] && !(typeof data['product_id'] === 'string' || data['product_id'] instanceof String)) {
            throw new Error("Expected the field `product_id` to be a primitive type in the JSON string but got " + data['product_id']);
        }
        // ensure the json data is a string
        if (data['stage_display'] && !(typeof data['stage_display'] === 'string' || data['stage_display'] instanceof String)) {
            throw new Error("Expected the field `stage_display` to be a primitive type in the JSON string but got " + data['stage_display']);
        }
        if (data['borrowers']) { // data not null
            // ensure the json data is an array
            if (!Array.isArray(data['borrowers'])) {
                throw new Error("Expected the field `borrowers` to be an array in the JSON data but got " + data['borrowers']);
            }
            // validate the optional field `borrowers` (array)
            for (const item of data['borrowers']) {
                Borrower.validateJSON(item);
            };
        }
        if (data['guarantors']) { // data not null
            // ensure the json data is an array
            if (!Array.isArray(data['guarantors'])) {
                throw new Error("Expected the field `guarantors` to be an array in the JSON data but got " + data['guarantors']);
            }
            // validate the optional field `guarantors` (array)
            for (const item of data['guarantors']) {
                Guarantor.validateJSON(item);
            };
        }
        // validate the optional field `broker`
        if (data['broker']) { // data not null
          BrokerDetail.validateJSON(data['broker']);
        }
        // validate the optional field `bd`
        if (data['bd']) { // data not null
          BDM.validateJSON(data['bd']);
        }
        // validate the optional field `branch`
        if (data['branch']) { // data not null
          Branch.validateJSON(data['branch']);
        }
        // ensure the json data is an array
        if (!Array.isArray(data['documents'])) {
            throw new Error("Expected the field `documents` to be an array in the JSON data but got " + data['documents']);
        }
        // ensure the json data is an array
        if (!Array.isArray(data['notes'])) {
            throw new Error("Expected the field `notes` to be an array in the JSON data but got " + data['notes']);
        }
        // ensure the json data is an array
        if (!Array.isArray(data['fees'])) {
            throw new Error("Expected the field `fees` to be an array in the JSON data but got " + data['fees']);
        }
        // ensure the json data is an array
        if (!Array.isArray(data['repayments'])) {
            throw new Error("Expected the field `repayments` to be an array in the JSON data but got " + data['repayments']);
        }
        // ensure the json data is an array
        if (!Array.isArray(data['ledger_entries'])) {
            throw new Error("Expected the field `ledger_entries` to be an array in the JSON data but got " + data['ledger_entries']);
        }
        // ensure the json data is a string
        if (data['security_address'] && !(typeof data['security_address'] === 'string' || data['security_address'] instanceof String)) {
            throw new Error("Expected the field `security_address` to be a primitive type in the JSON string but got " + data['security_address']);
        }
        // ensure the json data is a string
        if (data['security_type'] && !(typeof data['security_type'] === 'string' || data['security_type'] instanceof String)) {
            throw new Error("Expected the field `security_type` to be a primitive type in the JSON string but got " + data['security_type']);
        }
        // ensure the json data is a string
        if (data['security_value'] && !(typeof data['security_value'] === 'string' || data['security_value'] instanceof String)) {
            throw new Error("Expected the field `security_value` to be a primitive type in the JSON string but got " + data['security_value']);
        }
        // ensure the json data is a string
        if (data['valuer_company_name'] && !(typeof data['valuer_company_name'] === 'string' || data['valuer_company_name'] instanceof String)) {
            throw new Error("Expected the field `valuer_company_name` to be a primitive type in the JSON string but got " + data['valuer_company_name']);
        }
        // ensure the json data is a string
        if (data['valuer_contact_name'] && !(typeof data['valuer_contact_name'] === 'string' || data['valuer_contact_name'] instanceof String)) {
            throw new Error("Expected the field `valuer_contact_name` to be a primitive type in the JSON string but got " + data['valuer_contact_name']);
        }
        // ensure the json data is a string
        if (data['valuer_phone'] && !(typeof data['valuer_phone'] === 'string' || data['valuer_phone'] instanceof String)) {
            throw new Error("Expected the field `valuer_phone` to be a primitive type in the JSON string but got " + data['valuer_phone']);
        }
        // ensure the json data is a string
        if (data['valuer_email'] && !(typeof data['valuer_email'] === 'string' || data['valuer_email'] instanceof String)) {
            throw new Error("Expected the field `valuer_email` to be a primitive type in the JSON string but got " + data['valuer_email']);
        }
        // ensure the json data is a string
        if (data['valuation_amount'] && !(typeof data['valuation_amount'] === 'string' || data['valuation_amount'] instanceof String)) {
            throw new Error("Expected the field `valuation_amount` to be a primitive type in the JSON string but got " + data['valuation_amount']);
        }
        // ensure the json data is a string
        if (data['qs_company_name'] && !(typeof data['qs_company_name'] === 'string' || data['qs_company_name'] instanceof String)) {
            throw new Error("Expected the field `qs_company_name` to be a primitive type in the JSON string but got " + data['qs_company_name']);
        }
        // ensure the json data is a string
        if (data['qs_contact_name'] && !(typeof data['qs_contact_name'] === 'string' || data['qs_contact_name'] instanceof String)) {
            throw new Error("Expected the field `qs_contact_name` to be a primitive type in the JSON string but got " + data['qs_contact_name']);
        }
        // ensure the json data is a string
        if (data['qs_phone'] && !(typeof data['qs_phone'] === 'string' || data['qs_phone'] instanceof String)) {
            throw new Error("Expected the field `qs_phone` to be a primitive type in the JSON string but got " + data['qs_phone']);
        }
        // ensure the json data is a string
        if (data['qs_email'] && !(typeof data['qs_email'] === 'string' || data['qs_email'] instanceof String)) {
            throw new Error("Expected the field `qs_email` to be a primitive type in the JSON string but got " + data['qs_email']);
        }
        // ensure the json data is a string
        if (data['signed_by'] && !(typeof data['signed_by'] === 'string' || data['signed_by'] instanceof String)) {
            throw new Error("Expected the field `signed_by` to be a primitive type in the JSON string but got " + data['signed_by']);
        }
        // ensure the json data is a string
        if (data['uploaded_pdf_path'] && !(typeof data['uploaded_pdf_path'] === 'string' || data['uploaded_pdf_path'] instanceof String)) {
            throw new Error("Expected the field `uploaded_pdf_path` to be a primitive type in the JSON string but got " + data['uploaded_pdf_path']);
        }
        // validate the optional field `created_by_details`
        if (data['created_by_details']) { // data not null
          User.validateJSON(data['created_by_details']);
        }

        return true;
    }


}

ApplicationDetail.RequiredProperties = ["id", "stage_display", "created_at", "updated_at", "borrowers", "guarantors", "broker", "bd", "branch", "documents", "notes", "fees", "repayments", "ledger_entries", "created_by_details"];

/**
 * @member {Number} id
 */
ApplicationDetail.prototype['id'] = undefined;

/**
 * @member {String} reference_number
 */
ApplicationDetail.prototype['reference_number'] = undefined;

/**
 * @member {Number} loan_amount
 */
ApplicationDetail.prototype['loan_amount'] = undefined;

/**
 * Loan term in months
 * @member {Number} loan_term
 */
ApplicationDetail.prototype['loan_term'] = undefined;

/**
 * @member {Number} interest_rate
 */
ApplicationDetail.prototype['interest_rate'] = undefined;

/**
 * @member {String} purpose
 */
ApplicationDetail.prototype['purpose'] = undefined;

/**
 * @member {module:models/RepaymentFrequencyEnum} repayment_frequency
 */
ApplicationDetail.prototype['repayment_frequency'] = undefined;

/**
 * @member {module:models/ApplicationCreateApplicationType} application_type
 */
ApplicationDetail.prototype['application_type'] = undefined;

/**
 * @member {String} product_id
 */
ApplicationDetail.prototype['product_id'] = undefined;

/**
 * @member {Date} estimated_settlement_date
 */
ApplicationDetail.prototype['estimated_settlement_date'] = undefined;

/**
 * @member {module:models/StageEnum} stage
 */
ApplicationDetail.prototype['stage'] = undefined;

/**
 * @member {String} stage_display
 */
ApplicationDetail.prototype['stage_display'] = undefined;

/**
 * @member {Date} created_at
 */
ApplicationDetail.prototype['created_at'] = undefined;

/**
 * @member {Date} updated_at
 */
ApplicationDetail.prototype['updated_at'] = undefined;

/**
 * @member {Array.<module:models/Borrower>} borrowers
 */
ApplicationDetail.prototype['borrowers'] = undefined;

/**
 * @member {Array.<module:models/Guarantor>} guarantors
 */
ApplicationDetail.prototype['guarantors'] = undefined;

/**
 * @member {module:models/BrokerDetail} broker
 */
ApplicationDetail.prototype['broker'] = undefined;

/**
 * @member {module:models/BDM} bd
 */
ApplicationDetail.prototype['bd'] = undefined;

/**
 * @member {module:models/Branch} branch
 */
ApplicationDetail.prototype['branch'] = undefined;

/**
 * @member {Array.<Object>} documents
 */
ApplicationDetail.prototype['documents'] = undefined;

/**
 * @member {Array.<Object>} notes
 */
ApplicationDetail.prototype['notes'] = undefined;

/**
 * @member {Array.<Object>} fees
 */
ApplicationDetail.prototype['fees'] = undefined;

/**
 * @member {Array.<Object>} repayments
 */
ApplicationDetail.prototype['repayments'] = undefined;

/**
 * @member {Array.<Object>} ledger_entries
 */
ApplicationDetail.prototype['ledger_entries'] = undefined;

/**
 * @member {String} security_address
 */
ApplicationDetail.prototype['security_address'] = undefined;

/**
 * @member {String} security_type
 */
ApplicationDetail.prototype['security_type'] = undefined;

/**
 * @member {Number} security_value
 */
ApplicationDetail.prototype['security_value'] = undefined;

/**
 * @member {String} valuer_company_name
 */
ApplicationDetail.prototype['valuer_company_name'] = undefined;

/**
 * @member {String} valuer_contact_name
 */
ApplicationDetail.prototype['valuer_contact_name'] = undefined;

/**
 * @member {String} valuer_phone
 */
ApplicationDetail.prototype['valuer_phone'] = undefined;

/**
 * @member {String} valuer_email
 */
ApplicationDetail.prototype['valuer_email'] = undefined;

/**
 * @member {Date} valuation_date
 */
ApplicationDetail.prototype['valuation_date'] = undefined;

/**
 * @member {Number} valuation_amount
 */
ApplicationDetail.prototype['valuation_amount'] = undefined;

/**
 * @member {String} qs_company_name
 */
ApplicationDetail.prototype['qs_company_name'] = undefined;

/**
 * @member {String} qs_contact_name
 */
ApplicationDetail.prototype['qs_contact_name'] = undefined;

/**
 * @member {String} qs_phone
 */
ApplicationDetail.prototype['qs_phone'] = undefined;

/**
 * @member {String} qs_email
 */
ApplicationDetail.prototype['qs_email'] = undefined;

/**
 * @member {Date} qs_report_date
 */
ApplicationDetail.prototype['qs_report_date'] = undefined;

/**
 * @member {String} signed_by
 */
ApplicationDetail.prototype['signed_by'] = undefined;

/**
 * @member {Date} signature_date
 */
ApplicationDetail.prototype['signature_date'] = undefined;

/**
 * @member {String} uploaded_pdf_path
 */
ApplicationDetail.prototype['uploaded_pdf_path'] = undefined;

/**
 * Stores the current funding calculation result
 * @member {Object} funding_result
 */
ApplicationDetail.prototype['funding_result'] = undefined;

/**
 * @member {module:models/User} created_by_details
 */
ApplicationDetail.prototype['created_by_details'] = undefined;






export default ApplicationDetail;

