import pandas as pd

orders_filepath = r"C:\\Users\\osasy\\Downloads\\pandas_first_project\\orders.csv"
products_filepath = r"C:\\Users\\osasy\\Downloads\\pandas_first_project\\products.csv"
customers_filepath = r"C:\\Users\\osasy\\Downloads\\pandas_first_project\\customers.csv"

orders_data = pd.read_csv(orders_filepath)
products_data = pd.read_csv(products_filepath)
customers_data = pd.read_csv(customers_filepath)

print("Orders:")
print(orders_data)
print("\n")



print("Products:")
print(products_data)
print("\n")



print("Customers:")
print(customers_data)




print("\n")
print("Master Dataset: ")
master_dataset = orders_data.set_index(["product_id", "customer_id"]).join(
    products_data.set_index("product_id")).join(
        customers_data.set_index("customer_id"))

master_dataset = master_dataset.reset_index()
master_dataset = master_dataset.set_index("order_id")


print(master_dataset)
print(master_dataset.columns.to_list())


for col in master_dataset.columns:
    if master_dataset[col].dtype == "int64" or master_dataset[col].dtype == "float64":
        master_dataset[col] = master_dataset[col].fillna(0.0)
    else:
        master_dataset[col]  = master_dataset[col].fillna("Unknown")



master_dataset["order_date"] = master_dataset["order_date"].astype("datetime64[us]")
master_dataset["signup_date"] = master_dataset["signup_date"].astype("datetime64[us]")


print(master_dataset)
print("\n")
print(master_dataset.dtypes)

# Phase 4: Feature Engineering and Aggregation

master_dataset["total_sales_revenue"] = master_dataset["quantity"] * master_dataset["unit_price"]
print(master_dataset)
print(master_dataset.columns.to_list())
print("\n")


master_dataset = master_dataset.groupby(["category", "region"]).agg({"total_sales_revenue": ["sum", "mean"], "quantity": "sum"})
print(master_dataset)
print("\n")


# Phase 5: Ranking and Exporting the Data
master_dataset.sort_values(by=[("total_sales_revenue", "sum")], ascending=False, inplace=True)
print(master_dataset)
print("\n")
master_dataset.reset_index(inplace=True)
print(master_dataset)
master_dataset.to_csv("summary_report.csv", index=False)