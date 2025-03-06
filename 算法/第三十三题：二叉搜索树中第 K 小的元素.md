#### [二叉搜索树中第 K 小的元素](https://leetcode.cn/problems/kth-smallest-element-in-a-bst/)

* 给定一个二叉搜索树的根节点 `root` ，和一个整数 `k` ，请你设计一个算法查找其中第 `k` 小的元素（从 1 开始计数）。

  ```java
  class Solution {
      int h=0;
      public int kthSmallest(TreeNode root, int k) {
          this.h=k;
          return dfs(root);
      }
      public int dfs(TreeNode root){
                  //中序遍历
          if (root != null) {
              // 遍历左子树
              int value=dfs(root.left);
              if(value!=-1){
                  return value; 
              }
              // 访问根节点
              h--;
              if(h==0){
                  return root.val;
              }
              // 遍历右子树，左根没有，一定在右边
              return  dfs(root.right);
          }
          return -1;
      } 
  }
  ```

  