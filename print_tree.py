from anytree import Node, RenderTree
import queue


def load_operations():
    ret = {}
    with open("gates.txt", "r") as op_file:
        for line in op_file:
            line = line.strip()
            tokens = line.split(' ')
            idx_out = int(tokens[0])
            op = tokens[2]
            idxs_in = list(map(int, tokens[3:]))
            ret[idx_out] = [op, idxs_in]
    return ret


def build_tree(head, operations):
    traversal_queue = queue.Queue()
    head_node = Node(head)
    traversal_queue.put(head_node)
    while not traversal_queue.empty():
        this_node = traversal_queue.get()
        idx = this_node.name
        op, idxs_in = operations[idx]
        this_node.name = op
        if op in ["CONST0", "CONST1"]:
            continue
        elif op in ["I", "NOT_I"]:
            this_node.name = this_node.name + str(idxs_in[0])
        elif op in ["O"]:
            this_node.name = this_node.name + str(idxs_in[0])
        else:
            for idx in idxs_in:
                new_node = Node(idx, parent=this_node)
                traversal_queue.put(new_node)

    return head_node


operations = load_operations()

for head in [128, 140, 136, 148, 145, 158, 154, 167, 163, 160, 173, 14, 96, 119, 123]:
    print("-----------------"+str(head)+"------------------")
    tree = build_tree(head, operations)
    for pre, fill, node in RenderTree(tree):
        print("%s%s" % (pre, node.name))
    print("---------------------------------------")
