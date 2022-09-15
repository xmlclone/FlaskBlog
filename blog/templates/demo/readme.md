1. extends和include的方式均可以访问render_template传递的变量
2. extends如果{% block xxx %}中间有内容，继承的一方如果覆盖了这块，那么原始内容会被替换，完全覆盖掉
3. extends 'path/xxx.html' 扩展的内容需要有引号，并且路径是相对于templates目录的路径，而不是相对于扩展者自己的路径
4. include相当于是直接把include的内容插入到当前模板，注意被include的我们通常叫做局部模板，不是一个完整的html页面，一般在文件名前面加一个下划线_用于区分普通模板
5. 同理from import导入宏的原始模板路径也需要相对于templates目录来定义
6. from import不是直接引用，需要在html中指定的位置进行调用后才能生效
7. macro是无法直接访问render_template传递的变量，但是在引入的时候加上with context后，macro就可以直接访问了，参考macro2.html的示例代码