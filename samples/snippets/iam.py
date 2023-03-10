#!/usr/bin/env python

# Copyright 2019 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to perform basic operations on IAM
policies with the Cloud Pub/Sub API.

For more information, see the README.md under /pubsub and the documentation
at https://cloud.google.com/pubsub/docs.
"""

import argparse


def get_topic_policy(project_id: str, topic_id: str) -> None:
    """Prints the IAM policy for the given topic."""
    # [START pubsub_get_topic_policy]
    from google.cloud import pubsub_v1

    # TODO(developer): Choose an existing topic.
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"

    client = pubsub_v1.PublisherClient()
    topic_path = client.topic_path(project_id, topic_id)

    policy = client.get_iam_policy(request={"resource": topic_path})

    print("Policy for topic {}:".format(topic_path))
    for binding in policy.bindings:
        print("Role: {}, Members: {}".format(binding.role, binding.members))
    # [END pubsub_get_topic_policy]


def get_subscription_policy(project_id: str, subscription_id: str) -> None:
    """Prints the IAM policy for the given subscription."""
    # [START pubsub_get_subscription_policy]
    from google.cloud import pubsub_v1

    # TODO(developer): Choose an existing subscription.
    # project_id = "your-project-id"
    # subscription_id = "your-subscription-id"

    client = pubsub_v1.SubscriberClient()
    subscription_path = client.subscription_path(project_id, subscription_id)

    policy = client.get_iam_policy(request={"resource": subscription_path})

    print("Policy for subscription {}:".format(subscription_path))
    for binding in policy.bindings:
        print("Role: {}, Members: {}".format(binding.role, binding.members))

    client.close()
    # [END pubsub_get_subscription_policy]


def set_topic_policy(project_id: str, topic_id: str) -> None:
    """Sets the IAM policy for a topic."""
    # [START pubsub_set_topic_policy]
    from google.cloud import pubsub_v1

    # TODO(developer): Choose an existing topic.
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"

    client = pubsub_v1.PublisherClient()
    topic_path = client.topic_path(project_id, topic_id)

    policy = client.get_iam_policy(request={"resource": topic_path})

    # Add all users as viewers.
    policy.bindings.add(role="roles/pubsub.viewer", members=["domain:google.com"])

    # Add a group as a publisher.
    policy.bindings.add(
        role="roles/pubsub.publisher", members=["group:cloud-logs@google.com"]
    )

    # Set the policy
    policy = client.set_iam_policy(request={"resource": topic_path, "policy": policy})

    print("IAM policy for topic {} set: {}".format(topic_id, policy))
    # [END pubsub_set_topic_policy]


def set_subscription_policy(project_id: str, subscription_id: str) -> None:
    """Sets the IAM policy for a topic."""
    # [START pubsub_set_subscription_policy]
    from google.cloud import pubsub_v1

    # TODO(developer): Choose an existing subscription.
    # project_id = "your-project-id"
    # subscription_id = "your-subscription-id"

    client = pubsub_v1.SubscriberClient()
    subscription_path = client.subscription_path(project_id, subscription_id)

    policy = client.get_iam_policy(request={"resource": subscription_path})

    # Add all users as viewers.
    policy.bindings.add(role="roles/pubsub.viewer", members=["domain:google.com"])

    # Add a group as an editor.
    policy.bindings.add(role="roles/editor", members=["group:cloud-logs@google.com"])

    # Set the policy
    policy = client.set_iam_policy(
        request={"resource": subscription_path, "policy": policy}
    )

    print("IAM policy for subscription {} set: {}".format(subscription_id, policy))

    client.close()
    # [END pubsub_set_subscription_policy]


def check_topic_permissions(project_id: str, topic_id: str) -> None:
    """Checks to which permissions are available on the given topic."""
    # [START pubsub_test_topic_permissions]
    from google.cloud import pubsub_v1

    # TODO(developer): Choose an existing topic.
    # project_id = "your-project-id"
    # topic_id = "your-topic-id"

    client = pubsub_v1.PublisherClient()
    topic_path = client.topic_path(project_id, topic_id)

    permissions_to_check = ["pubsub.topics.publish", "pubsub.topics.update"]

    allowed_permissions = client.test_iam_permissions(
        request={"resource": topic_path, "permissions": permissions_to_check}
    )

    print(
        "Allowed permissions for topic {}: {}".format(topic_path, allowed_permissions)
    )
    # [END pubsub_test_topic_permissions]


def check_subscription_permissions(project_id: str, subscription_id: str) -> None:
    """Checks to which permissions are available on the given subscription."""
    # [START pubsub_test_subscription_permissions]
    from google.cloud import pubsub_v1

    # TODO(developer): Choose an existing subscription.
    # project_id = "your-project-id"
    # subscription_id = "your-subscription-id"

    client = pubsub_v1.SubscriberClient()
    subscription_path = client.subscription_path(project_id, subscription_id)

    permissions_to_check = [
        "pubsub.subscriptions.consume",
        "pubsub.subscriptions.update",
    ]

    allowed_permissions = client.test_iam_permissions(
        request={"resource": subscription_path, "permissions": permissions_to_check}
    )

    print(
        "Allowed permissions for subscription {}: {}".format(
            subscription_path, allowed_permissions
        )
    )

    client.close()
    # [END pubsub_test_subscription_permissions]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Your Google Cloud project ID")

    subparsers = parser.add_subparsers(dest="command")

    get_topic_policy_parser = subparsers.add_parser(
        "get-topic-policy", help=get_topic_policy.__doc__
    )
    get_topic_policy_parser.add_argument("topic_id")

    get_subscription_policy_parser = subparsers.add_parser(
        "get-subscription-policy", help=get_subscription_policy.__doc__
    )
    get_subscription_policy_parser.add_argument("subscription_id")

    set_topic_policy_parser = subparsers.add_parser(
        "set-topic-policy", help=set_topic_policy.__doc__
    )
    set_topic_policy_parser.add_argument("topic_id")

    set_subscription_policy_parser = subparsers.add_parser(
        "set-subscription-policy", help=set_subscription_policy.__doc__
    )
    set_subscription_policy_parser.add_argument("subscription_id")

    check_topic_permissions_parser = subparsers.add_parser(
        "check-topic-permissions", help=check_topic_permissions.__doc__
    )
    check_topic_permissions_parser.add_argument("topic_id")

    check_subscription_permissions_parser = subparsers.add_parser(
        "check-subscription-permissions",
        help=check_subscription_permissions.__doc__,
    )
    check_subscription_permissions_parser.add_argument("subscription_id")

    args = parser.parse_args()

    if args.command == "get-topic-policy":
        get_topic_policy(args.project_id, args.topic_id)
    elif args.command == "get-subscription-policy":
        get_subscription_policy(args.project_id, args.subscription_id)
    elif args.command == "set-topic-policy":
        set_topic_policy(args.project_id, args.topic_id)
    elif args.command == "set-subscription-policy":
        set_subscription_policy(args.project_id, args.subscription_id)
    elif args.command == "check-topic-permissions":
        check_topic_permissions(args.project_id, args.topic_id)
    elif args.command == "check-subscription-permissions":
        check_subscription_permissions(args.project_id, args.subscription_id)
