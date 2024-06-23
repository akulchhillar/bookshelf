import streamlit as st
import requests


    


def query_book(name):
    url = f"https://openlibrary.org/search.json?q={name}"
    req = requests.get(url,verify=False)
    res = req.json()
    st.session_state['book_data'] = res['docs']

def AddToSupabase():
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVzdm5maHdsZmNya3Bkd2d2a2x0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODczNTY5OTcsImV4cCI6MjAwMjkzMjk5N30.hPS22Wlb6jhg3zRCDWfMBz3fW2bLXAvvyjxH0TPyajY"
    headers = {
    'apikey': key,
    'Authorization': f'Bearer {key}',
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal',
}

    json_data = {
        'book_name': st.session_state.selectedbook[0],
        'book_img': st.session_state.selectedbook[2],
        'status': 'Reading',
        'Author': st.session_state.selectedbook[1],
        'total_pages': st.session_state.selectedbook[3]
    }

    response = requests.post('https://esvnfhwlfcrkpdwgvklt.supabase.co/rest/v1/books', headers=headers, json=json_data,verify=False)
    if response.status_code == 201:
        st.success('Book Added',icon='🎈')
    
def GetLatestReading():
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVzdm5maHdsZmNya3Bkd2d2a2x0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODczNTY5OTcsImV4cCI6MjAwMjkzMjk5N30.hPS22Wlb6jhg3zRCDWfMBz3fW2bLXAvvyjxH0TPyajY"
    headers = {
    'apikey': key,
    'Authorization': f'Bearer {key}',
    'Range': '0-9'}

    response = requests.get('https://esvnfhwlfcrkpdwgvklt.supabase.co/rest/v1/books?status=eq.Reading&select=*', headers=headers,verify=False)
    return (response.json())

def UpdateCurrentReading():
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVzdm5maHdsZmNya3Bkd2d2a2x0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODczNTY5OTcsImV4cCI6MjAwMjkzMjk5N30.hPS22Wlb6jhg3zRCDWfMBz3fW2bLXAvvyjxH0TPyajY"
    headers = {
    'apikey': key,
    'Authorization': f'Bearer {key}',
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal'}

    params = {
    'status': 'eq.Reading'}

    json_data = {
        'pages_completed': (int(st.session_state.updateddata[0])),
        'total_pages': int(st.session_state.updateddata[1])
    }

    

    response = requests.patch('https://esvnfhwlfcrkpdwgvklt.supabase.co/rest/v1/books', params=params, headers=headers, json=json_data,verify=False)
 
    if response.status_code == 204:
        st.success('Updated!',icon="🎈")

if 'querybooks' in st.session_state:
    img_id = st.session_state.querybooks.split(',')[1].strip().split('-')[0].strip()
    title = st.session_state.querybooks.split('by')[0].strip()
    author = st.session_state.querybooks.split('by')[1].split(',')[0].strip()
    total_pages = st.session_state.querybooks.split(',')[1].strip().split('-')[1].strip()
    st.session_state.selectedbook = [title,author,img_id,total_pages]
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
                    books.append(f'{book['title']} by {book['author_name'][0]} , {book['cover_edition_key']} - {book['number_of_pages_median']}')
                except:
                    pass
            query_books = st.radio('Select a book to add',
                                   books,index=None,
                                   key="querybooks")

        
with tab2:
    data = GetLatestReading()[0]


    with st.form("search_form"):
        
        st.markdown(f'### You are currently reading ***{data['book_name']}*** by ***{data['Author']}***')
        st.number_input('You have read',value = data['pages_completed'],key="readpages")
        st.number_input('Total Pages',value = data['total_pages'],key="totalpages")
        st.session_state.updateddata = [st.session_state.readpages,st.session_state.totalpages]
        submitted = st.form_submit_button("Submit",on_click=UpdateCurrentReading)



