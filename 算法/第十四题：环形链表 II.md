#### 环形链表2

* 给定一个链表的头节点  `head` ，返回链表开始入环的第一个节点。 *如果链表无环，则返回 `null`。*

* 如果链表中有某个节点，可以通过连续跟踪 `next` 指针再次到达，则链表中存在环。 为了表示给定链表中的环，评测系统内部使用整数 `pos` 来表示链表尾连接到链表中的位置（**索引从 0 开始**）。如果 `pos` 是 `-1`，则在该链表中没有环。**注意：`pos` 不作为参数进行传递**，仅仅是为了标识链表的实际情况。

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
      public ListNode detectCycle(ListNode head) {
          //首先定义快指针和慢指针
          ListNode fastNode=new ListNode();
          ListNode slowNode=new ListNode();
          fastNode=head;
          slowNode=head;
          while (fastNode!=null && fastNode.next!=null){
              //相当于每次比他快一步
              fastNode=fastNode.next.next;
              slowNode=slowNode.next;
              if (fastNode==slowNode){
                  //相遇之后，根据公式求相遇节点
                  //相遇，慢指针是x步，快指针必定是2x步。
                  //假设环长为b，则2x-x=nb，即是快指针比慢指针多走的
                  //则慢指针的路程x=nb，假设没进环的长度是a
                  //则慢指针走进环里面的指针是nb-a
                  //如果再走a步，一定是环的起点，所以让一个指针重头再走a步
                  fastNode=head;
                  while (fastNode!=slowNode){
                      fastNode=fastNode.next;
                      slowNode=slowNode.next;
                  }
                  return fastNode;
              }
          }
          return null;
      }
  }
  ```

  