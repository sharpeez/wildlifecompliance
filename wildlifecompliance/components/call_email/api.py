import traceback
import os
import base64
import geojson
from django.db.models import Q, Min
from django.db import transaction
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.conf import settings
from wildlifecompliance import settings
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework import viewsets, serializers, status, generics, views
import rest_framework.exceptions as rest_exceptions
from rest_framework.decorators import (
    detail_route,
    list_route,
    renderer_classes,
    parser_classes,
    api_view
)
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission
from rest_framework.pagination import PageNumberPagination
from datetime import datetime, timedelta
from collections import OrderedDict
from django.core.cache import cache
from ledger.accounts.models import EmailUser, Address
from ledger.address.models import Country
from ledger.checkout.utils import calculate_excl_gst
from datetime import datetime, timedelta, date
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from wildlifecompliance.helpers import is_customer, is_internal
from wildlifecompliance.components.call_email.models import (
    CallEmail,
    Classification,
    Location,
    ComplianceFormDataRecord,
    ReportType,
)
from wildlifecompliance.components.call_email.serializers import (
    CallEmailSerializer,
    ClassificationSerializer,
    # CreateCallEmailSerializer,
    UpdateRendererDataSerializer,
    ComplianceFormDataRecordSerializer,
    UpdateRendererDataSerializer,
    ComplianceLogEntrySerializer,
    LocationSerializer,
    ComplianceUserActionSerializer,
    # UpdateCallEmailSerializer,
    LocationSerializer,
    ReportTypeSerializer,
    SaveCallEmailSerializer,
)
from utils import SchemaParser

from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.renderers import DatatablesRenderer


