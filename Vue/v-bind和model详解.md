#### v-bind详解

* 实现一个绑定

  ```html
  <body>
      <div id="app">
          <span v-bind:wang="msg"></span>
      </div>
  <script>
      const vm = new Vue({
      el:'#app',
      data: {
          msg:'aa'
      }
      })
  </script>
  </body>
  ```

  * 在浏览器的真实渲染为

    ```java
    <span wang="aa"></span>
    ```

  * 所以建议冒号后面的参数写html的属性，就可以实现动态绑定

    ```html
    <img v-bind:src="msg">
    ```

  * v-bind简写，直接使用:

    ```html
    <img :src="msg">
    ```

  * 以前可以src=“{{}}”，现在已经被淘汰了

  * 他可以使用在任何html标签

* v-model

  * 它是双向绑定

  * 可以使用在表单标签上，其他不行

    <img src="v-bind%E8%AF%A6%E8%A7%A3.assets/1720160763151.png" alt="1720160763151" style="zoom:50%;" />

