# Create your views here.
from .models import WebHookTrigger
import json

def webhook_view(request, web_hook_id):
    webhook_trigger = WebHookTrigger.objects.get(pk=web_hook_id)
    webhook_data_type = webhook_trigger.data_type
    
    if webhook_data_type == 'json':
        data = json.loads(request.raw_post_data)
    else:
        data = request.REQUEST.dict()
    

    data.params = request.REQUEST
    webhook_trigger.trigger({"data": data, "headers": request.META})

