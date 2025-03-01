SELECT
    oi.freight_value,
    product_weight_g,
    ROUND(oi.freight_value / NULLIF(product_weight_g, 0), 2) AS costo_envio_por_gramo
FROM olist_order_items oi
JOIN olist_products p
    ON oi.product_id = p.product_id
WHERE product_weight_g IS NOT NULL;