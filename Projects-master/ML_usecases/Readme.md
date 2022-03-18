It will classic usecases with creative and abstractive workflows


## Building Permit Classification
Building Permit is task to classify Building type to accommodation of various sector.

Type of Building Permit 
SINGLE FAMILY / DUPLEX
COMMERCIAL
INSTITUTIONAL
MULTIFAMILY
INDUSTRIAL

Feature engineering
![image](Projects-master/ML_usecases/Building_Permit_Classification/featureclassify.jpeg)

# KMeans for Clustering Geospatial Locations
Missing values
![Missing value](Projects-master/ML_usecases/Building_Permit_Classification/insights/missing_count.png)

Categorical Distribution
![Categorical plot](Projects-master/ML_usecases/Building_Permit_Classification/insights/categorical_count.png)

Kmeans Clustering
![Kmeans](Projects-master/ML_usecases/Building_Permit_Classification/insights/kmeans_clustering.png)

DateTime Conversion 
./ML_usecases/Building_Permit_Classification/

Model Training 
As we have Text features so we use TFIDF with 20 features and 50 features 
and use catboost model for classification and shap to get insights
![catboost](Projects-master/ML_usecases/Building_Permit_Classification/insights/catboost_results.png)
![shap](Projects-master/ML_usecases/Building_Permit_Classification/insights/catboost_shap.png)

Finally Deep learning 
![Deep learning](Projects-master/ML_usecases/Building_Permit_Classification/Deep_learning_LSTM.png)

Evaluation metrics
![Evaluation](Projects-master/ML_usecases/Building_Permit_Classification/insights/ROC_AUC_Plot.JPG)


## Loan Top Up Prediction(Hackathon)

LTFS Top-up loan Up-sell prediction
A loan is when you receive the money from a financial institution in exchange for future repayment of the principal, plus interest. Financial institutions provide loans to the industries, corporates and individuals. The interest received on these loans is one among the main sources of income for the financial institutions.

A top-up loan, true to its name, is a facility of availing further funds on an existing loan. When you have a loan that has already been disbursed and under repayment and if you need more funds then, you can simply avail additional funding on the same loan thereby minimizing time, effort and cost related to applying again.

LTFS provides it’s loan services to its customers and is interested in selling more of its Top-up loan services to its existing customers so they have decided to identify when to pitch a Top-up during the original loan tenure.  If they correctly identify the most suitable time to offer a top-up, this will ultimately lead to more disbursals and can also help them beat competing offerings from other institutions.


To understand this behaviour, LTFS has provided data for its customers containing the information whether that particular customer took the Top-up service and when he took such Top-up service, represented by the target variable Top-up Month.
You are provided with two types of information: 

1. Customer’s Demographics: The demography table along with the target variable & demographic information contains variables related to Frequency of the loan, Tenure of the loan, Disbursal Amount for a loan & LTV.

2. Bureau data:  Bureau data contains the behavioural and transactional attributes of the customers like current balance, Loan Amount, Overdue etc. for various tradelines of a given customer

As a data scientist, LTFS  has tasked you with building a model given the Top-up loan bucket of 128655 customers along with demographic and bureau data, predict the right bucket/period for 14745 customers in the test data.

## Insurance claim Prediction


