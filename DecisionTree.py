import sys

def gini_index(groups, classes):
    n = sum([len(group) for group in groups])

    gini = 0.0

    for group in groups:
        size = len(group)
        if size != 0:
            score = 0.0
            for class_val in classes:
                p = [data_point[0] for data_point in group].count(class_val) / size
                score += p ** 2
            gini += (1.0 - score) * (size / n)
    return gini

def split_on_value(index, value, data):
    L = list()
    R = list()
    for data_point in data:
        if data_point[index] < value:
            L.append(data_point)
        else:
            R.append(data_point)
    return L, R

def split_node(data):
    class_values = list(set(data_point[0] for data_point in data))
    m_index = sys.maxsize
    m_value = sys.maxsize
    m_score = sys.maxsize
    m_groups = None
    for index in range(1, len(data[0])):
        attr_values = list(set(data_point[index] for data_point in data))
        for val in attr_values:
            groups = split_on_value(index, val, data)
            gini = gini_index(groups, class_values)
            if gini < m_score:
                m_index = index
                m_value = val
                m_score = gini
                m_groups = groups
    return {'index': m_index, 'value': m_value, 'groups': m_groups}

def terminal(group):
    outcomes = [data_point[0] for data_point in group]
    return max(set(outcomes), key=outcomes.count)

def split(node, max_depth, min_size, depth):
    L, R = node['groups']
    del(node['groups'])

    if len(L) == 0 or len(R) == 0:
        node['L'] = node['R'] = terminal(L + R)
    else:
        if depth >= max_depth:
            node['L'], node['R'] = terminal(L), terminal(R)

        if len(L) <= min_size and len(L):
            node['L'] = terminal(L)
        else:
            node['L'] = split_node(L)
            split(node['L'], max_depth, min_size, depth + 1)

        if len(R) <= min_size and len(R):
            node['R'] = terminal(R)
        else:
            node['R'] = split_node(R)
            split(node['R'], max_depth, min_size, depth + 1)

def build_tree(data, max_depth, min_size):
    root = split_node(data)
    split(root, max_depth, min_size, 1)
    return root

def predict(node, data_point):
    direction = ''
    if data_point[node['index']] < node['value']:
        direction = 'L'
    else:
        direction = 'R'

    if isinstance(node[direction], dict):
        return predict(node[direction], data_point)
    else:
        return node[direction]

def print_matrix(matrix):
    k = len(matrix)
    for i in range(k):
        line = ""
        for j in range(k):
            line += str(matrix[i][j]) + " "
        line.rstrip()
        print(line)

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

classes = list(set(data_point[0] for data_point in data))
classes.sort()

n_classes = len(classes)

confusion_matrix = [[0 for i in range(n_classes)] for j in range(n_classes)]

tree = build_tree(test_data, depth, size)

for data_point in test_data:
    prediction = predict(tree, data_point)
    confusion_matrix[int(data_point[0]) - 1][int(prediction) - 1] += 1

if sys.argv[0] == "DecisionTree.py":
    print_matrix(confusion_matrix)