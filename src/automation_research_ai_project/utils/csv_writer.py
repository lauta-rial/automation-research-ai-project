import csv

def write_csv(file_path, data):
    """
    Writes data to a CSV file.

    Args:
        file_path (str): The path to the CSV file.
        data (list of dict): The data to write.
    """
    if not data:
        print("\n⚠️ No expenses to export to CSV.")
        return

    with open(file_path, mode="w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(f"\n✅ CSV exported to: {file_path}")

if __name__ == '__main__':
    # Example Usage
    file_path = 'example.csv'
    data = [
        {'name': 'Alice', 'age': 30, 'city': 'New York'},
        {'name': 'Bob', 'age': 25, 'city': 'Los Angeles'},
        {'name': 'Charlie', 'age': 35, 'city': 'Chicago'}
    ]
    write_csv(file_path, data)
    print(f"CSV file '{file_path}' created successfully.")
