#### [删除链表的倒数第 N 个结点](https://leetcode.cn/problems/remove-nth-node-from-end-of-list/)

* 给你一个链表，删除链表的倒数第 `n` 个结点，并且返回链表的头结点。

* 思路：先让一个指针移动N个位置，两个指针在一起移动，第一个结束第二个就是倒数第N

  ```java
  /**
   * Definition for singly-linked list.
   * public class ListNode {
   *     int val;
   *     ListNode next;
   *     ListNode() {}
   *     ListNode(int val) { this.val = val; }
   *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
   * }
   */
  class Solution {
      public ListNode removeNthFromEnd(ListNode head, int n) {
          ListNode domNode=new ListNode();
          domNode.next=head;
          ListNode conTemp= new ListNode();
          ListNode secondTemp=new ListNode();
          conTemp=domNode;
          secondTemp=domNode;
          //因为有个虚拟节点，相当于真实节点的n-1
          while (n>0 && secondTemp.next!=null){
              n--;
              secondTemp=secondTemp.next;
          }
          while (secondTemp.next!=null){
              conTemp=conTemp.next;
              secondTemp=secondTemp.next;
          }
          conTemp.next=conTemp.next.next;
          return domNode.next;
      }
  }
  ```

  