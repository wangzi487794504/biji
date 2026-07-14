#### 虚拟dom

* 虚拟dom是指在内存当中的dom对象

* diff算法：这是一种快速的比较两个事物的不同之处

  * 举例

    ```js
    <body>
        <div id="app">
            <h1>{{msg}}</h1>
            <table>
                <tr>
                    <th>序号</th>
                    <th>英雄</th>
                    <th>能量值</th>
                    <th>选择</th>
                </tr>
                <!-- 
                    v-for指令所在的标签中，还有一个非常重要的属性：
                        :key
                    如果没有指定 :key 属性，会自动拿index作为key。
                    这个key是这个dom元素的身份证号/唯一标识。
    
                    分析以下：采用 index 作为key存在什么问题？
                        第一个问题：效率低。
                        第二个问题：非常严重了。产生了错乱。尤其是对数组当中的某些元素进行操作。（非末尾元素。）
                    怎么解决这个问题？
                        建议使用对象的id作为key
                 -->
                <tr v-for="(hero,index) in heros" :key="hero.id">
                    <td>{{index+1}}</td>
                    <td>{{hero.name}}</td>
                    <td>{{hero.power}}</td>
                    <td><input type="checkbox"></td>
                </tr>
            </table>
    
            <button @click="add">添加英雄麦文</button>
        </div>
        <script>
            const vm = new Vue({
                el : '#app',
                data : {
                    msg : '虚拟dom与diff算法',
                    heros : [
                        {id:'101',name:'艾格文',power:10000},
                        {id:'102',name:'麦迪文',power:9000},
                        {id:'103',name:'古尔丹',power:8000},
                        {id:'104',name:'萨尔',power:6000}
                    ]
                },
                methods : {
                    add(){
                        this.heros.unshift({id:'105',name:'麦文',power:9100})
                    }
                }
            })
        </script>
    </body>>
    ```

    ![1712586490397](%E8%99%9A%E6%8B%9Fdom%E5%92%8Cdiff%E7%AE%97%E6%B3%95.assets/1712586490397.png)

  

