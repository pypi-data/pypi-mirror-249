def preprocessing(data,target,drop_cols,label_encode=True,class_imbalance=False,classification = True):
    '''data            : DataFrame (for which you want to do preprocessing)
       target          : str (column name of the target)
       drop_cols       : List (list of columns which you want to drop)
       label_encode    : bool (True by default,False if you dont have the need of labeling the target)
       class_imbalance : bool (Fasle by defualt,True if there is class imbalance in target variable)
       classification: bool (True by default,False if it a non classification)
       
       
       Returns the data which is ready for model building
       if it is a regression problem then it return:
      x_train_con,x_test_con,y_train,y_test,new_cols,sc_1
      
       and if it is a classification problem and labels should be encoded then:
      x_train_con,x_test_con,y_train,y_test,new_cols,le
      
       and if it is a classification problem and the labels are already encoded then:
      x_train_con,x_test_con,y_train,y_test,new_cols'''
    
    
    print('============================DROPPING UNNECESSARY COLUMNS====================================')
    if len(drop_cols)!=0:
        print('Before dropping unnecessary columns:',data.shape)
        data.drop(drop_cols,axis=1,inplace=True)
    else:
        pass
    print('After dropping unnecessary columns:',data.shape)
    
    print('=================================DEALING WITH DATATYPES====================================')
    obj_cols = data.select_dtypes(('object','bool')).columns
    print('Object Columns:\n',obj_cols)
    if len(obj_cols)!=0:
        print('Before converting dtypes:\n',data.dtypes)
        data[obj_cols] = data[obj_cols].astype('category')
    else:
        pass
    print('After converting dtypes:\n',data.dtypes)
    
    print('==================================SPLITTING X and Y========================================')
    x = data.drop(target,axis=1)
    print('x shape:',x.shape)
    y = data[target]
    print('y shape:',y.shape)
    cat_attr = x.select_dtypes(('category','bool')).columns
    print('cat_attr \n{}'.format(cat_attr))
    num_attr = x.select_dtypes(('int','float')).columns
    print('num_attr \n{}'.format(num_attr))
    
    print('=========================SPLITTING DATA AS TRAINING and TESTING=============================')
    from sklearn.model_selection import train_test_split
    if y.dtypes=='category':
        x_train , x_test , y_train , y_test = train_test_split(x,y,test_size=0.2,random_state=123,stratify=y)
    else:
        x_train , x_test , y_train , y_test = train_test_split(x,y,test_size=0.2,random_state=123)
    print('x_train',x_train.shape)
    print('x_test',x_test.shape)
    print('y_train',y_train.shape)
    print('y_test',y_test.shape)
    
    print('==============================IMPUTING NULL VALUES====================================')
    from sklearn.impute import SimpleImputer
    if (x[cat_attr].isna().sum()).sum != 0 and len(cat_attr)!=0:
        print('Before imputing Nan values for x_train\n',x_train.isna().sum())
        print('Before imputing Nan values for x_test\n',x_test.isna().sum())
        print('Before imputing Nan values for y_train\n',y_train.isna().sum())
        print('Before imputing Nan values for y_test\n',y_test.isna().sum())
        si_cat = SimpleImputer(strategy='most_frequent')
        si_cat.fit(x_train[cat_attr])
        x_train[cat_attr] = si_cat.transform(x_train[cat_attr])
        x_test[cat_attr] = si_cat.transform(x_test[cat_attr])
    else:
        pass
    if (x[num_attr].isna().sum()).sum !=0 and len(num_attr)!=0:
        si_num = SimpleImputer(strategy='median')
        si_num.fit(x_train[num_attr])
        x_train[num_attr] = si_num.transform(x_train[num_attr])
        x_test[num_attr] = si_num.transform(x_test[num_attr])
    else:
        pass
    if y.isna().sum() != 0:
        if y.dtype=='category':
            si_cat_y = SimpleImputer(strategy='most_frequent')
            y_train = si_cat_y.transform(y_train)
            y_test = si_cat_y.transform(y_test)
        else:
            si_num_y = SimpleImputer(strategy='median')
            y_train = si_num_y.transform(y_train)
            y_test = si_num_y.transform(y_test)
    else:
        pass
    print('After imputing Nan values for x_train\n',x_train.isna().sum())
    print('After imputing Nan values for x_test\n',x_test.isna().sum())
    print('After imputing Nan values for y_train\n',y_train.isna().sum())
    print('After imputing Nan values for y_test\n',y_test.isna().sum())
          
    print('=====================================ONEHOTENCODING=====================================')
    if len(cat_attr)!=0:
        from sklearn.preprocessing import OneHotEncoder
        ohe = OneHotEncoder(handle_unknown='ignore',drop='first')
        ohe.fit(x_train[cat_attr])
        ohe_cols = ohe.get_feature_names_out()
        x_train_ohe = ohe.transform(x_train[cat_attr]).toarray()
        x_test_ohe = ohe.transform(x_test[cat_attr]).toarray()
    else:
        pass
    
    print('======================================SCALING===========================================')
    if len(num_attr)!=0:
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        sc.fit(x_train[num_attr])
        x_train[num_attr] = sc.transform(x_train[num_attr])
        x_test[num_attr] = sc.transform(x_test[num_attr])
    else:
        pass
    if classification==False:
        from sklearn.preprocessing import StandardScaler
        sc_1 = StandardScaler()
        sc_1.fit(y_train.to_numpy().reshape(-1,1))
        y_train = sc_1.transform(y_train.to_numpy().reshape(-1,1))
        y_test = sc_1.transform(y_test.to_numpy().reshape(-1,1))
    else:
        pass
    
    if label_encode == True:
        print('====================================LABELENCODING===================================')
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        le.fit(y_train)
        y_train = le.transform(y_train)
        y_test = le.transform(y_test)
    else:
        pass
    
    print('=======================CONCATENATING SCLAED AND ENCODED DATA===============================')
    if len(cat_attr)!=0:
        import numpy as np
        x_train_con = np.concatenate((x_train_ohe,x_train[num_attr]),axis=1)
        x_test_con = np.concatenate((x_test_ohe,x_test[num_attr]),axis=1)
        new_cols = np.concatenate((ohe_cols,num_attr),axis=0)
    else:
        import numpy as np
        x_train_con = x_train
        x_test_con = x_test
        new_cols = np.concatenate((cat_attr,num_attr),axis=0)
    if class_imbalance==True:
        from imblearn.over_sampling import SMOTE
        sm=SMOTE(random_state=123)
        x_train_sm,y_train_sm = sm.fit_resample(x_train_con,y_train)
    else:
        x_train_sm = x_train_con
        y_train_sm = y_train
    
    if classification == False:
        return x_train_sm,x_test_con,y_train_sm,y_test,new_cols,sc_1
    elif classification == True and label_encode == True:
        return x_train_sm,x_test_con,y_train_sm,y_test,new_cols,le
    elif classification == True and label_encode == False:
        return x_train_sm,x_test_con,y_train_sm,y_test,new_cols







