from velocity.misc.format import to_json
import json
import traceback

class SqsHandler:
    def __init__(self, event, context):
        self.event = event
        self.context = context
        self.serve_action_default = True

    def serve(self, tx):
        records = self.event.get('Records', [])
        print(f"Handling batch of {len(records)} records from SQS")
        for record in records:
            print(f"Start MessageId {record.get('messageId')}")
            attrs = record.get('attributes')
            try:
                postdata = {}
                if record.get('body'):
                    postdata = json.loads(record.get('body'))
                if hasattr(self, 'beforeAction'):
                    self.beforeAction(attrs=attrs, postdata=postdata)
                actions = []
                action = postdata.get('action')
                if action:
                    actions.append(
                        f"on action {action.replace('-', ' ').replace('_', ' ')}"
                        .title().replace(' ', ''))
                if self.serve_action_default:
                    actions.append('OnActionDefault')
                for action in actions:
                    if hasattr(self, action):
                        getattr(self, action)(attrs=attrs, postdata=postdata)
                        break
                if hasattr(self, 'afterAction'):
                    self.afterAction(attrs=attrs, postdata=postdata)
            except Exception as e:
                if hasattr(self, 'onError'):
                    self.onError(attrs=attrs,
                                 postdata=postdata,
                                 exc=e,
                                 tb=traceback.format_exc())

    def OnActionDefault(self, tx, attrs, postdata):
        print(
            "Action handler not found. Calling default action `SqsHandler.OnActionDefault` with the following parameters for tx, attrs, and postdata:"
        )
        print({'tx': tx, 'attrs': attrs, 'postdata': postdata})
