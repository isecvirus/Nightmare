def Table(headers:list or str, data:list or dict) -> str:
    return tabulate(tabular_data=data, tablefmt='plaintext', numalign='center', stralign='center', headers=headers)
