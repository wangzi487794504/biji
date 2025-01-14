#### [和为 K 的子数组](https://leetcode.cn/problems/subarray-sum-equals-k/)

* 给你一个整数数组 nums 和一个整数 k ，请你统计并返回 该数组中和为 k 的子数组的个数 。子数组是数组中元素的连续非空序列。

  ```java
  public class Day2 {
      public static void main(String[] args) {
         Day2 day2=new Day2();
          int i = day2.subarraySum(new int[]{-1, -1, 1}, 0);
          System.out.println(i);
      }
      public int subarraySum(int[] nums, int k) {
          //先写出前缀和数组
          int [] preSum = new int[nums.length + 1];
          //得出前缀和数组
          for (int i = 0; i < nums.length; i++) {
              preSum[i+1] = preSum[i ] + nums[i];
          }
          Map<Integer, Integer> map = new HashMap<>();
          int result=0;
          for (int i : preSum) {
              //把找和为k的，变为一个数-k得到另一个数存在这个数组中补
              result += map.getOrDefault(i-k, 0);
              map.merge(i , 1, Integer::sum);
          }
          return result;
      }
  }
  ```

  