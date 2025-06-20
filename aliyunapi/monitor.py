from aliyunsdkcore.client import AcsClient
from aliyunsdkcms.request.v20190101 import DescribeMetricListRequest
import json

class CloudMonitor:
    def __init__(self, access_key, access_secret, region):
        self.client = AcsClient(access_key, access_secret, region)

    def query_metric(self, namespace, metric_name, instance_id, start_time, end_time, period='300'):
        request = DescribeMetricListRequest.DescribeMetricListRequest()
        request.set_accept_format('json')
        request.set_Namespace(namespace)
        request.set_MetricName(metric_name)
        request.set_Dimensions(json.dumps({"instanceId": instance_id}))
        request.set_Period(period)
        request.set_StartTime(start_time)
        request.set_EndTime(end_time)
        try:
            response = self.client.do_action_with_exception(request)
            data = json.loads(response)
            datapoints = json.loads(data['Datapoints']) if data['Datapoints'] else []
            return datapoints
        except Exception as e:
            print(f"监控接口异常: {e}")
            return []

