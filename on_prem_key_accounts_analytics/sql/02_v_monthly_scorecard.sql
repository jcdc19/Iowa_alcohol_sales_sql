CREATE OR REPLACE VIEW v_monthly_scorecard AS
SELECT
  county AS account,
  sale_month,
  SUM(volume_liters) AS total_volume_liters,
  SUM(sale_dollars) AS total_sales_dollars,
  SUM(bottles_sold) AS total_bottles,
  COUNT(DISTINCT store_id) AS active_locations,
  COUNT(DISTINCT item_id) AS active_items
FROM v_sales_clean
GROUP BY 1,2;