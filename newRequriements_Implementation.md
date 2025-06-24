# 🚀 New Requirements Implementation Document

## 📋 Overview
This document outlines the detailed implementation plan for the 18 new requirements provided by the client. The implementation covers both backend (Django) and frontend (Vue.js) changes required to enhance the CRM Loan Management System.

## 🎯 Requirements Analysis & Implementation Plan

### **Requirement 1: Remove Required Field Validations**
> *"When entering the fields, I don't want anything that is a required field, because we need to enter in the details as soon as we receive the scenario, but we don't necessarily have all the information at that point."*

#### Backend Changes:
- **File**: `PVDOCKER-0e9d989a06b724cfb597e3148652e687871d3891/backenddjango/applications/models.py`
  - Review all model fields and ensure `null=True, blank=True` for most fields
  - Update `ApplicationCreateSerializer` in `serializers.py` to remove required field validations
  - Modify form validation to allow partial data entry

#### Frontend Changes:
- **File**: `ICfding/ICprivate-funding/src/view/application/application.vue`
  - Remove `required` attributes from form inputs
  - Update form validation to be non-blocking
  - Add visual indicators for recommended fields vs. optional fields

#### Implementation Priority: **HIGH** ⚡
#### Estimated Effort: **2-3 days**

---

### **Requirement 2: Add "Next" Button in Application Form**
> *"Could we please add a "Next" button between the "Cancel" and "Save" button when we're adding a new application?"*

#### Frontend Changes:
- **File**: `ICfding/ICprivate-funding/src/view/application/application.vue`
  - Add "Next" button in form navigation
  - Implement step-by-step form progression
  - Add form state management for multi-step navigation

#### Implementation Priority: **MEDIUM** 🔶
#### Estimated Effort: **1 day**

---

### **Requirement 3: Remove Auto-selection on General Solvency Enquiries**
> *"Get rid of the auto-selection on the "General Solvency Enquiries" tab"*

#### Backend Changes:
- **File**: `PVDOCKER-0e9d989a06b724cfb597e3148652e687871d3891/backenddjango/applications/models.py`
  - Change default values for solvency fields from `default=False` to `default=None`
  - Update model fields to use `BooleanField(null=True, blank=True, default=None)`

#### Frontend Changes:
- **File**: Form components handling solvency enquiries
  - Remove default checked states
  - Update radio buttons/checkboxes to have no pre-selection

#### Implementation Priority: **MEDIUM** 🔶
#### Estimated Effort: **0.5 days**

---

### **Requirement 4: Update Application Type Dropdown**
> *"In Loan Details > Application Type, change the drop down list to Acquisition, Refinance, Equity Release, Refinance & Equity Release, 2nd Mortgage, Caveat, Other (add textbox if other is selected)"*

#### Backend Changes:
- **File**: `PVDOCKER-0e9d989a06b724cfb597e3148652e687871d3891/backenddjango/applications/models.py`
  ```python
  APPLICATION_TYPE_CHOICES = [
      ('acquisition', 'Acquisition'),
      ('refinance', 'Refinance'),
      ('equity_release', 'Equity Release'),
      ('refinance_equity_release', 'Refinance & Equity Release'),
      ('second_mortgage', '2nd Mortgage'),
      ('caveat', 'Caveat'),
      ('other', 'Other'),
  ]
  ```
  - Add `application_type_other` field: `models.TextField(null=True, blank=True)`

#### Frontend Changes:
- **File**: Application form components
  - Update dropdown options
  - Add conditional text input when "Other" is selected
  - Update form validation logic

#### Implementation Priority: **HIGH** ⚡
#### Estimated Effort: **1 day**

---

### **Requirement 5: Add Capitalised Interest Term Field**
> *"In Loan Details we also need to add in Capitalised Interest Term (Months)"*

