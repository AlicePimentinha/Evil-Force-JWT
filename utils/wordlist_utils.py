def save_wordlist(wordlist, filepath):
    """Salva uma wordlist fornecida em um arquivo."""
    with open(filepath, 'w') as f:
        for word in wordlist:
            f.write(f"{word}\n")
    return filepath 