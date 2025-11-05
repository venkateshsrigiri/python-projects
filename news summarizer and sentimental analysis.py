from newspaper import Article
from textblob import TextBlob
import nltk
import tkinter as tk
from tkinter import *

# Download punkt (needed by newspaper3k)
nltk.download('punkt')

def summarize():
    try:
        url = utext.get('1.0', 'end').strip()
        if not url:
            summary.delete('1.0', 'end')
            summary.insert('1.0', "⚠️ Please enter a valid news URL!")
            return

        article = Article(url)

        # Download and parse article
        article.download()
        article.parse()

        # Apply NLP processing (title, authors, summary, keywords)
        article.nlp()

        # Enable text boxes for editing
        for box in [title, author, publication, summary, sentiment]:
            box.config(state='normal')
            box.delete('1.0', 'end')

        # Fill details
        title.insert('1.0', article.title if article.title else "N/A")
        author.insert('1.0', ', '.join(article.authors) if article.authors else "Unknown")
        publication.insert('1.0', str(article.publish_date) if article.publish_date else "Unknown")
        summary.insert('1.0', article.summary if article.summary else "Summary not available")

        # Sentiment analysis
        analysis = TextBlob(article.text)
        polarity = round(analysis.polarity, 2)

        if polarity > 0:
            sentiment_text = f"Positive 😊 ({polarity})"
        elif polarity < 0:
            sentiment_text = f"Negative 😞 ({polarity})"
        else:
            sentiment_text = f"Neutral 😐 ({polarity})"

        sentiment.insert('1.0', sentiment_text)

        # Disable editing after update
        for box in [title, author, publication, summary, sentiment]:
            box.config(state='disabled')

    except Exception as e:
        summary.delete('1.0', 'end')
        summary.insert('1.0', f"❌ Error: {str(e)}")


# ---------------- GUI ----------------
root = tk.Tk()
root.title("News Summarizer and Sentiment Analyzer")
root.geometry('900x650')
root.configure(bg='lightyellow')

Label(root, text="Enter News Article URL:", font=('Helvetica', 14, 'bold'), bg='lightyellow').pack()
utext = Text(root, height=2, width=100)
utext.pack()

Button(root, text="Summarize", command=summarize, bg='lightgreen', font=('Helvetica', 12, 'bold')).pack(pady=10)

# Title
Label(root, text="Title:", font=('Helvetica', 12, 'bold'), bg='lightyellow').pack()
title = Text(root, height=2, width=100, state='disabled')
title.pack()

# Author
Label(root, text="Author(s):", font=('Helvetica', 12, 'bold'), bg='lightyellow').pack()
author = Text(root, height=2, width=100, state='disabled')
author.pack()

# Publication Date
Label(root, text="Publication Date:", font=('Helvetica', 12, 'bold'), bg='lightyellow').pack()
publication = Text(root, height=2, width=100, state='disabled')
publication.pack()

# Summary
Label(root, text="Article Summary:", font=('Helvetica', 12, 'bold'), bg='lightyellow').pack()
summary = Text(root, height=12, width=100, wrap=WORD, state='disabled')
summary.pack()

# Sentiment
Label(root, text="Sentiment Analysis:", font=('Helvetica', 12, 'bold'), bg='lightyellow').pack()
sentiment = Text(root, height=2, width=100, state='disabled')
sentiment.pack()

root.mainloop()
