"""
This library provides an easy way to interact with security policies.

"""

from googleapiclient.discovery import build


def add_rule(project, security_policy_name, rule, credentials):
    """
    Add a rule in a specific policy

    Parameters:
    ----------
        project: The project name where the policy is allocated.
        security_policy_name: The security policy name where you want to add the rule.
        rule: Object. Form of the rule:

            { # Represents a rule that describes one or more match conditions along with the action to be taken when traffic matches this condition (allow or deny).
                "kind": "compute#securityPolicyRule", # [Output only] Type of the resource. Always compute#securityPolicyRule for security policy rules
                "description": "A String", # An optional description of this resource. Provide this property when you create the resource.
                "priority": 42, # An integer indicating the priority of a rule in the list. The priority must be a positive value between 0 and 2147483647. Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest prority.
                "action": "A String", # The Action to preform when the client connection triggers the rule. Can currently be either "allow" or "deny()" where valid values for status are 403, 404, and 502.
                "preview": True or False, # If set to true, the specified action is not enforced.
                "match": { # Represents a match condition that incoming traffic is evaluated against. Exactly one field must be specified. # A match condition that incoming traffic is evaluated against. If it evaluates to true, the corresponding 'action' is enforced.
                    "config": { # The configuration options available when specifying versioned_expr. This field must be specified if versioned_expr is specified and cannot be specified if versioned_expr is not specified.
                        "srcIpRanges": [ # CIDR IP address range.
                            "A String",
                        ],
                    },
                    "versionedExpr": "A String", # Preconfigured versioned expression. If this field is specified, config must also be specified. Available preconfigured expressions along with their requirements are: SRC_IPS_V1 - must specify the corresponding src_ip_range field in config.
                },
            }
        credentials: oauth2client.Credentials or google.auth.credentials.Credentials, credentials to be used for
            authentication. You can get them with 'get_workspace_impersonate_credentials_sa' method.

    """
    service = build("compute", "v1", credentials=credentials)

    added_rule = (
        service.securityPolicies()
        .addRule(
            project=project, securityPolicy=security_policy_name, body=rule
        )
        .execute()
    )

    return added_rule


def updated_rule(project, security_policy_name, rule, priority, credentials):
    """
    Update a rule in a specific policy

    Parameters:
    ----------
        project: The project name where the policy is allocated.
        security_policy_name: The security policy name where you want to add the rule.
        rule: Object. Form of the rule:

            { # Represents a rule that describes one or more match conditions along with the action to be taken when traffic matches this condition (allow or deny).
                "kind": "compute#securityPolicyRule", # [Output only] Type of the resource. Always compute#securityPolicyRule for security policy rules
                "description": "A String", # An optional description of this resource. Provide this property when you create the resource.
                "priority": 42, # An integer indicating the priority of a rule in the list. The priority must be a positive value between 0 and 2147483647. Rules are evaluated from highest to lowest priority where 0 is the highest priority and 2147483647 is the lowest prority.
                "action": "A String", # The Action to preform when the client connection triggers the rule. Can currently be either "allow" or "deny()" where valid values for status are 403, 404, and 502.
                "preview": True or False, # If set to true, the specified action is not enforced.
                "match": { # Represents a match condition that incoming traffic is evaluated against. Exactly one field must be specified. # A match condition that incoming traffic is evaluated against. If it evaluates to true, the corresponding 'action' is enforced.
                    "config": { # The configuration options available when specifying versioned_expr. This field must be specified if versioned_expr is specified and cannot be specified if versioned_expr is not specified.
                        "srcIpRanges": [ # CIDR IP address range.
                            "A String",
                        ],
                    },
                    "versionedExpr": "A String", # Preconfigured versioned expression. If this field is specified, config must also be specified. Available preconfigured expressions along with their requirements are: SRC_IPS_V1 - must specify the corresponding src_ip_range field in config.
                },
            }
        priority: Integer. The priority you want to assign to the rule.
        credentials: oauth2client.Credentials or google.auth.credentials.Credentials, credentials to be used for
            authentication. You can get them with 'get_workspace_impersonate_credentials_sa' method.

    """
    service = build("compute", "v1", credentials=credentials)

    updated_policy = (
        service.securityPolicies()
        .patchRule(
            project=project,
            securityPolicy=security_policy_name,
            body=rule,
            priority=priority,
        )
        .execute()
    )

    return updated_policy


def list_policies(project, credentials):
    """
    List all security policies of a GCP project.

    Parameters:
    ----------
        project: The project name where the policy is allocated.
        credentials: oauth2client.Credentials or google.auth.credentials.Credentials, credentials to be used for
            authentication. You can get them with 'get_workspace_impersonate_credentials_sa' method.

    """
    service = build("compute", "v1", credentials=credentials)

    policies = service.securityPolicies().list(project=project).execute()

    return policies