#### Backend Changes:
- **File**: `PVDOCKER-0e9d989a06b724cfb597e3148652e687871d3891/backenddjango/applications/models.py`
  - Add field: `capitalised_interest_term = models.PositiveIntegerField(null=True, blank=True, help_text="Capitalised Interest Term in months")`
  - Update serializers to include this field

#### Frontend Changes:
- **File**: Loan details form component
  - Add input field for capitalised interest term
  - Add validation for positive integers only

#### Implementation Priority: **MEDIUM** 🔶
#### Estimated Effort: **0.5 days**

---

### **Requirement 6: Add Valuer and QS as Related People**
> *"I need a valuer and QS as related people so we're not re-entering their details every time"*

#### Backend Changes:
- **New Models**: Create dedicated models for reusable contacts
  ```python
  class Valuer(models.Model):
      company_name = models.CharField(max_length=255)
      contact_name = models.CharField(max_length=255)
      phone = models.CharField(max_length=20)
      email = models.EmailField()
      # ... metadata fields
  
  class QuantitySurveyor(models.Model):
      company_name = models.CharField(max_length=255)
      contact_name = models.CharField(max_length=255)
      phone = models.CharField(max_length=20)
      email = models.EmailField()
      # ... metadata fields
  ```
- **File**: `PVDOCKER-0e9d989a06b724cfb597e3148652e687871d3891/backenddjango/applications/models.py`
  - Add ForeignKey relationships to Application model
  - Create CRUD endpoints for valuers and QS
  - Create management views for maintaining the lists

#### Frontend Changes:
- **New Views**: 
  - Valuer management page
  - QS management page
- **Application Form**: 
  - Replace flat input fields with dropdown selection
  - Add "Add New" option for quick entry

#### Implementation Priority: **HIGH** ⚡
#### Estimated Effort: **3-4 days**

---

### **Requirement 7: Fix Application Save Issue**
> *"It doesn't allow me to change save the application despite filling everything in as required"*

#### Backend Changes:
- **File**: `PVDOCKER-0e9d989a06b724cfb597e3148652e687871d3891/backenddjango/applications/serializers.py`
  - Debug and fix validation issues in ApplicationSerializer
  - Remove blocking validations that prevent saving
  - Add comprehensive error logging

#### Frontend Changes:
- **File**: Application form components
  - Improve error handling and display
  - Add debug logging for save operations
  - Implement auto-save functionality

#### Implementation Priority: **CRITICAL** 🔴
#### Estimated Effort: **2 days**

---

### **Requirement 8: Add Broker/BDM/Branch Linking**
> *"There's nowhere in the application that allows me to link it to the broker, BDM, Branch etc. That should ideally be the first thing we fill out"*

#### Backend Changes:
- **File**: `PVDOCKER-0e9d989a06b724cfb597e3148652e687871d3891/backenddjango/applications/models.py`
  - Ensure ForeignKey relationships exist (already implemented)
  - Update serializers to include broker/BDM/branch data

#### Frontend Changes:
- **File**: `ICfding/ICprivate-funding/src/view/application/application.vue`
  - Add broker/BDM/branch selection as **Step 1** of the form
  - Create dropdown components with search functionality
  - Make this section prominent and easily accessible

#### Implementation Priority: **HIGH** ⚡
#### Estimated Effort: **2 days**

---

### **Requirement 9: Simplify Branch Section**
> *"In the "Branch" section, get rid of address, phone number and email address. We only need the branch name as they're all internal entities anyway. Could we also change Branch to Branch/Subsidiary?"*

#### Backend Changes:
- **File**: `PVDOCKER-0e9d989a06b724cfb597e3148652e687871d3891/backenddjango/brokers/models.py`
  - Keep address, phone, email fields in model (for data integrity) but mark as deprecated
  - Update model verbose names to "Branch/Subsidiary"

#### Frontend Changes:
- **Forms**: Remove address, phone, email fields from branch forms
- **Labels**: Update all references from "Branch" to "Branch/Subsidiary"
- **Lists**: Display only branch name in selection dropdowns

#### Implementation Priority: **LOW** 🔵
#### Estimated Effort: **0.5 days**

