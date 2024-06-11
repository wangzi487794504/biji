#### Vue事件绑定

* 点击事件@click

  ```js
  <body>
      <div id="app">
          <h1>{{msg}}</h1>
          <!-- 原生js -->
          <button onclick="alert('hello')">hello</button>\
          <!-- vue -->
          <button v-on:click="sayhello()">hello</button>
          <!-- v-on简写 -->
          <button @click="sayhello()"></button>
          <!-- 继续简写，如果不传递任何参数，括号可以省略 -->
          <button @click="sayhello"></button>
          <!-- vue在调用回调函数时，会自动给回调函数传递一个对象，这个对象是当前发生的事件对象 -->
          <button @click="sayok()"></button>
          <!--如果本身有参数，需要使用$event传过去,vue看见$even会以对象的形式传过去  -->
          <button @click="saywhat('jack',$event)"></button>
      </div>
       <!--
          回顾Vue指令格式
          <标签 v-指令名：参数名='表达式'>{{插值语法}}
          
          </标签>
          表达式可以使常量，js表达式，vue管理的实例
          在vue中所关联的回调函数，需要在vue实例的methods中进行定义
          -->
      <script>
         
           const vm = new Vue({
           el:'#app',
           data: {
              msg:'Vue事件绑定'
           },
           methods: {
              sayhello:function(){
                  alert('hello')
              },
              sayok:function(e){
                  console.log(e);
                  alert('hello')
              },
              saywhat:function(a,event){
                  console.log(a);
                  alert('hello')
              }
           },
           })
      </script>
  </body>
  ```

  

* 回调函数中的this

  ```js
  <body>
      <div id="app">
          <h1>{{msg}}</h1>
          <h1>计数器：{{count}}</h1>
          <!-- 变量写法 -->
          <h1 @click="count++">点击我加一</h1>
          <!-- 函数写法 -->
          <h1 @click="add">函数点击我加一</h1>
      </div>
      <script>
          const vm = new Vue({
          el:'#app',
          data: {
              msg:'事件回调函数的this',
              count:0
          },
          methods: {
              add(){
                  console.log(vm==this);//true
                  //通过代理模式访问count
                  this.count++
                  //直接用count肯定不对，都不是一个对象的
                  //也可以使用vm访问，考虑以后组件开发一般不使用
              },
              //箭头函数中没有this，箭头函数的this是从父级作用域继承过来的，对于当前程序来说，父级作用域就是window
              add2:()=>{
                  //this.count++在箭头函数不行
              }
          },
          })
      </script>
  </body>
  ```

  



* methods方法的原理

  * 1.methods对象的方法可以通过vm去访问吗
    * 可以
  * 2.methods对象中的方法有没有做数据代理
    * 做了

