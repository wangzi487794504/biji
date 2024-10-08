#### TCP/IP协议簇

* 计算机与网络设备要相互通信，双方就必须基于相同的方法。比如，如何探测到通信目标、由哪一边先发起通信、使用哪种语言进行通信、怎样结束通信等规则都需要事先确定。不同的硬件、操作系统之间的通信，所有的这一切都需要一种规则。而我们就把这种规则称为协议(protocol)。
* TCP/IP协议族按层次分别分为以下4层：应用层、传输层、网络层和数据链路层。
* TCP/IP协议族内预存了各类通用的应用服务。比如，FTP（File Transfer Protocol，文件传输协议）和DNS（Domain Name System，域名系统）服务就是其中两类。
* 在传输层有两个性质不同的协议：TCP（Transmission Control Protocol，传输控制协议）和UDP（User Data Protocol，用户数据报协议）。
* 发送端在层与层之间传输数据时，每经过一层时必定会被打上一个该层所属的首部信息。反之，接收端在层与层传输数据时，每经过一层时会把对应的首部消去。这种把数据信息包装起来的做法称为封装(encapsulate)。
* IP地址指明了节点被分配到的地址，MAC地址是指网卡所属的固定地址。IP地址可以和MAC地址进行配对。IP地址可变换，但MAC地址基本上不会更改
* ARP是一种用以解析地址的协议，根据通信方的IP地址就可以反查出对应的MAC地址
* TCP位于传输层，提供可靠的字节流服务。所谓的字节流服务(Byte Stream Service)是指，为了方便传输，将大块数据分割成以报文段(segment)为单位的数据包进行管理。而可靠的传输服务是指，能够把数据准确可靠地传给对方。一言以蔽之，TCP协议为了更容易传送大数据才把数据分割，而且TCP协议能够确认数据最终是否送达到对方。
  * TCP协议采用了三次握手(three-way handshaking)策略。用TCP协议把数据包送出去后，TCP不会对传送后的情况置之不理，它一定会向对方确认是否成功送达。握手过程中使用了TCP的标志(flag)——SYN(synchronize)和ACK(acknowledgement)。发送端首先发送一个带SYN标志的数据包给对方。接收端收到后，回传一个带有SYN/ACK标志的数据包以示传达确认信息。最后，发送端再回传一个带ACK标志的数据包，代表“握手”结束。若在握手过程中某个阶段莫名中断，TCP协议会再次以相同的顺序发送相同的数据包。
* DNS(Domain Name System)服务是和HTTP协议一样位于应用层的协议。它提供域名到IP地址之间的解析服务。