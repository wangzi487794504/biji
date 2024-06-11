#### HTML

* HTML是由W3C（世界万维网）制定的，目前最高版本为HTML5

* Pre标签：保存预留格式。 hr换行  del删除字  ins 插入字   i斜体字   b粗体字   sup右上角   sub右下角  font字体标签

* 实体符号（以&开始, ;结束）：&lt ;小于  &gt ;大于  空格&nbsp ;  & &amp ;

* 表格：tr  td

* 按照标签的结构来分：

  * 围堵标签
    * <标签>内容</标签>
    * 自闭合标签<标签>

* 按照标签效果分

  * 行内标签（可以和其他标签在一行内共存）
  * 块级标签（会独立成为一行，不和其他标签成为一行）

* 标签嵌套规则

  * 块级标签可以嵌套块级和行内
  * 行内只能嵌套行内
  * 围堵标签才可以嵌套其他标签

* 属性：所有标签都有属性

  * disable不能使用，当只有一个属性名时即为省略，值为布尔属性
  * 属性值的引号可以省略，但不建议

* 所有不在页面的信息都放到head标签当中

* 元标签：meta。

  * 用于设置编码集charset

  * 作者信息设置

  * 关键词设置

  * 描述设置

    ```html
    <head>
        <meta charset="UTF-8">
        <!-- 配置作者 -->
        <meta name="author" content="wangzi"></meta>
        <!-- 配置关键词，浏览器可以搜索到，多个关键字用逗号隔开 -->
        <meta name="keywords" content="aa,bb,cc"></meta>
        <!-- 描述 -->
        <meta name="desccription" content="dd,cc"></meta>
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    ```

    

* em和i标签，都是斜体强调，但是em有语义化，可以让网络检索到，阅读器朗读时有重读效果
* 加粗：strong标签，带有语义化。b标签也可以，但没有语义化
* img的一些属性：alt没加载出来显示的，title悬浮提示信息