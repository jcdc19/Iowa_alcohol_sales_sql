CREATE OR REPLACE VIEW v_drivers_detractors AS
WITH last_month AS (
  SELECT MAX(sale_month) AS sale_month
  FROM v_sales_clean
),
cur_prev AS (
  SELECT
    l.sale_month AS cur_month,
    l.sale_month - INTERVAL '1 month' AS prev_month
  FROM last_month l
),
cat_month AS (
  SELECT
    county AS account,
    sale_month,
    category_name AS driver_key,
    SUM(volume_liters) AS vol
  FROM v_sales_clean
  GROUP BY 1,2,3
),
cat_delta AS (
  SELECT
    account,
    sale_month,
    'category' AS driver_type,
    driver_key,
    vol - LAG(vol) OVER (PARTITION BY account, driver_key ORDER BY sale_month) AS delta_volume
  FROM cat_month
),
item_month AS (
  SELECT
    county AS account,
    sale_month,
    item_description AS driver_key,
    SUM(volume_liters) AS vol
  FROM v_sales_clean
  GROUP BY 1,2,3
),
item_delta AS (
  SELECT
    account,
    sale_month,
    'item' AS driver_type,
    driver_key,
    vol - LAG(vol) OVER (PARTITION BY account, driver_key ORDER BY sale_month) AS delta_volume
  FROM item_month
),
store_month AS (
  SELECT
    county AS account,
    sale_month,
    store_name AS driver_key,
    SUM(volume_liters) AS vol
  FROM v_sales_clean
  GROUP BY 1,2,3
),
store_delta AS (
  SELECT
    account,
    sale_month,
    'store' AS driver_type,
    driver_key,
    vol - LAG(vol) OVER (PARTITION BY account, driver_key ORDER BY sale_month) AS delta_volume
  FROM store_month
),
all_delta AS (
  SELECT * FROM cat_delta
  UNION ALL
  SELECT * FROM item_delta
  UNION ALL
  SELECT * FROM store_delta
),
filtered AS (
  SELECT d.*
  FROM all_delta d
  JOIN cur_prev cp
    ON d.sale_month = cp.cur_month
  WHERE d.delta_volume IS NOT NULL
),
ranked AS (
  SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY account, driver_type ORDER BY delta_volume DESC) AS rank_pos,
    ROW_NUMBER() OVER (PARTITION BY account, driver_type ORDER BY delta_volume ASC)  AS rank_neg
  FROM filtered
)
SELECT
  account,
  sale_month,
  driver_type,
  driver_key,
  delta_volume,
  CASE
    WHEN rank_pos <= 10 THEN 'top_driver'
    WHEN rank_neg <= 10 THEN 'top_detractor'
    ELSE NULL
  END AS driver_bucket
FROM ranked
WHERE rank_pos <= 10 OR rank_neg <= 10;
