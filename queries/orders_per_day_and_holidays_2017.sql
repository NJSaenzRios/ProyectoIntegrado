SELECT 
    STRFTIME('%m', order_delivered_customer_date) AS month_no,
    CASE 
        WHEN STRFTIME('%m', order_delivered_customer_date) = '01' THEN 'Ene'
        WHEN STRFTIME('%m', order_delivered_customer_date) = '02' THEN 'Feb'
        WHEN STRFTIME('%m', order_delivered_customer_date) = '03' THEN 'Mar'
        WHEN STRFTIME('%m', order_delivered_customer_date) = '04' THEN 'Abr'
        WHEN STRFTIME('%m', order_delivered_customer_date) = '05' THEN 'May'
        WHEN STRFTIME('%m', order_delivered_customer_date) = '06' THEN 'Jun'
        WHEN STRFTIME('%m', order_delivered_customer_date) = '07' THEN 'Jul'
        WHEN STRFTIME('%m', order_delivered_customer_date) = '08' THEN 'Ago'
        WHEN STRFTIME('%m', order_delivered_customer_date) = '09' THEN 'Sep'
        WHEN STRFTIME('%m', order_delivered_customer_date) = '10' THEN 'Oct'
        WHEN STRFTIME('%m', order_delivered_customer_date) = '11' THEN 'Nov'
        WHEN STRFTIME('%m', order_delivered_customer_date) = '12' THEN 'Dic'
    END AS month,
    COUNT(CASE WHEN DATE(order_delivered_customer_date) IN (
        '2023-01-01', '2023-04-07', '2023-05-01', '2023-07-20', '2023-12-25'
    ) THEN order_id END) AS holiday_orders,
    COUNT(CASE WHEN DATE(order_delivered_customer_date) NOT IN (
        '2023-01-01', '2023-04-07', '2023-05-01', '2023-07-20', '2023-12-25'
    ) THEN order_id END) AS non_holiday_orders
FROM olist_orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
GROUP BY month_no, month
ORDER BY month_no;