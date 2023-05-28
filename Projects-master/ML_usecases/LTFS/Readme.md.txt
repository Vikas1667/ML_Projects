LTFS Top-up loan Up-sell prediction
A loan is when you receive the money from a financial institution in exchange for future repayment of the principal, plus interest. Financial institutions provide loans to the industries, corporates and individuals. The interest received on these loans is one among the main sources of income for the financial institutions.

A top-up loan, true to its name, is a facility of availing further funds on an existing loan. When you have a loan that has already been disbursed and under repayment and if you need more funds then, you can simply avail additional funding on the same loan thereby minimizing time, effort and cost related to applying again.

LTFS provides it’s loan services to its customers and is interested in selling more of its Top-up loan services to its existing customers so they have decided to identify when to pitch a Top-up during the original loan tenure.  If they correctly identify the most suitable time to offer a top-up, this will ultimately lead to more disbursals and can also help them beat competing offerings from other institutions.


To understand this behaviour, LTFS has provided data for its customers containing the information whether that particular customer took the Top-up service and when he took such Top-up service, represented by the target variable Top-up Month.



You are provided with two types of information: 



1. Customer’s Demographics: The demography table along with the target variable & demographic information contains variables related to Frequency of the loan, Tenure of the loan, Disbursal Amount for a loan & LTV.

2. Bureau data:  Bureau data contains the behavioural and transactional attributes of the customers like current balance, Loan Amount, Overdue etc. for various tradelines of a given customer

As a data scientist, LTFS  has tasked you with building a model given the Top-up loan bucket of 128655 customers along with demographic and bureau data, predict the right bucket/period for 14745 customers in the test data.

Important Note

Note that feasibility of implementation of top solutions in real production scenario will be considered while adjudging winners and can change the final standing for Prize Eligibility


Data Dictionary
Train_Data.zip 
This zip file contains the train files for demography data and bureau data. The data dictionary is also included here.

Test_Data.zip
This zip file contains information on demography data and bureau data for a different set of customers

Sample Submission
This file contains the exact submission format for the predictions. Please submit CSV file only.



Variable	Definition
ID	Unique Identifier for a row
Top-up Month	(Target) bucket/period for the Top-up Loan




How to Make a Submission?
All Submissions are to be done at the solution checker tab.
For a step by step view on how to make a submission check the below video





Evaluation
The evaluation metric for this competition is macro_f1_score across all entries in the test set.



Public and Private Split
Test data is further divided into Public 40% and Private 60%

Your initial responses will be checked and scored on the Public data.
The final rankings would be based on your private score which will be published once the competition is over.
 

Guidelines for Final Submission
Please ensure that your final submission includes the following:

Solution file containing the predicted Top-up Month bucket in the test dataset (format is given in sample submission CSV)
Code file containing the following:
Code: Note that it is mandatory to submit your code for a valid final submission
Approach: Please share your approach to solve the problem (doc/ppt/pdf format). It should cover the following topics:
A brief on the approach, which you have used to solve the problem.
What data-preprocessing / feature engineering ideas really worked? How did you discover them?
What does your final model look like? How did you reach it?
 

How to Set Final Submission?


Hackathon Rules
The final standings would be based on private leaderboard score and presentations made in Online Interview round with LTFS & Analytics Vidhya which will be held after contest close.
Setting the final submission is recommended. Without a final submission, the submission corresponding to best public score will be taken as the final submission
Use of external data is prohibited
You can only make 10 submissions per day
Entries submitted after the contest is closed, will not be considered
The code file pertaining to your final submission is mandatory while setting final submission
Throughout the hackathon, you are expected to respect fellow hackers and act with high integrity.
Analytics Vidhya and LTFS hold the right to disqualify any participant at any stage of the competition if the participant(s) are deemed to be acting fraudulently.
Use of multiple Login IDs will lead to immediate disqualification