import pandas as pd
import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt
import os

# Function to compute total sales
def compute_total_sales(chunk):
    chunk['TotalSales'] = chunk['Quantity'] * chunk['UnitPrice']
    chunk['MonthYear'] = chunk['InvoiceDate'].dt.to_period('M')
    return chunk

if __name__ == '__main__':
    # Loading the dataset
    file_path = 'Online Retail.xlsx'
    data = pd.read_excel(file_path, sheet_name='Online Retail')

    # Data cleaning
    data.dropna(subset=['CustomerID'], inplace=True)
    data = data[data['Quantity'] > 0]
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])

    # Splitting data into chunks
    num_chunks = mp.cpu_count()
    data_chunks = np.array_split(data, num_chunks)

    # Creating a pool of workers
    pool = mp.Pool(num_chunks)

    # Parallel processing to compute total sales and extracting month-year
    results = pool.map(compute_total_sales, data_chunks)

    # Combining the results
    processed_data = pd.concat(results)

    # Closing the pool
    pool.close()
    pool.join()

    # sales by month-year
    monthly_sales = processed_data.groupby('MonthYear')['TotalSales'].sum().reset_index()

    # Plotting the sales trends over time
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_sales['MonthYear'].astype(str), monthly_sales['TotalSales'], marker='o')
    plt.xticks(rotation=45)
    plt.xlabel('Month-Year')
    plt.ylabel('Total Sales')
    plt.title('Sales Trends Over Time')
    plt.grid(True)
    plt.tight_layout()

    # Ensuring the output directory exists
    if not os.path.exists('output'):
        os.makedirs('output')

    # Saving the plot to the output directory
    plot_path = 'output/sales_trends_over_time.png'
    plt.savefig(plot_path)
    print(f"Plot saved to {plot_path}")

    # Saving the processed data and monthly sales to a new file
    processed_data.to_excel('output/Processed_Online_Retail.xlsx', index=False)
    monthly_sales.to_excel('output/Monthly_Sales_Online_Retail.xlsx', index=False)

    print("Total sales and plot computed and data saved to 'output/Processed_Online_Retail.xlsx', 'output/Monthly_Sales_Online_Retail.xlsx', and 'output/sales_trends_over_time.png'")
