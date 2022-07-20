<!-- README.md -->
<!--
Author: Chien Ho
Date: 2022.07.18
*** Reference links are enclosed in brackets [ ] instead of parentheses
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- Title -->
<div align="center">
  <h1 style="color:blue;" align="center">Healthcare Claims Metric Builder</h1>
</div>

<!-- The menu links to the various readme sections. Make these whatever works for your project -->      
<p align="center">
  <a href="#about">About</a> •  
  <a href="#test-data">Test Data</a> •  
  <a href="#code">Code</a> •
  <a href="#credits">Credits</a> •
</p>


---
<!-- ABOUT --> 
<a name="about"></a>

## About
What will we do?
   1) Build Python code that creates metrics from medical and pharmacy claims.
   2) Deploy this code to a Lambda function
   3) Enable access through an API Gateway

<br/>

<!-- CONTAINER --> 
<a name="test-data"></a>

## Test Data
Test data consists of 9 randomly selected members and associated Facility (I), Professional (P), and Pharmacy (R) claims.  

| member\_id | claimtype | clm\_cnt | line\_cnt |
| :--- | :--- | :--- | :--- |
| mbr_01 | P | 1 | 3 |
| mbr_01 | R | 2 | 1 |
| mbr_01 | P | 8 | 2 |
| mbr_03 | I | 1 | 11 |
| mbr_03 | P | 15 | 2 |


*note:*
- The test data can be found here: lambda_project_dummy_data.json

<br/>

*partial example of lambda_project_dummy_data.json:*
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



<br/><br/>



<!-- Build Schema and Initialize --> 
<a name="code"></a>

## Code



<br/><br/>



<!-- CREDITS or ACKNOWLEDGEMENTS -->
<a name="credits"></a>

## Credits
Huge thank you to Rich King and Gary Cattabriga for their guidance through this project.                   			                          	    |
<br/><br/>
