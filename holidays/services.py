from core.services import BaseService
from .models import Holiday

class HolidayService(BaseService):
    model = Holiday

    @classmethod
    def is_holiday(cls, check_date):
        return cls.model.objects.filter(start_date__lte=check_date, end_date__gte=check_date).exists()

    @classmethod
    def get_upcoming(cls, limit=5):
        from django.utils import timezone
        return cls.model.objects.filter(start_date__gte=timezone.now().date()).order_by('start_date')[:limit]

    @classmethod
    def get_by_date_range(cls, start_date, end_date):
        return cls.model.objects.filter(start_date__lte=end_date, end_date__gte=start_date)
