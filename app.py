import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "https://fastapi-project-4-library-management.onrender.com"

st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)

st.sidebar.title("📚 Library System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Books",
        "Users",
        "Borrow / Return",
        "Add Data"
    ]
)

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

books = get_books()
users = get_users()

df_books = pd.DataFrame(books)
df_users = pd.DataFrame(users)

if page == "Dashboard":

    st.title("📊 Library Dashboard")

    stats = get_stats()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📚 Total Books", stats["total_books"])
    col2.metric("✅ Available", stats["available_books"])
    col3.metric("📖 Borrowed", stats["borrowed_books"])
    col4.metric("👥 Users", stats["total_users"])

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Books by Category")

        category_data = get_category_stats()

        df = pd.DataFrame({
            "category": category_data.keys(),
            "count": category_data.values()
        })

        fig = px.pie(df, names="category", values="count")
        st.plotly_chart(fig, use_container_width=True)

    with col2:

        st.subheader("Availability")

        df = pd.DataFrame({
            "status": ["Available", "Borrowed"],
            "count": [
                stats["available_books"],
                stats["borrowed_books"]
            ]
        })

        fig = px.bar(df, x="status", y="count")
        st.plotly_chart(fig, use_container_width=True)

if page == "Books":

    st.title("📚 Books")

    search = st.text_input("Search Book")

    if search:
        df_books = df_books[
            df_books["title"].str.contains(search, case=False)
        ]

    st.dataframe(df_books, use_container_width=True)

    st.subheader("Delete Book")

    book_id = st.number_input("Book ID", step=1)

    if st.button("Delete Book"):
        delete_book(book_id)
        st.success("Book Deleted")
        st.rerun()

if page == "Users":

    st.title("👥 Users")

    search = st.text_input("Search User")

    if search:
        df_users = df_users[
            df_users["name"].str.contains(search, case=False)
        ]

    st.dataframe(df_users, use_container_width=True)

    st.subheader("Delete User")

    user_id = st.number_input("User ID", step=1)

    if st.button("Delete User"):
        delete_user(user_id)
        st.success("User Deleted")
        st.rerun()

if page == "Borrow / Return":

    st.title("📖 Borrow / Return Books")

    st.subheader("Borrow Book")

    col1, col2 = st.columns(2)

    user_id = col1.number_input("User ID", step=1, key="borrow_user")
    book_id = col2.number_input("Book ID", step=1, key="borrow_book")

    if st.button("Borrow Book"):
        borrow_book(user_id, book_id)
        st.success("Borrow request sent")
        st.rerun()

    st.divider()

    st.subheader("Return Book")

    col1, col2 = st.columns(2)

    user_id = col1.number_input("User ID", step=1, key="return_user")
    book_id = col2.number_input("Book ID", step=1, key="return_book")

    if st.button("Return Book"):
        return_book(user_id, book_id)
        st.success("Return request sent")
        st.rerun()

if page == "Add Data":

    st.title("➕ Add Data")

    st.subheader("Add Book")

    col1, col2 = st.columns(2)

    id_book = col1.number_input("Book ID", step=1)
    title = col2.text_input("Title")

    col3, col4 = st.columns(2)

    author = col3.text_input("Author")
    category = col4.text_input("Category")

    if st.button("Add Book"):

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

    st.subheader("Add User")

    col1, col2 = st.columns(2)

    user_id = col1.number_input("User ID", step=1)
    name = col2.text_input("Name")

    if st.button("Add User"):

        data = {
            "id": int(user_id),
            "name": name,
            "borrowed_books": []
        }

        add_user(data)
        st.success("User Added")
        st.rerun()
