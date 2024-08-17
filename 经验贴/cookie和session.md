#### cookie和session

* 当服务器tomcat第一次接收到客户端的请求时，会开辟一块独立的session空间，建立一个session对象，同时会生成一个session id，通过响应头的方式保存到客户端浏览器的cookie当中。以后客户端的每次请求，都会在请求头部带上这个session id，这样就可以对应上服务端的一些会话的相关信息，比如用户的登录状态。
* 如果没有客户端的Cookie，Session是无法进行身份验证的。
* 当服务端从单体应用升级为分布式之后，cookie+session这种机制要怎么扩展?
  * session黏贴: 在负载均衡中，通过一个机制保证同一个客户端的所有请求都会转发到同一个tomcat实例当中。
    * 问题:当这个tomcat实例出现问题之后，请求就会被转发到其他实例，这时候用户的session信息就丢了。
  * 2、session复制:当一个tomcat实例上保存了session信息后，主动将session 复制到集群中的其他实例。
    * 问题: 复制是需要时间的，在复制过程中，容易产生session信息丢失。
  * 3、session共享: 就是将服务端的session信息保存到一个第三方中，比如Redis