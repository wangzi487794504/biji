#### 环形链表

* 找是不是环形链表

  ```java
  /**
   * Definition for singly-linked list.
   * class ListNode {
   *     int val;
   *     ListNode next;
   *     ListNode(int x) {
   *         val = x;
   *         next = null;
   *     }
   * }
   */
  public class Solution {
      public boolean hasCycle(ListNode head) {
          //使用快慢指针，他们两个相遇就是循环链表
          ListNode fast=head;
          ListNode slow=head;
          while(fast!=null && fast.next!=null){
              fast=fast.next.next;
              slow=slow.next;
              if(fast==slow){
                  return true;
              }
          }
          return false;
      }
  }
  ```

  