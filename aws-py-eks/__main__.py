import iam
import vpc
import pulumi
from pulumi_aws import eks

## EKS Cluster

eks_cluster = eks.Cluster(
    "eks-cluster",
    role_arn=iam.eks_role.arn,
    tags= {"Name":"pulumi-eks-cluster"},
    vpc_config = {
        "publicAccessCidrs": ["0.0.0.0/0"],
        "security_group_ids": [vpc.eks_security_group.id],
        "subnet_ids": [vpc.vpc_subnet_1.id, vpc.vpc_subnet_2.id],
    }
)

eks_node_group = eks.NodeGroup(
    "eks-node-group",
    cluster_name=eks_cluster.name,
    node_group_name="pulumi-eks-nodegroup",
    node_role_arn=iam.ec2_role.arn,
    subnet_ids=[vpc.vpc_subnet_1.id, vpc.vpc_subnet_2.id],
    tags={
        'Name' : 'pulumi-cluster-nodeGroup'
    },
    scaling_config = {
        "desired_size": 2,
        "max_size": 2,
        "min_size": 1,
  },
)

pulumi.export("cluster-name", eks_cluster.name)
