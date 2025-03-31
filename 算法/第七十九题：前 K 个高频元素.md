#### [前 K 个高频元素](https://leetcode.cn/problems/top-k-frequent-elements/)

* 给你一个整数数组 `nums` 和一个整数 `k` ，请你返回其中出现频率前 `k` 高的元素。你可以按 **任意顺序** 返回答案。

  ```java
  class Solution {
      public int[] topKFrequent(int[] nums, int k) {
          HashMap<Integer,Integer> hashMap=new HashMap<>();
          for (int num : nums) {
              hashMap.put(num,hashMap.getOrDefault(num,0)+1);
          }
          PriorityQueue<Map.Entry<Integer,Integer>> queue=new PriorityQueue<>((o1,o2)-> o2.getValue()-o1.getValue());
          Set<Map.Entry<Integer, Integer>> entries = hashMap.entrySet();
          for (Map.Entry<Integer, Integer> entry : entries) {
              queue.offer(entry);
          }
          int[] result=new int[k];
          for (int i = 0; i < k; i++) {
             result[i]= queue.poll().getKey();
          }
          return result;
      }
  }
  ```

  