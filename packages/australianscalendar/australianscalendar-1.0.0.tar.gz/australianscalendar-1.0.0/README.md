# 🇯🇵澳洲节假日

[![License](https://img.shields.io/github/license/LKI/chinese-calendar.svg)](https://github.com/LKI/chinese-calendar/blob/master/LICENSE)

判断某年某月某一天是不是工作日/节假日。
支持 2023~2024年

## 安装

```
pip install australianscalendar
```

## 升级

```
pip install -U australianscalendar
```

澳洲的公众假期无调休，假期预测相比较很容易

## 样例

``` python
import datetime

# 判断 2023年1月1号 是不是节假日
from australians_calendar import is_holiday, is_workday
new_year = datetime.date(2023, 1, 1)
assert is_workday(new_year) is False
assert is_holiday(new_year) is True

# 或者在判断的同时，获取节日名
import australians_calendar as calendar  # 也可以这样 import
on_holiday, holiday_name = calendar.get_holiday_detail(new_year)
assert on_holiday is True
assert holiday_name == calendar.Holiday.new_years_day.value

```

## 其它语言

假如你没法使用Python，
你也可以转译现成的[常量文件][constants.py]来获取最全的节假日安排表。

## 贡献代码

1. Fork + Clone 项目到本地
2. 修改[节假日定义][scripts/data.py]
3. 执行[脚本][scripts/__init__.py]自动生成[常量文件][constants.py]
4. 提交PR

[constants.py]: https://github.com/hack-fang/australians-calendar/blob/main/australians_calendar/constants.py
[scripts/data.py]: https://github.com/hack-fang/australians-calendar/blob/main/australians_calendar/scripts/data.py
[scripts/__init__.py]: https://github.com/hack-fang/australians-calendar/blob/main/australians_calendar/scripts/__init__.py

## 致谢

本项目参考了LKI的[chinese-calendar](https://github.com/LKI/chinese-calendar),感谢开发者的付出