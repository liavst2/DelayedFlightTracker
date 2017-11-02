#############################################################
# FILE: LogisticLearn.py
# EXERCISE : A needle in a data haystack - final project
#############################################################


from sklearn.metrics import accuracy_score
from sklearn import preprocessing
import pandas as pd
import json
from sklearn.preprocessing import scale
from sklearn.linear_model import LogisticRegression, SGDClassifier
from numpy import float32
import glob


def preprocess_category(training_set):
    """ this function gets a data set and chnges it's week colmun
    into 7 coulmns that represent days for example:'DAY_OF_WEEK_7' """
    X_train_1= training_set
    # one hot encoder is the encoder used to split the columns in the rught way
    one_enc = preprocessing.OneHotEncoder(sparse=False)
    cat_columns = ["DAY_OF_WEEK"]

    # will run once, in loop for the case we want to run on more then one column
    for col in cat_columns:
        # creating an exhaustive list of all possible categorical values
        data = training_set[[col]]
        one_enc.fit(data)
        # Fitting One Hot Encoding on train data
        temp = one_enc.transform(training_set[[col]])
        # Changing the encoded features into a data frame with new column names
        colt = [(col + "_" + str(i)) for i in data[col].value_counts().index]
        temp = pd.DataFrame(temp, columns=colt)
        # Setting the index values similar to the X_train data frame
        temp = temp.set_index(training_set.index.values)
        # adding the new One Hot Encoded varibales to the train data frame
        X_train_1 = pd.concat([X_train_1, temp], axis=1)

    return X_train_1


def preprocess_to_cont(path):
    """This is the main pre-process the given data"""
    # opens json that translate from airline\airport ID to it's size
    with open("jsons\\airport_to_sizes_dict.json") as ports:
        airportToSizeDict = json.load(ports)
    with open("jsons\\airline_id_to_size.json") as airlineToSize:
        airlineToSizeDict = json.load(airlineToSize)
    # the foll
    filenames = glob.glob(path + "/*.csv")
    dfs = []
    for filename in filenames:
        dfs.append(pd.read_csv(filename,usecols=["MONTH","DAY_OF_WEEK","AIRLINE_ID","ORIGIN_AIRPORT_ID","DEST_AIRPORT_ID","DEP_TIME","DEP_DELAY"]))
    # Concatenate all data into one DataFrame
    data_set = pd.concat(dfs, ignore_index=True)

    # traslte airport\airline ID to it's size using the json file
    for i,row in data_set.iterrows():
        data_set.set_value(i,"AIRLINE_ID",airlineToSizeDict[str(int(row["AIRLINE_ID"]))])
        data_set.set_value(i,"ORIGIN_AIRPORT_ID",airportToSizeDict[str(int(row["ORIGIN_AIRPORT_ID"]))])
        data_set.set_value(i, "DEST_AIRPORT_ID", airportToSizeDict[str(int(row["DEST_AIRPORT_ID"]))])

    print("Before Preprocess week days")
    data_set = preprocess_category(data_set)
    print("After Preprocess week days")

    # drops the rows contains NaN
    data_set = data_set[pd.notnull(data_set)]
    data_set = data_set.dropna()

    # scaling the data by normalizing around 0
    data_set[["MONTH","AIRLINE_ID","ORIGIN_AIRPORT_ID","DEST_AIRPORT_ID","DEP_TIME"]] = scale(data_set[["MONTH","AIRLINE_ID","ORIGIN_AIRPORT_ID","DEST_AIRPORT_ID","DEP_TIME"]]).astype(float32)

    # splitting the test and training sets
    train_set = data_set.sample(frac=0.8, random_state=200)
    test_set = data_set.drop(train_set.index)
    print("End Of Preprocess")
    test_set.to_csv("test.csv")
    train_set.to_csv("train.csv")
    return  train_set, test_set


def dictionize():
    """helper function used to bring the json to the right configuration"""
    with open("jsons\\airport_id_to_size.json") as json_file:
        json_dict = json.load(json_file)
        clean_dict = {}
        for jas in json_dict:
            for key in json_dict[jas]:
                clean_dict[key] = json_dict[jas][key]

        with open("jsons\\airport_to_sizes_dict.json","w") as jf:
            json.dump(clean_dict,jf)
    return



def learn_logistic(train_set, test_set):
    """the function which does the Logistic Regression training and returns the accuracy """
    log = LogisticRegression(penalty='l2', C=.01)
    print("Start Of Training")
    # the training
    log.fit(train_set[["MONTH","AIRLINE_ID","ORIGIN_AIRPORT_ID","DEST_AIRPORT_ID","DEP_TIME"]], train_set[["DEP_DELAY"]])
    print("Start of Testing")
    a=accuracy_score(test_set[["DEP_DELAY"]],log.predict(test_set[["MONTH","AIRLINE_ID","ORIGIN_AIRPORT_ID","DEST_AIRPORT_ID","DEP_TIME"]]))
    print("Accuracy Score:",a)


def learn_SGD(train_set, test_set):
    """the function which does the SGD classification training and returns the accuracy """
    log = SGDClassifier()
    print("Start Of Training SGD")
    # the training
    log.fit(train_set[["MONTH","AIRLINE_ID","ORIGIN_AIRPORT_ID","DEST_AIRPORT_ID","DEP_TIME"]], train_set[["DEP_DELAY"]])
    print("Start of Testing SGD")
    a=accuracy_score(test_set[["DEP_DELAY"]],log.predict(test_set[["MONTH","AIRLINE_ID","ORIGIN_AIRPORT_ID","DEST_AIRPORT_ID","DEP_TIME"]]))
    print("Accuracy Score:",a)



def y_column_edit(data_set):
    """converts the delay parameters to 1/0 depending on the chosen threshold"""
    threshold = 1
    for i, row in data_set.iterrows():
        # data_set.set_value(i, "AIRLINE_ID", airlineToSizeDict[str(int(row["AIRLINE_ID"]))])
        if row["DEP_DELAY"] < threshold:
            data_set.set_value(i,"DEP_DELAY",0)
        else:
            data_set.set_value(i, "DEP_DELAY", 1)
    return data_set


def main():
    train_set, test_set = preprocess_to_cont("C:\\My Documents\\cs\\needle\\project\\csvs")
    learn_SGD(y_column_edit(train_set),y_column_edit(test_set))

    return


if __name__ == "__main__":
    main()
