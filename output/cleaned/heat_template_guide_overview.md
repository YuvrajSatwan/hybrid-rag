# Template Guide Â¶

- Heat Orchestration Template (HOT) Guide Status Writing a hello world HOT template

- Status

- Writing a hello world HOT template

- Writing a hello world HOT template A most basic template Input parameters Template outputs

- A most basic template

- Input parameters

- Template outputs

- Guideline for features Multi-Clouds support

- Multi-Clouds support

- Heat Orchestration Template (HOT) specification Status Template structure Heat template version Parameter groups section Parameters section Resources section Outputs section Conditions section Intrinsic functions

- Status

- Template structure

- Heat template version

- Parameter groups section

- Parameters section

- Resources section

- Outputs section

- Conditions section

- Intrinsic functions

- Instances Manage instances Manage networks Manage volumes

- Manage instances

- Manage networks

- Manage volumes

- Software configuration Image building User-data boot scripts and cloud-init Software deployment resources

- Image building

- User-data boot scripts and cloud-init

- Software deployment resources

- Environments Environment file format Environment Merging Global and effective environments Usage examples

- Environment file format

- Environment Merging

- Global and effective environments

- Usage examples

- Template composition Use the template filename as type Define a new resource type Get access to nested attributes Making your template resource more âtransparentâ

- Use the template filename as type

- Define a new resource type

- Get access to nested attributes

- Making your template resource more âtransparentâ

- OpenStack Resource Types OS::Aodh::CompositeAlarm OS::Aodh::EventAlarm OS::Aodh::GnocchiAggregationByMetricsAlarm OS::Aodh::GnocchiAggregationByResourcesAlarm OS::Aodh::GnocchiResourcesAlarm OS::Aodh::LBMemberHealthAlarm OS::Aodh::PrometheusAlarm OS::Barbican::CertificateContainer OS::Barbican::GenericContainer OS::Barbican::Order OS::Barbican::RSAContainer OS::Barbican::Secret OS::Blazar::Host OS::Blazar::Lease OS::Cinder::EncryptedVolumeType OS::Cinder::QoSAssociation OS::Cinder::QoSSpecs OS::Cinder::Quota OS::Cinder::Volume OS::Cinder::VolumeAttachment OS::Cinder::VolumeType OS::Designate::RecordSet OS::Designate::Zone OS::Glance::WebImage OS::Heat::AccessPolicy OS::Heat::AutoScalingGroup OS::Heat::CloudConfig OS::Heat::Delay OS::Heat::DeployedServer OS::Heat::InstanceGroup OS::Heat::MultipartMime OS::Heat::None OS::Heat::RandomString OS::Heat::ResourceChain OS::Heat::ResourceGroup OS::Heat::ScalingPolicy OS::Heat::SoftwareComponent OS::Heat::SoftwareConfig OS::Heat::SoftwareDeployment OS::Heat::SoftwareDeploymentGroup OS::Heat::Stack OS::Heat::StructuredConfig OS::Heat::StructuredDeployment OS::Heat::StructuredDeploymentGroup OS::Heat::SwiftSignal OS::Heat::SwiftSignalHandle OS::Heat::TestResource OS::Heat::UpdateWaitConditionHandle OS::Heat::Value OS::Heat::WaitCondition OS::Heat::WaitConditionHandle OS::Ironic::Port OS::Keystone::Domain OS::Keystone::Endpoint OS::Keystone::Group OS::Keystone::GroupRoleAssignment OS::Keystone::Project OS::Keystone::Region OS::Keystone::Role OS::Keystone::Service OS::Keystone::User OS::Keystone::UserRoleAssignment OS::Magnum::Cluster OS::Magnum::ClusterTemplate OS::Manila::SecurityService OS::Manila::Share OS::Manila::ShareNetwork OS::Manila::ShareType OS::Mistral::CronTrigger OS::Mistral::ExternalResource OS::Mistral::Workflow OS::Neutron::AddressScope OS::Neutron::ExtraRouteSet OS::Neutron::Firewall OS::Neutron::FirewallPolicy OS::Neutron::FirewallRule OS::Neutron::FloatingIP OS::Neutron::FloatingIPAssociation OS::Neutron::FloatingIPPortForward OS::Neutron::IKEPolicy OS::Neutron::IPsecPolicy OS::Neutron::IPsecSiteConnection OS::Neutron::L2Gateway OS::Neutron::L2GatewayConnection OS::Neutron::MeteringLabel OS::Neutron::MeteringRule OS::Neutron::Net OS::Neutron::NetworkGateway OS::Neutron::Port OS::Neutron::ProviderNet OS::Neutron::QoSBandwidthLimitRule OS::Neutron::QoSDscpMarkingRule OS::Neutron::QoSMinimumBandwidthRule OS::Neutron::QoSMinimumPacketRateRule OS::Neutron::QoSPolicy OS::Neutron::Quota OS::Neutron::RBACPolicy OS::Neutron::Router OS::Neutron::RouterInterface OS::Neutron::SecurityGroup OS::Neutron::SecurityGroupRule OS::Neutron::Segment OS::Neutron::Subnet OS::Neutron::SubnetPool OS::Neutron::TaaS::TapFlow OS::Neutron::TaaS::TapService OS::Neutron::Trunk OS::Neutron::VPNService OS::Nova::Flavor OS::Nova::HostAggregate OS::Nova::KeyPair OS::Nova::Quota OS::Nova::Server OS::Nova::ServerGroup OS::Octavia::AvailabilityZone OS::Octavia::AvailabilityZoneProfile OS::Octavia::Flavor OS::Octavia::FlavorProfile OS::Octavia::HealthMonitor OS::Octavia::L7Policy OS::Octavia::L7Rule OS::Octavia::Listener OS::Octavia::LoadBalancer OS::Octavia::Pool OS::Octavia::PoolMember OS::Octavia::Quota OS::Swift::Container OS::Trove::Cluster OS::Trove::Instance OS::Zaqar::MistralTrigger OS::Zaqar::Queue OS::Zaqar::SignedQueueURL OS::Zaqar::Subscription OS::Zun::Container

