# Deployment Trigger
# This file is used to trigger new deployments on Render
# Last updated: 2025-10-03 - Fixed payment redirect and mobile money config

DEPLOYMENT_VERSION = "v2.1.0"
LAST_UPDATE = "2025-10-03"
CHANGES = [
    "Fixed payment redirect to upload page",
    "Enhanced transaction animations",
    "Fixed mobile money configuration",
    "Improved demo mode reliability",
    "Fixed admin user delete functionality"
]

def get_deployment_info():
    return {
        'version': DEPLOYMENT_VERSION,
        'last_update': LAST_UPDATE,
        'changes': CHANGES
    }
