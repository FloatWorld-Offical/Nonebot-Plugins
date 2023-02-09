# FWNP_MinecraftServerStatus
![Status](https://img.shields.io/badge/Build-Success-brightgreen)
![Status](https://img.shields.io/badge/Status-ContinuousUpdate-brightgreen)
![Status](https://img.shields.io/badge/Version-v0.3-blue)
![Status](https://img.shields.io/badge/Team-FloatWorld-blue)
![Status](https://img.shields.io/badge/Author-皇橙籽-blue)
![Status](https://img.shields.io/badge/Language-Python-blue)
### 插件依赖库
- mcstatus 10.0.1（可以使用pip下载）
- json（标准库）

### 使用方法
0. 安装插件(见主目录README)  
1. 打开info.json修改参数(参数信息详见下方文件说明)
2. 打开command.json修改触发命令(参数信息详见下方文件说明)
3. 重启机器人

### data文件说明
#### info.json
- server(List)
  - 列表中每一项用字符串进行存储，代表该位置的服务器名称
- address(List)
  - 列表中每一项使用字符串进行存储，代表该位置的服务器地址
  - 在地址前加上[B],则将会以基岩版协议进行检测（Java版无需增加前缀）
  - 注意！服务器名称与服务器地址的顺序需相同
  - 注意！服务器地址需为IP+端口，其他形式可能会出错
- message(Dict)
  - header(String)
    - 返回的消息的头部
  - body(String)
    - 返回消息的增量部分(即展示服务器信息的部分)
    - 在文字中输入以下标签以获取数据
      - <server_name> 服务器名称
      - <server_status> 服务器状态
      - <server_online> 服务器在线人数
      - <server_delay> 服务器延迟
      - <server_motd> 服务器MOTD(仅Java)
  - footer(String)
    - 返回的消息的尾部
#### command.json
- status(String)
  - 该命令用于触发服务器状态获取操作
