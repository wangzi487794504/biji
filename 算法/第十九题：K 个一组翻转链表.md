#### [K 个一组翻转链表](https://leetcode.cn/problems/reverse-nodes-in-k-group/)

* 给你链表的头节点 `head` ，每 `k` 个节点一组进行翻转，请你返回修改后的链表。

* `k` 是一个正整数，它的值小于或等于链表的长度。如果节点总数不是 `k` 的整数倍，那么请将最后剩余的节点保持原有顺序。

* 你不能只是单纯的改变节点内部的值，而是需要实际进行节点交换。

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
      public ListNode reverseKGroup(ListNode head, int k) {
          //双指针移动，移动K个，翻转
          //弄一个哨兵
          ListNode dummy=new ListNode(0);
          dummy.next=head;
          ListNode fast=dummy;
          ListNode slow=dummy;
          while(fast!=null){
  
              for(int i=0;i<k && fast!=null;i++){
                 fast=fast.next;
              }
              if(fast==null){
                  break;
              }
              //保存下面的位置
              ListNode start=fast.next;
              ListNode end=slow.next;
              //断开后面的,方便反转结尾判空
              fast.next=null;
              //翻转链表
              slow.next=reverseNode(end);
              //翻转成功再接回来
             // 连接反转后的当前组和下一组
             //因为翻转之后end跑到最后了
              end.next = start;
              // slow 移动到当前组的末尾（即反转前的起始节点，反转后变为末尾节点）
              slow = end;
              // fast 移动到下一组的起始位置
              fast = end;
          }
          return dummy.next;
      }
      public ListNode reverseNode(ListNode head){
          ListNode pre=null;
          ListNode cur=head;
          while(cur!=null){
              ListNode temp=cur.next;
              cur.next=pre;
              pre=cur;
              cur=temp;
          }
          return pre;
      }
  }
  ```

  