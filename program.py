import argparse
import pandas as pd

import decisiontree

def main():
    parser = argparse.ArgumentParser(description='Classify the data using decision trees.')

    parser.add_argument('training-set',   help='csv training set')
    parser.add_argument('validation-set', help='csv validation set')
    parser.add_argument('test-set',       help='csv test set')
    parser.add_argument('to-print',       help='prints tree', choices=['yes', 'no'])

    args = vars(parser.parse_args())

    training_set = pd.read_csv(args['training-set'])
    validation_set = pd.read_csv(args['validation-set'])
    test_set = pd.read_csv(args['test-set'])

    label = 'Class'

    # Train and predict on both heuristics
    for heuristic in ['entropy', 'variance_impurity']:
        print('\n-----------')

        tree = decisiontree.fit( training_set, label, heuristic=heuristic, print=True)

        # measure accuracy on test set
        accuracy_percentage = decisiontree(tree, test_set, label)

        if args['to-print'] == 'yes':
            print(tree)


    print('\n--------------------------')

if __name__ == '__main__':
    main()