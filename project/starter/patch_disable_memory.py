import argparse
import json
import sys
from pathlib import Path

import boto3
from botocore.exceptions import ClientError


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="agentcore_config.json",
                        help="Config file containing harness ARN and region.")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        sys.exit(f"Config file {args.config} not found.")

    config = json.loads(config_path.read_text(encoding="utf-8"))

    harness_id = config.get("harness_id")
    if not harness_id:
        sys.exit("No harness_id found in config.")

    region = config.get("region", "us-east-1")
    acc = boto3.client("bedrock-agentcore-control", region_name=region)

    try:
        # Get current harness details
        harness = acc.get_harness(harnessId=harness_id)["harness"]

        # Update to disable memory
        acc.update_harness(
            harnessId=harness_id,
            executionRoleArn=harness["executionRoleArn"],
            model=harness["model"],
            systemPrompt=harness["systemPrompt"],
            memory={"optionalValue": {"disabled": {}}},
        )
        print(f"Successfully disabled memory for harness {harness_id}")

        # Optionally update config to reflect
        config["memory_disabled"] = True
        config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

    except ClientError as e:
        print(f"Error updating harness: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()