def regression_model_building(x_train,x_test,y_train,y_test):
    '''x_train   : array of independent feature of train set
       x_test    : array of independent feature of test set
       y_train   : array of dependent feature of train set
       y_test    : array of dependent feature of test set
       
       
       Returns a DataFrame Metrics for every regression model available in sklearn
       error_df'''
    
    import warnings
    warnings.filterwarnings('ignore')
    import pandas as pd
    import numpy as np
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.svm import SVR
    from sklearn.linear_model import LinearRegression
    from xgboost import XGBRegressor
    from sklearn.ensemble import AdaBoostRegressor
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score,mean_absolute_percentage_error
    
    def reg_metrics(train_actual,train_predict,test_actual,test_predict):
        
        n=train_actual.shape[0]
        k=train_actual.shape[1]
        train =[mean_squared_error(train_actual,train_predict,squared=False),
                mean_squared_error(train_actual,train_predict),
                 mean_squared_error(train_actual,train_predict),
                  mean_absolute_percentage_error(train_actual,train_predict),
                    1 - (1-r2_score(train_actual,train_predict))*(n-1)/(n-k-1)]

        n_1=test_actual.shape[0]
        k_1=test_actual.shape[1]
        test = [mean_squared_error(test_actual,test_predict,squared=False),
                mean_squared_error(test_actual,test_predict),
                  mean_absolute_error(test_actual,test_predict),
                    mean_absolute_percentage_error(test_actual,test_predict),
                     1 - (1-r2_score(test_actual,test_predict))*(n_1-1)/(n_1-k_1-1)]
        return train,test
    
    models = [GradientBoostingRegressor,AdaBoostRegressor,XGBRegressor,
             SVR,RandomForestRegressor,LinearRegression,KNeighborsRegressor,DecisionTreeRegressor]
    error_list = []
    for i in models:
        reg = i()
        reg.fit(x_train,y_train)
        y_pred_train = reg.predict(x_train)
        y_pred_test = reg.predict(x_test)
        train,test = reg_metrics(train_actual=y_train,train_predict=y_pred_train,\
                   test_actual=y_test,test_predict=y_pred_test)
        error_list.append(train)
        error_list.append(test)
    models_index = ['GradientBoosting_Train','GradientBoosting_Test','AdaBoost_Train','AdaBoost_Test',
                'XGBoost_Train','XGBoost_Test','SVR_Train','SVR_Test','RandomForest_Train','RandomForest_Test',
                   'LinearRegression_Train','LinearRegression_Test','KNeighbors_Train','KNeighbors_Test',
                   'DecisionTree_Train','DecisionTree_Test']
    columns_list = ['Root_mean_squared_error','Mean_squared_error','Mean_absolute_error',
                   'Mean_absolute_percentage_error','Adjusted_R2_score']
    error_df = pd.DataFrame(error_list,index=models_index,columns=columns_list)
    return error_df.T




