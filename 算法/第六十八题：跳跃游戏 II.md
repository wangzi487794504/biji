#### [跳跃游戏 II](https://leetcode.cn/problems/jump-game-ii/)

* 给定一个长度为 `n` 的 **0 索引**整数数组 `nums`。初始位置为 `nums[0]`。

* 每个元素 `nums[i]` 表示从索引 `i` 向后跳转的最大长度。换句话说，如果你在 `nums[i]` 处，你可以跳转到任意 `nums[i + j]` 处:

  - `0 <= j <= nums[i]` 
  - `i + j < n`

* 返回到达 `nums[n - 1]` 的最小跳跃次数。生成的测试用例可以到达 `nums[n - 1]`。

  ```java
  class Solution {
      public  int jump(int[] nums) {
          //贪心
          int time=0;
          int mx=0;
          //记录最新的mx
          int position=0;
          for (int i = 0; i < nums.length-1; i++) {
              mx=Math.max(mx,nums[i]+i);
              if (i==position){
                  time++;
                  position=mx;
                  if (position >= nums.length - 1) {
                  break;
              }
              }
              
          }
          return time;
      }
  }
  ```

  