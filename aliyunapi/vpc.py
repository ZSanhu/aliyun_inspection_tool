from alibabacloud_tea_openapi.models import Config
from alibabacloud_ecs20140526.client import Client as EcsClient  # 新增ECS客户端
from alibabacloud_ecs20140526 import models as ecs_models  # 新增ECS模型
from alibabacloud_vpc20160428.client import Client as VpcClient
from alibabacloud_vpc20160428 import models as vpc_models  # 导入VPC模型


def get_ecs_client(access_key, access_secret, region_id="cn-hangzhou"):
    """
    构建新版 SDK 的 ECS 客户端
    """
    config = Config(
        access_key_id=access_key,
        access_key_secret=access_secret,
        region_id=region_id,
    )
    return EcsClient(config)


def get_vpc_client(access_key, access_secret, region_id="cn-hangzhou"):
    """
    构建新版 SDK 的 VPC 客户端
    """
    config = Config(
        access_key_id=access_key,
        access_key_secret=access_secret,
        region_id=region_id,
    )
    return VpcClient(config)


def _expand_port_range(port_range):
    """
    将端口范围字符串展开为列表
    """
    if not port_range:
        return []

    if '-' in port_range:
        try:
            start, end = map(int, port_range.split('-'))
            return list(range(start, end + 1))
        except:
            return []
    try:
        return [int(port_range)]
    except:
        return []


def check_open_ports(access_key, access_secret, region_id="cn-hangzhou", danger_ports=None):
    """
    检查对 0.0.0.0/0 开放的高危端口（基于新版 SDK）
    """
    if danger_ports is None:
        danger_ports = [22, 3306, 6379, 27017, 9200, 9001, 8080, 3458]

    # 使用ECS客户端而不是VPC客户端
    client = get_ecs_client(access_key, access_secret, region_id)
    result = []

    try:
        # 创建请求对象
        list_req = ecs_models.DescribeSecurityGroupsRequest()
        list_req.region_id = region_id

        # 获取安全组列表
        sg_response = client.describe_security_groups(list_req)
        sg_list = sg_response.body.security_groups.security_group

        for sg in sg_list:
            sg_id = sg.security_group_id

            # 创建安全组属性请求对象
            attr_req = ecs_models.DescribeSecurityGroupAttributeRequest(
                security_group_id=sg_id,
                region_id=region_id
            )

            # 获取安全组属性
            sg_attr = client.describe_security_group_attribute(attr_req)
            permissions = sg_attr.body.permissions.permission

            for rule in permissions:
                if rule.source_cidr_ip == "0.0.0.0/0":
                    proto = rule.ip_protocol
                    port_range = rule.port_range

                    if port_range and port_range != "-1/-1":
                        ports = _expand_port_range(port_range)
                        for port in ports:
                            if port in danger_ports:
                                result.append([
                                    "安全组", "高危端口暴露", sg_id,
                                    f"{proto}:{port}", "0.0.0.0/0",
                                    "异常（高危端口开放）"
                                ])
    except Exception as e:
        print(f"❌ 安全组检查异常: {e}")
        result.append(["安全组", "检查失败", "N/A", str(e), "异常"])

    return result


def check_unbound_eip(access_key, access_secret, region_id="cn-hangzhou"):
    """
    检查未绑定实例的 EIP（新版 SDK）
    """
    client = get_vpc_client(access_key, access_secret, region_id)
    result = []

    try:
        # 创建请求对象
        req = vpc_models.DescribeEipAddressesRequest()
        req.region_id = region_id

        # 获取EIP列表
        eip_response = client.describe_eip_addresses(req)
        eip_list = eip_response.body.eip_addresses.eip_address

        for eip in eip_list:
            ip = eip.ip_address
            instance_id = eip.instance_id
            bandwidth = eip.bandwidth
            bind_status = "未绑定" if not instance_id else f"已绑定到 {instance_id}"
            state = "异常（闲置未绑定）" if not instance_id else "正常"

            result.append([
                "EIP", "绑定状态", ip, f"{bandwidth}Mbps", bind_status, state
            ])
    except Exception as e:
        print(f"❌ EIP 检查异常: {e}")
        result.append(["EIP", "检查失败", "N/A", str(e), "异常"])

    return result