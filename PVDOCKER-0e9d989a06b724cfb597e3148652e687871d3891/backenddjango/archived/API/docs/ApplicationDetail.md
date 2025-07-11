# CrmClientJs.ApplicationDetail

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **Number** |  | [readonly] 
**referenceNumber** | **String** |  | [optional] 
**loanAmount** | **Number** |  | [optional] 
**loanTerm** | **Number** | Loan term in months | [optional] 
**interestRate** | **Number** |  | [optional] 
**purpose** | **String** |  | [optional] 
**repaymentFrequency** | [**RepaymentFrequencyEnum**](RepaymentFrequencyEnum.md) |  | [optional] 
**applicationType** | [**ApplicationCreateApplicationType**](ApplicationCreateApplicationType.md) |  | [optional] 
**productId** | **String** |  | [optional] 
**estimatedSettlementDate** | **Date** |  | [optional] 
**stage** | [**StageEnum**](StageEnum.md) |  | [optional] 
**stageDisplay** | **String** |  | [readonly] 
**createdAt** | **Date** |  | [readonly] 
**updatedAt** | **Date** |  | [readonly] 
**borrowers** | [**[Borrower]**](Borrower.md) |  | [readonly] 
**guarantors** | [**[Guarantor]**](Guarantor.md) |  | [readonly] 
**broker** | [**BrokerDetail**](BrokerDetail.md) |  | [readonly] 
**bd** | [**BDM**](BDM.md) |  | [readonly] 
**branch** | [**Branch**](Branch.md) |  | [readonly] 
**documents** | **[Object]** |  | [readonly] 
**notes** | **[Object]** |  | [readonly] 
**fees** | **[Object]** |  | [readonly] 
**repayments** | **[Object]** |  | [readonly] 
**ledgerEntries** | **[Object]** |  | [readonly] 
**securityAddress** | **String** |  | [optional] 
**securityType** | **String** |  | [optional] 
**securityValue** | **Number** |  | [optional] 
**valuerCompanyName** | **String** |  | [optional] 
**valuerContactName** | **String** |  | [optional] 
**valuerPhone** | **String** |  | [optional] 
**valuerEmail** | **String** |  | [optional] 
**valuationDate** | **Date** |  | [optional] 
**valuationAmount** | **Number** |  | [optional] 
**qsCompanyName** | **String** |  | [optional] 
**qsContactName** | **String** |  | [optional] 
**qsPhone** | **String** |  | [optional] 
**qsEmail** | **String** |  | [optional] 
**qsReportDate** | **Date** |  | [optional] 
**signedBy** | **String** |  | [optional] 
**signatureDate** | **Date** |  | [optional] 
**uploadedPdfPath** | **String** |  | [optional] 
**fundingResult** | **Object** | Stores the current funding calculation result | [optional] 
**createdByDetails** | [**User**](User.md) |  | [readonly] 


