import os
import csv
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def load_expenses():
    with open("data/categorized_expenses.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def get_total_by_category(expenses, category):
    total = 0.0
    count = 0
    for row in expenses:
        if row["category"].lower() == category.lower():
            try:
                total += float(row["total"])
                count += 1
            except (ValueError, TypeError):
                pass
    return total, count

def get_all_categories(expenses):
    return sorted(set(row["category"] for row in expenses if row["category"]))

# Fix 1: synonym mapping - maps common words to real category names
CATEGORY_SYNONYMS = {
    "food": ["Dining", "Groceries"],
    "eating out": ["Dining"],
    "restaurants": ["Dining"],
    "meals": ["Dining"],
    "medicine": ["Pharmacy"],
    "health": ["Pharmacy"],
    "tools": ["Hardware"],
    "books": ["Stationery"],
    "shopping": ["Retail"],
}

def find_matched_categories(question, categories):
    """Returns a list of matched categories - handles exact names, synonyms, and multiple mentions."""
    question_lower = question.lower()
    matched = []

    # Check exact category names first
    # Check exact category names first (handles singular/plural variations)
    # Check exact category names first (handles singular/plural variations)
    for cat in categories:
        cat_lower = cat.lower()
        # Check both directions: category name in question, or question words matching category root
        if cat_lower in question_lower and cat not in matched:
            matched.append(cat)
        elif cat_lower.rstrip('ies') + 'y' in question_lower and cat not in matched:  # Groceries -> Grocery
            matched.append(cat)
        elif cat_lower.rstrip('s') in question_lower and cat not in matched:  # Snacks -> Snack
            matched.append(cat)

    # Check synonyms (only if not already matched via exact name)
    for synonym, mapped_categories in CATEGORY_SYNONYMS.items():
        if synonym in question_lower:
            for cat in mapped_categories:
                if cat in categories and cat not in matched:
                    matched.append(cat)

    return matched

def build_context(question, expenses, categories):
    matched_categories = find_matched_categories(question, categories)

    if not matched_categories:
        # No category matched - overall summary
        total = 0.0
        count = 0
        for row in expenses:
            try:
                total += float(row["total"])
                count += 1
            except (ValueError, TypeError):
                pass
        return (f"Total spending across all categories: RM{total:.2f} across {count} receipts.\n"
                f"Available categories: {', '.join(categories)}")

    # Build data for each matched category (handles single OR multiple)
    lines = []
    for cat in matched_categories:
        total, count = get_total_by_category(expenses, cat)
        avg = total / count if count > 0 else 0
        lines.append(f"{cat}: total RM{total:.2f} across {count} receipts, average RM{avg:.2f} per receipt")

    return "\n".join(lines)

def ask_ai(question, context):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful expense tracking assistant. "
                    "Answer only based on the data provided. "
                    "If the data doesn't fully answer the question, say so honestly. "
                    "Be concise and friendly."
                ),
            },
            {"role": "user", "content": f"Data:\n{context}\n\nQuestion: {question}"},
        ],
    )
    return response.choices[0].message.content

def answer_question(question, expenses, categories):
    context = build_context(question, expenses, categories)
    answer = ask_ai(question, context)
    return answer, context

# ---- Run tests ----
expenses = load_expenses()
categories = get_all_categories(expenses)

test_questions = [
    "How much did I spend on food?",
    "how much on GROCERIES",
    "What did I spend on Entertainment?",
    "Compare my Dining and Hardware spending",
    "What's my average spend per Grocery receipt?",
]

for q in test_questions:
    answer, context = answer_question(q, expenses, categories)
    print("\n" + "=" * 60)
    print(f"Question : {q}")
    print(f"Context  : {context}")
    print(f"Answer   : {answer}")
    