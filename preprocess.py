
import numpy as np
import io_helper
import inputdata

random_data_dup = 10  # each sample randomly duplicated between 0 and 9 times, see dropin function


def dropin(X, y):
    """
    The name suggests the inverse of dropout, i.e. adding more samples. See Data Augmentation section at
    http://simaaron.github.io/Estimating-rainfall-from-weather-radar-readings-using-recurrent-neural-networks/
    :param X: Each row is a training sequence
    :param y: Tne target we train and will later predict
    :return: new augmented X, y
    """
    print("X shape:", X.shape)
    print("y shape:", y.shape)
    X_hat = []
    y_hat = []
    for i in range(0, len(X)):
        for j in range(0, np.random.random_integers(0, random_data_dup)):
            X_hat.append(X[i, :])
            y_hat.append(y[i])
    return np.asarray(X_hat), np.asarray(y_hat)



def preprocess(load=True,step='train'):
    dirc = "ADFA-LD/Training_Data_Master/"
    dirc_val = "ADFA-LD/Validation_Data_Master/"
    dic_attack ="ADFA-LD/Attack_Data_Master/"
    arraydir = "arrayfile/"
    xtrainlist=[]
    ytrainlist=[]
    xtestlist=[]
    ytestlist=[]
    train_arrlist=[]
    test_arrlist=[]
    att_arrlist=[]
    # to fix ,only read a test pickle file
    if load :
        
        if step == 'train':   
            train_arrfs=inputdata.readfilesfromAdir(arraydir+'/train')
        
            for each in train_arrfs:
                train_arr= io_helper.loadfrompickle(each)
                train_arrlist.append(train_arr)
        if step == 'test':      
            test_arrfs = inputdata.readfilesfromAdir(arraydir+'/val')
            for each in test_arrfs:
                test_arr= io_helper.loadfrompickle(each)
                test_arrlist.append(test_arr)
    else :
        train_arrlist,test_arrlist,att_arrlist=inputdata.process_log()
        
    if step == 'train':  
        for array in train_arrlist:
            x_train = array[:,:-1]
            y_train = array[:,-1]
            print ("The train data size:","xtrain",x_train.shape,"ytrain",y_train.shape)
            xtrainlist.append(x_train)
            ytrainlist.append(y_train)
            return (xtrainlist,ytrainlist)
    if step == 'test':  
        for array in test_arrlist:
            x_test = array[:,:-1]
            y_test = array[:,-1]
            print ("The train data size:","xtrain",x_test.shape,"ytrain",y_test.shape)
            xtestlist.append(x_test)
            ytestlist.append(y_test)
            return (xtestlist,ytestlist)


if __name__ =="__main__":
    
    preprocess()