---

### **Requirement 10a: Add BDM Assignment to Broker**
> *"In the Broker section could we add a drop down menu to assign a BDM to them?"*

#### Backend Changes:
- **File**: `PVDOCKER-0e9d989a06b724cfb597e3148652e687871d3891/backenddjango/brokers/models.py`
  - The `bdms` ManyToManyField already exists in Broker model
  - Update serializers to handle BDM assignment

#### Frontend Changes:
- **File**: Broker form components
  - Add BDM selection dropdown
  - Allow multiple BDM assignments
  - Add search functionality

#### Implementation Priority: **MEDIUM** 🔶
#### Estimated Effort: **1 day**

---

### **Requirement 10b: Lock Commission Account**
> *"In the Broker section, make it locked so that only the Super User and Accounts can change the Commission Account once it's been entered for the first time"*

#### Backend Changes:
- **File**: `PVDOCKER-0e9d989a06b724cfb597e3148652e687871d3891/backenddjango/brokers/models.py`
  - Add `commission_account_locked` field
  - Add permission checks in serializers and views

#### Frontend Changes:
- **File**: Broker form components
  - Disable commission fields based on user role and lock status
  - Add visual indicators for locked fields
  - Show appropriate messages for restricted access

#### Implementation Priority: **HIGH** ⚡
#### Estimated Effort: **1-2 days**

---

### **Requirement 11: Update User Roles**
> *"In the User > Roles section, could we please make them the following: Accounts, Admin, Business Development Manager, Business Development Associate, Credit Manager, Super User"*

#### Backend Changes:
- **File**: `PVDOCKER-0e9d989a06b724cfb597e3148652e687871d3891/backenddjango/users/models.py`
  ```python
  ROLE_CHOICES = [
      ('accounts', 'Accounts'),
      ('admin', 'Admin'),
      ('business_development_manager', 'Business Development Manager'),
      ('business_development_associate', 'Business Development Associate'),
      ('credit_manager', 'Credit Manager'),
      ('super_user', 'Super User'),
  ]
  ```
- Update permission framework throughout the application
- Create migration for existing users

#### Frontend Changes:
- Update all role-based UI elements
- Implement Super User access controls
- Update role selection dropdowns

#### Implementation Priority: **HIGH** ⚡
#### Estimated Effort: **3-4 days**


---

### **Requirement 13: Test Notifications/Alerts System**
> *"As I wasn't able to create an application, I can't test out the notifications/alerts systems."*

#### Backend Changes:
- Fix the application creation issue (related to Requirement 7)
- Ensure notification system is working correctly
- Add comprehensive logging for notification triggers

#### Frontend Changes:
- Ensure notification center is fully functional
- Add notification testing interface for admins
- Improve notification display and management

#### Implementation Priority: **HIGH** ⚡
#### Estimated Effort: **1-2 days**

---

### **Requirement 14: Add Alerts Section with User Filtering**
> *"I can't seem to see a section for alerts either to sort by user. Can we please get this made when we enter the alerts systems?"*

#### Backend Changes:
- **File**: `PVDOCKER-0e9d989a06b724cfb597e3148652e687871d3891/backenddjango/users/models.py`
  - Add filtering capabilities to Notification model
  - Create notification management endpoints

#### Frontend Changes:
- **New View**: Alerts management page
- **Features**: 
  - Filter notifications by user
  - Bulk notification actions
  - Notification statistics dashboard

#### Implementation Priority: **MEDIUM** 🔶
#### Estimated Effort: **2-3 days**

---

### **Requirement 15: Document Search by App ID & Borrower**
> *"For the Documents Upload section, could we make it so we can search the app ID & Borrower ID by name/address?"*

#### Backend Changes:
- **File**: `PVDOCKER-0e9d989a06b724cfb597e3148652e687871d3891/backenddjango/documents/views.py`
  - Add search functionality to document endpoints
  - Implement full-text search across application and borrower fields

