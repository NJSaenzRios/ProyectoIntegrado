SELECT 
    p.product_category_name AS Category, 
    COUNT(DISTINCT o.order_id) AS Num_order, 
    SUM(oi.price + oi.freight_value) AS Revenue
FROM olist_orders o
JOIN olist_order_items oi ON o.order_id = oi.order_id
JOIN olist_products p ON oi.product_id = p.product_id
WHERE o.order_status = 'delivered' 
    AND o.order_delivered_customer_date IS NOT NULL
    AND p.product_category_name IS NOT NULL
GROUP BY p.product_category_name
ORDER BY Revenue ASC
LIMIT 10;

