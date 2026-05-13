import pandas as pd
from django.shortcuts import render, redirect
from .models import Dataset

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import pandas as pd
from .models import Dataset


def export_pdf(request):
    dataset = Dataset.objects.last()

    if not dataset:
        return HttpResponse("No data available")

    path = dataset.file.path

    if path.endswith('.csv'):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)

    numeric = df.select_dtypes(include='number')

    total = numeric.sum().sum()
    mean = numeric.mean().mean()
    max_val = numeric.max().max()
    min_val = numeric.min().min()

    template = get_template('dashboard/report.html')

    html = template.render({
        'total': total,
        'mean': mean,
        'max': max_val,
        'min': min_val,
        'table': df.head(15).to_html()
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response
# def upload_file(request):
#     if request.method == 'POST':
#         file = request.FILES.get('file')
#
#         if not file:
#             return render(request, 'dashboard/upload.html', {'error': 'No file selected'})
#
#         Dataset.objects.create(
#             name=file.name,
#             file=file
#         )
#
#         return redirect('dashboard')
#
#     return render(request, 'dashboard/upload.html')
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        file_type = request.POST.get('file_type')

        if not file:
            return render(request, 'dashboard/upload.html', {'error': 'No file selected'})

        Dataset.objects.create(
            name=file.name,
            file=file,
            file_type=file_type
        )

        return redirect('dashboard')

    return render(request, 'dashboard/upload.html')
import pandas as pd
from django.shortcuts import render
from .models import Dataset

import pandas as pd
import numpy as np
from django.shortcuts import render
from .models import Dataset

def dashboard_view(request):
    dataset = Dataset.objects.last()

    if not dataset:
        return render(request, 'dashboard/dashboard.html', {'error': 'No data uploaded'})

    path = dataset.file.path

    # Load file
    if path.endswith('.csv'):
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)

    numeric = df.select_dtypes(include='number')

    if numeric.empty:
        return render(request, 'dashboard/dashboard.html', {'error': 'No numeric data'})

    # Column selection
    col = request.GET.get('column', numeric.columns[0])
    data = numeric[col].fillna(0)

    labels = list(range(len(data)))
    values = data.tolist()

    # KPI Metrics
    total = data.sum()
    mean = data.mean()
    median = data.median()
    std = data.std()
    max_val = data.max()
    min_val = data.min()
    count = data.count()

    growth = ((data.iloc[-1] - data.iloc[0]) / data.iloc[0])*100 if len(data) > 1 else 0

    # Multi-column
    multi_data = numeric.head(10).to_dict(orient='list')
    multi_labels = list(range(len(numeric.head(10))))

    context = {
        'columns': numeric.columns,
        'selected': col,
        'labels': labels,
        'values': values,
        'total': round(total,2),
        'mean': round(mean,2),
        'median': round(median,2),
        'std': round(std,2),
        'max': max_val,
        'min': min_val,
        'count': count,
        'growth': round(growth,2),
        'multi_labels': multi_labels,
        'multi_data': multi_data,
        'table': df.head(15).to_html()
    }

    return render(request, 'dashboard/dashboard.html', context)
import pandas as pd
import numpy as np
from django.shortcuts import render
from .models import Dataset
#
# def analytics_view(request):
#     dataset = Dataset.objects.last()
#
#     if not dataset:
#         return render(request, 'dashboard/analytics.html', {'error': 'No data uploaded'})
#
#     path = dataset.file.path
#
#     if path.endswith('.csv'):
#         df = pd.read_csv(path)
#     else:
#         df = pd.read_excel(path)
#
#     numeric = df.select_dtypes(include='number')
#
#     if numeric.empty:
#         return render(request, 'dashboard/analytics.html', {'error': 'No numeric data'})
#
#     col = numeric.columns[0]
#     data = numeric[col].dropna()
#
#     total = data.sum()
#     mean = data.mean()
#     median = data.median()
#     std = data.std()
#     var = data.var()
#     max_val = data.max()
#     min_val = data.min()
#
#     # Growth (simple)
#     growth = ((data.iloc[-1] - data.iloc[0]) / data.iloc[0]) * 100 if len(data) > 1 else 0
#
#     # Top & Bottom
#     top5 = data.sort_values(ascending=False).head(5)
#     bottom5 = data.sort_values().head(5)
#
#     # Correlation
#     corr = numeric.corr().to_html()
#
#     # Insights
#     insight = ""
#     if mean > median:
#         insight = "Data is positively skewed (higher values dominate)"
#     elif mean < median:
#         insight = "Data is negatively skewed"
#     else:
#         insight = "Data is balanced"
#
#     if std > mean:
#         insight += " | High variation in dataset ⚠️"
#     else:
#         insight += " | Stable dataset ✅"
#
#     context = {
#         'total': round(total,2),
#         'mean': round(mean,2),
#         'median': round(median,2),
#         'std': round(std,2),
#         'var': round(var,2),
#         'max': max_val,
#         'min': min_val,
#         'growth': round(growth,2),
#         'top5': top5.to_dict(),
#         'bottom5': bottom5.to_dict(),
#         'correlation': corr,
#         'insight': insight
#     }
#
#     return render(request, 'dashboard/analytics.html', context)



# import pandas as pd
# from django.shortcuts import render
#
# def analytics_view(request):
#     try:
#         df = pd.read_csv('media/data.csv')  # change if dynamic
#     except:
#         return render(request, 'dashboard/analytics.html', {'error': 'No dataset found'})
#
#     numeric = df.select_dtypes(include='number')
#
#     if numeric.empty:
#         return render(request, 'dashboard/analytics.html', {'error': 'No numeric columns'})
#
#     col = request.GET.get('column', numeric.columns[0])
#     data = numeric[col].dropna()
#
#     # 🔢 BASIC STATS
#     total = round(data.sum(), 2)
#     mean = round(data.mean(), 2)
#     median = round(data.median(), 2)
#     std = round(data.std(), 2)
#     var = round(data.var(), 2)
#     min_val = round(data.min(), 2)
#     max_val = round(data.max(), 2)
#
#     # 📈 GROWTH
#     growth = 0
#     if len(data) > 1 and data.iloc[0] != 0:
#         growth = round(((data.iloc[-1] - data.iloc[0]) / data.iloc[0]) * 100, 2)
#
#     # 🔝 TOP / BOTTOM
#     top5 = data.sort_values(ascending=False).head(5).tolist()
#     bottom5 = data.sort_values().head(5).tolist()
#
#     # 📊 HISTOGRAM
#     bins = pd.cut(data, bins=8).value_counts().sort_index()
#     bin_labels = [str(b) for b in bins.index]
#     bin_values = bins.tolist()
#
#     # 📈 TREND
#     labels = list(range(len(data)))
#     values = data.tolist()
#
#     # 🔗 CORRELATION
#     correlation = numeric.corr().to_html(classes='table')
#
#     # 🧠 INSIGHT
#     insight = f"Mean is {mean}, max is {max_val}, growth is {growth}%."
#
#     context = {
#         'columns': numeric.columns,
#         'selected': col,
#         'total': total,
#         'mean': mean,
#         'median': median,
#         'std': std,
#         'var': var,
#         'min': min_val,
#         'max': max_val,
#         'growth': growth,
#         'top5': top5,
#
#         'bottom5': bottom5,
#         'bin_labels': bin_labels,
#         'bin_values': bin_values,
#         'labels': labels,
#         'values': values,
#         'correlation': correlation,
#         'insight': insight
#     }
#
#     return render(request, 'dashboard/analytics.html', context)



import pandas as pd
from django.shortcuts import render
from .models import Dataset

def analytics_view(request):
    dataset = Dataset.objects.last()

    if not dataset:
        return render(request, 'dashboard/analytics.html', {'error': 'No dataset uploaded'})

    file_path = dataset.file.path

    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            return render(request, 'dashboard/analytics.html', {'error': 'Unsupported file'})
    except Exception as e:
        return render(request, 'dashboard/analytics.html', {'error': str(e)})

    numeric = df.select_dtypes(include='number')

    if numeric.empty:
        return render(request, 'dashboard/analytics.html', {'error': 'No numeric columns'})

    col = request.GET.get('column', numeric.columns[0])
    data = numeric[col].dropna()

    # Stats
    total = round(data.sum(), 2)
    mean = round(data.mean(), 2)
    median = round(data.median(), 2)
    std = round(data.std(), 2)
    var = round(data.var(), 2)
    min_val = round(data.min(), 2)
    max_val = round(data.max(), 2)

    growth = 0
    if len(data) > 1 and data.iloc[0] != 0:
        growth = round(((data.iloc[-1] - data.iloc[0]) / data.iloc[0]) * 100, 2)

    top5 = data.sort_values(ascending=False).head(5).tolist()
    bottom5 = data.sort_values().head(5).tolist()

    bins = pd.cut(data, bins=8).value_counts().sort_index()
    bin_labels = [str(b) for b in bins.index]
    bin_values = bins.tolist()

    labels = list(range(len(data)))
    values = data.tolist()

    correlation = numeric.corr().to_html(classes='table')

    insight = f"Mean {mean}, Max {max_val}, Growth {growth}%"

    return render(request, 'dashboard/analytics.html', {
        'columns': numeric.columns,
        'selected': col,
        'total': total,
        'mean': mean,
        'median': median,
        'std': std,
        'var': var,
        'min': min_val,
        'max': max_val,
        'growth': growth,
        'top5': top5,
        'bottom5': bottom5,
        'bin_labels': bin_labels,
        'bin_values': bin_values,
        'labels': labels,
        'values': values,
        'correlation': correlation,
        'insight': insight
    })
