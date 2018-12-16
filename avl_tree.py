class Node(object):
    # our node for the tree
    def __init__(self, value):
        self.value = value
        self.right = None
        self.left = None
        self.parent = None
        self.height = 1
        self.rh = 0
        self.lh = 0
        self.rh_minus_lh = self.rh - self.lh

class Tree(object):
    # our tree
    def __init__(self):
        self.root = None

    def insert(self, value):
        # this function inserts only tree's root
        if(self.root is None):
            self.root = Node(value)
        else:
            self.n_r_insert(value, self.root)

    def n_r_insert(self, value, node):
        # recursively add the node (tree already has a root)
        is_added = False
        if(value > node.value):
            if(node.right is not None):
                self.n_r_insert(value,node.right)
            else:
                node.right = Node(value)
                node.right.parent = node
                node.rh = node.rh + 1
                is_added = True
        else:
            if(node.left is not None):
                self.n_r_insert(value,node.left)
            else:
                node.left = Node(value)
                node.left.parent = node
                node.lh = node.lh + 1
                is_added = True

        # re-organize heights and imbalances after a node is added
        if(is_added):
            self.fix_path_heights(node)
            self.find_fix_imbalaned(node)

    def find_fix_imbalaned(self, node):
        # find the node in which there is an imbalacne
        tmp = node
        while(tmp.parent is not None):
            tmp = tmp.parent

            # if there is an imbalance check which case it is and perform the required rotation type
            if(abs(tmp.lh - tmp.rh) > 1):
                if(tmp.lh > tmp.rh and tmp.left.lh > tmp.left.rh):
                    self.left_left_case(tmp)
                    break
                elif(tmp.lh > tmp.rh and tmp.left.lh < tmp.left.rh):
                    self.left_right_case(tmp)
                    break
                elif(tmp.lh < tmp.rh and tmp.right.rh > tmp.right.lh):
                    self.right_right_case(tmp)
                    break
                elif(tmp.lh < tmp.rh and tmp.right.rh < tmp.right.lh):
                    self.right_left_case(tmp)
                    break
                else:
                    break

    def fix_path_heights(self, node):
        tmp = node

        #go up the tree while fixing left and right heights of each node in the path
        while(tmp.parent is not None):
            if(tmp.parent.value < tmp.value):
                tmp.parent.rh = max(tmp.rh, tmp.lh) + 1
            else:
                tmp.parent.lh = max(tmp.rh, tmp.lh) + 1
            tmp = tmp.parent


    def left_left_case(self, rotate_node):
        n_root = rotate_node.left # n_root will be at the top after the rotation
        tmp = None #tmp is initially the right of the left of the rotate node
        if(n_root.right is not None):
            tmp = n_root.right
        n_root.right = rotate_node
        if(tmp is not None):
            rotate_node.left = tmp
            tmp.parent = rotate_node
        else:
            rotate_node.left = None
            rotate_node.lh = 0

        if(rotate_node.parent is None):
            n_root.parent = None
            self.root = n_root
        else:
            n_root.parent = rotate_node.parent
            if(rotate_node.parent.left is rotate_node):
                rotate_node.parent.left = n_root
            else:
                rotate_node.parent.right = n_root

        rotate_node.parent = n_root

        #change heights
        if(tmp is not None):
            rotate_node.lh = max(tmp.lh, tmp.rh) + 1
        else:
            rotate_node.lh =  0
        n_root.rh = max(rotate_node.lh, rotate_node.rh) + 1

        #update height paths
        self.fix_path_heights(n_root)

    def right_right_case(self, rotate_node):
        n_root = rotate_node.right # n_root will be at the top after the rotation
        tmp = None #tmp is initially the left of the right of the rotate node
        if(n_root.left is not None):
            tmp = n_root.left
        n_root.left = rotate_node
        if(tmp is not None):
            rotate_node.right = tmp
            tmp.parent = rotate_node
        else:
            rotate_node.right = None
            rotate_node.rh = 0

        if(rotate_node.parent is None):
            n_root.parent = None
            self.root = n_root
        else:
            n_root.parent = rotate_node.parent
            if(rotate_node.parent.left is rotate_node):
                rotate_node.parent.left = n_root
            else:
                rotate_node.parent.right = n_root

        rotate_node.parent = n_root

        #change heights
        if(tmp is not None):
            rotate_node.rh = max(tmp.lh, tmp.rh) + 1
        else:
            rotate_node.rh = 0
        n_root.lh = max(rotate_node.lh, rotate_node.rh) + 1

        #update path heights
        self.fix_path_heights(n_root)

    def left_right_case(self, rotate_node):
        #first change to left left case
        n_root = rotate_node.left.right
        tmp = None
        if(n_root.left is not None):
            tmp = n_root.left
        tmp_b = rotate_node.left
        rotate_node.left = n_root
        n_root.parent = rotate_node
        n_root.left = tmp_b
        tmp_b.parent = n_root
        if(tmp is not None):
            tmp_b.right = tmp
            tmp.parent = tmp_b
        else:
            tmp_b.right = None
            tmp_b.rh = 0

        #change heights
        if(tmp_b.left is not None):
            n_root.lh = max(tmp_b.left.lh, tmp_b.left.rh) + 1
        else:
            n_root.lh = 1
        if(tmp is not None):
            tmp_b.rh = max(tmp.lh, tmp.rh) + 1
        else:
            tmp_b.rh = 0

        #now it is a left left case
        self.left_left_case(rotate_node)

    def right_left_case(self, rotate_node):
        #first change to right right case
        n_root = rotate_node.right.left
        tmp = None
        if(n_root.right is not None):
            tmp = n_root.right
        tmp_b = rotate_node.right
        rotate_node.right = n_root
        n_root.parent = rotate_node
        n_root.right = tmp_b
        tmp_b.parent = n_root
        if(tmp is not None):
            tmp_b.left = tmp
            tmp.parent = tmp_b
        else:
            tmp_b.left = None
            tmp_b.lh = 0

        #change heights
        if(tmp_b.right is not None):
            n_root.rh = max(tmp_b.right.lh, tmp_b.right.rh) + 1
        else:
            n_root.rh = 1
        if(tmp is not None):
            tmp_b.lh = max(tmp.rh, tmp.lh) + 1
        else:
            tmp_b.lh = 0

        #now it is a right right case
        self.right_right_case(rotate_node)

    def query_pred(self, value):
        # find predecessor
        if(self.root is not None):
            tmp = self.root
        else:
            return None

        pred_val = None
        while(tmp is not None):
            if(tmp.value == value):
                pred_value = tmp.value
                break
            elif(tmp.value < value):
                pred_val = tmp.value
                tmp = tmp.right
            else:
                tmp = tmp.left
        return pred_val



avl_tree = Tree()


with open('output.txt', 'w') as outf:
    f = open("ops.txt")
    for line in f:
        entries = line.split(' ')
        if(entries[0] == "ins"):
            avl_tree.insert(int(entries[1]))
        elif(entries[0] == "qry"):
            if(avl_tree.query_pred(int(entries[1])) is None):
                outf.write('no')
            else:
                outf.write(str(avl_tree.query_pred(int(entries[1]))) + '\n')
    f.close()

