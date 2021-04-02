## Feature Engineering libraries with Comparision
##### ref (https://towardsdatascience.com/practical-code-implementations-of-feature-engineering-for-machine-learning-with-python-f13b953d4bcd)
<ul>
  <li>Scikit-learn</br>
  <li>Feature-engine</br>
  <li>Category Encoders</br>
</ul>

![image1](images/different_python_fe_lib.jpg)
### Table 1: Feature engineering methods supported by the different Python libraries

### Table 2 below summarizes these key differences between the three packages.
![image2](images/pckg_diff_fe.jpg)


### Imputation
Imputation is the process of replacing missing data in a column, or variable, with a probable value estimated by other available information in the data set, typically within the same variable
<ul>
  <li>Mean/Median Imputation:Mean imputation can be implemented similarly by simply replacing “median” with “mean”</li>
  <li>Frequent Category Imputation:This method applies to categorical variables and replaces missing data with the most frequent category (i.e., the mode), identified in the             variables in the training set</li>
</ul>
### Table 3 below summarizes the techniques supported by each package and the main takeaways of their advantages and shortcomings.
![image3](images/imputation_tech.jpg)
### Table 3: Comparison of Imputation techniques supported by each Python library

### Categorical Variable Encoding
Machine learning models require input data in a numerical format, which necessitates categorically labelled variables to be converted to numerical values. 
![image1](images/categorical_encod.jpg)

![image1](images/categorical_encod_1.jpg)
![image1](images/discretization.jpg)
![image1](images/discretization_1.jpg)

