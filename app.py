import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "https://fastapi-project-4-library-management.onrender.com"

st.set_page_config(page_title="Library Dashboard", layout="wide")

st.title("📚 Library Management Dashboard")

def get_books():
    return requests.get(f"{API_URL}/books").json()

def get_users():
    return requests.get(f"{API_URL}/users").json()

def get_stats():
    return requests.get(f"{API_URL}/stats/library").json()

def get_category_stats():
    return requests.get(f"{API_URL}/stats/books_per_category").json()

def add_book(data):
    requests.post(f"{API_URL}/books/add_book", json=data)

def add_user(data):
    requests.post(f"{API_URL}/users/add_user", json=data)

def borrow_book(user_id, book_id):
    requests.post(f"{API_URL}/borrow_book?user_id={user_id}&book_id={book_id}")

def return_book(user_id, book_id):
    requests.post(f"{API_URL}/return_book?user_id={user_id}&book_id={book_id}")

def delete_book(book_id):
    requests.delete(f"{API_URL}/books/delete_book/{book_id}")

def delete_user(user_id):
    requests.delete(f"{API_URL}/users/delete_user/{user_id}")

stats = get_stats()

col1, col2, col3, col4 = st.columns(4)

col1.metric("📚 Total Books", stats["total_books"])
col2.metric("✅ Available Books", stats["available_books"])
col3.metric("📖 Borrowed Books", stats["borrowed_books"])
col4.metric("👥 Total Users", stats["total_users"])

st.divider()

books = get_books()
users = get_users()

df_books = pd.DataFrame(books)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Books by Category")

    category_data = get_category_stats()
    cat_df = pd.DataFrame({
        "category": category_data.keys(),
        "count": category_data.values()
    })

    fig = px.pie(cat_df, names="category", values="count")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Available vs Borrowed")

    status_df = pd.DataFrame({
        "status": ["Available", "Borrowed"],
        "count": [stats["available_books"], stats["borrowed_books"]]
    })

    fig = px.bar(status_df, x="status", y="count")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("➕ Add Book")

with st.form("add_book"):

    col1, col2 = st.columns(2)

    id_book = col1.number_input("Book ID", step=1)
    title = col2.text_input("Title")

    col3, col4 = st.columns(2)

    author = col3.text_input("Author")
    category = col4.text_input("Category")

    submitted = st.form_submit_button("Add Book")

    if submitted:
        data = {
            "id": int(id_book),
            "title": title,
            "author": author,
            "category": category,
            "available": True
        }

        add_book(data)
        st.success("Book Added")
        st.rerun()

st.divider()

st.subheader("➕ Add User")

with st.form("add_user"):

    col1, col2 = st.columns(2)

    user_id = col1.number_input("User ID", step=1)
    name = col2.text_input("User Name")

    submitted = st.form_submit_button("Add User")

    if submitted:
        data = {
            "id": int(user_id),
            "name": name,
            "borrowed_books": []
        }

        add_user(data)
        st.success("User Added")
        st.rerun()

st.divider()

st.subheader("📖 Borrow Book")

col1, col2, col3 = st.columns(3)

borrow_user = col1.number_input("User ID", step=1, key="borrow_user")
borrow_book_id = col2.number_input("Book ID", step=1, key="borrow_book")

if col3.button("Borrow"):
    borrow_book(borrow_user, borrow_book_id)
    st.success("Borrow request sent")
    st.rerun()

st.subheader("🔄 Return Book")

col1, col2, col3 = st.columns(3)

return_user = col1.number_input("User ID", step=1, key="return_user")
return_book_id = col2.number_input("Book ID", step=1, key="return_book")

if col3.button("Return"):
    return_book(return_user, return_book_id)
    st.success("Return request sent")
    st.rerun()

st.divider()

st.subheader("📚 Books List")

if not df_books.empty:

    filter_category = st.selectbox(
        "Filter Category",
        ["All"] + sorted(df_books["category"].unique())
    )

    if filter_category != "All":
        df_books = df_books[df_books["category"] == filter_category]

    for _, row in df_books.iterrows():

        col1, col2, col3, col4, col5 = st.columns([2,2,2,2,1])

        col1.write(row["title"])
        col2.write(row["author"])
        col3.write(row["category"])
        col4.write("Available" if row["available"] else "Borrowed")

        if col5.button("Delete", key=f"book{row['id']}"):
            delete_book(row["id"])
            st.rerun()

st.divider()

st.subheader("👥 Users")

df_users = pd.DataFrame(users)

for _, row in df_users.iterrows():

    col1, col2, col3 = st.columns([3,3,1])

    col1.write(row["name"])
    col2.write(f"Borrowed: {len(row['borrowed_books'])}")

    if col3.button("Delete", key=f"user{row['id']}"):
        delete_user(row["id"])
        st.rerun()
