import itertools

operators = ['!', 'v', '^', '<=>', '=>']

#class tree
class TreeNode():
    def __init__(self, val):
        self.val = val
        self.parent = None
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def add_parent(self, parent):
        self.parent = parent

# Remove implication Statements for converting to CNF
def remove_imply(root):
    if root.val == '=>':
        Node = TreeNode('!')
        Node.add_child(root.children[0])
        Node.add_parent(root)
        root.children[0].add_parent(Node)
        root.children[0] = Node
        root.val = 'v'

    for i in root.children:
        remove_imply(i)


def findsubsets(S, m):
    return list(set(itertools.combinations(S, m)))

# Remove Bi - implications for converting to CNF
def remove_bimply(root):
    if root.val == '<=>':
        Node1 = TreeNode('=>')
        Node2 = TreeNode('=>')
        left = root.children[0]
        right = root.children[1]
        Node1.add_child(root.children[0])
        root.children[0].add_parent(Node1)
        Node1.add_child(right)
        right.add_parent(Node1)
        Node2.add_child(root.children[1])
        root.children[1].add_parent(Node2)
        Node2.add_child(left)
        left.add_parent(Node2)
        root.val = '^'
        root.children[0] = Node1
        root.children[1] = Node2

    for i in root.children:
        remove_bimply(i)

# Move Negations Inward
def clean_negations(root):
    if root.val == '!':
        if (root.children[0].val not in operators) and root.children[0].val[0] == '!':
            root.val = str(root.children[0].val[1])
            root.children = []
        elif (root.children[0].val not in operators) and root.children[0].val[0] != '!':
            root.val = '!' + str(root.children[0].val)
            root.children = []
        elif root.children[0].val == '^':
            root.val = 'v'
            for i in root.children[0].children:
                Node = TreeNode('!')
                Node.add_parent(root)
                Node.add_child(i)
                root.add_child(Node)
            root.children.remove(root.children[0])

        elif root.children[0].val == 'v':
            root.val = '^'
            for i in root.children[0].children:
                Node = TreeNode('!')
                Node.add_parent(root)
                Node.add_child(i)
                root.add_child(Node)
            root.children.remove(root.children[0])

    #		elif root.children[0].val == '!':
    #			root = root.children[0].children[0]

    for i in root.children:
        clean_negations(i)


def find_not(root):
    if root.val == '!':
        return True
    else:
        if root.val not in operators:
            return False
        else:
            for i in root.children:
                val = find_not(i)
                if val:
                    return True
    return False

# Find Clauses -- Partially working- Not correctly working in case of v
def makeCNF(root):
    if root.val not in operators:
        # print("Here",root.val)
        return [root.val]

    elif root.val == '^':
        list2 = []
        for i in root.children:
            list2.append(makeCNF(i))
        return list2

    elif root.val == 'v':
        list1 = []
        # list = []
        list2 = []
        for i in root.children:
            # print(i.val)
            if i.val not in operators:
                #		print(i.val)
                list1.append(i.val)
            else:
                list2.append(makeCNF(i))

        print(list1, list2)
        list_final = []
        if list1 != [] and list2 == []:
            return [list1]

        elif list1 != [] and list2 != []:

            list2.append([list1])
            print("HERE", list2)
            for i in range(len(list2)):
                for j in range(len(list2)):
                    if i < j:
                        for k in range(len(list2[i])):
                            for m in range((len(list2[j]))):
                                # print("List is",list2[i][k],"&", list2[j][m])

                                list_final.append(list(set(list2[i][k]).union(set(list2[j][m]))))
            return list_final
        else:
            for i in range(len(list2)):
                for j in range(len(list2)):
                    if i < j:
                        for k in range(len(list2[i])):
                            for m in range((len(list2[j]))):
                                list_final.append(list(set(list2[i][k]).union(set(list2[j][m]))))
            return list_final


def toCNF(root):
    remove_bimply(root)
    # print("remove bi imply")
    # print_dfs(root,0)
    # print("remove imply")
    remove_imply(root)
    # print_dfs(root,0)
    # print("remove negations")
    while find_not(root):
        #		print_dfs(root,0)
        clean_negations(root)

    print_dfs(root, 0)
    subset = makeCNF(root)

    print("Subset is", subset)

