import sys
import DecisionTree

def split_data(data, num_split):


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
num_trees = depth

classes = list(set(row[0] for row in data))
classes.sort()

n_classes = len(classes)

confusion_matrix = [[0 for i in range(n_classes)] for j in range(n_classes)]

trees = []

tree = build_tree(test_data, depth, size)

for row in test_data:
    prediction = predict(tree, row)
    confusion_matrix[int(row[0]) - 1][int(prediction) - 1] += 1