#### Frontend Changes:
- **File**: `ICfding/ICprivate-funding/src/view/document.vue`
  - Add search bar with autocomplete
  - Implement search by application ID, borrower name, and address
  - Add search result highlighting

#### Implementation Priority: **MEDIUM** 🔶
#### Estimated Effort: **2 days**

---

### **Requirement 16: Application Stage Management**
> *"I need a section again in the beginning of the app section to show what stage the application is at and we can also filter apps using this. The stages are as follows: Received, Sent to Lender/Investor, Funding Table Issued, Indicative Letter Issued, Indicative Letter Signed, Commitment Fee Received, Application Submitted, Valuation Ordered, Valuation Received, More Information Required, Formal Approval, Loan Documents Instructed, Loan Documents Issued, Loan Documents Signed, Settlement Conditions, Settled, Closed, Discharged."*

#### Backend Changes:
- **File**: `PVDOCKER-0e9d989a06b724cfb597e3148652e687871d3891/backenddjango/applications/models.py`
  ```python
  STAGE_CHOICES = [
      ('received', 'Received'),
      ('sent_to_lender', 'Sent to Lender/Investor'),
      ('funding_table_issued', 'Funding Table Issued'),
      ('indicative_letter_issued', 'Indicative Letter Issued'),
      ('indicative_letter_signed', 'Indicative Letter Signed'),
      ('commitment_fee_received', 'Commitment Fee Received'),
      ('application_submitted', 'Application Submitted'),
      ('valuation_ordered', 'Valuation Ordered'),
      ('valuation_received', 'Valuation Received'),
      ('more_information_required', 'More Information Required'),
      ('formal_approval', 'Formal Approval'),
      ('loan_documents_instructed', 'Loan Documents Instructed'),
      ('loan_documents_issued', 'Loan Documents Issued'),
      ('loan_documents_signed', 'Loan Documents Signed'),
      ('settlement_conditions', 'Settlement Conditions'),
      ('settled', 'Settled'),
      ('closed', 'Closed'),
      ('discharged', 'Discharged'),
  ]
  ```
- Update existing applications with migration
- Add stage change tracking and audit trail

#### Frontend Changes:
- **Application List**: Add stage filter dropdown
- **Application Detail**: Prominent stage display at the top
- **Dashboard**: Stage-based application counts and visual indicators
- **Stage Management**: Easy stage progression interface

#### Implementation Priority: **CRITICAL** 🔴
#### Estimated Effort: **3-4 days**

---

### **Requirement 17: Auto-archive Closed Applications**
> *"All apps with the status of "Closed" are automatically archived and removed from the dashboard. However, we still need to be able to search for it."*

---

### ✅ Cursor Prompt (Safe Additive Implementation)

```markdown
### Task: Add Auto-Archive Feature for Closed Applications

---

#### Backend Tasks (Non-intrusive)

1. Add a new boolean field `is_archived` (default: false) to the application model. Do not modify existing logic.
2. In the application save or update logic, add a new check:
   - If `stage` is `"Closed"` (case-insensitive), set `is_archived = true`.
3. Without touching the main query logic, add an optional filter:
   - If query param `include_archived=true` is passed, include archived records.
   - By default, return only non-archived applications.
4. Keep search functionality unchanged, but allow search across all records (archived and active).
5. Keep the existing API stable. Only append logic.

---

#### Frontend Tasks (Minimal Invasive UI Addition)

1. Add a toggle/switch labeled “Include Archived” to the application list page.
   - When on, fetch applications with `include_archived=true`.
2. Add a visual indicator (e.g. tag “Archived”) for archived applications in the list view.
3. In dashboard view:
   - Add a count display of archived applications.
   - Add a new button labeled “View Archived” which routes to the list view with archived toggle enabled(please create a list view that shows all the archived applications, please do not use the application Original list page).

---

### Constraints

- ✅ Do not remove or rewrite any core logic.
- ✅ Only add new fields, new conditions, or optional toggles.
- ✅ Ensure all added logic is non-breaking and backward-compatible.

---


```


