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
