from .monitor import CloudMonitor
def check_disk_usage_exceed(monitor: CloudMonitor, start_time, end_time, threshold=90):
    instance_ids = [
        "i-xxxxxx"
    ]

    result = []
    for iid in instance_ids:
        datapoints = monitor.query_metric(
            namespace='acs_ecs_dashboard',
            metric_name='diskusage_utilization',
            instance_id=iid,
            start_time=start_time,
            end_time=end_time,
            period="300"
        )

        if datapoints:
            latest = datapoints[-1]  # 取最新一条
            percent = float(latest['Average'])  # 不需要 *100，ECS 这个指标原本就是百分比
            status = "异常（高于90%）" if percent > threshold else "正常"
            row = ["ECS", "磁盘使用率", iid, round(percent, 2), status]
            result.append(row)
        else:
            row = ["ECS", "磁盘使用率", iid, "N/A", "无数据"]
            result.append(row)

    return result
