# selinux/serializers.py

from rest_framework import serializers
from .models import Selinux, SElinuxEvent


class SElinuxEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SElinuxEvent
        fields = ['digest', 'hostname', 'event', 'date', 'time', 'serial_num', 'event_kind', 'session', 'subj_prime', 'subj_sec', 'subj_kind', 'action', 'result', 'obj_prime', 'obj_sec', 'obj_kind', 'how']

class SelinuxDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selinux
        fields = ['hostname', 'status', 'mount', 'rootdir', 'policyname', 'current_mode', 'configured_mode', 'mslstatus', 'memprotect', 'maxkernel', 'total', 'success', 'failed', 'sealerts']


