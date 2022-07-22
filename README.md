<!-- README.md -->
<!--
Author: Chien Ho
Date: 2022.07.20
*** Reference links are enclosed in brackets [ ] instead of parentheses
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- Title -->
<div align="center">
  <h1 align="center">Healthcare Claims Metric Builder</h1>
</div>

<!-- The menu links to the various readme sections. Make these whatever works for your project -->      
<p align="center">
  <a href="#project-overview">Project Overview</a> •  
  <a href="#learning-concepts">Learning Concepts</a> •  
  <a href="#test-data">Test Data</a> •  
  <a href="#code">Code</a> •
  <a href="#aws-architecture">AWS Architecture</a> •
  <a href="#api-output">API Output</a> •
  <a href="#credits">Credits</a> •
</p>

---
<!-- PROJECT OVERVIEW --> 
<a name="project-overview"></a>
## Project Overview
   1) Build Python code that creates metrics from medical claims
   2) Deploy this code to a Lambda function
   3) Enable access through an API Gateway

<br/>

<!-- LEARNING CONCEPTS --> 
<a name="learning-concepts"></a>
## Learning Concepts
   * Python - Process medical claims to create and return metrics
      * To start, we're going to identify [inpatient admissions](https://info.medinsight.milliman.com/2016/09/methodology-for-identifying-inpatient-admission-events/) and calculate corresponding length of stay.
   * Healthcare Concepts - Types of Billing (Institutional/Hospital vs Professional/Physician), Types of Codes (Revenue vs Procedure vs Diagnosis)
      * Revenue codes are used on hospital bills to tell the payers (e.g. insurance companies) where the patient was when they received treatment (e.g. room and board).
      * Procedure codes (e.g CPT codes) are used by healthcare providers to describe the services they provided to the insurance companies for payment. 
      * Diagnosis codes (e.g. DRGs) describe the patient's medical condition and are required on claims submitted by healthcare professionals to the payers.
   * REST APIs - What are they and how can we interact with them?
   * JSON - Build a JSON structure for medical claims / Return a JSON structure with metrics
   * AWS (Lambda & API Gateway) - Set up a Lambda function and API Gateway in AWS 
      *  AWS Lambda is a serverless, event-driven compute service that lets you run code for virtually any type of application or backend service without provisioning or managing servers. 
      * Amazon API Gateway is a fully managed service to create, publish, maintain, monitor, and secure APIs at any scale. APIs act as the "front door" for applications to access data, business logic, or functionality from your backend services.

<br/>

<!-- TEST DATA --> 
<a name="test-data"></a>
## Test Data
Test data consists of nine members and their associated Facility (I), Professional (P), and Pharmacy (R) claims.

| member\_id | claimtype | clm\_cnt | line\_cnt |
| :--- | :--- | :--- | :--- |
| mbr_01 | P | 1 | 3 |
| mbr_01 | R | 2 | 1 |
| mbr_01 | P | 8 | 2 |
| mbr_03 | I | 1 | 11 |
| mbr_03 | P | 15 | 2 |


*Note: The test data, called 'lambda_project_dummy_data.json', can be found in [test data](https://github.com/chienqho/project_lambda/tree/main/test_data) folder*

<br/>

*Partial example of the test data JSON file:*
```
{
    "contents":[
      {
         "member_id":"mbr_01",
         "member_age":348,
         "member_sex":"F",
         "claim":[
            {
               "claim_id":"clm_0101",
               "claim_type":"P",
               "type_of_bill":null,
               "admission_date":"2019-02-12",
               "discharge_date":"2019-02-12",
               "taxonomy_code":"363A00000X",
               "place_of_service":11,
               "principle_diagnosis":"F909",
               "diagnosis_codes":[
                  "F909",
                  null,
                  null,
                  null,
                  null,
                  null,
                  null,
                  null,
                  null,
                  null
               ],
               "drg":null,
               "drg_severity":null,
               "drg_type":null,
               "claim_line":[
                  {
                     "line_number":1,
                     "from_date":"2019-02-12",
                     "thru_date":"2019-02-12",
                     "revenue_code":null,
                     "procedure_code":"99215",
                     "ndc_code":null,
                     "quantity":1,
                     "allowed_amount":174.25
                  },
                  {
                     "line_number":2,
                     "from_date":"2019-02-12",
                     "thru_date":"2019-02-12",
                     "revenue_code":null,
                     "procedure_code":"96127",
                     "ndc_code":null,
                     "quantity":2,
                     "allowed_amount":0
                  },
                  {
                     "line_number":3,
                     "from_date":"2019-02-12",
                     "thru_date":"2019-02-12",
                     "revenue_code":null,
                     "procedure_code":"96138",
                     "ndc_code":null,
                     "quantity":1,
                     "allowed_amount":45.8999999999999986
                  }
               ]
            },
            {
               "claim_id":"clm_0102",
               "claim_type":"R",
               "type_of_bill":null,
               "admission_date":"2019-04-09",
               "discharge_date":"2019-04-09",
               "taxonomy_code":null,
               "place_of_service":null,
               "principle_diagnosis":null,
               "diagnosis_codes":[
                  null,
                  null,
                  null,
                  null,
                  null,
                  null,
                  null,
                  null,
                  null,
                  null
               ],
               "drg":null,
               "drg_severity":null,
               "drg_type":null,
               "claim_line":[
                  {
                     "line_number":1,
                     "from_date":"2019-04-09",
                     "thru_date":"2019-04-09",
                     "revenue_code":null,
                     "procedure_code":null,
                     "ndc_code":"68462013281",
                     "quantity":63,
                     "allowed_amount":33
                  }
               ]
            },
...
```

<br/>

<!-- CODE --> 
<a name="code"></a>
## Code
[Python code](https://github.com/chienqho/project_lambda/blob/main/querying-json.py) can also be viewed as a [juypter notebook](https://github.com/chienqho/project_lambda/blob/main/querying-json.ipynb).

<br/>

<!-- ARCHITECTURE --> 
<a name="aws-architecture"></a>
## AWS Architecture
   1) Set up a Lambda function in AWS Deploy our Python code 
   2) Create and configure an API Gateway to invoke our Lambda function 
   3) Implement access control (API Key) to prevent unauthorized access 
   4) Test our work

<br/>

<!-- API OUTPUT --> 
<a name="api-output"></a>
## API Output
Enter the following in terminal to access API output:
```
$ curl -X GET https://3lrj8ubm6e.execute-api.us-west-1.amazonaws.com/default/metrics -H 'x-api-key: feoKP2EInRai02yPy3ojs8b8t77ViLaz7ojPAi7c'
```

<!-- CREDITS -->
<a name="credits"></a>

## Credits
Giving the BIGGEST THANK YOU to [Rich King](https://www.linkedin.com/in/richwking/) and [Gary Cattabriga](https://www.linkedin.com/in/gcattabriga/) for their guidance through this project and for always being there when I had questions.
<br/>