def classification_model_building(x_train,x_test,y_train,y_test):
    '''x_train   : array of independent feature of train set
       x_test    : array of independent feature of test set
       y_train   : array of dependent feature of train set
       y_test    : array of dependent feature of test set
       
       Returns a DataFrame Metrics for every regression model available in sklearn
       error_df'''
    
    import warnings
    warnings.filterwarnings('ignore')
    import pandas as pd
    import numpy as np
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.linear_model import LogisticRegression
    from xgboost import XGBClassifier
    from sklearn.ensemble import AdaBoostClassifier
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.metrics import accuracy_score,recall_score,precision_score,f1_score
    
    if len(np.unique(y_train))>2:
        def error_metrics(train_actual_data,train_pred_data,test_actual_data,test_pred_data):
            train_list=[accuracy_score(train_actual_data,train_pred_data),
                    recall_score(train_actual_data,train_pred_data,average='weighted'),
                    precision_score(train_actual_data, train_pred_data,average='weighted'),
                    f1_score(train_actual_data,train_pred_data,average='weighted')]
            test_list=[accuracy_score(test_actual_data, test_pred_data),
                   recall_score(test_actual_data, test_pred_data,average='weighted'),
                   precision_score(test_actual_data, test_pred_data,average='weighted'),
                   f1_score(test_actual_data,test_pred_data,average='weighted')]
            return train_list , test_list
    else:
        def error_metrics(train_actual_data,train_pred_data,test_actual_data,test_pred_data):
            train_list=[accuracy_score(train_actual_data,train_pred_data),
                    recall_score(train_actual_data,train_pred_data),
                    precision_score(train_actual_data, train_pred_data),
                    f1_score(train_actual_data,train_pred_data)]
            test_list=[accuracy_score(test_actual_data, test_pred_data),
                   recall_score(test_actual_data, test_pred_data),
                   precision_score(test_actual_data, test_pred_data),
                   f1_score(test_actual_data,test_pred_data)]
            return train_list , test_list

    models = [DecisionTreeClassifier,RandomForestClassifier,KNeighborsClassifier,
             SVC,LogisticRegression,XGBClassifier,AdaBoostClassifier,GradientBoostingClassifier]
    error_list = []
    for i in models:
        clf = i()
        clf.fit(x_train,y_train)
        y_pred_train = clf.predict(x_train)
        y_pred_test = clf.predict(x_test)
        train_list,test_list = error_metrics(train_actual_data=y_train,train_pred_data=y_pred_train,
                      test_actual_data=y_test,test_pred_data=y_pred_test)
        error_list.append(train_list)
        error_list.append(test_list)
    models_index=['DecisionTree_Train','DecisionTree_Test','RandomForest_Train','RandomForest_Test',
                  'KNeighbors_Train','KNeighbors_Test','SVC_Train','SVC_Test',
                  'LogisticRegression_Train','LogisticRegression_Test','XGBClassifier_Train',
                  'XGBClassifier_Test',
                    'AdaBoostClassifier_Train','AdaBoostClassifier_Test',
                   'GradientBoostingClassifier_Train','GradientBoostingClassifier_Test']
    columns_list = ['Accuracy score','Recall score','Precision score','F1 Score']
    error_df = pd.DataFrame(error_list,columns=columns_list,index = models_index)
    return error_df.T





def clf_metrics(train_actual,train_predict,test_actual,test_predict):
    '''train_actual   : array of actual training data
       train_predict  : array of predicted training data
       test_actual    : array of actual testing data
       test_predict   : array of predicted testing data
       
       Returns the metrics for Classification such as Accuracy,Recall,Precision,F1 Score'''
    from sklearn.metrics import accuracy_score,recall_score,precision_score,f1_score
    import numpy as np
    if len(np.unique(train_actual))>2 and len(np.unique(test_actual))>2:
        print('*******METRICS FOR TRAINING DATA********')
        print('Accuracy score:\n',accuracy_score(train_actual,train_predict))
        print('Recall score:\n',recall_score(train_actual,train_predict,average='weighted'))
        print('Precision score:\n',precision_score(train_actual,train_predict,average='weighted'))
        print('F1 Score:\n',f1_score(train_actual,train_predict,average='weighted'))
        print('*******METRICS FOR TESTING DATA*******')
        print('Accuracy score:\n',accuracy_score(test_actual,test_predict))
        print('Recall score:\n',recall_score(test_actual,test_predict,average='weighted'))
        print('Precision score:\n',precision_score(test_actual,test_predict,average='weighted'))
        print('F1 Score:\n',f1_score(test_actual,test_predict,average='weighted'))
    else:
        print('*******METRICS FOR TRAINING DATA********')
        print('Accuracy score:\n',accuracy_score(train_actual,train_predict))
        print('Recall score:\n',recall_score(train_actual,train_predict))
        print('Precision score:\n',precision_score(train_actual,train_predict))
        print('F1 Score:\n',f1_score(train_actual,train_predict))
        print('*******METRICS FOR TESTING DATA*******')
        print('Accuracy score:\n',accuracy_score(test_actual,test_predict))
        print('Recall score:\n',recall_score(test_actual,test_predict))
        print('Precision score:\n',precision_score(test_actual,test_predict))
        print('F1 Score:\n',f1_score(test_actual,test_predict))



def reg_metrics(train_actual,train_predict,test_actual,test_predict):
    '''train_actual   : array of actual training data
       train_predict  : array of predicted training data
       test_actual    : array of actual testing data
       test_predict   : array of predicted testing data
       
       Returns the metrics for Regression such as MSE,RMSE,MAE,MAPE,R2 Score'''
    
    from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score,mean_absolute_percentage_error
    from sklearn.metrics import r2_score
    n=train_actual.shape[0]
    k=train_actual.shape[1]
    print('*******METRICS FOR TRAINING DATA********')
    print('Root_Mean_Squared_Srror       \t',mean_squared_error(train_actual,train_predict,squared=False))
    print('Mean_Squared_Error            \t',mean_squared_error(train_actual,train_predict))
    print('Mean_Absolute_Error           \t',mean_absolute_error(train_actual,train_predict))
    print('Mean_Absolute_Percentage_Error\t',mean_absolute_percentage_error(train_actual,train_predict))
    print('Adjusted_R2_Score:            \t',1 - (1-r2_score(train_actual,train_predict))*(n-1)/(n-k-1))
    print('\n')
    n_1=test_actual.shape[0]
    k_1=test_actual.shape[1]
    print('*******METRICS FOR TESTING DATA*******')
    print('Root_Mean_Squared_Srror       \t',mean_squared_error(test_actual,test_predict,squared=False))
    print('Mean_Squared_Error            \t',mean_squared_error(test_actual,test_predict))
    print('Mean_Absolute_Error           \t',mean_absolute_error(test_actual,test_predict))
    print('Mean_Absolute_Percentage_Error\t',mean_absolute_percentage_error(test_actual,test_predict))
    print('Adjusted_R2_Score             \t',1 - (1-r2_score(test_actual,test_predict))*(n_1-1)/(n_1-k_1-1))






