class Node:
    def __init__(self, data):
        self.data = data
        self.n = len(data)
        self.children = []

    def split(self, data, attr):
        sorted_data = sorted(data, key=lambda x: x[attr])
        attr_value = data[0][attr]
        split_data = []
        for i in range(self.n):
            if attr_value == data[i][attr]:
                split_data.append(data[i])
            else:
                self.children.append(Node(split_data))
                split_data = [data[i]]
                attr_value = data[i][attr]

    def gini(self, data):
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

    def find_split(self, data):
        attr = 0
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
            gini_index += n / len(classes[key]) * self.gini(classes[key])
