SELECT 
    o.order_id,
    SUM(oi.freight_value) AS freight_value,
    SUM(p.product_weight_g) AS product_weight_g
FROM olist_orders o
JOIN olist_order_items oi ON o.order_id = oi.order_id
JOIN olist_products p ON oi.product_id = p.product_id
WHERE o.order_status = 'delivered'
GROUP BY o.order_id;
