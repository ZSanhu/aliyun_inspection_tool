from .monitor import CloudMonitor

def check_rds_cpu_exceed(monitor: CloudMonitor, start_time, end_time, threshold=0.8):  # 阈值也用原始值0.8
    instance_ids = ["rm-xxxxxx"]
    result = []

    for iid in instance_ids:
        datapoints = monitor.query_metric(
            namespace='acs_rds_dashboard',
            metric_name='CpuUsage',
            instance_id=iid,
            start_time=start_time,
            end_time=end_time,
            period="300"
        )

        if datapoints:
            latest = datapoints[-1]
            value = float(latest['Average'])  # 保持原始小数值
            status = "异常（高于0.8）" if value > threshold else "正常"
            row = ["RDS", "CPU使用率", iid, round(value, 4), status]  # 保留4位小数展示更清晰
            result.append(row)
        else:
            row = ["RDS", "CPU使用率", iid, "N/A", "无数据"]
            result.append(row)

    return result
