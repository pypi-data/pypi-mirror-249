# Install

```shell
pip install ricco
```

# Update

```shell
pip install ricco -U
pip install ricco --upgrade
```

## 目录结构

```tree
ricco
├── etl # ETL模块
│   ├── data_reporter.py  # 数据报告
│   ├── entropy.py  # 熵值法工具
│   ├── extract.py  # 读取、抽取数据
│   ├── file.py  # 基于文件的数据处理
│   ├── load.py  # 数据加载、保存
│   ├── stat.py  # 数据统计
│   └── transformer.py  # 数据转换处理
├── geocode  # geocoding模块
│   ├── amap.py  # 高德 api
│   ├── baidu.py  # 百度 api
│   ├── geocode.py  # geocoding模块
│   └── util.py
├── geometry  # 地理处理模块
│   └── coord_trans.py  # 坐标转换
│   └── df.py  # 基于DataFrame或GeoDataFrame的地理工具
│   └── topology_check.py  # 拓扑检查
│   └── util.py  # 基础地理工具
└── util  # 常用工具
    ├── address_tools.py  # 地址处理
    ├── assertion.py  # 断言、校验
    ├── building_address.py  # 楼宇地址处理
    ├── coord_trans.py  # 坐标转换（弃用）
    ├── decorator.py  # 常用装饰器
    ├── dt.py  # 时间处理
    ├── geom.py  # 地理处理（弃用）
    ├── id_number.py  # 身份证号
    ├── os.py  # os模块
    ├── phone_number.py  # 手机号
    ├── strings.py  # 字符串处理
    └── util.py
```




