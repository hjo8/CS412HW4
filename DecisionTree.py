import sys

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
