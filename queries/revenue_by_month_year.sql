SELECT
    strftime('%m', o.order_purchase_timestamp) AS month_no,
    CASE
        WHEN strftime('%m', o.order_purchase_timestamp) = '01' THEN 'Ene'
        WHEN strftime('%m', o.order_purchase_timestamp) = '02' THEN 'Feb'
        WHEN strftime('%m', o.order_purchase_timestamp) = '03' THEN 'Mar'
        WHEN strftime('%m', o.order_purchase_timestamp) = '04' THEN 'Abr'
        WHEN strftime('%m', o.order_purchase_timestamp) = '05' THEN 'May'
        WHEN strftime('%m', o.order_purchase_timestamp) = '06' THEN 'Jun'
        WHEN strftime('%m', o.order_purchase_timestamp) = '07' THEN 'Jul'
        WHEN strftime('%m', o.order_purchase_timestamp) = '08' THEN 'Ago'
        WHEN strftime('%m', o.order_purchase_timestamp) = '09' THEN 'Sep'
        WHEN strftime('%m', o.order_purchase_timestamp) = '10' THEN 'Oct'
        WHEN strftime('%m', o.order_purchase_timestamp) = '11' THEN 'Nov'
        WHEN strftime('%m', o.order_purchase_timestamp) = '12' THEN 'Dic'
    END AS month,
    SUM(CASE WHEN strftime('%Y', o.order_purchase_timestamp) = '2016' THEN op.payment_value ELSE 0 END) AS Year2016,
    SUM(CASE WHEN strftime('%Y', o.order_purchase_timestamp) = '2017' THEN op.payment_value ELSE 0 END) AS Year2017,
    SUM(CASE WHEN strftime('%Y', o.order_purchase_timestamp) = '2018' THEN op.payment_value ELSE 0 END) AS Year2018
FROM olist_orders o
JOIN olist_order_payments op ON o.order_id = op.order_id
WHERE strftime('%Y', o.order_purchase_timestamp) IN ('2016', '2017', '2018')
GROUP BY strftime('%m', o.order_purchase_timestamp)
ORDER BY month_no;