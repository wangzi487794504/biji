#### [LRU 缓存](https://leetcode.cn/problems/lru-cache/)

* 请你设计并实现一个满足 [LRU (最近最少使用) 缓存](https://baike.baidu.com/item/LRU) 约束的数据结构。

* 实现 `LRUCache` 类：

  - `LRUCache(int capacity)` 以 **正整数** 作为容量 `capacity` 初始化 LRU 缓存
  - `int get(int key)` 如果关键字 `key` 存在于缓存中，则返回关键字的值，否则返回 `-1` 。
  - `void put(int key, int value)` 如果关键字 `key` 已经存在，则变更其数据值 `value` ；如果不存在，则向缓存中插入该组 `key-value` 。如果插入操作导致关键字数量超过 `capacity` ，则应该 **逐出** 最久未使用的关键字。

* 函数 `get` 和 `put` 必须以 `O(1)` 的平均时间复杂度运行。

  ```java
  class LRUCache {
      private static class Node{
          public int key,value;
          Node prev,next;
          Node(int k,int v){
              key=k;
              value=v;
          }
      }
      private final int capacity;
      private final Node dummy=new Node(0,0);
      private final HashMap<Integer,Node> keyToNode=new HashMap<>();
  
      public LRUCache(int capacity) {
          this.capacity=capacity;
          dummy.prev=dummy;
          dummy.next=dummy;
      }
      
      public int get(int key) {
          Node node=getNode(key);
          return node==null ? -1 : node.value;
      }
      
      public void put(int key, int value) {
          //查看有没有
          Node node =getNode(key);
          if(node!=null){
              //更新值
              node.value=value;
              return;
          }
          //没有
          node=new Node(key,value);
          //放到hash上
          keyToNode.put(key,node);
          pushFirst(node);
          //看看有没有超过容量
          if(keyToNode.size()>capacity){
              //移除最老的元素
              Node lateNode=dummy.prev;
              //移除hashmap
              keyToNode.remove(lateNode.key);
              //移除链表
              remove(lateNode);
          }
      
  
      }
      public Node getNode(int key){
          if(!keyToNode.containsKey(key)){
              return null;
          }
          //拿出来这本书
          Node node =keyToNode.get(key);
          //移除这个位置，然后放最上面
          remove(node);
          pushFirst(node);
          return node;
      }
      public void remove(Node node){
          node.prev.next=node.next;
          node.next.prev=node.prev;
      }
      public void pushFirst(Node node){
          node.next=dummy.next;
          dummy.next.prev=node;
          dummy.next=node;
          node.prev=dummy;
      }
  }
  
  /**
   * Your LRUCache object will be instantiated and called as such:
   * LRUCache obj = new LRUCache(capacity);
   * int param_1 = obj.get(key);
   * obj.put(key,value);
   */