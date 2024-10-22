#### 插值语法

* 插值语法能放什么

  * 常量,data里声明的变量，数组，函数。js表达式

  * 属性内部不能插值，要用指令才行

  *  模板表达式都被放在沙盒中，只能访问[全局变量的一个白名单](https://github.com/vuejs/vue/blob/v2.6.10/src/core/instance/proxy.js#L9)，如 `Math` 和 `Date` 。你不应该在模板表达式中试图访问用户定义的全局变量。 

    * 白名单包括：'Infinity,undefined,NaN,isFinite,isNaN,' +'parseFloat,parseInt,decodeURI,decodeURIComponent,encodeURI,encodeURIComponent,' + 'Math,Number,Date,Array,Object,Boolean,String,RegExp,Map,Set,JSON,Intl,' +
          'require' // for Webpack/Browserify

    ```vue
    <body>
        <!-- 研究{{}}可以写什么 大前提在data中进行了声明，变量，函数,常量，运算符,js表达式都支持-->
        <div class="app">{{msg}}
            <h1>{{sayhello()}}</h1>
            <h1>{{1+1}}</h1>
            <h1>{{"hello"+"vue"}}</h1>
            <h1>{{"hello"+"vue"}}</h1>
            <h1>{{sex.split('').reverse().join('')}}</h1>
            <!-- 白名单 -->
            <h1>{{Date.now()}}</h1>
        </div>
        <script>
            new Vue({
                el:'.app',
                data:{
                    msg:'hello',
                    sayhello:function(){
                        console.log("hello")
                    },
                    sex:'man'
                }
            })
        </script>
    </body>
    ```

    



#### 指令语法

* Vue所有指令的名字都以v-作为前缀

* 所以指令写在html标签属性里面

*  指令的职责是，当表达式的值改变时，将其产生的连带影响，响应式地作用于 DOM。 

* 指令需要通过vue框架编译，不编译浏览器看不懂

* 格式：<HTML标签 v-指令名:参数=“表达式”>

  * 表达式能写的和插值一样，但不需要写{{}}
  * 不是所以有的指令都有参数和表达式
  * 有的指令只需要表达式，不需要参数

* v-once

  * **不需要表达式**
  * **详细**：只渲染元素和组件**一次**。随后的重新渲染，元素/组件及其所有的子节点将被视为静态内容并跳过。这可以用于优化更新性能。(只有加载界面那一次渲染，以后data变了也不会渲染)

* v-if

  * 根据表达式的值的 truthiness 来有条件地渲染元素。在切换时元素及它的数据绑定组件被销毁并重建。如果元素是 <template>，将提出它的内容作为条件块。

  ```vue
  <body>
      <!-- 研究{{}}可以写什么 大前提在data中进行了声明，变量，函数,常量，运算符,js表达式都支持-->
      <div class="app">{{msg}}
          <!-- 只渲染元素和组件**一次**。随后的重新渲染，元素/组件及其所
              有的子节点将被视为静态内容并跳过。这可以用于优化更新性能。 -->
          <h1 v-once>{{msg}}</h1>
          <!-- 根据表达式的值的 truthiness 来有条件地渲染元素。在切换时元素及它的数据绑定 
               组件被销毁并重建。如果元素是 <template>，将提出它的内容作为条件块。 -->
          <!-- false不会被渲染到界面上 -->
          <h1 v-if="true">{{msg}}</h1>
          <!-- <span xyz="hello">aa</span> -->
          <span v-bind:xyz="msg">aa</span>
          <img v-bind:src="path">
          <!-- 简写的动态数据绑定 -->
          <input type="text" name="usernamae" id="aa" :value="name">
          v-bind指令<input type="text" name="aa" id="aa" value="{{name}}">
          v-model指令<input type="text" name="sex" id="sex" v-model:value="{{sex}}">
      </div>
      <script>
          new Vue({
              el:'.app',
              data:{
                  msg:'hello',
                  sayhello:function(){
                      console.log("hello")
                  },
                  sex:'man',
                  path:'../img/fusion.bmp',
                  name:"zhangsan"
              }
          })
      </script>
  </body>
  ```

  

* v-bind
  *  动态地绑定一个或多个 attribute，或一个组件 prop 到表达式。 让标签属性产生一个动态效果
  * 编译前：<HTML标签 v-bind:参数=“表达式”> 编译后  <HTML标签 参数=“表达式的执行结果”> 
  * 因为这个命令很常用,vue提供了一种简写<HTML标签 :参数=“表达式”>
  * 是单向数据绑定
  * 适用范围：所有html标签
  
* v-model

  * 双向绑定（data和视图互相使用）
  * 适用范围：
    * input标签，select标签，textarea标签以及component。
    * 因为表单类的输入才会给用户提供输入的界面
    * 通常用在value属性上
    * 简写方式  v-model:value=“表达式” 变为  v-model:=“表达式”



#### MVVM思想

* M指Model（模型/数据）,V指视图，VM是视图模型（它是核心）。是前端非常流行的架构设计模式
* Vue虽然没有完全遵循，但基本符合
* MVVM提倡Model和View分离。
  * 如果数据不发生改动，数据发现任意的改动，就的写一大堆去改进Dom元素
  * 把这两个分离之后，出现了一个VM核心，当Model发生改动之后，VM自动更新View，当View发生改动之后，VM自动更新Model，再也不用去写操纵dom

![1703640850956](%E8%AF%AD%E6%B3%95.assets/1703640850956.png)··

```vue
<body>
    <!-- View V视图-->
    <div class="app">
        v-bind指令<input type="text" name="aa" id="aa" value="{{name}}">
    </div>
    <script>
        // 整个Vue实例就是VM
        new Vue({
            el:'.app',
            // Model M
            data:{
                msg:'hello',
                sayhello:function(){
                    console.log("hello")
                },
                sex:'man',
                path:'../img/fusion.bmp',
                name:"zhangsan"
            }
        })
    </script>
</body>
```

* 所以一般用vm表示Vue的实例，因为Vue实例代表了VM思想

  ```sql
  const vm = new Vue
  ```

  



#### vscode代码片段

* "Print to console": 是提示信息

* 双引号开始，双引号结束

* prefix是快捷字，定义输入什么字符敲回车会生成这个代码片段

* body里是写你需要的代码片段

* $数字是光标的定位顺序，按tab自动跑到下一个光标位置

* 双引号开始，双引号结束是生成代码的内容，一般一个双引号，一个逗号代表是一行代码的开始和结束

* description是代码片段的作用描述，和实际代码无关，只用于提示

  ```js
  	"Print to console": {
  		"prefix": "log",
  		"body": [
  			"console.log('$1');",
  			"$2"
  		],
  		"description": "Log output to console"
  	},
  	"创建一个Vue实例":{
  		"prefix": "vmobj",
  		"body": [
  			"const vm = new Vue({",
              "el:'#app',",
              "data: {}",
  			"})",
  		],
  		"description":"Vue描述"
  	}     
  ```

  * "创建一个Vue实例"是光标提示





#### Vue对象的属性

* 查看vm对象属性

  ![1703642543002](%E8%AF%AD%E6%B3%95.assets/1703642543002.png)



![1703642595382](%E8%AF%AD%E6%B3%95.assets/1703642595382.png)

* Vue属性很多，有的以$开始，有的以__开始
* ==所有的以$开始的属性，可以看作是公开的属性，这些属性是供程序员属性的==
* **所有以—开始的属性，可以看作是私有的属性，这些属性是Vue框架底层使用的，一般我们程序员不去使用****
* 也可以访问Vue实例对象的原型对象属性，如vm.$delete
* 有一个msg属性，可以访问其他对象，它使用了数据代理机制。
  * 必须先知道Object.defineProperty()方法，它是ES5新增的，作用给对象新增属性，这个新增的属性名叫啥
  
  * ==格式：Object.defineProperty(给哪个对象新增属性，新增的这个属性名叫啥,{给新增属性设置配置项})==
  
    ```vue
        <script>
            let phone={}
            //defineProperty有三个参数，第一个给哪个对象新增属性，新增的这个属性名叫啥，{给新增的属性设置相关的配置项key:value}
            Object.defineProperty(phone,'color',{
                value:'太空灰',
                // 允许属性修改
                writable:true,
                // 这两个方法不需要我们调用，当访问color或者修改color，会自动调用
                //当有get和set方法，value和writable都不能存在，但是上面两个配置项都不能存在，负责会报错
                //set方法是有一个参数的，接收你的赋值
                //不能写return this.color，负责会递归，因为this.color本身调用的就是get
                //get必须要有返回值
                get:function(){
    
                },
                set:function(){
    
                }
            })
        </script>
    ```
  
    * 当给属性复制的时候set方法被调用
  
    * get方法必须要有return
  
    * set方法是有一个参数的，接收你的赋值
  
    * 不能写return this.color，负责会递归，因为this.color本身调用的就是get
  
      ```sql
          <script>
              let phone={}
              // 临时变量
              let temp;
              //defineProperty有三个参数，第一个给哪个对象新增属性，新增的这个属性名叫啥，{给新增的属性设置相关的配置项key:value}
              Object.defineProperty(phone,'color',{
                  // value:'太空灰',
                  // // 允许属性修改
                  // writable:true,
                  // 这两个方法不需要我们调用，当访问color或者修改color，会自动调用
                  //当有get和set方法，value和writable都不能存在，但是上面两个配置项都不能存在，负责会报错
                  //set方法是有一个参数的
                  //不能写return this.color，负责会递归，因为this.color本身调用的就是get
                  //get必须要有返回值
                  get:function(){
                      return temp;
                  },
                  set:function(val){
                      temp=val;
                  }
              })
          </script>
      ```
  
      ![1711949021137](%E8%AF%AD%E6%B3%95.assets/1711949021137.png)



* 什么是数据代理机制

  * 通过访问代理对象的属性来间接访问目标对象的属性

  * 数据代理对象的实现需要依靠：Object.defineProperty()方法

    ```vue
        <script>
            //目标对象
            let target={
                name:'zhangsan'
            }
            //代理对象
            let proxy={}
            //如果要实现数据代理机制的话，就需要给proxy新增一个name属性
            //注意：代理对象新增的整个属性的名字和目标属性名要一致
            Object.defineProperty(proxy,'name',{
                get:function(){
                    //间接访问目标对象的属性
                    return target.name;
                },
                set:function(val){
                    target.name=val;
                }
            })   
        </script>
    ```

  * 因此，在vue中

    ```html
            const vm = new Vue({
            el:'#app',
            data: {
                name:'zhanghsan'
            }
            })
    ```

    等价于

    ```sql
            let target= {
                name:'zhanghsan'
            }
            const proxy = new Vue({
            el:'#app',
            data: target
            })
    ```

  * ES6新特性，在对象中的函数，冒号和function是可以不要的

    ```vue
            const proxy = new Vue({
            el:'#app',
            data: target,
            set(){
    
            },
            get(){
    
            }
            })
    ```

* vue种的数据展示九十通过代理模式实现

  ```html
      <div id="app"> <h1>{{msg}}</h1></div>
      <script>
          const proxy = new Vue({
          el:'#app',
          data: {
              msg:'hello vue'
          }
          })
      </script>
  ```

  *  可以看到vue也有一个msg属性，她间接的访问目标对象的data里的msg属性

    ![1711953090059](%E8%AF%AD%E6%B3%95.assets/1711953090059.png)



* ==当data对象以美元符号或者下划线开始，vue不会给你代理，如果给你做代理，可能会和vue框架自身的属性名冲突。==

* data既可以是一个函数，也可以是一个对象