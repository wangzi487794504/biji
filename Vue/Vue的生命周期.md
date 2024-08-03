#### Vue的生命周期

* Vue的生命周期是指：vm对象从创建到最终销毁的整个过程

* ==Vue的生命周期可以被划分为4个阶段:初始阶段、挂载阶段、更新阶段、销毁阶段。每个阶段会调用两个钩子函数。==两个钩子函数名的特点: beforeXxx()、xxxed().

  * 初始阶段：生成虚拟dom，两个钩子函数：

    * beforeCreate()创建前，此时是访问不到数据，他要进行动态代理

    * created() 创建后。查看是否存在el配置项，el有，template也有,最终编译template模板语句。``el有，template没有，最终编译el模板语句。el有. template也有,最终编译```template模板语句``。el有. template没有,最终编译el模板语句。==el没有的时候，需要手动调用vm.$mount(el)进行手动挂载，然后流程才能继续。否则就会在这个流程卡主。此时如果template没有，最终编译为el模板语句==

      ```js
      <body>
          <div id="app">
             <h1> {{mag}}</h1>
          </div>
          <script type="text/javascript" src="js/vue.js">
          </script>
          <script>
              //此时页面会显示template渲染的内容
              var vm = new Vue({
                  el: '#app',
                  template: msg1,
                  data: {
                      mag: 'hello vue',
                      msg1: '<h1>html</h1>',
                      num: 0,
                      uname: '',
                      password: ''
                  }
              });
          </script>
      </body>
      ```

      

  * 挂载阶段：真实dom，两个钩子函数：

    * beforeMount()挂载前，此时你操作dom，真实的被修改了，但是内存虚拟的会覆盖真实的。所以这个函数就是虚拟的转成真实的
    * mounted() 挂载后，这里改可以生效，因为已经转换成真实的了。

  * 更新阶段：数据改变时执行。两个钩子函数：

    * beforeUpdate()更新前，此时只更新了内存dom，还没有更新真实的dom
    * updated() 更新后，此时用diff算法进行比对，更新真实dom

  * 销毁阶段：调用this.$.destroy()两个钩子函数：

    * beforeDestroy()销毁前，==他就是解绑前，虽然此时还没有卸载，但已经不让用了==
    * destroyed()销毁后,他不是释放vm的空间，==它是卸载监视器，子组件、自定义事件==

    ![1720314763253](Vue%E7%9A%84%E7%94%9F%E5%91%BD%E5%91%A8%E6%9C%9F.assets/1720314763253.png)

    ```js
    <script>
            Vue.cofig.keyCode.aaa = 65
            var vm = new Vue({
                el: '#app',
                data: {
                    mag: 'hello vue',
                    msg1: '<h1>html</h1>',
                    num: 0,
                    uname: '',
                    password: ''
                },
                //初始阶段创建前
                beforeCreate() {
                    console.log('初始阶段创建前');
                    
                },
                //初始阶段创建后
                created() {
                    console.log('初始阶段创建后');
                },
                //挂载阶段挂载前
                beforeMount() {
                    console.log('挂载阶段挂载前');
                },
                //挂载阶段挂载后
                mounted() {
                    console.log('挂载阶段挂载后');
                },
                //更新阶段更新前
                beforeUpdate() {
                    console.log('更新阶段更新前');
                },
                //更新阶段更新后
                updated() {
                    console.log('更新阶段更新后');
                },
                //销毁阶段销毁前
                beforeDestroy() {
                    console.log('销毁阶段销毁前');
                },
                //销毁阶段销毁后
                destroyed() {
                    console.log('销毁阶段销毁后');
                },
    
            });
        </script>
    ```

    