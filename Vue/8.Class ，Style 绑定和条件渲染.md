####Class 与 Style 绑定

* 数据绑定的一个常见需求场景是操纵元素的 CSS class 列表和内联样式。因为 class 和 style 都是 attribute，我们可以和其他 attribute 一样使用 v-bind 将它们和动态的字符串绑定。

  * 但是，在处理比较复杂的绑定时，通过拼接生成字符串是麻烦且易出错的。因此，Vue 专门为 class 和 style 的 v-bind 用法提供了特殊的功能增强。
  * ==除了字符串外，表达式的值也可以是对象或数组。==

* 表达式值三种方式

  * class绑定之字符串形式 （确定样式只有一个，但是名字不确定）

    ```js
    <style>
        .static{
            border: 1px solid black;
            background-color: antiquewhite;
        }
        .big{
            width: 100px;
            height: 100px;
        }
        .small{
            width: 100px;
            height: 100px;
        }
    </style>
    <body>
        <div id="app">
            <div class="static small">{{msg}}</div>
            <!-- v-bind可以省略 -->
            <div class="static" v-bind:class="c1">{{msg}}</div>
        </div>
        <script>
            const vm = new Vue({
            el:'#app',
            data: {
                msg:'class绑定字符串',
                c1:'small'
            }
            })
        </script>
    </body>
    ```

  * class绑定之数组形式

    ```js
    <style>
        .static{
            border: 1px solid black;
            background-color: antiquewhite;
        }
        .big{
            width: 100px;
            height: 100px;
        }
        .small{
            width: 100px;
            height: 100px;
        }
        .text-danger{
            color: red;
        }
    </style>
    <body>
        <div id="app">
            <div class="static small">{{msg}}</div>
            <!-- v-bind可以省略，数组里可以是变量，也可以是字符串 -->
            <div class="static" :class="[c1,'text-danger']">{{msg}}</div>
        </div>
        <script>
            const vm = new Vue({
            el:'#app',
            data: {
                msg:'class绑定字符串',
                c1:'small'
            }
            })
        </script>
    </body>
    ```

    * 也可以用的数组变量(样式个数和名字都不确定使使用)

      ```js
      <body>
          <div id="app">
              <div class="static small">{{msg}}</div>
              <!-- v-bind可以省略，数组里可以是变量，也可以是字符串 -->
              <div class="static" :class="c1">{{msg}}</div>
          </div>
          <script>
              const vm = new Vue({
              el:'#app',
              data: {
                  msg:'class绑定字符串',
                  c1:['small','text-danger']
              }
              })
          </script>
      </body>
      ```

  * class绑定之对象形式（样式个数固定，样式名字固定，但是需要动态决定用不用）





* stytle绑定

  * 字符串形式

    ```js
    <body>
        <div id="app">
            <div class="static small" style="background-color:green ;">{{msg}}</div>
            <!-- v-bind可以省略，数组里可以是变量，也可以是字符串 -->
            <div class="static" :class="c1" :style="mystyle">{{msg}}</div>
        </div>
        <script>
            const vm = new Vue({
            el:'#app',
            data: {
                msg:'class绑定字符串',
                c1:{
                    //属性名和样式名要一致
                    small:true,
                },
                mystyle:'background-color:green ;'
            }
            })
        </script>
    </body
    ```

  * 对象形式

    ```js
    <body>
        <div id="app">
            //注意，直接写中间的-一定要改为驼峰，并且加单引号
            <div class="static small" :style="backgroundColor:'green' ;">{{msg}}</div>
            <!-- v-bind可以省略，数组里可以是变量，也可以是字符串 -->
            <div class="static" :class="c1" :style="mystyle">{{msg}}</div>
        </div>
        <script>
            const vm = new Vue({
            el:'#app',
            data: {
                msg:'class绑定字符串',
                c1:{
                    //属性名和样式名要一致
                    small:true,
                },
                mystyle:{'background-color':'green'}
            }
            })
        </script>
    </body>
  ```
  
* 数组形式
  
    ```js
    <body>
        <div id="app">
            <div class="static small" style="background-color:green ;">{{msg}}</div>
            <!-- v-bind可以省略，数组里可以是变量，也可以是字符串 -->
            <div class="static" :class="c1" :style="mystyle">{{msg}}</div>
        </div>
        <script>
            const vm = new Vue({
            el:'#app',
            data: {
                msg:'class绑定字符串',
                c1:{
                    //属性名和样式名要一致
                    small:true,
                },
                mystyle:[{'background-color':'green'}]
            }
            })
        </script>
    </body>
  ```
  
    



