import plotly.express as px
import plotly.offline as opy
import plotly.graph_objects as go
import pandas as pd

def sold_percentage(soldcars,total):
    return (total-soldcars)*100/total

def frequency_table(df):
    # Simple counts
    manufacturer_counts = df['manufacturer'].value_counts().reset_index()
    manufacturer_counts.columns = ['Manufacturer', 'Count']
    # Convert to HTML using the correct method name: .to_html()
    table_html = manufacturer_counts.to_html(
    classes="table table-bordered table-striped table-sm",
    float_format='%.2f',
    justify='center'
    )
    
    # Create Plotly bar chart
    fig = px.bar(
        manufacturer_counts,
        x='Manufacturer',
        y='Count',
        title='Vehicle Count by Manufacturer',
        color='Count',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(height=550)
    
    # Convert chart to HTML div
    chart_html = opy.plot(fig, auto_open=False, output_type="div")
    
    return table_html + chart_html

def find_aggregate_things(df):
   df["profit"]=df["selling_price"]-df["wholesale_price"]
   df["range"]=df["selling_price"].max() - df["selling_price"].min()
   df["wholesale_range"]=df["wholesale_price"].max() - df["wholesale_price"].min()
   
   mansum=df.groupby(["manufacturer","transmission","body_type"]).agg({
        "selling_price":["sum","min","max"],
        "wholesale_price":"sum",
        "profit":"sum",
        "range":"sum",
        "wholesale_range":"sum"
    })

   return mansum.to_html(
    classes="table table-bordered table-striped table-sm",
    float_format='%.2f',
    justify='center'
    )




def display_crosstab_table(df):
   myfunc= pd.crosstab([df["manufacturer"],df["body_type"]],[df["transmission"],df["vehicle_condition"]])
   return myfunc.to_html(
    classes="table table-bordered table-striped table-sm",
    float_format='%.2f',
    justify='center'
    )

def get_range(x):
    return x.max()-x.min()

get_range.__name__="Rane"

def display_cross(df):
    myfunc= pd.crosstab([df["manufacturer"],df["body_type"],df["fuel_type"],df["engine_type"]],df["transmission"],values=df["selling_price"],aggfunc=["sum",get_range],margins=True)
    return myfunc.to_html(
    classes="table table-bordered table-striped table-sm",
    float_format='%.2f',
    justify='center'
    )


def display_pivot_table(df):
    mytable=pd.pivot_table(df,index=["client_continent","client_country","manufacturer"],values=["selling_price","wholesale_price"],aggfunc=["max","min","sum"])
    
    
    return mytable.to_html(
    classes="table table-bordered table-striped table-sm",
    float_format='%.2f',
    justify='center'
    )






def visualizing_sales_with_sunburst_chart(df,height=800):
    fig=px.treemap(df,path=["manufacturer","fuel_type","body_type"],values="selling_price")
    fig.update_traces(textinfo="label+value")
    
    fig.update_layout(height=height,updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=["type", "treemap"],
                    label="Treemap Chart",
                    method="restyle"
                ),
                dict(
                    args=["type", "sunburst"],
                    label="Sunburst Chart",
                    method="restyle"
                ),
                    dict(
                        args=["type", "icicle"],
                        label="Icicle Chart",
                        method="restyle"
                    ),

            ]),
            direction="down",
        ),
    ],)
    return opy.plot(fig,auto_open=False,output_type="div")












# def visualizing_sales_world_map(df, height=600):
    country_clients = df.groupby("client_country").size().reset_index(name="num_clients")

    # Create choropleth map (background colors)
    fig = px.choropleth(
        country_clients,
        locations="client_country",
        locationmode="country names",
        color="num_clients",
        color_continuous_scale="Viridis",
        title="Number of Clients by Country"
    )

    # Overlay text labels with country name + client count
    fig.add_trace(
        go.Scattergeo(
            locations=country_clients['client_country'],
            locationmode='country names',
            text=[f"{c}: {n}" for c, n in zip(country_clients['client_country'], country_clients['num_clients'])],
            mode='text',
            textfont=dict(size=12, color="black")
        )
    )

    # Adjust layout
    fig.update_layout(
        height=height,
        geo=dict(showframe=False, showcoastlines=True),
        margin=dict(l=0, r=0, t=50, b=0)
    )

    # Render as HTML div
    div = opy.plot(fig, auto_open=False, output_type="div")
    return div