- OS::Aodh::CompositeAlarm

- OS::Aodh::EventAlarm

- OS::Aodh::GnocchiAggregationByMetricsAlarm

- OS::Aodh::GnocchiAggregationByResourcesAlarm

- OS::Aodh::GnocchiResourcesAlarm

- OS::Aodh::LBMemberHealthAlarm

- OS::Aodh::PrometheusAlarm

- OS::Barbican::CertificateContainer

- OS::Barbican::GenericContainer

- OS::Barbican::Order

- OS::Barbican::RSAContainer

- OS::Barbican::Secret

- OS::Blazar::Host

- OS::Blazar::Lease

- OS::Cinder::EncryptedVolumeType

- OS::Cinder::QoSAssociation

- OS::Cinder::QoSSpecs

- OS::Cinder::Quota

- OS::Cinder::Volume

- OS::Cinder::VolumeAttachment

- OS::Cinder::VolumeType

- OS::Designate::RecordSet

- OS::Designate::Zone

- OS::Glance::WebImage

- OS::Heat::AccessPolicy

- OS::Heat::AutoScalingGroup

- OS::Heat::CloudConfig

- OS::Heat::Delay

- OS::Heat::DeployedServer

- OS::Heat::InstanceGroup

- OS::Heat::MultipartMime

- OS::Heat::None

- OS::Heat::RandomString

- OS::Heat::ResourceChain

- OS::Heat::ResourceGroup

- OS::Heat::ScalingPolicy

- OS::Heat::SoftwareComponent

- OS::Heat::SoftwareConfig

- OS::Heat::SoftwareDeployment

- OS::Heat::SoftwareDeploymentGroup

- OS::Heat::Stack

- OS::Heat::StructuredConfig

- OS::Heat::StructuredDeployment

- OS::Heat::StructuredDeploymentGroup

- OS::Heat::SwiftSignal

- OS::Heat::SwiftSignalHandle

- OS::Heat::TestResource

- OS::Heat::UpdateWaitConditionHandle

- OS::Heat::Value

- OS::Heat::WaitCondition

- OS::Heat::WaitConditionHandle

- OS::Ironic::Port

- OS::Keystone::Domain

- OS::Keystone::Endpoint

- OS::Keystone::Group

- OS::Keystone::GroupRoleAssignment

- OS::Keystone::Project

- OS::Keystone::Region

- OS::Keystone::Role

- OS::Keystone::Service

- OS::Keystone::User

- OS::Keystone::UserRoleAssignment

- OS::Magnum::Cluster

- OS::Magnum::ClusterTemplate

- OS::Manila::SecurityService

- OS::Manila::Share

- OS::Manila::ShareNetwork

- OS::Manila::ShareType

- OS::Mistral::CronTrigger

- OS::Mistral::ExternalResource

- OS::Mistral::Workflow

- OS::Neutron::AddressScope

- OS::Neutron::ExtraRouteSet

- OS::Neutron::Firewall

- OS::Neutron::FirewallPolicy

- OS::Neutron::FirewallRule

- OS::Neutron::FloatingIP

- OS::Neutron::FloatingIPAssociation

- OS::Neutron::FloatingIPPortForward

- OS::Neutron::IKEPolicy

- OS::Neutron::IPsecPolicy

- OS::Neutron::IPsecSiteConnection

- OS::Neutron::L2Gateway

- OS::Neutron::L2GatewayConnection

- OS::Neutron::MeteringLabel

- OS::Neutron::MeteringRule

- OS::Neutron::Net

- OS::Neutron::NetworkGateway

- OS::Neutron::Port

- OS::Neutron::ProviderNet

- OS::Neutron::QoSBandwidthLimitRule

