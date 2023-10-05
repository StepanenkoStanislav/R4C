from django.db.models import Count
from django.http import HttpResponse
from django.views.decorators.http import require_GET

from robots.services import WEEK_AGO
from robots.services.make_robots_excel_report_service import (
    MakeExcelRobotsSummaryService)
from robots.models import Robot


@require_GET
def download_robots_summary(request):
    robots = Robot.objects.filter(created__gte=WEEK_AGO).values(
        'model', 'version').annotate(total=Count('model')).order_by('model')
    excel = MakeExcelRobotsSummaryService(
        robots,
        headers=['Модель', 'Версия', 'Количество за неделю'],
    )
    filename = excel.generate_filename(filename='robots_summary')
    response = HttpResponse(
        content=excel.create_report(),
        content_type='application/ms-excel'
    )
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response