def preprocessing_final(data,test_data,target,drop_cols,class_imbalance=False,label_encode=True,classification = True):
    '''data            : DataFrame (for which you want to do preprocessing)
       test_data       : Test DataFrame
       target          : str (column name of the target)
       drop_cols       : List (list of columns which you want to drop)
       class_imbalance : bool (False by default,True if there is class imblanace in target feature)
       label_encode    : bool (True by default,False if you dont have the need of labeling the target)
       classification  : bool (True by default,False if it a non classification)
       
       
       Returns the data which is ready for model building
       if it is a regression problem then it return:
      x_train_con,x_test_con,y_train,y_test,final_test,new_cols,sc_1
      
       and if it is a classification problem and labels should be encoded then:
      x_train_con,x_test_con,y_train,y_test,final_test,new_cols,le
      
       and if it is a classification problem and the labels are already encoded then:
      x_train_con,x_test_con,y_train,y_test,final_test,new_cols'''
    
    print('============================DROPPING UNNECESSARY COLUMNS====================================')
    if len(drop_cols)!=0:
        print('Before dropping unnecessary columns:',data.shape)
        data.drop(drop_cols,axis=1,inplace=True)
    else:
        pass
    print('After dropping unnecessary columns:',data.shape)
    
    print('=================================DEALING WITH DATATYPES====================================')
    obj_cols = data.select_dtypes(('object','bool')).columns
    print('Object Columns:\n',obj_cols)
    if len(obj_cols)!=0:
        print('Before converting dtypes:\n',data.dtypes)
        data[obj_cols] = data[obj_cols].astype('category')
    else:
        pass
    print('After converting dtypes:\n',data.dtypes)
    
    print('==================================SPLITTING X and Y========================================')
    x = data.drop(target,axis=1)
    print('x shape:',x.shape)
    y = data[target]
    print('y shape:',y.shape)
    cat_attr = x.select_dtypes(('category','bool')).columns
    print('cat_attr \n{}'.format(cat_attr))
    num_attr = x.select_dtypes(('int','float')).columns
    print('num_attr \n{}'.format(num_attr))
    
    print('=========================SPLITTING DATA AS TRAINING and TESTING=============================')
    from sklearn.model_selection import train_test_split
    if y.dtypes=='category':
        x_train , x_test , y_train , y_test = train_test_split(x,y,test_size=0.2
                                                               ,random_state=123,stratify=y)
    else:
        x_train , x_test , y_train , y_test = train_test_split(x,y,test_size=0.2,random_state=123)
    print('x_train',x_train.shape)
    print('x_test',x_test.shape)
    print('y_train',y_train.shape)
    print('y_test',y_test.shape)
    
    print('==============================IMPUTING NULL VALUES====================================')
    from sklearn.impute import SimpleImputer
    from sklearn.impute import KNNImputer
    if (x[cat_attr].isna().sum()).sum != 0 and len(cat_attr)!=0:
        print('Before imputing Nan values for x_train\n',x_train.isna().sum())
        print('Before imputing Nan values for x_test\n',x_test.isna().sum())
        print('Before imputing Nan values for y_train\n',y_train.isna().sum())
        print('Before imputing Nan values for y_test\n',y_test.isna().sum())
        si_cat = SimpleImputer(strategy='most_frequent')
        si_cat.fit(x_train[cat_attr])
        x_train[cat_attr] = si_cat.transform(x_train[cat_attr])
        x_test[cat_attr] = si_cat.transform(x_test[cat_attr])
    else:
        pass
    if (x[num_attr].isna().sum()).sum !=0 and len(num_attr)!=0:
        Knn_num = KNNImputer()
        Knn_num.fit(x_train[num_attr])
        x_train[num_attr] = Knn_num.transform(x_train[num_attr])
        x_test[num_attr] = Knn_num.transform(x_test[num_attr])
    else:
        pass
    if y.isna().sum() != 0:
        if y.dtype=='category':
            si_cat_y = SimpleImputer(strategy='most_frequent')
            y_train = si_cat_y.transform(y_train)
            y_test = si_cat_y.transform(y_test)
        else:
            si_num_y = SimpleImputer(strategy='median')
            y_train = si_num_y.transform(y_train)
            y_test = si_num_y.transform(y_test)
    else:
        pass
    print('After imputing Nan values for x_train\n',x_train.isna().sum())
    print('After imputing Nan values for x_test\n',x_test.isna().sum())
    print('After imputing Nan values for y_train\n',y_train.isna().sum())
    print('After imputing Nan values for y_test\n',y_test.isna().sum())
          
    print('=====================================ONEHOTENCODING=====================================')
    if len(cat_attr)!=0:
        from sklearn.preprocessing import OneHotEncoder
        ohe = OneHotEncoder(handle_unknown='ignore',drop='first')
        ohe.fit(x_train[cat_attr])
        ohe_cols = ohe.get_feature_names_out()
        x_train_ohe = ohe.transform(x_train[cat_attr]).toarray()
        x_test_ohe = ohe.transform(x_test[cat_attr]).toarray()
    else:
        pass
    
    print('======================================SCALING===========================================')
    if len(num_attr)!=0:
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        sc.fit(x_train[num_attr])
        x_train[num_attr] = sc.transform(x_train[num_attr])
        x_test[num_attr] = sc.transform(x_test[num_attr])
    else:
        pass
    if classification==False:
        from sklearn.preprocessing import StandardScaler
        sc_1 = StandardScaler()
        sc_1.fit(y_train.to_numpy().reshape(-1,1))
        y_train = sc_1.transform(y_train.to_numpy().reshape(-1,1))
        y_test = sc_1.transform(y_test.to_numpy().reshape(-1,1))
    else:
        pass
    
    if label_encode == True:
        print('====================================LABELENCODING===================================')
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        le.fit(y_train)
        y_train = le.transform(y_train)
        y_test = le.transform(y_test)
    else:
        pass
    
    print('=======================CONCATENATING SCLAED AND ENCODED DATA===============================')
    if len(cat_attr)!=0:
        import numpy as np
        x_train_con = np.concatenate((x_train_ohe,x_train[num_attr]),axis=1)
        x_test_con = np.concatenate((x_test_ohe,x_test[num_attr]),axis=1)
    else:
        x_train_con = x_train
        x_test_con = x_test
    
    print('===================================TESTING DATA=========================================')
    
    print('============================DROPPING UNNECESSARY COLUMNS====================================')
    print('Before dropping unnecessary columns from Test Data:',test_data.shape)
    if len(drop_cols)!=0:
        test_data.drop(drop_cols,axis=1,inplace=True)
    else:
        pass
    print('After dropping unnecessary columns from Test Data:',test_data.shape)
    print('=================================DEALING WITH DATATYPES====================================')
    obj_cols_test = test_data.select_dtypes(('object','bool')).columns
    print('Object Columns:\n',obj_cols_test)
    if len(obj_cols_test)!=0:
        print('Before converting dtypes from Test Data:\n',test_data.dtypes)
        test_data[obj_cols_test] = test_data[obj_cols_test].astype('category')
    else:
        pass
    print('After converting dtypes from Test Data:\n',test_data.dtypes)
    
    print('==============================IMPUTING NULL VALUES====================================')
    
    from sklearn.impute import SimpleImputer
    from sklearn.impute import KNNImputer
    print('Before imputing Nan values for Test Data \n',test_data.isna().sum())
    if (test_data[cat_attr].isna().sum()).sum != 0 and len(cat_attr)!=0:
        test_data[cat_attr] = si_cat.transform(test_data[cat_attr])
    else:
        pass
    if (test_data[num_attr].isna().sum()).sum !=0 and len(num_attr)!=0:
        test_data[num_attr] = Knn_num.transform(test_data[num_attr])
    else:
        pass
    print('After imputing Nan values for Test Data\n',test_data.isna().sum())
    
    print('=====================================ONEHOTENCODING=====================================')
    
    if len(cat_attr)!=0:
        test_ohe = ohe.transform(test_data[cat_attr]).toarray()
    else:
        pass
    
    print('======================================SCALING===========================================')
    
    if len(num_attr)!=0:
        test_data[num_attr] = sc.transform(test_data[num_attr])
    else:
        pass
    
    print('=======================CONCATENATING SCLAED AND ENCODED DATA===============================')
    if len(cat_attr)!=0:
        import numpy as np
        final_test = np.concatenate((test_ohe,test_data[num_attr]),axis=1)
    else:
        final_test = test_data
    import numpy as np    
    if len(cat_attr)!=0:
        new_cols = np.concatenate((ohe_cols,num_attr),axis=0)
    else:
        new_cols = np.concatenate((cat_attr,num_attr),axis=0) 
        
    if class_imbalance==True:
        from imblearn.over_sampling import SMOTE
        sm=SMOTE(random_state=123)
        x_train_sm,y_train_sm = sm.fit_resample(x_train_con,y_train)
    else:
        x_train_sm = x_train_con
        y_train_sm = y_train
        
    if classification == False:
        return x_train_sm,x_test_con,y_train_sm,y_test,final_test,new_cols,sc_1
    elif classification == True and label_encode == True:
        return x_train_sm,x_test_con,y_train_sm,y_test,final_test,new_cols,le
    elif classification == True and label_encode == False:
        return x_train_sm,x_test_con,y_train_sm,y_test,final_test,new_cols