- OS::Neutron::QoSDscpMarkingRule

- OS::Neutron::QoSMinimumBandwidthRule

- OS::Neutron::QoSMinimumPacketRateRule

- OS::Neutron::QoSPolicy

- OS::Neutron::Quota

- OS::Neutron::RBACPolicy

- OS::Neutron::Router

- OS::Neutron::RouterInterface

- OS::Neutron::SecurityGroup

- OS::Neutron::SecurityGroupRule

- OS::Neutron::Segment

- OS::Neutron::Subnet

- OS::Neutron::SubnetPool

- OS::Neutron::TaaS::TapFlow

- OS::Neutron::TaaS::TapService

- OS::Neutron::Trunk

- OS::Neutron::VPNService

- OS::Nova::Flavor

- OS::Nova::HostAggregate

- OS::Nova::KeyPair

- OS::Nova::Quota

- OS::Nova::Server

- OS::Nova::ServerGroup

- OS::Octavia::AvailabilityZone

- OS::Octavia::AvailabilityZoneProfile

- OS::Octavia::Flavor

- OS::Octavia::FlavorProfile

- OS::Octavia::HealthMonitor

- OS::Octavia::L7Policy

- OS::Octavia::L7Rule

- OS::Octavia::Listener

- OS::Octavia::LoadBalancer

- OS::Octavia::Pool

- OS::Octavia::PoolMember

- OS::Octavia::Quota

- OS::Swift::Container

- OS::Trove::Cluster

- OS::Trove::Instance

- OS::Zaqar::MistralTrigger

- OS::Zaqar::Queue

- OS::Zaqar::SignedQueueURL

- OS::Zaqar::Subscription

- OS::Zun::Container

- CloudFormation Compatible Resource Types AWS::AutoScaling::AutoScalingGroup AWS::AutoScaling::LaunchConfiguration AWS::AutoScaling::ScalingPolicy AWS::CloudFormation::Stack AWS::CloudFormation::WaitCondition AWS::CloudFormation::WaitConditionHandle AWS::EC2::EIP AWS::EC2::EIPAssociation AWS::EC2::Instance AWS::EC2::InternetGateway AWS::EC2::NetworkInterface AWS::EC2::RouteTable AWS::EC2::SecurityGroup AWS::EC2::Subnet AWS::EC2::SubnetRouteTableAssociation AWS::EC2::VPC AWS::EC2::VPCGatewayAttachment AWS::EC2::Volume AWS::EC2::VolumeAttachment AWS::ElasticLoadBalancing::LoadBalancer AWS::IAM::AccessKey AWS::IAM::User AWS::S3::Bucket

- AWS::AutoScaling::AutoScalingGroup

- AWS::AutoScaling::LaunchConfiguration

- AWS::AutoScaling::ScalingPolicy

- AWS::CloudFormation::Stack

- AWS::CloudFormation::WaitCondition

- AWS::CloudFormation::WaitConditionHandle

- AWS::EC2::EIP

- AWS::EC2::EIPAssociation

- AWS::EC2::Instance

- AWS::EC2::InternetGateway

- AWS::EC2::NetworkInterface

- AWS::EC2::RouteTable

- AWS::EC2::SecurityGroup

- AWS::EC2::Subnet

- AWS::EC2::SubnetRouteTableAssociation

- AWS::EC2::VPC

- AWS::EC2::VPCGatewayAttachment

- AWS::EC2::Volume

- AWS::EC2::VolumeAttachment

- AWS::ElasticLoadBalancing::LoadBalancer

- AWS::IAM::AccessKey

- AWS::IAM::User

- AWS::S3::Bucket

- Unsupported Heat Resource Types OS::Aodh::Alarm OS::Neutron::ExtraRoute OS::Neutron::FlowClassifier OS::Neutron::PortChain OS::Neutron::PortPair OS::Neutron::PortPairGroup OS::Vitrage::Template

- OS::Aodh::Alarm

- OS::Neutron::ExtraRoute

- OS::Neutron::FlowClassifier

- OS::Neutron::PortChain

- OS::Neutron::PortPair

- OS::Neutron::PortPairGroup

- OS::Vitrage::Template

- Contributed Heat Resource Types DockerInc Resource

- DockerInc Resource

- CloudFormation Compatible Functions Ref Fn::Base64 Fn::FindInMap Fn::GetAtt Fn::GetAZs Fn::Join Fn::Select Fn::Split Fn::Replace Fn::ResourceFacade Fn::MemberListToMap Fn::Equals Fn::If Fn::Not Fn::And Fn::Or

- Ref

- Fn::Base64

- Fn::FindInMap

- Fn::GetAtt

- Fn::GetAZs

- Fn::Join

- Fn::Select

- Fn::Split

- Fn::Replace

- Fn::ResourceFacade

- Fn::MemberListToMap

- Fn::Equals

- Fn::If

- Fn::Not

- Fn::And

- Fn::Or