class CallEmailViewSet(viewsets.ModelViewSet):
    queryset = CallEmail.objects.all()
    serializer_class = CallEmailSerializer

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            return CallEmail.objects.all()
        return CallEmail.objects.none()

    @list_route(methods=['GET', ])
    def datatable_list(self, request, *args, **kwargs):
        try:
            qs = self.get_queryset()
            serializer = self.get_serializer(
                qs, many=True, context={'request': request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['post'])
    @renderer_classes((JSONRenderer,))
    def form_data(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            ComplianceFormDataRecord.process_form(
                request,
                instance,
                request.data,
                action=ComplianceFormDataRecord.ACTION_TYPE_ASSIGN_VALUE
            )
            return redirect(reverse('external'))
        # except MissingFieldsException as e:
         #   return Response({
          #      'missing': e.error_list},
           #     status=status.HTTP_400_BAD_REQUEST
            # )
        except ValidationError as e:
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
        raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST'])
    @renderer_classes((JSONRenderer,))
    def process_document(self, request, *args, **kwargs):
        try:
            print("process_document")
            print(request.data)
            instance = self.get_object()
            action = request.data.get('action')
            section = request.data.get('input_name')
            if action == 'list' and 'input_name' in request.data:
                pass

            elif action == 'delete' and 'document_id' in request.data:
                document_id = request.data.get('document_id')
                document = instance.documents.get(id=document_id)

                if document._file and os.path.isfile(
                        document._file.path) and document.can_delete:
                    os.remove(document._file.path)

                document.delete()
                instance.save(version_comment='Approval File Deleted: {}'.format(
                    document.name))  # to allow revision to be added to reversion history

            elif action == 'save' and 'input_name' in request.data and 'filename' in request.data:
                application_id = request.data.get('application_id')
                filename = request.data.get('filename')
                _file = request.data.get('_file')
                if not _file:
                    _file = request.data.get('_file')

                document = instance.documents.get_or_create(
                    input_name=section, name=filename)[0]
                path = default_storage.save(
                    'applications/{}/documents/{}'.format(
                        application_id, filename), ContentFile(
                        _file.read()))

                document._file = path
                document.save()
                # to allow revision to be added to reversion history
                instance.save(
                    version_comment='File Added: {}'.format(filename))

            return Response(
                [
                    dict(
                        input_name=d.input_name,
                        name=d.name,
                        file=d._file.url,
                        id=d.id,
                        can_delete=d.can_delete) for d in instance.documents.filter(
                        input_name=section) if d._file])

        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e, 'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                raise serializers.ValidationError(repr(e[0].encode('utf-8')))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET', ])
    def action_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.action_logs.all()
            serializer = ComplianceUserActionSerializer(qs, many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET', ])
    def comms_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.comms_logs.all()
            serializer = ComplianceLogEntrySerializer(qs, many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST', ])
    @renderer_classes((JSONRenderer,))
    def add_comms_log(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                request.data['call_email'] = u'{}'.format(instance.id)
                # request.data['staff'] = u'{}'.format(request.user.id)
                print("request.data")
                print(request.data)
                serializer = ComplianceLogEntrySerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                comms = serializer.save()
                # Save the files
                for f in request.FILES:
                    document = comms.documents.create()
                    document.name = str(request.FILES[f])
                    document._file = request.FILES[f]
                    document.save()
                # End Save Documents

                return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    # def create_call_location_renderer(self, request, *args, **kwargs):
    def create(self, request, *args, **kwargs):
        print("create")
        #print(request.data)
        try:
            with transaction.atomic():
                # request_data = {
                #     'classification': request.data.get('classification'),
                #     'report_type': request.data.get('report_type'),
                #     'classification_id': request.data.get('classification_id'),
                #     'report_type_id': request.data.get('report_type_id'),
                #     'caller': request.data.get('caller'),
                #     'assigned_to': request.data.get('assigned_to'),
                #     }
                request_data = request.data
                print(request_data)
                location_request_data = request.data.get('location')

                if (
                        location_request_data.get('geometry', {}).get('coordinates', {})[0] or
                        location_request_data.get('properties', {}).get('postcode', {})
                    ):
                    location_serializer = LocationSerializer(data=location_request_data, partial=True)
                    location_serializer.is_valid(raise_exception=True)
                    if location_serializer.is_valid():
                        location_instance = location_serializer.save()
                        request_data.update({'location_id': location_instance.id})

                serializer = SaveCallEmailSerializer(data=request_data, partial=True)
                serializer.is_valid(raise_exception=True)
                if serializer.is_valid():
                    serializer.save()
                    headers = self.get_success_headers(serializer.data)
                    returned_data = serializer.data
                    returned_data.update({'classification_id': request_data.get('classification_id')})
                    returned_data.update({'report_type_id': request_data.get('report_type_id')})
                    print("returned_data")
                    print(returned_data)
                    return Response(
                        returned_data,
                        status=status.HTTP_201_CREATED,
                        headers=headers
                        )
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))
    
    @detail_route(methods=['POST', ])
    def call_email_save(self, request, *args, **kwargs):
        print("call_email_save")
        #print(request.data)
        instance = self.get_object()
        try:
            with transaction.atomic():
                # request_data = {
                #     'classification': request.data.get('classification'),
                #     'report_type': request.data.get('report_type'),
                #     'classification_id': request.data.get('classification_id'),
                #     'report_type_id': request.data.get('report_type_id'),
                #     'caller': request.data.get('caller'),
                #     'assigned_to': request.data.get('assigned_to'),
                #     }
                request_data = request.data
                print(request_data)

                location_request_data = request.data.get('location')
                
                if (
                        location_request_data.get('geometry', {}).get('coordinates', {})[0] or
                        location_request_data.get('properties', {}).get('postcode', {})
                    ):
                    if location_request_data.get('id'):
                        location_instance = instance.location
                        location_serializer = LocationSerializer(instance=location_instance, data=request.data, partial=True)
                        location_serializer.is_valid(raise_exception=True)
                        if location_serializer.is_valid():
                            location_serializer.save()
                    else:
                        location_serializer = LocationSerializer(data=location_request_data, partial=True)
                        location_serializer.is_valid(raise_exception=True)
                        if location_serializer.is_valid():
                            location_instance = location_serializer.save()
                            request_data.update({'location_id': location_instance.id})
                
                if request_data.get('renderer_data'):
                    # post_data = {'user': request.user, 'data': request_data.get('renderer_data')}
                    # print("request")
                    # print(request)
                    # print("post_data")
                    # print(post_data)
                    request.data = request_data.get('renderer_data')
                    form_data_response = self.form_data(instance, request)
                    print("form_data_response")
                    print(form_data_response)
                    request_data.update({'data': form_data_response})

            serializer = SaveCallEmailSerializer(instance, data=request_data)
            serializer.is_valid(raise_exception=True)
            if serializer.is_valid():
                serializer.save()
                headers = self.get_success_headers(serializer.data)
                returned_data = serializer.data
                returned_data.update({'classification_id': request_data.get('classification_id')})
                returned_data.update({'report_type_id': request_data.get('report_type_id')})
                print("returned_data")
                print(returned_data)
                return Response(
                    returned_data,
                    status=status.HTTP_201_CREATED,
                    headers=headers
                    )
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    # def bak_create(self, request, *args, **kwargs):
    #     print("create")
    #     print(request.data)
    #     try:
    #         request_classification_str = request.data.get(
    #                     'classification')
    #         request_classification_obj = Classification.objects.get(
    #                 name=request_classification_str.capitalize())
    #         # parser = SchemaParser()
    #         # form_data = request.data.get('schema')
    #         # parsed_json = parser.create_data_from_form(form_data)
    #         request_data = {
    #                 'status': request.data.get('status'),
    #                 'classification': request_classification_obj.id,
    #                 'number': request.data.get('number'),
    #                 'caller': request.data.get('caller'),
    #                 'assigned_to': request.data.get('assigned_to'),
    #                 # 'data': parsed_json,
    #                 }
    #         serializer = CreateCallEmailSerializer(data=request_data)
    #         serializer.is_valid(raise_exception=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             headers = self.get_success_headers(serializer.data)
    #             return Response(
    #                 serializer.data,
    #                 status=status.HTTP_201_CREATED,
    #                 headers=headers
    #                 )
    #     except serializers.ValidationError:
    #         print(traceback.print_exc())
    #         raise
    #     except ValidationError as e:
    #         print(traceback.print_exc())
    #         raise serializers.ValidationError(repr(e.error_dict))
    #     except Exception as e:
    #         print(traceback.print_exc())
    #         raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST', ])
    @renderer_classes((JSONRenderer,))
    def new_location(self, request, *args, **kwargs):
        print("request.data")
        print(request.data)
        try:
            #instance = self.get_object()
            #location_instance = instance.location
            serializer = LocationSerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            if serializer.is_valid():
                print("serializer.validated_data")
                print(serializer.validated_data)
                serializer.save()
                headers = self.get_success_headers(serializer.data)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                    headers=headers
                    )
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e, 'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                raise serializers.ValidationError(repr(e[0].encode('utf-8')))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST', ])
    @renderer_classes((JSONRenderer,))
    def update_location(self, request, *args, **kwargs):
        print("request.data")
        print(request.data)
        try:
            instance = self.get_object()
            location_instance = instance.location
            serializer = LocationSerializer(instance=location_instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            if serializer.is_valid():
                print("serializer.validated_data")
                print(serializer.validated_data)
                serializer.save()
                headers = self.get_success_headers(serializer.data)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                    headers=headers
                    )
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e, 'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                raise serializers.ValidationError(repr(e[0].encode('utf-8')))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


class ClassificationViewSet(viewsets.ModelViewSet):
    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            return Classification.objects.all()
        return Classification.objects.none()


class ReportTypeViewSet(viewsets.ModelViewSet):
    queryset = ReportType.objects.all()
    serializer_class = ReportTypeSerializer

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            return ReportType.objects.all()
        return ReportType.objects.none()


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            return Location.objects.all()
        return Location.objects.none()

    #@detail_route(methods=['POST', ])
    #@renderer_classes((JSONRenderer,))
    def create(self, request, *args, **kwargs):
        print("request.data")
        print(request.data)
        try:
            #instance = self.get_object()
            #location_instance = instance.location
            serializer = LocationSerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            if serializer.is_valid():
                print("serializer.validated_data")
                print(serializer.validated_data)
                serializer.save()
                headers = self.get_success_headers(serializer.data)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                    headers=headers
                    )
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e, 'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                raise serializers.ValidationError(repr(e[0].encode('utf-8')))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


# class CallEmailViewSet(viewsets.ModelViewSet):
#     queryset = Location.objects.all()
#     serializer_class = CallEmailSerializer

