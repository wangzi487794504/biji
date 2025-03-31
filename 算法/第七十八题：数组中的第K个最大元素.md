#### [数组中的第K个最大元素](https://leetcode.cn/problems/kth-largest-element-in-an-array/)

* 给定整数数组 `nums` 和整数 `k`，请返回数组中第 `**k**` 个最大的元素。
* 请注意，你需要找的是数组排序后的第 `k` 个最大的元素，而不是第 `k` 个不同的元素。
* 你必须设计并实现时间复杂度为 `O(n)` 的算法解决此问题。

```java
class Solution {
    public int findKthLargest(int[] nums, int k) {
        //建立优先级堆
        PriorityQueue<Integer> queue=new PriorityQueue<>();
        for (int num : nums) {
            queue.add(num);
            //小根堆
            if (queue.size() > k) {
                queue.poll();
            }
        }
        return queue.peek();
    }
}
```

