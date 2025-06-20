# 阿里云运维巡检工具

本项目是一个基于 Python 和 阿里云 OpenAPI SDK 实现的**一站式运维巡检系统**，适用于生产环境中定期检查以下资源状态：

- ECS 实例（CPU/内存/磁盘使用、按量付费、磁盘快照）
- RDS、Redis 实例（资源利用率、备份策略、按量付费）
- 云监控指标（支持告警项）
- 云安全中心（评分、漏洞、基线检查）
- 安全组、EIP、资源包等网络配置
- RAM 账号使用分析
- 即将过期的资源与 SSL 证书
- 可生成 Excel 报告并自动分类展示

---

## 🧩 项目目录结构

| 路径                | 描述                             |
|-------------------| -------------------------------- |
| `aliyunapi/`      | 阿里云 API 模块封装目录          |
| ├── `__init__.py` | 模块初始化入口                   |
| ├── `ecs.py`      | ECS 实例巡检                     |
| ├── `rds.py`      | RDS 实例巡检                     |
| ├── `redis.py`    | Redis 实例巡检                   |
| ├── `monitor.py`  | 云监控指标接口                   |
| ├── `sas.py`      | 云安全中心评分、漏洞、基线检查   |
| ├── `ram.py`      | RAM 用户、AK 使用、权限策略分析  |
| ├── `vpc.py`      | 安全组配置检查、EIP 信息获取     |
| ├── `cas.py`      | SSL 证书有效期检查               |
| └── `bill.py`     | 资源包剩余额、账单使用信息       |
| `reports/`        | 巡检报告输出目录（Excel）        |
| `config.json`     | 配置文件：密钥、区域、时间等参数 |
| `requirements.txt` | Python 第三方依赖列表            |
| `main.py`         | 程序入口，控制整体巡检流程       |
| `utils.py`        | 公共工具函数封装                 |
| `README.md`       | 项目说明文档（当前文件）         |
| `collectdata.py`    | 整合采集模块（类比数据聚合核心） |


---

## 📦 aliyunapi 模块介绍

模块名 | 说明
------ | ----
`__init__.py` | 初始化入口，统一导入所有子模块的 API 封装类
`ecs.py` | 实现对 ECS 实例基本信息、按量判断、磁盘快照、云助手命令执行等操作
`rds.py` | 实现对 RDS 实例信息、备份策略检查、按量判断等（待实现）
`redis.py` | Redis 实例属性获取、备份策略、性能指标等（待实现）
`monitor.py` | 使用阿里云云监控接口，查询 ECS/RDS/Redis 等实例的性能指标（待实现）
`sas.py` | 云安全中心的评分、漏洞扫描结果、基线安全检查等（待实现）
`ram.py` | RAM 用户列表、AK 使用时间分析、策略合规检查（待实现）
`vpc.py` | 安全组配置检查、EIP 绑定状态获取等（待实现）
`cas.py` | 获取证书列表并识别即将过期证书（待实现）
`bill.py` | 查询资源包剩余量、可续费实例、账单使用量等（待实现）

---

## 🛠 使用方式

### 1. 配置文件 `config.json`

```json
{
  "AccessKeyID": "your-access-key",
  "AccessKeySecret": "your-secret-key",
  "Region": ["cn-hangzhou"],
  "AuthorizeKey": "custom-auth-key",
  "StartTime": "2025-06-01 00:00:00",
  "EndTime": "2025-06-13 23:59:59",
  "Level": 2,
  "FilePath": "/root/reports/aliyun_inspection_20250613.xlsx"
}
```
### 2. 运行命令
```
python run_inspection.py --config ./config.json
```



## 📝 未来可拓展功能 
✅ 发送报告至钉钉、飞书、邮件
    
✅ 生成 HTML 或 Markdown 报告（便于上传 OSS）
    
✅ 多账号/多 Region 支持
    
✅ 基于标签筛选实例资源