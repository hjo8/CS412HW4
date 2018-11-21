import sys
import node

def gini(data):
    n = len(data)
    num_classes = {}
    for i in range(n):
        _class = data[i][0]
        if _class in num_classes:
            num_classes[_class] += 1
        else:
            num_classes[_class] = 1

    gini_index = 1

    for _class in num_classes:
        gini_index -= (num_classes[_class] / n) ** 2

    return gini_index

def split(data, attr):
    sorted_data = sorted(data, key=lambda x: x[attr])
    classes = {}
    n = len(data)
    for i in range(n):
        if sorted_data[i][attr] in classes:
            classes[sorted_data[i][attr]].append(sorted_data[i])
        else:
            classes[sorted_data[i][attr]] = [sorted_data[i]]
    gini_index = 0
    for key in classes:
        gini_index += n / len(classes[key]) * gini(classes[key])
    return gini_index

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

# TRAIN

for i in range(num_attributes):
    gini_index = split(test_data, i + 1)