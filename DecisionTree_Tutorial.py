import sys

def gini_index(groups, classes):
	n = 0.0
	for group in groups:
		n += len(group)

	gini = 0.0

	for group in groups:
		size = len(group)
		if size != 0:
			score = 0.0
			for class_val in classes:
				p = [row[0] for row in group].count(class_val) / size
				score += p ** 2
			gini += (1.0 - score) * (size / n)

	return gini

def test_split(index, value, data):
	left, right = list(), list()
	for row in data:
		if row[index] < value:
			left.append(row)
		else:
			right.append(row)
	return left, right

def get_split(data):
	class_values = list(set(row[0] for row in data))
	b_index, b_value, b_score, b_groups = 9999, 9999, 9999, None
	for index in range(1, len(data[0])):
		for row in data:
			groups = test_split(index, row[index], data)
			gini = gini_index(groups, class_values)
			if gini < b_score:
				b_index, b_value, b_score, b_groups = index, row[index], gini, groups
	return {'index': b_index, 'value': b_value, 'groups': b_groups}

def to_terminal(group):
	outcomes = [row[0] for row in group]
	return max(set(outcomes), key=outcomes.count)

def split(node, max_depth, min_size, depth):
	left, right = node['groups']
	del(node['groups'])

	if not left or not right:
		node['left'] = node['right'] = to_terminal(left + right)

	if depth >= max_depth:
		node['left'], node['right'] = to_terminal(left), to_terminal(right)

	if len(left) <= min_size:
		node['left'] = to_terminal(left)
	else:
		node['left'] = get_split(left)
		split(node['left'], max_depth, min_size, depth + 1)

	if len(right) <= min_size:
		node['right'] = to_terminal(right)
	else:
		node['right'] = get_split(right)
		split(node['right'], max_depth, min_size, depth + 1)

def build_tree(data, max_depth, min_size):
	root = get_split(data)
	split(root, max_depth, min_size, 1)
	return root

def predict(node, row):
	direction = ''
	if row[node['index']] < node['value']:
		direction = 'left'
	else:
		direction = 'right'

	if isinstance(node[direction], dict):
		return predict(node[direction], row)
	else:
		return node[direction]

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

max_depth = len(test_data[0]) - 1
min_size = int(len(test_data) / max_depth)

tree = build_tree(test_data, max_depth, min_size)
n_right = 0
n_wrong = 0
for row in test_data:
	prediction = predict(tree, row)
	if row[0] == prediction:
		n_right += 1
	else:
		n_wrong += 1

print(n_right, n_wrong)