#Parser
def parser(list_val):
    i = 0
    # print(list_val)
    root = None
    operator_list = []
    leaf_list = []
    while i < len(list_val):
        #	print(i)
        if list_val[i] == '!':
            tree_node = TreeNode(list_val[i])
            i = i + 1
            operator_list.append(tree_node)

        elif list_val[i] == '(':
            # operator_list.append(tree_node)
            count = 1
            i = i + 1
            list_subset = []
            while count != 0:
                if list_val[i] == '(':
                    count = count + 1
                    list_subset.append(list_val[i])
                    i = i + 1

                elif list_val[i] == ')':
                    count = count - 1
                    if count != 0:
                        list_subset.append(list_val[i])
                    i = i + 1

                else:
                    list_subset.append(list_val[i])
                    i = i + 1

            leaf_node = parser(list_subset)

            if len(operator_list) > 0:
                if operator_list[len(operator_list) - 1].val == '!':

                    leaf_node.add_parent(operator_list[len(operator_list) - 1])
                    operator_list[len(operator_list) - 1].add_child(leaf_node)
                    leaf_list.append(operator_list[len(operator_list) - 1])
                    operator_list.remove(operator_list[len(operator_list) - 1])

                else:
                    leaf_list.append(leaf_node)
            else:
                leaf_list.append(leaf_node)


        elif list_val[i] not in operators:
            leaf_node = TreeNode(list_val[i])
            i = i + 1

            if len(operator_list) > 0:
                if operator_list[len(operator_list) - 1].val == '!':
                    leaf_node.add_parent(operator_list[len(operator_list) - 1])
                    operator_list[len(operator_list) - 1].add_child(leaf_node)
                    leaf_list.append(operator_list[len(operator_list) - 1])
                    operator_list.remove(operator_list[len(operator_list) - 1])
                else:
                    leaf_list.append(leaf_node)

            else:
                leaf_list.append(leaf_node)

        elif list_val[i] in operators:
            tree_node = TreeNode(list_val[i])
            operator_list.append(tree_node)
            i = i + 1

    if operator_list == []:
        return leaf_list[0]

    else:
        for i in range(len(leaf_list)):
            # print(leaf_list)
            operator_list[0].add_child(leaf_list[i])
            leaf_list[i].add_parent(operator_list[0])
        return operator_list[0]

#not definition
def not_func(value):
    return not value

#Or definition
def or_func(list):
    for i in list:
        if i:
            return True

    return False

#And definition
def and_func(list):
    for i in list:
        if not i:
            return False
    return True

#imply Definition
def imply_func(list):
    if list[0] == True and list[1] == False:
        return False
    else:
        return True

#Bi imply definition
def biimply_func(list):
    if list[0] != list[1]:
        return False
    else:
        return True

# Takes a dictionary and evaluates the output
def evaluate(root, dict):
    if root.val not in operators:
        if root.val[0] == '!':
            return not (dict[root.val[1:len(root.val)]])
        else:
            return dict[root.val]

    elif root.val == '!':
        return not_func(evaluate(root.children[0], dict))

    elif root.val == 'v':
        return or_func([evaluate(child, dict) for child in root.children])

    elif root.val == '^':
        return and_func([evaluate(child, dict) for child in root.children])

    elif root.val == '=>':
        return imply_func([evaluate(child, dict) for child in root.children])

    elif root.val == '<=>':
        return biimply_func([evaluate(child, dict) for child in root.children])

# Can print a tree
def print_dfs(root, c):
    str = ""
    for i in range(c):
        str = str + '  '
    str = str + root.val
    print(str)
    for i in range(len(root.children)):
        print_dfs(root.children[i], c + 1)


# All the letters need to be separated by a space. even the brackets. !B is allowed but !( is not it needs to be ! (. All open brackets must be closed. An example is shown below. Uncomment if you want to test the below expressions. Print_dfs prints the output tree.		
#expr= "A v ( !B ^ C )"
# list_val = expr.split(' ')
# root = parser(list_val)
#print_dfs(root)
# toCNF(root)
# print(evaluate(root,dict))
