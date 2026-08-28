@'
import json
import os
import uuid
from datetime import datetime, timezone

import boto3

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])


def _tool_name(context):
    """AgentCore Gateway passes the tool name via the Lambda client context."""
    client_context = getattr(context, "client_context", None)
    custom = getattr(client_context, "custom", None) or {}
    name = custom.get("bedrockAgentCoreToolName", "")
    return name.split("___")[-1] if "___" in name else name


def lambda_handler(event, context):
    print("EVENT:", json.dumps(event, default=str))

    tool_name = _tool_name(context)
    print("TOOL NAME:", tool_name)

    if tool_name and tool_name != "create_bug_report":
        return {"error": f"unsupported tool: {tool_name}"}

    if not isinstance(event, dict):
        return {"error": "unexpected event shape", "event": str(event)}

    values = {
        "description": event.get("description"),
        "stepsToReproduce": event.get("stepsToReproduce"),
        "environment": event.get("environment"),
    }

    invalid = [
        name
        for name, value in values.items()
        if not isinstance(value, str) or not value.strip()
    ]

    if invalid:
        return {
            "error": (
                "required field(s) must be non-empty strings: "
                + ", ".join(invalid)
            )
        }

    description = values["description"].strip()
    steps = values["stepsToReproduce"].strip()
    environment = values["environment"].strip()

    ticket_id = str(uuid.uuid4())

    item = {
        "ticketId": ticket_id,
        "description": description,
        "stepsToReproduce": steps,
        "environment": environment,
        "status": "OPEN",
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }

    table.put_item(Item=item)

    print("CREATED TICKET:", ticket_id)

    return {
        "ticketId": ticket_id,
        "status": "OPEN",
    }
'@ | Set-Content -Path .\index.py -Encoding UTF8