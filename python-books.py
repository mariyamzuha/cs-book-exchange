import mysql.connector as sql
conn=sql.connect (host='localhost' , user='root' , password='m12345', database='exchangebooks')
cursr=conn.cursor()
print ("==============================================================================================================================")
print ("""                                   Second-Hand Book Exchanging Platform
                                                -Swap and Get Books Easily""" )

print ("==============================================================================================================================")
def Main_Menu():
    while True:
        print ("1. To create a new account")
        print ("2. To log in to your existing account")
        print ("3. Exit")
        print ("==============================================================================================================================")
        cho=input("Enter Your Choice : ")
        print ("==============================================================================================================================")
        if cho== "1":
           uss=input("Enter a username : ")
           create_acc(uss)
        elif cho == "2":
            usser=input("Enter your username : ")
            check_acc(usser)
        elif cho == "3":
            print ("Thankyou !")
            break
        else:
            print("Invalid choice. Please try again")
            print ("==============================================================================================================================")
def create_acc (username):
    a="y"
    while a=="y":
        ch="select * from users where username = '{}'".format(username)
        cursr.execute(ch)
        d=cursr.fetchall()
        if d:
            print("Username already exists")
            print ("==============================================================================================================================")
            a=input("Do you want to try another username ? y/n ")

        else :
            print("Username Valid")
            passw=input("Enter a password for your account : ")
            locate=input('Enter your location : ')
            ins="insert into users(username,password,location) values('{}','{}','{}')".format(username,passw,locate)
            cursr.execute(ins)
            conn.commit()
            print ("==============================================================================================================================")
            print ("Account created")
            print ("==============================================================================================================================")
            user_menu(username)
    else:
          Main_Menu()
def check_acc(user_name):
    passd=input("Enter your password : ")
    check = "SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(user_name, passd)
    cursr.execute(check)
    users=cursr.fetchone()
    if users:
         print ("==============================================================================================================================")
         print("Login Successful")
         print ("==============================================================================================================================")
         user_menu(user_name)
    else:
        print ("==============================================================================================================================")
        print ("Invalid username or password")

def user_menu(users_name):
    while True:
        print ("1. To sell a book")
        print ("2. To buy a book")
        print ("3. To check credits")
        print ("4. Modify location")
        print("5. Logout")
        print ("==============================================================================================================================")
        choice=input("Enter your choice : ")
        if choice=="1":
            sell_book(users_name)
        elif choice=="2":
            buy_book(users_name)
        elif choice=="3":
            check_credits(users_name)
        elif choice=="4":
            modify_locations(users_name)
        elif choice=="5":
            break
        else:
            print("Invalid choice. Please try again")

def sell_book(usernames):
    print ("==============================================================================================================================")
    title = input("Enter the book title: ")
    author = input("Enter the author: ")
    titles= title.upper()
    authors= author.upper()
    condition = input("Enter the condition of the book: ")
    print ("==============================================================================================================================")
    inse="INSERT INTO books (username, title, author, book_condition) VALUES ('{}', '{}', '{}', '{}')".format(usernames, titles, authors, condition)
    cursr.execute(inse)
    conn.commit()
    update_credits (usernames, 10)
    print("Book out for sale. THANKYOU!")
    print ("10 credits are added to your account")
    print ("==============================================================================================================================")

def buy_book(buyer_name):
    while True:
        print("1. See all the available books")
        print ("2. Select the book")
        print ("3. Exit")
        print ("==============================================================================================================================")
        chh=input("Enter your choice: ")
        if chh == "1":
            see="select title,author from books "
            cursr.execute(see)
            available=cursr.fetchall()
            print ("==============================================================================================================================")
            for row in available:
                print (row[0],"by",row[1])
            print ("==============================================================================================================================")
        elif chh=="2":
            select_book(buyer_name)
        elif chh=="3" :
            break
        else:
            print("Invalid choice. Please try again")
            print ("==============================================================================================================================")
            
        
def select_book(buy):
    book_title = input("Enter the title of the book you want to buy: ")
    book_author = input("Enter the author of the book : ")
    book_titles= book_title.upper()
    book_authors= book_author.upper()
    print ("==============================================================================================================================")
    chk = "select * from books where title ='{}' and author = '{}'". format(book_titles,book_authors)
    cursr.execute(chk)
    book = cursr.fetchone()
    if book:
        cond= "select book_condition from books where title='{}'".format(book_titles,)
        cursr.execute(cond)
        condition=cursr.fetchone()
        credits3="select username from books where title = '{}'".format (book_titles,)
        cursr.execute(credits3)
        seller_s=cursr.fetchone()
        seller_username = seller_s[0]
        if buy==seller_username:
            print("The book is being donated by you. Please select another book")
            print ("==============================================================================================================================")
            return
        else:
            print ("The condition of the book is " , condition[0])
            chk_con=input("Would you like to proceed? (y/n): " )
            if chk_con=="y" or chk_con=="Y":
                cc="select credits from users where username = '{}'".format(buy,)
                cursr.execute (cc)
                bal=cursr.fetchone()
                if bal[0] >= 10:
                    update_transactions(buy,seller_username,book_titles)
                    print ("Book titled",book_title,"by",book_author)
                    update_credits(buy, -10)
                    update_credits(seller_username,3)
                    print ("Your book has been ordered, THANKYOU!")
                    print ("==============================================================================================================================")
        
                else:
                    print ("You don't have enough credit balance in your account to purchase the book")
                    print ("==============================================================================================================================")
            else:
                buy_book(buy)
            
    else:
        print("Book not available")
        print ("==============================================================================================================================")

def check_credits (name):
    cred="select credits from users where username = '{}'".format(name)
    cursr.execute(cred)
    cre=cursr.fetchone()
    cred=cre[0]
    print ("==============================================================================================================================")
    print("Your current credit balance is ",cred)
    print ("==============================================================================================================================")


def update_credits (upname , credit):
    upd="update users set credits = credits + {} where username = '{}'".format(credit,upname)
    cursr.execute (upd)
    conn.commit()

def modify_locations (mn):
    new=input("Enter your new location : ")
    mod="update users set location = '{}' where username ='{}'".format (new,mn)
    cursr.execute (mod)
    conn.commit ()
    print("Your location has been changed to",new)
    print ("==============================================================================================================================")

    
def update_transactions (buyer , seller,bookname):
    rec="insert into transactions values ('{}','{}','{}')".format (buyer , seller ,bookname)
    cursr.execute (rec)
    conn.commit()
    delete= "delete from books where title = '{}'".format(bookname,)
    cursr.execute (delete)
    conn.commit()

Main_Menu()
cursr.close()
conn.close()

                

            
    
        
    
             
