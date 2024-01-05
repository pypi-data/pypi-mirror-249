from aws_cdk.aws_ec2 import SecurityGroup
from constructs import Construct, IConstruct

from infraflow.cdk import ServiceStageStack
from infraflow.cdk.sg import tier_maps


class SecurityGroupNeeds:
    def __init__(
            self,
            needs_outbound_internet=None,
            needs_inbound_internet=None
    ):
        self.needs_inbound_internet = needs_inbound_internet
        self.needs_outbound_internet = needs_outbound_internet


class SecurityGroupTarget:
    def __init__(
            self,
            scope: Construct, id: str, *args,
            cdk_type: type = None,
            infraflow_pattern: object = None,
    ):
        self.infraflow_pattern = infraflow_pattern
        self.cdk_type = cdk_type
        self.id = id
        self.scope = scope


class SecurityGroupStructurePattern:
    def __init__(self, stack: ServiceStageStack):
        self.stack = stack

    def get_group(
            self,
            target: SecurityGroupTarget,
            tier: str = None,
            needs: SecurityGroupNeeds = SecurityGroupNeeds()

    ) -> SecurityGroup:
        raise NotImplemented()


class SingleSecurityGroup(SecurityGroupStructurePattern):
    def __init__(self, stack: ServiceStageStack):
        super().__init__(stack)

    def get_group(
            self,
            target: SecurityGroupTarget,
            tier: str = None,
            needs: SecurityGroupNeeds = SecurityGroupNeeds()

    ) -> SecurityGroup:
        return self.stack.default_sg


class SecurityGroupPerResource(SecurityGroupStructurePattern):
    def __init__(self, stack: ServiceStageStack):
        super().__init__(stack)

    def get_group(
            self,
            target: SecurityGroupTarget,
            tier: str = None,
            needs: SecurityGroupNeeds = SecurityGroupNeeds()

    ) -> SecurityGroup:
        return SecurityGroup(scope=target.scope, id=target.id+"Sg")


class Tiered(SecurityGroupStructurePattern):
    def __init__(self, stack: ServiceStageStack, allow_all_within_app_group=True, allow_all_within_group: bool = False):
        super().__init__(stack)
        self.dbs = SecurityGroup(self.stack, 'DbSg')
        self.app = SecurityGroup(self.stack, 'AppSg')
        self.web = SecurityGroup(self.stack, 'WebSg')
        self.web.connections.allow_to(self.app)
        self.app.connections.allow_to(self.dbs)

        if allow_all_within_group or allow_all_within_app_group:
            self.app.connections.allow_to(self.app)

        if allow_all_within_group:
            self.dbs.connections.allow_to(self.dbs)
            self.web.connections.allow_to(self.web)

    def get_group(
            self,
            target: SecurityGroupTarget,
            tier: str = None,
            needs: SecurityGroupNeeds = SecurityGroupNeeds()

    ) -> SecurityGroup:
        if tier == 'app':
            return self.app
        elif tier == 'db':
            return self.dbs
        elif tier == 'web':
            return self.web
        elif target.cdk_type in tier_maps.app_services:
            return self.app
        elif target.cdk_type in tier_maps.web_services:
            return self.web
        elif target.cdk_type in tier_maps.db_services:
            return self.dbs
        else:
            return self.stack.default_sg

