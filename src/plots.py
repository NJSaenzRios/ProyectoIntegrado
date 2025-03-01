import matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from pandas import DataFrame

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_revenue_by_month_year(df: pd.DataFrame, year: int):
    """Plot revenue by month in a given year.

    Args:
        df (DataFrame): Dataframe with revenue by month and year query result
        year (int): It could be 2016, 2017 or 2018.
    """
    if f"Year{year}" not in df.columns:
        raise ValueError(f"El DataFrame no contiene la columna 'Year{year}'")

    # Resetear estilos de Matplotlib
    plt.rcdefaults()
    sns.set_style("whitegrid")

    # Crear la figura
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Línea de ingresos por mes
    sns.lineplot(data=df, x="month", y=f"Year{year}", marker="o", ax=ax1, label="Revenue")

    # Crear segundo eje para barras
    ax2 = ax1.twinx()
    sns.barplot(data=df, x="month", y=f"Year{year}", alpha=0.5, ax=ax2, color="skyblue")

    # Configurar títulos y etiquetas
    ax1.set_title(f"Revenue by Month in {year}", fontsize=14)
    ax1.set_xlabel("Month", fontsize=12)
    ax1.set_ylabel("Revenue", fontsize=12)
    
    plt.xticks(rotation=45)  # Rotar etiquetas del eje X si es necesario
    plt.legend()

    plt.show()


def plot_real_vs_predicted_delivered_time(df: DataFrame, year: int):
    """Plot real vs predicted delivered time by month in a given year

    Args:
        df (DataFrame): Dataframe with real vs predicted delivered time by month and
                        year query result
        year (int): It could be 2016, 2017 or 2018
    """
    matplotlib.rc_file_defaults()
    sns.set_style(style=None, rc=None)

    _, ax1 = plt.subplots(figsize=(12, 6))

    sns.lineplot(data=df[f"Year{year}_real_time"], marker="o", sort=False, ax=ax1)
    ax1.twinx()
    g = sns.lineplot(
        data=df[f"Year{year}_estimated_time"], marker="o", sort=False, ax=ax1
    )
    g.set_xticks(range(len(df)))
    g.set_xticklabels(df.month.values)
    g.set(xlabel="month", ylabel="Average days delivery time", title="some title")
    ax1.set_title(f"Average days delivery time by month in {year}")
    ax1.legend(["Real time", "Estimated time"])

    plt.show()


def plot_global_amount_order_status(df: DataFrame):
    """Plot global amount of order status

    Args:
        df (DataFrame): Dataframe with global amount of order status query result
    """
    _, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    elements = [x.split()[-1] for x in df["order_status"]]

    wedges, texts, autotexts = ax.pie(df["Ammount"], textprops=dict(color="w"), autopct='%1.1f%%')

    ax.legend(
        wedges,
        elements,
        title="Order Status",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    plt.setp(autotexts, size=8, weight="bold")

    ax.set_title("Order Status Total")

    my_circle = plt.Circle((0, 0), 0.7, color="white")
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    plt.show()


def plot_revenue_per_state(df: DataFrame):
    """Plot revenue per state

    Args:
        df (DataFrame): Dataframe with revenue per state query result
    """
    fig = px.treemap(
        df, path=["customer_state"], values="Revenue", width=800, height=400
    )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show()


def plot_top_10_least_revenue_categories(df: DataFrame):
    """Plot top 10 least revenue categories.

    Args:
        df (DataFrame): Dataframe with top 10 least revenue categories query result.
    """

    # Verificar si el DataFrame tiene las columnas esperadas
    if "Revenue" not in df.columns or "Category" not in df.columns:
        raise ValueError("El DataFrame debe contener las columnas 'Revenue' y 'Category'.")

    # Filtrar las 10 categorías con menor Revenue
    df = df.nsmallest(10, "Revenue")

    # Manejar valores no válidos en 'Category' para evitar errores
    df["Category"] = df["Category"].astype(str).fillna("Unknown")

    # Extraer la última palabra de cada categoría para etiquetas de la leyenda
    elements = [str(x).split()[-1] for x in df["Category"]]

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    # Crear el gráfico de pastel
    wedges, texts, autotexts = ax.pie(
        df["Revenue"], labels=df["Category"], autopct="%1.1f%%", textprops=dict(color="w")
    )

    # Configurar leyenda correctamente
    ax.legend(
        wedges,
        elements,
        title="Top 10 Categories",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    # Ajustar el tamaño de los textos dentro del gráfico
    plt.setp(autotexts, size=8, weight="bold")

    # Agregar un círculo blanco en el centro para hacer un gráfico tipo "donut"
    my_circle = plt.Circle((0, 0), 0.7, color="white")
    plt.gcf().gca().add_artist(my_circle)

    # Título corregido
    ax.set_title("Top 10 Least Revenue Categories Amount")

    # Mostrar el gráfico
    plt.show()

def plot_top_10_revenue_categories_ammount(df: DataFrame):
    """Plot top 10 revenue categories

    Args:
        df (DataFrame): Dataframe with top 10 revenue categories query result
    """
    # Plotting the top 10 revenue categories ammount
    _, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    elements = [x.split()[-1] for x in df["Category"]]

    revenue = df["Revenue"]
    wedges, autotexts = ax.pie(revenue, textprops=dict(color="w"))

    ax.legend(
        wedges,
        elements,
        title="Top 10 Revenue Categories",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
    )

    plt.setp(autotexts, size=8, weight="bold")
    my_circle = plt.Circle((0, 0), 0.7, color="white")
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    ax.set_title("Top 10 Revenue Categories ammount")

    plt.show()


def plot_delivery_date_difference(df: DataFrame):
    """Plot delivery date difference

    Args:
        df (DataFrame): Dataframe with delivery date difference query result
    """
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x="Delivery_Difference", y="State")
    plt.title("Difference Between Delivery Estimate Date and Delivery Date")
    plt.xlabel("Delivery Difference (Days)")
    plt.ylabel("State")
    plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_orders_per_day_and_holidays_2017(df: DataFrame):
    """Plot orders per day and  holidays 2017.

    Args:
        df (DataFrame): Dataframe with orders per day and holidays 2017 query result.
    """
    # Lista de feriados predefinidos para 2017
    holidays = [
        "2017-01-01", "2017-04-14", "2017-05-01", 
        "2017-07-04", "2017-09-16", "2017-11-02", 
        "2017-12-25"
    ]
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x="order_date", y="order_amount", marker="o")

    for holiday in holidays:
        plt.axvline(x=holiday, color="red", linestyle="--", alpha=0.7, label="Holiday")

    plt.xlabel("Order Date")
    plt.ylabel("Order Amount")
    plt.title("Orders per Day and Holidays 2017")
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()



def plot_get_freight_value_weight_relationship(df: DataFrame):
    """Plot the relationship between freight value and product weight."""
    plt.figure(figsize=(8, 5))
    
    sns.scatterplot(
        x=df["product_weight_g"], 
        y=df["freight_value"], 
        alpha=0.5
    )
    
    plt.xlabel("Peso del Producto (g)")
    plt.ylabel("Valor del Flete ($)")
    plt.title("Relación entre Peso del Producto y Valor del Flete")
    plt.grid(True)
    plt.show()


def plot_top_10_revenue_categories(df: DataFrame):
    """Plot top 10 revenue categories

    Args:
        df (DataFrame): Dataframe with top 10 revenue categories query result
    """
    fig = px.treemap(df, path=["Category"], values="Num_order", width=800, height=400)
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    fig.show()
