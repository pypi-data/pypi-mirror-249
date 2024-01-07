from velocity.misc.format import to_json
import json
import pprint
import traceback

class LambdaHandler:
    def __init__(self, event, context):
        self.event = event
        self.context = context
        self.serve_action_default = True

        requestContext = event.get('requestContext', {})
        identity = requestContext.get('identity', {})
        headers = event.get('headers', {})
        self.session = {
            'authentication_provider':
            identity.get('cognitoAuthenticationProvider'),
            'authentication_type':
            identity.get('cognitoAuthenticationType'),
            'cognito_user':
            identity.get('user'),
            'is_desktop':
            headers.get('CloudFront-Is-Desktop-Viewer') == 'true',
            'is_mobile':
            headers.get('CloudFront-Is-Mobile-Viewer') == 'true',
            'is_smart_tv':
            headers.get('CloudFront-Is-SmartTV-Viewer') == 'true',
            'is_tablet':
            headers.get('CloudFront-Is-Tablet-Viewer') == 'true',
            'origin':
            headers.get('origin'),
            'path':
            event.get('path'),
            'referer':
            headers.get('Referer'),
            'source_ip':
            identity.get('sourceIp'),
            'user_agent':
            identity.get('userAgent'),
        }
        if self.session.get('is_mobile'):
            self.session['device_type'] = 'mobile'
        elif self.session.get('is_desktop'):
            self.session['device_type'] = 'desktop'
        elif self.session.get('is_tablet'):
            self.session['device_type'] = 'tablet'
        elif self.session.get('is_smart_tv'):
            self.session['device_type'] = 'smart_tv'
        else:
            self.session['device_type'] = 'unknown'

    def serve(self, tx):
        response = {
            'statusCode': 200,
            'body': '{}',
            'headers': {
                'Content-Type': 'application/json',
                "Access-Control-Allow-Origin": "*",
            },
        }
        try:
            postdata = {}
            if self.event.get('body'):
                postdata = json.loads(self.event.get('body'))
            req_params = self.event.get('queryStringParameters') or {}
            if hasattr(self, 'beforeAction'):
                self.beforeAction(args=req_params,
                                  postdata=postdata,
                                  response=response)
            actions = []
            action = postdata.get('action', req_params.get('action'))
            if action:
                actions.append(
                    f"on action {action.replace('-', ' ').replace('_', ' ')}".
                    title().replace(' ', ''))
            if self.serve_action_default:
                actions.append('OnActionDefault')
            for action in actions:
                if hasattr(self, action):
                    getattr(self, action)(args=req_params,
                                          postdata=postdata,
                                          response=response)
                    break
            if hasattr(self, 'afterAction'):
                self.afterAction(args=req_params,
                                 postdata=postdata,
                                 response=response)

        except Exception as e:
            response = {
                'statusCode':
                500,
                'body':
                to_json({
                    'type': 'Unhandled Exception',
                    'error_message': str(e),
                    'user_message': 'Oops! An unhandled error occurred.',
                    'traceback': traceback.format_exc() if DEBUG else None
                }),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
            if hasattr(self, 'onError'):
                self.onError(args=req_params,
                             postdata=postdata,
                             response=response,
                             exc=e,
                             tb=traceback.format_exc())

        return response

    def OnActionDefault(self, tx, args, postdata, response):
        response['body'] = to_json({'event': self.event, 'postdata': postdata})

    def onError(self, tx, args, postdata, response, exc, tb):
        pprint.pprint({
            'message': 'Unhandled Exception',
            'exception': str(exc),
            'traceback': traceback.format_exc()
        })