def classification_model_building_final(x_train,x_test,y_train,y_test,final_test):
    '''x_train   : array of independent feature of train set
       x_test    : array of independent feature of test set
       y_train   : array of dependent feature of train set
       y_test    : array of dependent feature of test set
       
       Returns a DataFrame Metrics for every regression model available in sklearn and 
       the predicitons on the final test data as
       error_df,pred_df'''
    
    
    import warnings
    warnings.filterwarnings('ignore')
    import pandas as pd
    import numpy as np
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.linear_model import LogisticRegression
    from xgboost import XGBClassifier
    from sklearn.ensemble import AdaBoostClassifier
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.metrics import accuracy_score,recall_score,precision_score,f1_score
    
    if len(np.unique(y_train))>2:
        def error_metrics(train_actual_data,train_pred_data,test_actual_data,test_pred_data):
            train_list=[accuracy_score(train_actual_data,train_pred_data),
                    recall_score(train_actual_data,train_pred_data,average='weighted'),
                    precision_score(train_actual_data, train_pred_data,average='weighted'),
                    f1_score(train_actual_data,train_pred_data,average='weighted')]
            test_list=[accuracy_score(test_actual_data, test_pred_data),
                   recall_score(test_actual_data, test_pred_data,average='weighted'),
                   precision_score(test_actual_data, test_pred_data,average='weighted'),
                   f1_score(test_actual_data,test_pred_data,average='weighted')]
            return train_list , test_list
    else:
        def error_metrics(train_actual_data,train_pred_data,test_actual_data,test_pred_data):
            train_list=[accuracy_score(train_actual_data,train_pred_data),
                    recall_score(train_actual_data,train_pred_data),
                    precision_score(train_actual_data, train_pred_data),
                    f1_score(train_actual_data,train_pred_data)]
            test_list=[accuracy_score(test_actual_data, test_pred_data),
                   recall_score(test_actual_data, test_pred_data),
                   precision_score(test_actual_data, test_pred_data),
                   f1_score(test_actual_data,test_pred_data)]
            return train_list , test_list

    models = [DecisionTreeClassifier,RandomForestClassifier,KNeighborsClassifier,
             SVC,LogisticRegression,XGBClassifier,AdaBoostClassifier,GradientBoostingClassifier]
    error_list = []
    pred_list = []
    for i in models:
        clf = i()
        clf.fit(x_train,y_train)
        y_pred_train = clf.predict(x_train)
        y_pred_test = clf.predict(x_test)
        y_pred_final = clf.predict(final_test)
        train_list,test_list = error_metrics(train_actual_data=y_train,train_pred_data=y_pred_train,
                      test_actual_data=y_test,test_pred_data=y_pred_test)
        pred_list.append(y_pred_final)
        error_list.append(train_list)
        error_list.append(test_list)
    models_index=['DecisionTree_Train','DecisionTree_Test','RandomForest_Train','RandomForest_Test',
                  'KNeighbors_Train','KNeighbors_Test','SVC_Train','SVC_Test',
                  'LogisticRegression_Train','LogisticRegression_Test','XGBClassifier_Train',
                  'XGBClassifier_Test',
                    'AdaBoostClassifier_Train','AdaBoostClassifier_Test',
                   'GradientBoostingClassifier_Train','GradientBoostingClassifier_Test']
    columns_list = ['Accuracy score','Recall score','Precision score','F1 Score']
    error_df = pd.DataFrame(error_list,columns=columns_list,index = models_index)
    pred_df = pd.DataFrame(pred_list,index = ['DecisionTreeClassifier','RandomForestClassifier',
                                              'KNeighborsClassifier',
             'SVC','LogisticRegression','XGBClassifier','AdaBoostClassifier','GradientBoostingClassifier'])
    return error_df.T,pred_df.T








