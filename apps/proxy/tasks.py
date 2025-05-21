from datetime import timedelta

import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from .models import School, AvailabilitySlot, ChildcareCRMToken


@shared_task()
def renew_childcarecrm_token():
    url = f"{settings.CHILDCARECRM_BASE_URL}/api/v3/login"
    payload = {
        "username": settings.CHILDCARECRM_USERNAME,
        "password": settings.CHILDCARECRM_PASSWORD
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    data = response.json()
    token = data["token"]

    ChildcareCRMToken.objects.update_or_create(
        pk=1,
        defaults={
            "access_token": token
        }
    )

@shared_task
def sync_childcarecrm_slots():
    token = ChildcareCRMToken.get_token().access_token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    base_url = settings.CHILDCARECRM_BASE_URL

    # Start from yesterday, go 4 weeks forward
    start = (timezone.now() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=28)

    for school in School.objects.exclude(crm_id__isnull=True):
        if not school.crm_id:
            continue

        # Remove all existing availability slots in this full range
        AvailabilitySlot.objects.filter(
            school=school,
        ).delete()

        all_slots = []

        for offset in range(0, 28, 7):
            chunk_start = start + timedelta(days=offset)
            chunk_end = chunk_start + timedelta(days=7)

            params = {
                "start_datetime": chunk_start.strftime("%Y-%m-%d 00:00:00"),
                "end_datetime": chunk_end.strftime("%Y-%m-%d 23:59:59")
            }

            url = f"{base_url}/api/v3/centers/{school.crm_id}/tour-availability"

            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()

                for slot in data:
                    all_slots.append(AvailabilitySlot(
                        school=school,
                        start_datetime=slot["start_datetime"],
                        end_datetime=slot["end_datetime"],
                        is_available=slot["is_available"],
                        length=slot["length"],
                        start_datetime_raw=slot["start_datetime"],
                        end_datetime_raw=slot["end_datetime"]
                    ))

            except requests.RequestException as e:
                print(f"[ERROR] Failed for School {school.internal_uuid} (CRM {school.crm_id})")
                print(f"  URL: {response.url}")
                print(f"  Response: {response.text}")
                continue

        if all_slots:
            AvailabilitySlot.objects.bulk_create(all_slots)