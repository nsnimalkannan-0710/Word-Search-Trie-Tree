import ctypes
import tkinter as tk
from tkinter import filedialog, Text
from tkinter import font as tkFont
import os
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
trie = ctypes.CDLL(os.path.join(current_dir, './trie.so'))

trie.create.restype = ctypes.c_void_p
trie.insert.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int]
trie.search.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
trie.search.restype = ctypes.POINTER(ctypes.c_int)

class TextHighlighterApp:
    def __init__(self, window):
        self.window = window
        window.title("Text Highlighter with Trie")

        self.trie_root = trie.create()
        self.font = tkFont.Font(family="Helvetica", size=14)
        self.text_area = Text(window, wrap='word', font=self.font)
        self.text_area.pack(expand=True, fill='both')

        self.search_entry = tk.Entry(window)
        self.search_entry.pack()
        self.search_entry.bind("<KeyRelease>", self.auto_highlight)

        self.occurrence_label = tk.Label(window, text="")
        self.occurrence_label.pack()

        self.open_button = tk.Button(window, text="Open File", command=self.open_file)
        self.open_button.pack()

        self.search_entry.focus_set()

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)

                for match in re.finditer(r'\b[a-zA-Z]+\b', content):
                    word = match.group().lower()
                    start_pos = match.start()
                   # print(match,word,start_pos)
                    trie.insert(self.trie_root, word.encode('utf-8'), start_pos)

    def auto_highlight(self, event=None):
        self.text_area.tag_remove('highlight', '1.0', tk.END)

        search_term = self.search_entry.get().strip().lower()
        count = 0

        if search_term:
            search_term_filtered = ''.join([ch for ch in search_term if ch.isalpha()])
            positions = trie.search(self.trie_root, search_term_filtered.encode('utf-8'))

            if positions:
                index = 0
                while positions[index] != -1:
                    raw_pos = positions[index]
                    index += 1
                    start_index = self.text_area.index("1.0 + " + str(raw_pos) + " chars")
                    end_index = self.text_area.index(start_index + " + " + str(len(search_term_filtered)) + " chars")
                    self.text_area.tag_add('highlight', start_index, end_index)
                    count += 1

                self.text_area.tag_config('highlight', background='yellow')

        self.occurrence_label.config(text=f"Occurrences: {count}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextHighlighterApp(root)
    root.mainloop()