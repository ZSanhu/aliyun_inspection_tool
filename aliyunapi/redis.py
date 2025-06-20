from alibabacloud_r_kvstore20150101.client import Client as RedisClient
from alibabacloud_r_kvstore20150101 import models as redis_models


def check_redis_mem_exceed(monitor, redis_client: RedisClient, start_time, end_time, threshold=85):
    """
    检查 Redis 实例内存使用率是否超过阈值（默认 85%）
    """
    result = []

    # 获取 Redis 实例列表
    req = redis_models.DescribeInstancesRequest()
    req.page_number = 1
    req.page_size = 50
    resp = redis_client.describe_instances(req)

    instances = resp.body.instances.kvstore_instance or []

    for inst in instances:
        instance_id = inst.instance_id
        name = inst.instance_name or "-"
        capacity_gb = int(inst.capacity or 0)
        if capacity_gb == 0:
            continue
        max_memory = capacity_gb * 1024 * 1024 * 1024  # 字节

        # 查询 UsedMemory（单位：字节）
        datapoints = monitor.query_metric(
            namespace="acs_kvstore",
            metric_name="UsedMemory",
            instance_id=instance_id,
            start_time=start_time,
            end_time=end_time,
            period="300"
        )

        if datapoints:
            latest = datapoints[-1]
            used_memory = float(latest.get('Average', 0))
            percent = round(used_memory / max_memory * 100, 2)
            status = "异常（高于85%）" if percent > threshold else "正常"
            result.append(["Redis", "内存使用率", instance_id, f"{percent}%", status])
        else:
            result.append(["Redis", "内存使用率", instance_id, "N/A", "无监控数据"])

    return result


def check_redis_backup(redis_client: RedisClient):
    """
    检查 Redis 实例是否开启自动备份（通过 describe_instances 获取）
    """
    result = []

    req = redis_models.DescribeInstancesRequest()
    req.page_number = 1
    req.page_size = 50
    resp = redis_client.describe_instances(req)

    instances = resp.body.instances.kvstore_instance or []

    for inst in instances:
        instance_id = inst.instance_id
        name = inst.instance_name or "-"

        # 修复：使用正确的备份状态字段
        # 方法1：直接尝试可能的字段名
        backup_enabled = getattr(inst, 'enable_backup_log',
                                 getattr(inst, 'backup_log_enable',
                                         getattr(inst, 'is_backup_log_enable', 0)))

        # 方法2：使用更可靠的备份策略检查（推荐）
        # 获取备份策略详情
        backup_policy = getattr(inst, 'backup_policy', None)
        if backup_policy:
            # 如果有备份策略对象，检查其中的启用状态
            backup_enabled = getattr(backup_policy, 'enable_backup_log',
                                     getattr(backup_policy, 'backup_log_enable', 0))
        else:
            # 没有备份策略对象，则尝试从实例属性获取
            backup_enabled = getattr(inst, 'enable_backup_log', 0)

        # 确保值为整数（0/1）
        if isinstance(backup_enabled, bool):
            backup_enabled = int(backup_enabled)
        backup_enabled = int(backup_enabled) if str(backup_enabled).isdigit() else 0

        backup_status = "有" if backup_enabled else "无"
        status = "正常" if backup_enabled else "异常（无备份）"

        result.append(["Redis", "备份策略", instance_id, backup_status, status])

    return result