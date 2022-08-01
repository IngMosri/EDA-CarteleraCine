class TreeNode(object):
    def __init__(self, info = None):
        self.data = info
        self.left = None
        self.right = None

    def insert(self, key, info):
        if self.data:
            if self.data[key] == info[key]:
                return False
            elif info[key] < self.data[key]:
                if self.left:
                    return self.left.insert(key, info)
                else:
                    self.left = TreeNode(info)
                    return True
            else:
                if self.right:
                    return self.right.insert(key, info)
                else:
                    self.right = TreeNode(info)
                    return True
        else:
            self.data = info
            return True

    def find(self, key, info):
        if self.data[key] == info:
            return True
        elif info < self.data[key] and self.left:
            return self.left.find(key, info)
        elif info > self.data[key] and self.right:
            return self.right.find(key, info)
        return False

    def preorder(self, list):
        list.append(self.data)
        if self.left:
            self.left.preorder(list)
        if self.right:
            self.right.preorder(list)
        return list

    def postorder(self, list):
        if self.left:
            self.left.postorder(list)
        if self.right:
            self.right.postorder(list)
        list.append(self.data)
        return list

    def inorder(self, list, asc = True):
        if asc == True:
            if self.left:
                self.left.inorder(list, asc)
            list.append(self.data)
            if self.right:
                self.right.inorder(list, asc)
            return list
        else:
            if self.right:
                self.right.inorder(list, asc)
            list.append(self.data)
            if self.left:
                self.left.inorder(list, asc)
            return list
            


# class Tree(object):
#     def __init__(self):
#         self.root = None

#     # return True if successfully inserted, false if exists
#     def insert(self, info):
#         if self.root:
#             return self.root.insert(info)
#         else:
#             self.root = Node(info)
#             return True

#     # return True if info is found in tree, false otherwise
#     def find(self, info):
#         if self.root:
#             return self.root.find(info)
#         else:
#             return False

#     # return True if node successfully removed, False if not removed
#     def remove(self, info):
#         # If tree is empty
#         if self.root == None:
#             return False

#         # Deleting root node
#         if self.root.data == info:
#             # Root node has no children
#             if self.root.left is None and self.root.right is None:
#                 self.root = None
#                 return True
#             # Root node has left child
#             elif self.root.left and self.root.right is None:
#                 self.root = self.root.left
#                 return True
#             # Root node has right child
#             elif self.root.left is None and self.root.right:
#                 self.root = self.root.right
#                 return True
#             # Root node has two children
#             else:
#                 moveNode = self.root.right
#                 moveNodeParent = None
#                 while moveNode.left:
#                     moveNodeParent = moveNode
#                     moveNode = moveNode.left
#                 self.root.data = moveNode.data
#                 if moveNode.data < moveNodeParent.data:
#                     moveNodeParent.left = None
#                 else:
#                     moveNodeParent.right = None
#                 return True
#         # Find node to remove
#         parent = None
#         node = self.root
#         while node and node.data != info:
#             parent = node
#             if info < node.data:
#                 node = node.left
#             elif info > node.data:
#                 node = node.right
#         # Node not found
#         if node == None or node.data != info:
#             return False
#         # Node has no children
#         elif node.left is None and node.right is None:
#             if info < parent.data:
#                 parent.left = None
#             else:
#                 parent.right = None
#             return True
#         # Node has left child only
#         elif node.left and node.right is None:
#             if info < parent.data:
#                 parent.left = node.left
#             else:
#                 parent.right = node.left
#             return True
#         # Node has right child only
#         elif node.left is None and node.right:
#             if info < parent.data:
#                 parent.left = node.right
#             else:
#                 parent.right = node.right
#             return True
#         # Node has left and right child
#         else:
#             moveNodeParent = node
#             moveNode = node.right
#             while moveNode.left:
#                 moveNodeParent = moveNode
#                 moveNode = moveNode.left
#             node.data = moveNode.data
#             if moveNode.right:
#                 if moveNode.data < moveNodeParent.data:
#                     moveNodeParent.left = moveNode.right
#                 else:
#                     moveNodeParent.right = moveNode.right
#             else:
#                 if moveNode.data < moveNodeParent.data:
#                     moveNodeParent.left = None
#                 else:
#                     moveNodeParent.right = None
#             return True

#     # region recorridos
#     # return list of data elements PREORDER
#     def preorder(self):
#         if self.root:
#             return self.root.preorder([])
#         else:
#             return []

#     # return list of elements POSTORDER
#     def postorder(self):
#         if self.root:
#             return self.root.postorder([])
#         else:
#             return []

#     # return list of elements INORDER
#     def inorder(self):
#         if self.root:
#             return self.root.inorder([])
#         else:
#             return []

#     # endregion
