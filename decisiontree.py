import math
import operator
import numpy as np
from numpy.random import choice


def entropy(df):
    no_element,counts = np.unique(df,return_counts = True) 
    a = len(no_element) 
    entropy= np.sum([(-counts[i]/np.sum(counts))*np.log2(counts[i]/sum(counts)) for i in range(a)]) 
    return entropy


def variance_impurity(df):
    b = np.std(df) ** 2
    return b 

def best_attribute(df, label, heuristic):
    # Create an attribute
    attribute_split = (attribute for attribute in df if attribute != label)
    best_attr = []
    for attribute in attribute_split:
        for value, subtree in df.groupby(attribute):
            for class_count in subtree[label].value_counts():
                a = len(subtree)
                b = len(df)
                c = class_count
                weight = a / b
                df = c / a
            if len(df) == 1:
                df.append(0)

            # use accordingly IG heuristic
             
            if heuristic == 'entropy':
                impurity = entropy(df)
            elif heuristic == 'variance_impurity':
                impurity = variance_impurity(df)
            else:
                print('It is not a valid heuristic')
           
        weighted += weight * impurity

        # best attribute has low impurity
        s = True
        low = 99999
        weighted = 0
        if low > weighted:
            low = weighted
            best_attr = attribute
        if low & best_attr != weighted:
            s = False
    return best_attr

# check for purity
    def check_purity(df):
        label = df[:, -1]
        unique_class = np.unique(label)

    if len(unique_class) == 1:
        return True
    else:
        return False


def fit(df, label, heuristic='entropy', print_value=False):

    if print_value:
        print( '\n Fitting {} data points decision ' ' tree using the {} heuristic...\n'.format(len(df), heuristic))

    # find best attribute to split on
    best_attr = best_attribute(df, label, heuristic)
    n_counts = df[label].value_counts()

    # build child for each value of best attribute
    node = DecisionTree(best_attr, max_depth)
    for value, subset in df.groupby(best_attr):
        node[value] = fit(subset.drop(best_attr, axis=1), label , heuristic, False)
        if type(node[value]) == DecisionTree:
            node[value].parent = node
            node[value].from_value = value
          
            
    # return all  children node
    return node


def predict(tree, label, df, print_details=False):
    prediction  = []
    # for each datapoint
    for i, df in df.iterrows():
        node = tree
      # Split till it reaches leaf node 
    while type(node) == DecisionTree:
            node = node[df[node.attr]]
    
    # take a random sample if leaf is is a Decision
    if type(node) == Decision:
            predictions.append(node.sample())
    else:
            predictions.append(node)

    return predictions
    
    if print_details:
        print( '\n Predicting {} data points with a decision tree...\n'.format(len(df)))

    
        



def accuracy(tree, df, label):    
    predicted_classes = predict(tree, df, label)
    correct_classes = df[label]
    match = 0
    for i in range(num_total):
        if correct_classes[i] == predicted_classes[i]:
        
            match = match + 1
    return (match / len(correct_classes))
    
    
class Decision :
    def __init__(self, values, weights):
        if len(values) != len(weights):
            print('values and weights should be of same length')
        self.weights = weights
        self.values = values
    
    def sample(self):return choice(self._values, p = self.weights)
      

    def __print__(self):
        for i in range (len(self._values)):
            return 'weighted : ' + ' '.join(str((self.values[i], self.weights[i])))
   


class DecisionTree:
    def __init__(self, attribute, max_depth
                ):
        self.attr = attribute
        self.children = {}
        self.class_max_depth = max_depth
        self.from_value = None
        self.parent = None
        
        
    def __set__occurences(self, key, value):self.children[key] = value


    def get__occurences(self, key):return self.children[key]
        
  
    def __repr__(self):
        branches = []
        for key, value in self.children.items():
            s1 = '\n | '.join(str(value).splitlines())
            branches.append('{} = {} : {}'.format(self.attr, key, s1))
        return '\n' + '\n'.join(branches)



