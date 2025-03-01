import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from collections import namedtuple
from enum import Enum
from typing import Callable, Dict, List

import pandas as pd
from pandas import DataFrame, read_sql
from sqlalchemy import text
from sqlalchemy.engine.base import Engine

from src.config import QUERIES_ROOT_PATH

# Definición de estructura para los resultados de las consultas
QueryResult = namedtuple("QueryResult", ["query", "result"])

# Enumeración de las consultas disponibles
class QueryEnum(Enum):
    """This class enumerates all the queries that are available"""
    DELIVERY_DATE_DIFFERENCE = "delivery_date_difference"
    GLOBAL_AMMOUNT_ORDER_STATUS = "global_ammount_order_status"
    REVENUE_BY_MONTH_YEAR = "revenue_by_month_year"
    REVENUE_PER_STATE = "revenue_per_state"
    TOP_10_LEAST_REVENUE_CATEGORIES = "top_10_least_revenue_categories"
    TOP_10_REVENUE_CATEGORIES = "top_10_revenue_categories"
    REAL_VS_ESTIMATED_DELIVERED_TIME = "real_vs_estimated_delivered_time"
    ORDERS_PER_DAY_AND_HOLIDAYS_2017 = "orders_per_day_and_holidays_2017"
    GET_FREIGHT_VALUE_WEIGHT_RELATIONSHIP = "get_freight_value_weight_relationship"

# Función para leer consultas SQL desde archivos

def read_query(query_name: str) -> str:
    """Read the query from the file."""
    with open(f"{QUERIES_ROOT_PATH}/{query_name}.sql", "r") as f:
        sql_file = f.read()
        return text(sql_file)

# Definición de funciones de consulta

def query_delivery_date_difference(database: Engine) -> QueryResult:
    query_name = QueryEnum.DELIVERY_DATE_DIFFERENCE.value
    query = read_query(query_name)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_global_ammount_order_status(database: Engine) -> QueryResult:
    query_name = QueryEnum.GLOBAL_AMMOUNT_ORDER_STATUS.value
    query = read_query(query_name)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_revenue_by_month_year(database: Engine) -> QueryResult:
    query_name = QueryEnum.REVENUE_BY_MONTH_YEAR.value
    query = read_query(query_name)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_revenue_per_state(database: Engine) -> QueryResult:
    query_name = QueryEnum.REVENUE_PER_STATE.value
    query = read_query(query_name)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_top_10_least_revenue_categories(database: Engine) -> QueryResult:
    query_name = QueryEnum.TOP_10_LEAST_REVENUE_CATEGORIES.value
    query = read_query(query_name)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_top_10_revenue_categories(database: Engine) -> QueryResult:
    query_name = QueryEnum.TOP_10_REVENUE_CATEGORIES.value
    query = read_query(query_name)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_real_vs_estimated_delivered_time(database: Engine) -> QueryResult:
    query_name = QueryEnum.REAL_VS_ESTIMATED_DELIVERED_TIME.value
    query = read_query(query_name)
    return QueryResult(query=query_name, result=read_sql(query, database))


def query_orders_per_day_and_holidays_2017(database: Engine) -> QueryResult:
    query_name = QueryEnum.ORDERS_PER_DAY_AND_HOLIDAYS_2017.value
    holidays = read_sql("SELECT * FROM public_holidays", database)
    orders = read_sql("SELECT * FROM olist_orders", database)
   
    orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
    filtered_dates = orders[orders["order_purchase_timestamp"].dt.year == 2017]
    order_purchase_ammount_per_date = filtered_dates.groupby(filtered_dates["order_purchase_timestamp"].dt.date).size()
   
    result_df = pd.DataFrame({
        "date": order_purchase_ammount_per_date.index,
        "order_count": order_purchase_ammount_per_date.values,
    })
    result_df["holiday"] = result_df["date"].isin(holidays["date"])
   
    return QueryResult(query=query_name, result=result_df)


def query_freight_value_weight_relationship(database: Engine) -> QueryResult:
    query_name = QueryEnum.GET_FREIGHT_VALUE_WEIGHT_RELATIONSHIP.value
   
    orders = read_sql("SELECT * FROM olist_orders", database)
    items = read_sql("SELECT * FROM olist_order_items", database)
    products = read_sql("SELECT * FROM olist_products", database)
   
    data = items.merge(orders, on="order_id").merge(products, on="product_id")
    delivered = data[data["order_status"] == "delivered"]
   
    aggregations = delivered.groupby("order_id").agg({
        "freight_value": "sum",
        "product_weight_g": "sum"
    }).reset_index()
   
    return QueryResult(query=query_name, result=aggregations)

# Funciones para obtener y ejecutar todas las consultas
def get_all_queries() -> List[Callable[[Engine], QueryResult]]:
    """Return a list of all query functions."""
    return [
        query_delivery_date_difference,
        query_global_ammount_order_status,
        query_revenue_by_month_year,
        query_revenue_per_state,
        query_top_10_least_revenue_categories,
        query_top_10_revenue_categories,
        query_real_vs_estimated_delivered_time,
        query_orders_per_day_and_holidays_2017,
        query_freight_value_weight_relationship,
    ]


def run_queries(database: Engine) -> Dict[str, DataFrame]:
    """Execute all queries and return results as a dictionary."""
    query_results = {}
    for query in get_all_queries():
        query_result = query(database)
        query_results[query_result.query] = query_result.result
    return query_results