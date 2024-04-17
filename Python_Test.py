import tkinter as tk
from tkinter import messagebox
import json
from tkinter import font
class Book:
    def __init__(self, name, author, date):
        self.name = name
        self.author = author
        self.date = date

class Library:
    def __init__(self, file_path):
        self.file_path = file_path
        self.books = self.load_books()

    def load_books(self):
        try:
            with open(self.file_path, "r") as json_file:
                data = json.load(json_file)
                books = [Book(item['name'], item['author'], item['date']) for item in data]
            return books
        except FileNotFoundError:
            print("File not found. Creating a new empty library.")
            return []

    def save_books(self):
        with open(self.file_path, "w") as json_file:
            json.dump([{"name": book.name, "author": book.author, "date": book.date} for book in self.books], json_file, indent=4)

    def Addbook(self, name, author, date):
        self.books.append(Book(name, author, date))
        self.save_books()

    def query_books_by_author(self, author):
        found_books = [book for book in self.books if book.author == author]
        if found_books:
            for book in found_books:
                print(f"Name: {book.name}, Author: {book.author}, Date: {book.date}")
        else:
            print("No books found for this author.")

    def edit_book(self, book_index, name, author, date):
        if 0 <= book_index < len(self.books):
            self.books[book_index].name = name
            self.books[book_index].author = author
            self.books[book_index].date = date
            self.save_books()
            print("Book information updated successfully.")
        else:
            print("Invalid book index.")

    def delete_book(self, book_index):
        if 0 <= book_index < len(self.books):
            del self.books[book_index]
            self.save_books()
            print("Book deleted successfully.")
        else:
            print("Invalid book index.")
    def show_books(self):
        if self.books:
            for i, book in enumerate(self.books):
                print(f"Index: {i+1}, Name: {book.name}, Author: {book.author}, Date: {book.date}")
        else:
            print("Library is empty.")

def read_accounts_from_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def load_accounts_from_file():
    global accounts
    accounts = read_accounts_from_json('accounts.json')

def save_accounts_to_json(accounts, file_path):
    with open(file_path, 'w') as file:
        json.dump(accounts, file)

def register():
    username = entry_username.get()
    password = entry_password.get()

    if username in accounts:
        messagebox.showerror("Register", "Tên người dùng đã tồn tại!")
    else:
        accounts[username] = password
        save_accounts_to_json(accounts, 'accounts.json')
        messagebox.showinfo("Register", "Đăng ký thành công!")

def login():
    global logged_in
    username = entry_username.get()
    password = entry_password.get()

    if username in accounts and accounts[username] == password:
        messagebox.showinfo("Login", "Đăng nhập thành công!")
        logged_in = True
        show_library_management()
    else:
        messagebox.showerror("Login", "Sai tên đăng nhập hoặc mật khẩu!")
# Biến để lưu trạng thái đăng nhập

def show_library_management():
    
    # Xóa các widget của cửa sổ đăng nhập
    label_username.pack_forget()
    entry_username.pack_forget()
    label_password.pack_forget()
    entry_password.pack_forget()
    button_login.pack_forget()
    button_register.pack_forget()

    # Hiển thị giao diện quản lý thư viện
    label_welcome = tk.Label(root, text="ỨNG DỤNG QUẢN LÝ THƯ VIỆN ",fg='red', font=('cambria', 16))
    label_welcome.pack()

    # Tạo và hiển thị danh sách sách
    label_books = tk.Label(root, text="Danh sách sách có trong thư viện:")
    label_books.pack()

    listbox_books = tk.Listbox(root,width= 80, height=20)
    
    a=0
    for book in library.books:
        a=a+1
        listbox_books.insert(tk.END, f"{a}) Name: {book.name}, Author: {book.author}, Date: {book.date}")
    listbox_books.pack()

    # Tạo và hiển thị nút thêm sách mới
    button_add_book = tk.Button(root, text="Thêm sách", command=GUIadd_book)
    button_add_book.place(x=300, y=400)
    #nut xoa
    button_delete_book = tk.Button(root, text="Xóa sách", command=GUIdelete_book)
    button_delete_book.place(x=240,y=400)
   
    button_edit_book = tk.Button(root, text="cập nhật sách", command=GUI_edit_book)
    button_edit_book.place(x=100,y=400)

    # Tạo và hiển thị ô tìm kiếm sách
    button_search = tk.Button(root, text="Tìm kiếm", command=GUIsearch_book)
    button_search.place(x=30, y=450 )

def GUIsearch_book():
    new_window = tk.Toplevel(root, width=500, height=550)
    new_window['background'] = '#dcdcdc'  
    new_window.title("search_book")
    new_window.geometry(f"{500}x{500}")

    label_Book = tk.Label(new_window, text="Tên sách:", font=("bold", 10), fg='#b22222')
    label_Book.place(x=120, y=50)
    entry_Book = tk.Entry(new_window)
    entry_Book.place(x=235, y=50)

    label_Author = tk.Label(new_window, text="Tác giả:", font=("bold", 10), fg='#b22222')
    label_Author.place(x=120, y=85)
    entry_Author = tk.Entry(new_window)
    entry_Author.place(x=235, y=85)

    def handle_search():
        keyword = entry_Book.get()
        search_query = keyword
        search_book(search_query, listbox)

    search_button = tk.Button(new_window, text="Search", command=handle_search)
    search_button.place(x=200, y=120)

    listbox = tk.Listbox(new_window, width=50)
    listbox.place(x=50, y=150)

