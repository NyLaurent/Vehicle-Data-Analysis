from django.shortcuts import render

# Create your views here.
import pandas as pd
from django.shortcuts import render
from .dashboard import frequency_table,find_aggregate_things,display_crosstab_table,display_cross,display_pivot_table,visualizing_sales_with_sunburst_chart

def dashboard_view(request):
    queryset = pd.read_csv("dummy_data/vehicles_data_1000.csv")
    df = pd.DataFrame(queryset)
    return render(request, "vehicles/index.html", {
    "frequency_table": frequency_table(df),
    "aggregate_table": find_aggregate_things(df),
    "cross_tab":display_crosstab_table(df),
    "cross":display_cross(df),
    "pivot":display_pivot_table(df),
    "sunburst":visualizing_sales_with_sunburst_chart(df)




    })
