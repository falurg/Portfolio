# WORK IN PROGRESS

import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import csv


def scrape_web():
    # Get the url
    url = url_entry.get()
    search_terms = search_entry.get().split(',')

    # Make a request to the site
    response = requests.get(url)

    # Check if request was successful
    if response.status_code == 200:
        # Parse html content with soup
        soup = BeautifulSoup(response.content, 'html.parser')

        results = []

        for term in search_terms:
            term = term.strip()
            elements = []

            if term.startswith('id'):
                element = soup.find(id=term[3:])
                if element:
                    elements.append(element)

            elif term.startswith('class'):
                elements.extend(soup.find_all(class_=term[6:]))

            else:
                elements.extend(soup.find_all(term))

            results.extend([element.text for element in elements])

        result_text.delete(1.0, tk.END)

        for result in results:
            result_text.insert(tk.END, f'{result}\n')
            messagebox.showinfo("Success", "Web scraping completed!")
    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f'Error: {response.status_code}')


# def export_data():
#     data = result_text.get(1.0, tk.END)
#
#     file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV Files', '*.csv')])
#
#     if file_path:
#         with open(file_path, 'w', encoding='utf-8', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow([data])
#
#         result_text.insert(tk.END, f'\nData exported to: {file_path}')

def export_data():
    data = result_text.get(1.0, tk.END)

    file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV Files', '*.csv')])

    if file_path:
        try:
            export_to_csv(file_path, data)
            messagebox.showinfo("Success", f"Data exported to: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def export_to_csv(file_path, data):
    lines = data.strip().split('\n')
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(lines)


window = tk.Tk()
window.title('Scrape Bot')
window.geometry('400x400')

url_label = tk.Label(window, text='URL:')
url_label.pack()
url_entry = tk.Entry(window, width=50)
url_entry.pack()

search_label = tk.Label(window, text='Enter HTML tag or class/id')
search_label.pack()
search_entry = tk.Entry(window, width=50)
search_entry.pack()

scrape_button = tk.Button(window, text='Scrape', command=scrape_web)
scrape_button.pack()

result_text = tk.Text(window, height=10, width=50)
result_text.pack()

export_button = tk.Button(window, text='Export', command=export_data)
export_button.pack()

window.mainloop()
