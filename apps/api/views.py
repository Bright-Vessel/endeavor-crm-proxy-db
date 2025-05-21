from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AvailabilitySlotSerializer
from apps.proxy.models import AvailabilitySlot, School


class AvailabilitySlotListView(APIView):
    def get(self, request, crm_id):
        try:
            school = School.objects.get(crm_id=crm_id)
        except School.DoesNotExist:
            return Response({"error": "School not found."}, status=404)

        slots = AvailabilitySlot.objects.filter(school=school).order_by('start_datetime')
        serializer = AvailabilitySlotSerializer(slots, many=True)
        return Response(serializer.data)