def GUIadd_book():
    new_window = tk.Toplevel(root,width=500,height=550)
    new_window['background']='#dcdcdc'  
    new_window.title("add_book")
    new_window.geometry(f"{500}x{400}")
    label_Book = tk.Label(new_window, text="Tên sách:",font=("bold",10) , fg='#b22222')
    label_Book.place(x=120, y=50)
    entry_Book = tk.Entry(new_window)
    entry_Book.place(x=235, y=50)
    label_Author = tk.Label(new_window, text="Tác giả:",font=("bold",10) ,fg='#b22222')
    label_Author.place(x=120,y=85)
    entry_Author = tk.Entry(new_window)
    entry_Author.place(x=235,y=85)
    label_Date = tk.Label(new_window, text="Ngày(xx/yy/zzzz):",font=("bold",10) , fg='#b22222')
    label_Date.place(x=120, y=120)
    entry_Date = tk.Entry(new_window)
    entry_Date.place(x=235,y=120)
    def add_book():
            Name_book=entry_Book.get()
            Author=entry_Author.get()
            Date=entry_Date.get()
            if not Name_book or not Author or not Date:
                 messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin sách.")
                 return
            library.Addbook(Name_book,Author,Date)
            entry_Book.delete(0, tk.END)
            entry_Author.delete(0, tk.END)
            entry_Date.delete(0, tk.END)
    button_add = tk.Button(new_window, text="Thêm sách",bg='#F30D14', command=add_book)
    button_add.place(x=240, y=143)


 
def GUIdelete_book():
    new_window = tk.Toplevel(root,width=500,height=600) 
    new_window.title("delete")
    new_window.geometry(f"{500}x{400}")
    label_Book_delete = tk.Label(new_window, text="Vị trí sách muốn xóa")
    label_Book_delete.pack()
    entry_Book_delete = tk.Entry(new_window)
    entry_Book_delete.pack()
    def delete():
        library.show_books()
        STT=int(entry_Book_delete.get())
        STT=STT-1
        library.delete_book(STT)
        entry_Book_delete.delete(0,tk.END)
    button_add = tk.Button(new_window, text="xóa sách",bg='#F6ED08', command=delete)
    button_add.pack()

def GUI_edit_book():
    new_window = tk.Toplevel(root, width=500, height=600)
    new_window.title("edit")
    new_window.geometry(f"{500}x{400}")
    
    label_Book_edit = tk.Label(new_window, text="Vị trí sách muốn sửa")
    label_Book_edit.pack()
    entry_Book_edit = tk.Entry(new_window)
    entry_Book_edit.pack()
    
    label_Book = tk.Label(new_window, text="Tên sách:")
    label_Book.pack()
    entry_Book = tk.Entry(new_window)
    entry_Book.pack()
    
    label_Author = tk.Label(new_window, text="Tác giả:")
    label_Author.pack()
    entry_Author = tk.Entry(new_window)
    entry_Author.pack()
    
    label_Date = tk.Label(new_window, text="Ngày:")
    label_Date.pack()
    entry_Date = tk.Entry(new_window)
    entry_Date.pack()
    
    def edit():
        library.show_books()
        STT = int(entry_Book_edit.get())
        STT=STT-1
        Name_book = entry_Book.get()
        Author = entry_Author.get()
        Date = entry_Date.get()
        library.edit_book(STT, Name_book, Author, Date)
        entry_Book_edit.delete(0, tk.END)
        entry_Book.delete(0, tk.END)
        entry_Author.delete(0, tk.END)
        entry_Date.delete(0, tk.END)
    
    button_add = tk.Button(new_window, text="sửa sách", command=edit)
    button_add.pack()
    
        
         
def search_book(keyword, listbox):
    listbox.delete(0, tk.END)
    found_books = []
    a=0
    for book in library.books:# Sử dụng đối tượng library để truy cập danh sách sách
        a=a+1
        if keyword.lower() in book.name.lower() or keyword.lower() in book.author.lower():
            found_books.append(f"{a}) Name: {book.name}, Author: {book.author}, Date: {book.date}")
    if found_books:
        for book in found_books:
            listbox.insert(tk.END, book)
    else:
        listbox.insert(tk.END, "Không tìm thấy sách.")

# Tạo cửa sổ
root = tk.Tk()
root.title("Quản lý thư viện")
root.geometry(f"{500}x{500}")
#background
root['background']='#FCE5EB'  



# Tạo các widget cho cửa sổ đăng nhập
label_username = tk.Label(root, text="Tên đăng nhập:", fg='#2439EF',font=("Roman",10),width=12, padx=8, pady=5)
label_username.place(x=130,y=120)
entry_username = tk.Entry(root)
entry_username.place(x=230,y=125)

label_password = tk.Label(root, text="Mật khẩu:", fg='#2439EF',font=("Roman",10),width=12, padx=8, pady=5)
label_password.place(x=130,y=145)
entry_password = tk.Entry(root, show="*")
entry_password.place(x=230,y=150)

button_login = tk.Button(root, text="Đăng nhập", bg='#E32222', command=login)
button_login.place(x=230,y=175)


button_register = tk.Button(root, text="Đăng ký", bg='#E32222', command=register)
button_register.place(x=300,y=175)
button_add = tk.Button(root, text="Thoát",bg='#F30D14', command=quit)
button_add.place(x=150, y=175)
# Hiển thị cửa sổ
load_accounts_from_file()
file_path = "khanggvnz.json"
library = Library(file_path)
root.mainloop()