def regression_model_building_final(x_train,x_test,y_train,y_test,final_test):
    
    '''x_train   : array of independent feature of train set
       x_test    : array of independent feature of test set
       y_train   : array of dependent feature of train set
       y_test    : array of dependent feature of test set
       Returns a DataFrame Metrics for every regression model available in sklearn and
       predicitons on the test data as
       error_df,pred_df'''
    import warnings
    warnings.filterwarnings('ignore')
    import pandas as pd
    import numpy as np
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.svm import SVR
    from sklearn.linear_model import LinearRegression
    from xgboost import XGBRegressor
    from sklearn.ensemble import AdaBoostRegressor
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score,mean_absolute_percentage_error
    
    def reg_metrics(train_actual,train_predict,test_actual,test_predict):
        n=train_actual.shape[0]
        k=train_actual.shape[1]
        train =[mean_squared_error(train_actual,train_predict,squared=False),
                mean_squared_error(train_actual,train_predict),
                 mean_squared_error(train_actual,train_predict),
                  mean_absolute_percentage_error(train_actual,train_predict),
                    1 - (1-r2_score(train_actual,train_predict))*(n-1)/(n-k-1)]
        n_1=test_actual.shape[0]
        k_1=test_actual.shape[1]
        test = [mean_squared_error(test_actual,test_predict,squared=False),
                mean_squared_error(test_actual,test_predict),
                  mean_absolute_error(test_actual,test_predict),
                    mean_absolute_percentage_error(test_actual,test_predict),
                     1 - (1-r2_score(test_actual,test_predict))*(n_1-1)/(n_1-k_1-1)]
        return train,test
    models = [GradientBoostingRegressor,AdaBoostRegressor,XGBRegressor,
             SVR,RandomForestRegressor,LinearRegression,KNeighborsRegressor,DecisionTreeRegressor]
    error_list = []
    pred_list = []
    for i in models:
        reg = i()
        reg.fit(x_train,y_train)
        y_pred_train = reg.predict(x_train)
        y_pred_test = reg.predict(x_test)
        y_pred_final = reg.predict(final_test)
        train,test = reg_metrics(train_actual=y_train,train_predict=y_pred_train,\
                   test_actual=y_test,test_predict=y_pred_test)
        pred_list.append(y_pred_final)
        error_list.append(train)
        error_list.append(test)
    models_index = ['GradientBoosting_Train','GradientBoosting_Test','AdaBoost_Train','AdaBoost_Test',
                'XGBoost_Train','XGBoost_Test','SVR_Train','SVR_Test','RandomForest_Train','RandomForest_Test',
                   'LinearRegression_Train','LinearRegression_Test','KNeighbors_Train','KNeighbors_Test',
                   'DecisionTree_Train','DecisionTree_Test']
    columns_list = ['Root_Mean_Squared_Error','Mean_Squared_Error','Mean_Absolute_Error',
                   'Mean_Absolute_Percentage_Error','Adjusted_R2_score']
    error_df = pd.DataFrame(error_list,index=models_index,columns=columns_list)
    pred_df = pd.DataFrame(pred_list,index=['GradientBoostingRegressor','AdaBoostRegressor','XGBRegressor',
             'SVR','RandomForestRegressor','LinearRegression','KNeighborsRegressor','DecisionTreeRegressor'])
    return error_df.T,pred_df.T






