import json
import logging

from django.shortcuts import HttpResponse, redirect, get_object_or_404

from fundoo.settings import file_handler
from note.decorators import labelvalidator, collvalidator
from note.models import Label, Notes
from lib.redis import red
from django.core import signing
from pymitter import EventEmitter

# from django.urls import reverse
#
# current_url = reverse(request.path_info).url_name
ee = EventEmitter()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


class LabelCollaborators:
    def __init__(self, function):
        self.function = function
        # One-time configuration and initialization.

    def __call__(self, request, *args, **kwargs):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if request.get_full_path() == "/api/notes/" and request.method == 'POST':
            z = json.loads(request.body)

            try:
                if labelvalidator(z['label'], request.user.id):
                    smd = {'success': False, 'message': 'label is not created by this user or user does not exist',
                           'data': []}
                    return HttpResponse(json.dumps(smd, indent=2), status=400)
            except KeyError:
                pass
            try:
                # pdb.set_trace()
                if collvalidator(z['collaborators']):
                    smd = {'success': False, 'message': 'email not vaild',
                           'data': []}
                    return HttpResponse(json.dumps(smd, indent=2), status=400)
            except KeyError:
                pass

            response = self.function(request, *args, **kwargs)
            return response
        else:
            response = self.function(request, *args, **kwargs)
            return response
