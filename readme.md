# 项目使用到的一些内容记录

1. flask
2. sqlalchemy
1. wtform
1. pydantic
1. restful
1. click
1. logging
1. jinja
3. ajax
4. jquery
5. html
1. css
1. sqlite

> 后续增加redis mysql/pgsql vue等的使用集成

# 初次使用

1. 首先根据requirements.txt安装依赖,可以使用清华的源: https://pypi.tuna.tsinghua.edu.cn/simple
1. 首先应该在blog同级目录下手动创建`instance`目录(因为我们系统并没有自动创建这个目录)
2. 应该把blog下的`config.py`文件修改为实际的配置项后,放置到上面创建的`instance`目录下
3. 初次使用应该先使用命令行`flask --app blog init-db`初始化数据库

# 说明

## markdown支持

1. 使用过flask-pagedown,发现效果不是很好,转而使用富文本编辑器CKEditor,参考的: [为你的Flask项目添加富文本编辑器](https://zhuanlan.zhihu.com/p/23583960?refer=flask)
2. 后面又使用了[Flask-SimpleMDE](https://flask-simplemde.readthedocs.io/en/latest/)插件来支持md
3. 三方插件的js代码，如果没有修改原生代码，则未上传到git，另外instance目录也未归档到git

# 一些额外知识记录

## flask

### url_for与view视图类

```python
@bp.route('/url_param_test1')
# http://127.0.0.1:5000/demo/url_param_test1?a=1
def url_param_test1():
    # return request.args.get('a')
    return url_for('demo.url_param_test1', a=1, b=2) #/demo/url_param_test1?a=1&b=2

@bp.route('/url_param_test2/<string:b>')
# http://127.0.0.1:5000/demo/url_param_test2/123?a=3
def url_param_test2(b):
    # return request.args.get('a') + b
    return url_for('demo.url_param_test2', a=1, b=b) #/demo/url_param_test2/123?a=1

# 即url_for传递额外的参数，构造的url会根据实际的路由函数而定
# 如果url_for传递的参数，在路由函数中有定义，比如上面url_param_test2的b参数，那么会作为url的一部分传入
# 但是url_param_test2和url_param_test1都没有定义a这个参数，那么会作为url的查询参数部分传入

# 同理，视图类也遵循相同的原则，只不过url的匹配是通过add_url_rule处设置的
class UrlParamCls1(views.MethodView):
    def get(self, b=3):
        return url_for('demo.url_param_test3', a=1, b=2) + str(b)

class UrlParamCls2(views.MethodView):
    def get(self, b=3):
        return url_for('demo.url_param_test4', a=1, b=2) + str(b)

# url参数在这里进行设定，url_for也同理，根据get是否有额外的参数而确定应该是url参数还是查询参数
bp.add_url_rule('/url_param_test3', view_func=UrlParamCls1.as_view('url_param_test3'))
bp.add_url_rule('/url_param_test4/<string:b>', view_func=UrlParamCls2.as_view('url_param_test4'))
```

## css

### 选择器

```css
/*
两个元素并排，没有其它修饰，比如 div p 表示选择div下所有的p，不管p处于哪一个层级，只要在div下就生效
两个元素并排，有>修饰，比如 div > p 表示选择div下第一个p层级，只影响div下第一层p

上面两种描述适用于.#的类和ID选择符
比如:
li.pagination-item > a 表示选取class为pagination的所有li下的第一个层级的a
.content label 表示选择class为content下所有label，不分层级

多个选择器如果有相同的样式使用,即可，比如:
.content input, .content textarea { margin-bottom: 1em; }
表示.content input这个选择器和.content textarea这个选择器有相同的样式
*/
```

### 盒模型

从内容到最外层分为: content -> padding -> border -> margin

> 盒子的宽度 = width + padding-left + padding-right + border-left + border-right + margin-left + margin-right
> 盒子的高度 = height + padding-top + padding-bottom + border-top + border-bottom + margin-top + margin-bottom

> 注意: 很多浏览器默认body会有margin 8px，故一般可以使用如下代码设置为0。其实类似很多的元素都有默认的margin，比如我们常见的`p`

```css
body {
    margin: 0px;
    padding: 0px;
}
```

> 另外如果想让某一个盒子在页面左右居中显示，可以通过margin设置生效，比如:

```css
body {
    /* 即上下设置间距为0，左右设置为auto */
    margin: 0 auto;
}
```

### 块级元素和行内元素

#### 行内元素

> 行内元素也可以叫内联元素

1. 无法设置宽高
2. 针对padding和margin设置左右有效，上下无效
3. 默认情况下行内元素可以多个行内元素共存一行，即与其它行内元素并排

#### 块级元素

1. 可以设置宽高
2. padding、margin设置均有效
3. 自动换行
4. 块默认是从上到下排列
5. 不能与其它任何元素并排

### 盒模型相关的几个属性

```css
a {
    /* display有4个取值，
    none就是不渲染元素(注意和visibility属性的区别) 
    block表示是块级元素
    inline表示是内联元素，通过inline和block可以在行内和块级元素之间转换
    */
    display: none;

    /* 指定float后，元素变成块级元素，更准确的理解是inline-block类型，即同时具有内联和块级元素的特征
    none默认值，不浮动
    right向右浮动
    left向左浮动

    我们标准的文档流类似于水流一样，自上而下排列，不管是行内还是块级元素，只要一行满了就换行继续
    增加float后，元素就脱离了标准文档流，浮起来了，类似于漂浮在了标准文档流上
    对行内和块级元素的一个直接影响是: 行内元素可以设置宽高了、块级元素可以多个在同一行了

    浮动是相对于父元素就行浮动的，如果父元素的位置改变了，浮动也相当于父元素进行浮动

    指定了float的元素会浮动到包含边框(父元素)或者碰到另外一个浮动边框为止。其它非浮动元素该怎么排列仍然继续排列
     */
    float: left;

    /*指定元素某个方向不允许出现浮动元素
    none默认值，允许浮动元素出现
    left,左侧不允许有浮动元素
    right
    both 左右两侧均不允许
    注意只有左右，没有上下的概念
    */
    clear: none
}
```

### 参考

1. [css中float详解](https://blog.csdn.net/pingchuanz/article/details/82903397)
2. [常见的行内和块级元素](https://www.cnblogs.com/gujun1998/p/13917970.html)
