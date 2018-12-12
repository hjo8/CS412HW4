import sys
import DecisionTree
from random import choice

def split_data(data, num_split, num_samples):
    splits = []
    for i in range(num_split):
        split = []
        for j in range(num_samples):
            split.append(choice(data))
        splits.append(split)
    return splits

train_path = sys.argv[1]
test_path = sys.argv[2]

train_data = []

train_f = open(train_path, 'r')

line = train_f.readline()

num_attributes = len(line.split(" ")) - 1

while line is not "":
    data = line.rstrip().split(" ")
    for i in range(1, num_attributes + 1):
        data[i] = data[i].split(":")[1]
    train_data.append(data)
    line = train_f.readline()

train_f.close()

test_data = []

test_f = open(test_path, 'r')

line = test_f.readline()

while line is not "":
    data = line.rstrip().split(" ")
    for i in range(1, num_attributes + 1):
        data[i] = data[i].split(":")[1]
    test_data.append(data)
    line = test_f.readline()

test_f.close()

depth = len(test_data[0]) - 1
size = int(len(test_data) / depth)
num_trees = min(depth, 11)
if num_trees % 2 == 0:
    num_trees += 1

classes = list(set(data_point[0] for data_point in train_data))
classes.sort()

n_classes = len(classes)

confusion_matrix = [[0 for i in range(n_classes)] for j in range(n_classes)]

trees = []
num_samples = int(len(train_data) * 0.8)
data_samples = split_data(train_data, num_trees, num_samples)

for i in range(num_trees):
    tree = DecisionTree.build_tree(data_samples[i], depth, size)
    trees.append(tree)

for data_point in test_data:
    predictions = []
    for i in range(num_trees):
        prediction = DecisionTree.predict(trees[i], data_point)
        predictions.append(prediction)
    prediction = max(set(predictions), key=predictions.count)
    confusion_matrix[int(data_point[0]) - 1][int(prediction) - 1] += 1

DecisionTree.print_matrix(confusion_matrix)
DecisionTree.F_1(confusion_matrix)