def feature_imp(x_train_con,y_train,new_cols,classification=True):
    '''x_train_con     :  array of clean training data
       y_train         :  array of target feature
       new_cols        :  total columns generated after preprocessing
       classification  :  bool(Default is True,If its a regression problem then its False
     
    Returns the important features wise plot and also feature names
    imp_cols,cols_indices'''
    from sklearn.ensemble import RandomForestClassifier,RandomForestRegressor
    import plotly.express as px
    import matplotlib.pyplot as plt
    import numpy as np
    if classification==True:    
        clf = RandomForestClassifier(random_state=123)
        clf.fit(x_train_con,y_train)
        importances = clf.feature_importances_
        indices = np.argsort(importances)[::-1]
        if len(new_cols)>30:
            plt.figure(figsize=(15,15))
            fig = px.bar(y=importances[indices],color=new_cols,template = 'plotly_dark')
            fig.show()
        else:
            plt.figure(figsize=(15,15))
            fig = px.bar(x=new_cols[indices],y=importances[indices],color=new_cols,template = 'plotly_dark')
            fig.show()
        return new_cols[indices],indices
    else:
        reg = RandomForestRegressor(random_state=123)
        reg.fit(x_train_con,y_train)
        importances = reg.feature_importances_
        indices = np.argsort(importances)[::-1]
        if len(new_cols)>30:
            plt.figure(figsize=(15,15))
            fig = px.bar(y=importances[indices],color=new_cols,template = 'plotly_dark')
            fig.show()
        else:
            plt.figure(figsize=(15,15))
            fig = px.bar(x=new_cols[indices],y=importances[indices],color=new_cols,template = 'plotly_dark')
            fig.show()
        return new_cols[indices],indices







def pca(x_train_con,x_test_con,new_cols):
    '''x_train_con : array of pre-processed training data
       x_test_con  : array of pre-processed testing data
       new_cols    : features names after preprocessing part
       
       Returns the transformed data 
       x_train_pca,x_test_pca'''
    from sklearn.decomposition import PCA
    import matplotlib.pyplot as plt
    import seaborn as sns 
    import numpy as np
    
    principal_components = PCA()
    x_train_pca = principal_components.fit_transform(x_train_con)
    x_test_pca = principal_components.transform(x_test_con)
    
    if len(new_cols)>=30:
        plt.figure(figsize=(15,15))
        sns.set_style('white')
        plt.plot(np.cumsum(principal_components.explained_variance_ratio_))
        plt.xticks(rotation='vertical')
        plt.xlabel('Principal Components',color='black')
        plt.ylabel('% of Variance Explained',color='black')
        plt.show()

    else:
        plt.figure(figsize=(15,15))
        sns.set_style('white')
        sns.lineplot(y=np.cumsum(principal_components.explained_variance_ratio_),x=new_cols)
        plt.xticks(rotation='vertical')
        plt.xlabel('Principal Components',color='black')
        plt.ylabel('% of Variance Explained',color='black')
        plt.show()
        
    return x_train_pca,x_test_pca









def pca_final(x_train_con,x_test_con,final_test,new_cols):
    '''x_train_con : array of pre-processed training data
       x_test_con  : array of pre-processed testing data
       final_test  : array of final testing data
       new_cols    : features names after preprocessing part
       
       Returns the transformed data 
       x_train_pca,x_test_pca,final_test_pca'''
    from sklearn.decomposition import PCA
    import matplotlib.pyplot as plt
    import seaborn as sns 
    import numpy as np
    
    principal_components = PCA()
    x_train_pca = principal_components.fit_transform(x_train_con)
    x_test_pca = principal_components.transform(x_test_con)
    final_test_pca = principal_components.transform(final_test)
    
    if len(new_cols)>=30:
        plt.figure(figsize=(15,15))
        sns.set_style('white')
        plt.plot(np.cumsum(principal_components.explained_variance_ratio_))
        plt.xticks(rotation='vertical')
        plt.show()

    else:
        plt.figure(figsize=(15,15))
        sns.set_style('white')
        sns.lineplot(y=np.cumsum(principal_components.explained_variance_ratio_),x=new_cols)
        plt.xticks(rotation='vertical')
        plt.show()
    return x_train_pca,x_test_pca,final_test_pca