* 条件渲染

  * v-if   v-else-if   v-else  中间不能断开

    ```js
    <body>
        <div id="app">
            <!-- v-if为true渲染到界面上，false是不会渲染到界面上 -->
            <div v-if=""true>{{msg}}</div>
            <button @click="counter++">点击我加1</button>
            <h3>{{counter}}</h3>
            <img :src="imgpath1" alt="" srcset="" v-if="counter % 2 === 1">
            <!-- 为了提高效率，可以使用else，而不是在写一个判断语句 -->
            <img :src="imgpath2" alt="" srcset="" v-else>
    
            温度：<input type="number" name="" id="" v-model="temp">
            天气：<span v-if="temp <= 10">寒冷</span>
            <span v-else-if="temp >10 && temp <=25"</span>>凉爽</span>
            <span v-else>炎热</span>
        </div>
        <script>
            const vm = new Vue({
            el:'#app',
            data: {
                msg:'条件渲染',
                counter:1,
                imgpath1:'H:\\my APP\\MATR-main4_20\\fusion result\\1.png',
                imgpath2:'H:\\my APP\\MATR-main4_20\\fusion result\\2.png'
            }
            })
        </script>
    </body>
    ```

  * 还有一个条件渲染 v-show,他和v-if一样的效果

    * 不同之处在于 `v-show` 会在 DOM 渲染中保留该元素；`v-show` 仅切换了该元素上名为 `display` 的 CSS 属性。
    * `v-show` 不支持在 ` 元素上使用，也不能和 `v-else` 搭配使用。

  * 注意点： 因为 `v-if` 是一个指令，他必须依附于某个元素。但如果我们想要切换不止一个元素呢？在这种情况下我们可以在一个 ` 元素上使用 `v-if`，这只是一个不可见的包装器元素，最后渲染的结果并不会包含这个 ` 元素。 

    ```js
    <template v-if="ok">
      <h1>Title</h1>
      <p>Paragraph 1</p>
      <p>Paragraph 2</p>
    </template>
    ```

    



* 列表渲染

  *  我们可以使用 `v-for` 指令基于一个数组来渲染一个列表。`v-for` 指令的值需要使用 `item in items` 形式的特殊语法，其中 `items` 是源数据的数组，而 `item` 是迭代项的**别名**： 

    ```js
    <body>
        <div id="app">
            <ul>
                <li v-for="item in items">
                    {{ item }}
                </li>
            </ul>
        </div>
        <script>
            const vm = new Vue({
            el:'#app',
            data: {
                msg:'条件渲染',
                items:['张三','李四','王五']
            }
            })
        </script>
    </body>
    ```

    * 不仅可以用in，也可以用of
    * 完整语法  item,index  of items 还有个位置索引

  * 遍历数组中的对象

    ```js
    <body>
        <div id="app">
            <ul>
                <li v-for="item in items">
                    {{ item.message }}
                </li>
            </ul>
        </div>
        <script>
            const vm = new Vue({
            el:'#app',
            data: {
                msg:'条件渲染',
                items:[{ message: 'Foo' }, { message: 'Bar' }]
            }
            })
        </script>
    </body>
    ```

  * 遍历对象

    ```js
    <body>
            <!-- 遍历对象 -->
            <ul>
                <li v-for="(value,propertyName) of yObject">
                    {{value}},{{propertyName}}
                </li>
            </ul>
        </div>
        <script>
            const vm = new Vue({
            el:'#app',
            data: {
                msg:'条件渲染',
                items:[{ message: 'Foo' }, { message: 'Bar' }],
                yObject:{
                    title: 'How to do lists in Vue',
                    author: 'Jane Doe',
                    publishedAt: '2016-04-10'
                }
            }
            })
        </script>
    ```

  * 遍历字符串和指定的次数

    ```js
    <body>
            <!-- 遍历字符串 -->
            <ul>
                <li v-for="(value, index) of strs">
                    {{value}},{{index}}
                </li>
            </ul>
            <!-- 遍历指定的次数 -->
            <ul>
                <li v-for="(value, index) in counter">{{value}},{{index}}</li>
            </ul>
        </div>
        <script>
            const vm = new Vue({
            el:'#app',
            data: {
                msg:'条件渲染',
                items:[{ message: 'Foo' }, { message: 'Bar' }],
                yObject:{
                    title: 'How to do lists in Vue',
                    author: 'Jane Doe',
                    publishedAt: '2016-04-10'
                },
                strs:"asaswdxsecdc",
                counter:10
            }
            })
        </script>
    </body>
    ```

    