#### Implementation Priority: **HIGH** ⚡
#### Estimated Effort: **2 days**

---

### **Requirement 18: Active Loans Management & Alerts**
> *"All apps with the status of "Settled" are allocated towards "Active Loans" and will need to fill in an additional section with the following fields: Settlement Date, Capitalised Interest (Months), Interest Payments Required (Yes/No; if Yes, frequency & payment due date(s)), Loan Expiry Date. We also need an auto-reminder/alert set up so that the Admin gets an alert 2 weeks prior to the each interest payment is due and 1 month before Loan Expiry."*

#### Backend Changes:
- **New Model**: Create `ActiveLoan` model
  ```python
  class ActiveLoan(models.Model):
      application = models.OneToOneField(Application, on_delete=models.CASCADE)
      settlement_date = models.DateField()
      capitalised_interest_months = models.PositiveIntegerField()
      interest_payments_required = models.BooleanField()
      interest_payment_frequency = models.CharField(max_length=20)
      interest_payment_due_dates = JSONField()
      loan_expiry_date = models.DateField()
  ```
- **Celery Tasks**: 
  - Interest payment reminder (2 weeks prior)
  - Loan expiry reminder (1 month prior)
- **Auto-creation**: Trigger when application stage changes to 'settled'

#### Frontend Changes:
- **New Section**: Active Loans management interface
- **Application Detail**: Additional fields section for settled applications
- **Dashboard**: Active loans summary and alerts
- **Alerts**: Interest payment and expiry notifications

#### Implementation Priority: **HIGH** ⚡
#### Estimated Effort: **5-6 days**

---

## 📊 Implementation Summary

### **Priority Breakdown:**
- **CRITICAL** 🔴: Requirements 7, 16 (Application saving, Stage management)
- **HIGH** ⚡: Requirements 1, 4, 6, 8, 10b, 11, 13, 17, 18 (9 items)
- **MEDIUM** 🔶: Requirements 2, 3, 5, 10a, 12, 14, 15 (7 items)
- **LOW** 🔵: Requirement 9 (1 item)

### **Estimated Timeline:**
- **Phase 1 (Critical)**: 5-7 days
- **Phase 2 (High Priority)**: 15-20 days
- **Phase 3 (Medium Priority)**: 12-15 days
- **Phase 4 (Low Priority)**: 0.5 days

**Total Estimated Effort**: 32.5-42.5 days (6.5-8.5 weeks)

### **Resource Requirements:**
- 1 Full-stack Developer (Backend + Frontend)
- 1 QA Tester
- 1 Project Manager/Product Owner for requirement clarification

### **Technical Dependencies:**
1. Database migrations for model changes
2. Frontend component updates
3. Permission system overhaul
4. Notification system enhancement
5. Document generation system implementation

### **Testing Strategy:**
1. Unit tests for new models and serializers
2. Integration tests for API endpoints
3. Frontend component testing
4. End-to-end user workflow testing
5. Performance testing for search and filtering features

### **Deployment Considerations:**
1. Database migration scripts
2. Data migration for existing applications
3. User role migration
4. Template and document storage setup
5. Celery task scheduling configuration

---

## 🔧 Technical Implementation Notes

### **Database Migrations:**
- Careful migration planning needed for changing stage choices
- Data preservation for existing applications
- User role migration strategy

### **Performance Considerations:**
- Index creation for search functionality
- Pagination for large application lists
- Caching for frequently accessed data

### **Security Implications:**
- Enhanced role-based access control
- Commission account protection
- Document access permissions

### **API Documentation:**
- Update OpenAPI schema for new endpoints
- Frontend-backend contract validation
- Integration testing suite

---

This implementation document provides a comprehensive roadmap for implementing all 18 requirements with specific technical details, priorities, and estimated timelines. Each requirement has been analyzed for both backend and frontend implications, ensuring a complete solution. 