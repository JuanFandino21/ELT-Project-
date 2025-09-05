-- TODO: This query will return a table with two columns; customer_state, and 
-- Revenue. The first one will have the letters that identify the top 10 states 
-- with most revenue and the second one the total revenue of each.
-- HINT: All orders should have a delivered status and the actual delivery date 
-- should be not null. 
-- Top 10 estados por revenue (SUM(order_items.price)), solo delivered
-- Top 10 estados por revenue = SUM(price + freight_value). Solo delivered
-- Top 10 estados por revenue total
-- Revenue = SUM(price + freight_value)
-- Solo órdenes entregadas y con fecha de entrega real no nula.
-- Top 10 estados por revenue = SUM(olist_order_items.price), SOLO entregadas.
SELECT
  c.customer_state,
  ROUND(SUM(p.payment_value), 3) AS Revenue
FROM olist_orders          AS o
JOIN olist_order_payments  AS p ON p.order_id = o.order_id
JOIN olist_customers       AS c ON c.customer_id = o.customer_id
WHERE
  o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY c.customer_state
ORDER BY Revenue DESC
LIMIT 10;





