import tkinter as tk
from tkinter import messagebox
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pandas as pd

# ------------------- Training the Model -------------------
# Sample dataset for demonstration purposes (replace with actual dataset)
data = pd.DataFrame({
    'text': [
        "Your account has been compromised. Click here to reset your password.",
        "Win a million dollars now! Claim your prize.",
        "Meeting at 3 PM in conference room A.",
        "Urgent: Update your banking information immediately.",
        "Happy birthday! Hope you have a great day."
    ],
    'label': [1, 1, 0, 1, 0]  # 1 = phishing, 0 = not phishing
})

# Preprocessing and feature extraction
vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
X = vectorizer.fit_transform(data['text'])
y = data['label']

# Train the model
model = LogisticRegression()
model.fit(X, y)

# ------------------- Phishing Detection Function -------------------
def detect_phishing(email_text):
    # Preprocess email content
    email_vector = vectorizer.transform([email_text])
    prediction = model.predict(email_vector)
    confidence = model.predict_proba(email_vector)[0][1]
    if prediction == 1:
        return f"Phishing detected! Confidence: {confidence * 100:.2f}%"
    else:
        return f"Email is safe. Confidence: {(1 - confidence) * 100:.2f}%"

# ------------------- Tkinter UI -------------------
def check_email():
    email_text = email_entry.get("1.0", tk.END).strip()
    if not email_text:
        messagebox.showwarning("Input Error", "Please enter the email content.")
        return

    result = detect_phishing(email_text)
    result_label.config(text=result, fg="red" if "Phishing" in result else "green")

# Initialize Tkinter window
root = tk.Tk()
root.title("Phishing Email Detector")
root.geometry("500x400")
root.resizable(False, False)

# Title label
title_label = tk.Label(root, text="Phishing Email Detector", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Email input label and text box
email_label = tk.Label(root, text="Enter Email Content:", font=("Helvetica", 12))
email_label.pack(anchor="w", padx=20)

email_entry = tk.Text(root, height=10, width=60, wrap=tk.WORD, font=("Helvetica", 10))
email_entry.pack(pady=10)

# Check button
check_button = tk.Button(root, text="Check Email", command=check_email, font=("Helvetica", 12), bg="blue", fg="white")
check_button.pack(pady=10)

# Result label
result_label = tk.Label(root, text="", font=("Helvetica", 12))
result_label.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
