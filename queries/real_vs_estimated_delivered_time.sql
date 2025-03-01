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
    AVG(CASE WHEN STRFTIME('%Y', order_delivered_customer_date) = '2016'
             THEN julianday(order_delivered_customer_date) - julianday(order_purchase_timestamp)
        	 END) AS Year2016_real_time,
     AVG(CASE WHEN STRFTIME('%Y', order_delivered_customer_date) = '2017'
             THEN julianday(order_delivered_customer_date) - julianday(order_purchase_timestamp)
             END) AS Year2017_real_time,   
     AVG(CASE WHEN STRFTIME('%Y', order_delivered_customer_date) = '2018'
             THEN julianday(order_delivered_customer_date) - julianday(order_purchase_timestamp)
             END) AS Year2018_real_time,
    -- Tiempos estimados de entrega por año
     AVG(CASE WHEN STRFTIME('%Y', order_estimated_delivery_date) = '2016'
             THEN julianday(order_estimated_delivery_date) - julianday(order_purchase_timestamp)
             END) AS Year2016_estimated_time,   
     AVG(CASE WHEN STRFTIME('%Y', order_estimated_delivery_date) = '2017'
             THEN julianday(order_estimated_delivery_date) - julianday(order_purchase_timestamp)
             END) AS Year2017_estimated_time,   
     AVG(CASE WHEN STRFTIME('%Y', order_estimated_delivery_date) = '2018'
             THEN julianday(order_estimated_delivery_date) - julianday(order_purchase_timestamp)
             END) AS Year2018_estimated_time
FROM olist_orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
GROUP BY month_no, month
ORDER BY month_no;