class uni_plot:
    '''uni_plot is a class with two function objects
       .num and .cat'''
        
    def num(df,col=None,log_transform=False):
        '''df             :  DataFrame.
           log_transform  :  False is the default,True if you want
                              to do log transformation on feature.
           Displays the Kdeplot and the boxplot for every
           numerical feature in given Dataframe(df)'''
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np
        if col == None:
            num_cols = df.select_dtypes(('int','float'))
            for i in num_cols:
                if log_transform == False:
                    plt.figure(figsize=(15,15))
                    sns.set_style('whitegrid')
                    plt.subplot(221)
                    sns.kdeplot(df[i])
                    plt.subplot(222)
                    sns.boxplot(y=df[i])
                    plt.show()
                else:
                    plt.figure(figsize=(15,15))
                    sns.set_style('whitegrid')
                    plt.subplot(221)
                    sns.kdeplot(np.log(df[i]))
                    plt.subplot(222)
                    sns.boxplot(y=np.log(df[i]))
                    plt.show()
        else:
            if log_transform == False:
                    plt.figure(figsize=(15,15))
                    sns.set_style('whitegrid')
                    plt.subplot(221)
                    sns.kdeplot(df[col])
                    plt.subplot(222)
                    sns.boxplot(y=df[col])
                    plt.show()
            else:
                    plt.figure(figsize=(15,15))
                    sns.set_style('whitegrid')
                    plt.subplot(221)
                    sns.kdeplot(np.log(df[col]))
                    plt.subplot(222)
                    sns.boxplot(y=np.log(df[col]))
                    plt.show()
            
    def cat(df,col=None,pie='on'):
        '''df  :  DataFrame
           col :  Column Name
           pie :  Default is 'on','off' if you don't want to view pie chart
           Displays the counplot and the pie chart for every
           categorical feature in given Dataframe(df)'''
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np
        import warnings
        warnings.filterwarnings('ignore')
        if col == None:
            cat_cols = df.select_dtypes(('category','bool','object'))
            if pie=='on':
                for i in cat_cols:
                    plt.figure(figsize=(15,15))
                    sns.set_style('whitegrid')
                    plt.subplot(221)
                    ax = sns.countplot(df,x=i,order=df[i].value_counts(ascending = False).index)
                    for j in ax.containers:
                        ax.bar_label(j)
                    plt.xticks(rotation=90)
                    plt.subplot(222)
                    plt.title(i)
                    labels = df[i].value_counts(ascending = False).index
                    count = 0
                    explode = [0.1]
                    while count < len(labels)-1:
                        count = count + 1
                        explode.append(0)
                    plt.pie(df[i].value_counts(ascending = False),labels = labels,
                            autopct='%.2f%%',startangle=90,shadow=True,explode=explode)
                    if len(labels)<=5:
                        plt.legend(loc ='best')
                        plt.show()
                    else:
                        plt.show()
            else:
                for i in cat_cols:
                    plt.figure(figsize=(15,15))
                    sns.set_style('whitegrid')
                    ax = sns.countplot(df,x=i,order=df[i].value_counts(ascending = False).index)
                    for j in ax.containers:
                        ax.bar_label(j)
                    plt.xticks(rotation=90)
                    
        else:
            if pie=='on':
                plt.figure(figsize=(15,15))
                sns.set_style('whitegrid')
                plt.subplot(221)
                ax = sns.countplot(df,x=col,order=df[col].value_counts(ascending = False).index)
                for j in ax.containers:
                        ax.bar_label(j)
                plt.xticks(rotation=90)
                plt.subplot(222)
                plt.title(col)
                labels = df[col].value_counts(ascending = False).index
                count = 0
                explode = [0.1]
                while count < len(labels)-1:
                    count = count + 1
                    explode.append(0)
                plt.pie(df[col].value_counts(ascending = False),labels = labels,
                        autopct='%.2f%%',startangle=90,shadow=True,explode=explode)
                if len(labels)<=5:
                    plt.legend(loc ='best')
                    plt.show()
                else:
                    plt.show()
            else:
                plt.figure(figsize=(15,15))
                sns.set_style('whitegrid')
                ax = sns.countplot(df,x=col,order=df[col].value_counts(ascending = False).index)
                for j in ax.containers:
                        ax.bar_label(j)
                plt.xticks(rotation=90)
                plt.show()
    
    def heatmap(col):
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np
        import warnings
        warnings.filterwarnings('ignore')
        
        plt.figure(figsize=(15,7))
        annot_kws={'fontsize':12,'fontstyle':'italic','color':"k",'alpha':1,'verticalalignment':'center'}
        cmap = ['crest','flare','coolwarm','YlGnBu','RdPu']
        ax = sns.heatmap(col,annot=True,cmap=np.random.choice(cmap),linewidths=1, linecolor='black',annot_kws=annot_kws)
        for text in ax.get_yticklabels():
            text.set_size(12)
            text.set_weight('bold')
            text.set_style('italic')
        for text in ax.get_xticklabels():
            text.set_size(12)
            text.set_weight('bold')
            text.set_style('italic')
        plt.show()
        

def kill_outliers(data,kill):
    import numpy as np
    num_cols = data.select_dtypes(include=('int','float')).columns
    if kill=='trim':
        print('BEFORE KILLING THE OUTLIERS:',data.shape)
        before = data.shape[0]
    for i in num_cols:
        q3 = data[i].quantile(q=0.75)
        q1 = data[i].quantile(q=0.25)
        iqr = q3 - q1
        
        upper_bound = q3+1.5*(iqr)
        lower_bound = q1-1.5*(iqr)
        
        upper_index = data[data[i]>upper_bound].index
        lower_index = data[data[i]<lower_bound].index
        if kill == 'trim':
            data.drop(index=upper_index,inplace=True)
            data.drop(index=lower_index,inplace=True)
        elif kill == 'cap':
            data[i] = data[i].apply(lambda x:upper_bound if x>upper_bound else x)
            data[i] = data[i].apply(lambda x:lower_bound if x<lower_bound else x)
    if kill=='trim':
        print('AFTER KILLING THE OUTLIERS:',data.shape)
        after = data.shape[0]
        print('OUTLIERS % WAS:',((before-after)/before)*100)





def check_outliers(data,n=1.5):
    '''data : Dataframe 
       n    : int Default is 1.5,(IQR range)'''
    import numpy as np
    num_cols = data.select_dtypes(include=('int','float')).columns
    upper = []
    lower = []
    for i in num_cols:
        q3 = data[i].quantile(q=0.75)
        q1 = data[i].quantile(q=0.25)
        iqr = q3 - q1
        
        upper_bound = q3+n*(iqr)
        lower_bound = q1-n*(iqr)
        
        upper_index = data[data[i]>upper_bound].index
        lower_index = data[data[i]<lower_bound].index
        
        upper.append(upper_index)
        lower.append(lower_index)

        print(data.drop(index=upper_index).shape[0])
        print(data.drop(index=lower_index).shape[0])





def df_overview(df):
    '''df : pandas dataframe
    Returns : 
    Gives us the brief info about thte data in given dataframe'''
    from IPython.display import display
    
    print('-/-'*16+'Birds-Eye-View of the data'+'-/-'*16)
    print(end='\n')
    display(df.info())
    print('-/-'*16+'Checking the Null values in %'+'-/-'*16)
    print(end='\n')
    display((df.isna().sum())*100/df.shape[0])
    print(end='\n')
    print('-/-'*14+'Checking the Cardinality for each column'+'-/-'*14)
    print(end='\n')
    for i in df.columns:
        print('-*-'*10+i.upper()+'-*-'*10)
        print(df[i].value_counts())
        print(end='\n')
    print('-/-'*16+'Statistics for each numerical column'+'-/-'*16)
    display(df.describe(percentiles=[0.25,0.50,0.75,0.80,0.90,0.95]))    
