# raven_naodao_website

## www 下代码---web 服务器上运行代码

- 为实验中被试可看到的网站代码

- 须在配置好 apache web 服务器的服务器上运行（将 www/放在目录 var/中,apache 一般开机自启动，或 bash 运行 sudo service apache2 restart，输入网址即可访问）

- dataset 有省略

- 实现逻辑大概为，apache web 服务器启动后会自动运行 app.py 程序，访问网址默认为 index.html，根据 app.py 执行网页跳转

## www-local 下代码---本地上可运行代码

- www-local\templates\index.html 为网站首页

- www-local\templates\plot.html 为跳转后看题界面

- 无法实现跳转

- 图片链接写死，仅供示意

## figures---为实验中被试可看到的网站截图

## video---为实验中被试操作流程的录屏
