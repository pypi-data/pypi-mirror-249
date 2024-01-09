from fhir.resources.R4B.fhirtypes import Id

from kt2.models import (
    KT2ActivityDefinition,
    KT2AuditEvent,
    KT2CareTeam,
    KT2Endpoint,
    KT2Organization,
    KT2Patient,
    KT2Practitioner,
    KT2Subscription,
    KT2Task,
)

KT2AuditEventList = list[KT2AuditEvent]
KT2ActivityDefinitionList = list[KT2ActivityDefinition]
KT2CareTeamList = list[KT2CareTeam]
KT2CareTeamList = list[KT2CareTeam]
KT2EndpointList = list[KT2Endpoint]
KT2OrganizationList = list[KT2Organization]
KT2PatientList = list[KT2Patient]
KT2PracticionerList = list[KT2Practitioner]
KT2TaskList = list[KT2Task]
KT2SubscriptionList = list[KT2Subscription]
KT2Id = Id
