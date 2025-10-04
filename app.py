import streamlit as st
import requests

def query_book(name):
    url = f"https://openlibrary.org/search.json?q={name}"
    req = requests.get(url,verify=False)
    res = req.json()
    
    st.session_state['book_data'] = res['docs']

def AddToSupabase():
    key = "sb_publishable_pmWX5FiLCQjop9LrBk5hhw_CZCKbsah"
    headers = {
    'apikey': key,
    'Authorization': f'Bearer {key}',
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal',
}

    json_data = {
        'name': st.session_state.selectedbook[0],
        'img': st.session_state.selectedbook[2],
        'status': 'Reading',
        'author': st.session_state.selectedbook[1],
        
    }

    response = requests.post('https://qtydevnghftbunqvpyyo.supabase.co/rest/v1/books_read', headers=headers, json=json_data,verify=False)
    if response.status_code == 201:
        st.success('Book Added',icon='🎈')
    
def GetLatestReading():
    key = "sb_publishable_pmWX5FiLCQjop9LrBk5hhw_CZCKbsah"
    headers = {
    'apikey': key,
    'Authorization': f'Bearer {key}',
    'Range': '0-9'}

    response = requests.get('https://qtydevnghftbunqvpyyo.supabase.co/rest/v1/books_read?status=eq.Reading&select=*', headers=headers,verify=False)
    

    return (response.json())


def MarkRead():
    key = "sb_publishable_pmWX5FiLCQjop9LrBk5hhw_CZCKbsah"
    headers = {
    'apikey': key,
    'Authorization': f'Bearer {key}',
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal'}

    params = {
    'status': 'eq.Reading'}

    json_data = {
        'status': 'Read',
    }

    

    response = requests.patch('https://qtydevnghftbunqvpyyo.supabase.co/rest/v1/books_read', params=params, headers=headers, json=json_data,verify=False)
 
    if response.status_code == 204:
        st.success('Marked as Read!',icon="🎈")

st.set_page_config(page_title="Bookshelf",page_icon="📔")

if 'querybooks' in st.session_state:
    
    img_id = st.session_state.querybooks.split(',')[1].strip().split('-')[0].strip()
    title = st.session_state.querybooks.split('by')[0].strip()
    author = st.session_state.querybooks.split('by')[1].split(',')[0].strip()
    st.session_state.selectedbook = [title,author,img_id]
    
    st.button(label="Add " + st.session_state.querybooks,type="primary",on_click=AddToSupabase)


tab1, tab2 = st.tabs(["Add a new book", "Update current reading"])

with tab1:
    with st.form("my_form"):
        
        query = st.text_input("What's the name of the book")

        submitted = st.form_submit_button("Submit")
        
        if submitted:
            with st.spinner("Downloading data..."):

                st.write(query_book(query))
        
    if 'book_data' in st.session_state:
            
            books = []
            for book in st.session_state['book_data']:
       
                try:
                    books.append(f"{book['title']} by {book['author_name'][0]} , {book['cover_edition_key']}")
                except:
                    pass
            query_books = st.radio('Select a book to add',
                                   books,index=None,
                                   key="querybooks")

        
with tab2:

    try:
        
        data = GetLatestReading()[0]

        with st.form("search_form"):
        
            st.markdown(f"### You are currently reading ***{data['name']}*** by ***{data['author']}***")
            st.text_input('Name of the book',value = data['name'],key="bookname")
            st.text_input('Author',value = data['author'],key="author")
            read = st.form_submit_button('Mark as Read',on_click=MarkRead)
                
    except:
        st.write("There is no book that you are currently reading.")
        pass
        
    



