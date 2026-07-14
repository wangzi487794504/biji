#### Vue脚手架

*  Vue 的脚手架（Vue CLI: Command Line Interface）是 Vue 官方提供的标准化开发平台。它可以将我们.vue 的代码进行编译生成 html css js 代码，并且可以将这些代码自动发布到它自带的服务器上，为我们 Vue 的开发提供了一条龙服务。脚手架官网地址：https://cli.vuejs.org/zh

* 注意：Vue CLI 4.x 需要 Node.js v8.9 及以上版本，推荐 v10 以上。

*  脚手架安装步骤：

  * 建议先配置一下 npm 镜像：
    * 1) npm config set registry https://registry.npm.taobao.org
    * 2) npm config get registry 返回成功，表示设置成功
  * 安装脚手架（全局方式：表示只需要做一次即可）
    *  npm install -g @vue/cli
  * 安装完成后，重新打开 DOS 命令窗口，输入 vue 命令可用表示成功了
  * 创建项目（项目中自带脚手架环境，自带一个 HelloWorld 案例）
  * 切换到要创建项目的目录，然后使用 vue create vue_pro 

* 创建项目 vue create 项目名字，注意项目名字不能有大写

* 编译：npm run serve

* 终止ctrl+c

* npm结构

  ![1720340789684](vue%E8%84%9A%E6%89%8B%E6%9E%B6.assets/1720340789684.png)



*  ==可以看到在 index.html 中只有一个容器。没有引入 vue.js，也没有引入 main.js==

  * Vue 脚手架可以自动找到 main.js 文件。（所以 main.js 文件名不要修改，位置也不要随便移动）

    

*  Vue.config.js能有那些配置

  * 查阅官网：  [配置参考 | Vue CLI (vuejs.org)](https://cli.vuejs.org/zh/config/#devserver-proxy) 

* render解释

  ```js
  new Vue({
    render: h => h(App),
  }).$mount('#app')
  
  ```

  * 以前用的template，这里为什么使用render

    *  将 render 函数更换为：template 配置项，你会发现它是报错的。说明引入的 Vue 无法进行模板编译。
    * 原因：Vue 脚手架默认引入的是精简版的 Vue，这个精简版的 Vue 缺失模板编译器 
    *  实际引入的 vue.js 文件是：dist/vue.runtime.esm.js（esm 版本是 ES6 模块化版本）
      为什么缺失模板编译器？
    * Vue 包含两部分：一部分是 Vue 的核心，一部分是模板编译器（模板编译器可能占整个 vue.js 文件的一大部分体积）。程序员最终使用 webpack 进行打包的时候，显然 Vue 中的模板编译器就没有存在的必要了。为了缩小体积，所以在 Vue 脚手架中直接引入的就是一个缺失模板编译器的 vue.js。 

  * 解决方法

    *  第一种方式：引入一个完整的 vue.js
    * 第二种方式：使用 render 函数 

  *  render函数被 vue 自动调用，并且传递过来一个参数 createElement。createElement可以用于创建元素。简写形式可以使用箭头函数：

    ![1720344370880](vue%E8%84%9A%E6%89%8B%E6%9E%B6.assets/1720344370880.png) 

