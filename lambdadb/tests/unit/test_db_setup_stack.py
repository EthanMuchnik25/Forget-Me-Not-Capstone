import aws_cdk as core
import aws_cdk.assertions as assertions

from db_setup.db_setup_stack import DbSetupStack

# example tests. To run these tests, uncomment this file along with the example
# resource in db_setup/db_setup_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = DbSetupStack(app, "db-setup")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
