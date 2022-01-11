## gz-yaohao
## 广州中小客车指标摇号脚本
识别验证码，自动登录，申请延期


## chang log
- 2021-09-08 实现验证码识别（根据颜色占比最多来降噪，将颜色二值化）


## 运行环境
Python 3.6


## 第三方库
- [requests]: 简单好用，功能强大的Http请求库
- [urllib]: URL处理库
- [pytesseract]: 文字识别库
- [Pillow]: 图片处理


## 使用帮助
``` cmd
python __main__.py
```

## 实例输出
``` cmd
'raw: '
'main color filter: QSHM'
200
'https://apply.jtj.gz.gov.cn/apply/user/person/manage.do?rd=8650bb66b4c24cc0a50e49c6418ac254&message=建议您使用IE9及以上版本的浏览器，其他浏览器对系统兼容性不完善，如使用360安全浏览器请设置极速模式！'
'rd = 8650bb66b4c24cc0a50e49c6418ac254'
username_1 login success, start renew
200
'https://apply.jtj.gz.gov.cn/apply/person/manage.do?message=已确认延期！'