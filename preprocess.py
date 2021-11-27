
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



def preprocess(load=True):
    dirc = "ADFA-LD/Training_Data_Master/"
    dirc_val = "ADFA-LD/Validation_Data_Master/"
    dic_attack ="ADFA-LD/Attack_Data_Master/"
    arraydir = "arrayfile/"
    xtrainlist=[]
    ytrainlist=[]
    arraylist=[]
    # to fix ,only read a test pickle file
    if load :
        arrayfiles=inputdata.readfilesfromAdir(arraydir)
        for each in arrayfiles:
            array= io_helper.loadfrompickle(each)
            arraylist.append(array)
    else :
        alltraces = inputdata.get_all_call_sequences(dirc)
        arraylist=inputdata.list_to_matrix(alltraces)
    for array in arraylist:
        x_train = array[:,:-1]
        y_train = array[:,-1]
        print ("The train data size:","xtrain",x_train.shape,"ytrain",y_train.shape)
        # print (x_train.shape)
        # print (y_train.shape)
        xtrainlist.append(x_train)
        ytrainlist.append(y_train)

    return (xtrainlist,ytrainlist,xtestlist,ytestlist)


if __name__ =="__main__":
    
    preprocess()
