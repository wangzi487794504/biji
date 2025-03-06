#### [路径总和 III](https://leetcode.cn/problems/path-sum-iii/)

* 给定一个二叉树的根节点 `root` ，和一个整数 `targetSum` ，求该二叉树里节点值之和等于 `targetSum` 的 **路径** 的数目。

  **路径** 不需要从根节点开始，也不需要在叶子节点结束，但是路径方向必须是向下的（只能从父节点到子节点）。
  
  ```java
  /**
   * Definition for a binary tree node.
   * public class TreeNode {
   *     int val;
   *     TreeNode left;
   *     TreeNode right;
   *     TreeNode() {}
   *     TreeNode(int val) { this.val = val; }
   *     TreeNode(int val, TreeNode left, TreeNode right) {
   *         this.val = val;
   *         this.left = left;
   *         this.right = right;
   *     }
   * }
   */
  class Solution {
      public int pathSum(TreeNode root, int targetSum){
          //得到前缀和
         
          HashMap<Integer,Integer> hashMap=new HashMap<>();
          hashMap.put(0,1);
          bianli(root,0,targetSum,hashMap);
          return num;
      }
      int num;
      public void bianli(TreeNode root,int sum,int targetSum,HashMap<Integer,Integer> hashMap) {
          //前缀和加hsashmap
          //写先序遍历一下
          if (root!=null){
              sum+=root.val;
              num+=hashMap.getOrDefault(sum - targetSum,0);
              hashMap.merge(sum ,1,Integer::sum);
              bianli(root.left,sum,targetSum,hashMap);
              bianli(root.right,sum,targetSum,hashMap);
              hashMap.merge(sum ,-1,Integer::sum);
          }
      }
  } 
  ```
  
  