* 事件修饰符

  * 以前阻止事件的默认行为，使用event.preventDefault();

    ```js
    <body>
        <div id="app">
            <h1>{{msg}}</h1>
            <a href="https:baidu.com" @click="yi">去百度</a>
        </div>
        <script>
            const vm = new Vue({
            el:'#app',
            data: {
                msg:"事件修饰符"
            },
            methods: {
                yi(event){
                    alert('去百度')
                    //阻止事件的默认行为
                    event.preventDefault();
                }
            },
            })
        </script>
    </body>
    ```

  * 现在可以使用vue的事件修饰符

    ```html
        <div id="app">
            <h1>{{msg}}</h1>
            <a href="https:baidu.com" @click.prevent="yi">去百度</a>
        </div>
    ```

    

  * 在vue官方手册中写到在处理事件时调用 `event.preventDefault()` 或 `event.stopPropagation()` 是很常见的。尽管我们可以直接在方法内调用，==但如果方法能更专注于数据逻辑而不用去处理 DOM 事件的细节会更好。==为解决这一问题，Vue 为 `v-on` 提供了**事件修饰符**。修饰符是用 `.` 表示的指令后缀，包含以下这些：

    * `.stop`

      ```js
              <!-- 事件冒泡，只让事件冒泡到第二层 -->
              <div @click="yi">
                  <div  @click.stop="er">
                      <button  @click="san">事件冒泡</button>
                  </div>
              </div>
      ```

      

    * `.prevent`

    * `.self`

      ```js
      <!-- 仅当 event.target 是元素本身时才会触发事件处理器 -->
      <!-- 例如：事件处理器不来自子元素 -->
      <div @click.self="doThat">...</div>
      ```

      

    * `.capture`

      ```js
              <!-- 添加事件监听器包括两种不同的模式
                  一种是从内到外添加（事件冒泡排序）
                  一种是从外到内添加（事件捕获模式）
              -->
      <div @click.capture="san">
           <div  @click.capture="er">
              <button  @click.capture="yi">从外到内添加（事件捕获模式</button>
           </div>
      </div>
      ```

      

    * `.once`

      ```js
      <!-- 点击事件最多被触发一次 -->
      <a @click.once="doThis"></a>
      ```

      

    * `.passive`

      ```js
      passive`和`.prevent`是对立的，它是解除阻止，并且优先执行事件的默认行为
      <!-- 滚动事件的默认行为 (scrolling) 将立即发生而非等待 `onScroll` 完成 -->
      <!-- 以防其中包含 `event.preventDefault()` -->
      <div @scroll.passive="onScroll">...</div>
      ```

      

    * 注意

      ```j
      使用修饰符时需要注意调用顺序，因为相关代码是以相同的顺序生成的。因此使用 @click.prevent.self 会阻止元素及其子元素的所有点击事件的默认行为，而 @click.self.prevent 则只会阻止对元素本身的点击事件的默认行为。
      请勿同时使用 .passive 和 .prevent，因为 .passive 已经向浏览器表明了你不想阻止事件的默认行为。如果你这么做了，则 .prevent 会被忽略，并且浏览器会抛出警告。
      ```

* 按键修饰符

  *  在监听键盘事件时，我们经常需要检查特定的按键。Vue 允许在 `v-on` 或 `@` 监听按键事件时添加按键修饰符。 

  * 以前需要使用if语句判断是不是需要的符号

    ```js
    <div id="app">
            <h1>{{msg}}</h1>
            <input type="text" name="" id="" @keyup="getInfo">
     </div>  
    <script>
            const vm = new Vue({
            el:'#app',
            data: {
                msg:"按键修饰"
            },
            methods: {
                getInfo(event){
                    //当用户输入回车键
                    if(event.keyCode ===13){
                        console.log(event.target.value);
                    }
                }
            },
            })
        </script>
    ```

  * 现在可以直接用.enter就可以

    ```js
        <div id="app">
            <h1>{{msg}}</h1>
            <input type="text" name="" id="" @keyup.enter="getInfo">
        </div>
    ```

  * 常见的按键修饰符

    * `.enter`
    * `.tab`
    * `.delete` (捕获“Delete”和“Backspace”两个按键)
    * `.esc`
    * `.space`
    * `.up`
    * `.down`
    * `.left`
    * `.right`
    * 注意：tab键无法触发keyup事件。只能触发keydown事件

  * 如果是其他按键值

    * 通过event.key获取这个键的真实名字
    * 第二步：将这个真实名字以 kebab-case 形式。（比如名字是pagedown 命名之后为page-down） 

  * 自定义按键的名字

    ```js
            //也可以自定义按键修饰符，jie代表回车键
            Vue.config.keyCode.jie=13
    ```

  * 特殊的系统修饰键

    * `.ctrl`
    * `.alt`
    * `.shift`
    * `.meta`
    *  在 Mac 键盘上，meta 是 Command 键 (⌘)。在 Windows 键盘上，meta 键是 Windows 键 (⊞)。在 Sun 微机系统键盘上，meta 是钻石键 (◆)。 
    *  ==系统按键修饰符和常规按键不同。与 `keyup` 事件一起使用时，该按键必须在事件发出时处于按下状态。换句话说，`keyup.ctrl` 只会在你仍然按住 `ctrl` 但松开了另一个键时被触发。若你单独松开 `ctrl` 键将不会触发。 keydown不需要这样==
      * **当你只想按下ctrl和i执行，就用@keyup.ctrl.i**