# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 20:54:58 2024

@author: jp042
"""


import sqlite3
conn = sqlite3.connect('reviews.db')
c = conn.cursor()

#executed once, will give error that table already exists
'''c.execute("""
          CREATE TABLE BlahBlah(
          time text
          age integer
          gender text
          profession text
          review text
          sentiment integer)
          """)'''
conn.commit()


from tkinter import *

root1 = Tk()
main = "Restaurant Review Analysis System/"
root1.title(main+"Welcome Page")
 
label = Label(root1, text="RESTAURANT REVIEW ANALYSIS SYSTEM",
              bd=2, font=('Arial', 47, 'bold', 'underline'))
 
ques = Label(root1, text="Are you a Customer or Owner ???")

frame = Frame(root1)
frame.pack()
review =LabelFrame(frame, text='give review')
review.grid(row=0,column=0)
review_label = Label(review, text ='Give review')
review_label.grid(row=0,column=0)
review_entry = Entry(review)
review_entry.grid(row=1,column=0)
submit_review = Button(root2, text="Submit Review", font=(
    'Arial', 20), padx=100, pady=20, command=lambda: [
    estimate(rev_tf.get()), root2.destroy()])

'''cust = Button(root1, text="Customer", font=('Arial', 20),
              padx=80, pady=20, command=take_review)
 
owner = Button(root1, text="Owner", font=('Arial', 20),
               padx=100, pady=20, command=login)'''

def estimate(s):
 
    conn = sqlite3.connect('Restaurant_food_data.db')
    c = conn.cursor()
    review = re.sub('[^a-zA-Z]', ' ', s)
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not')
     
    review = [ps.stem(word)
              for word in review if not word in set(all_stopwords)]
    review = ' '.join(review)
    X = cv.transform([review]).toarray()
    res = classifier.predict(X)  # list
     
    if "not" in review:
        res[0] = abs(res[0]-1)
     
    selected_foods = []
    for i in range(len(foods)):
        if variables[i].get() == 1:
            selected_foods.append(foods[i])
     
    c.execute("SELECT *,oid FROM item")
    records = c.fetchall()
     
    for i in records:
        rec = list(i)
        if rec[0] in selected_foods:
            n_cust = int(rec[1])+1
            n_pos = int(rec[2])
            n_neg = int(rec[3])
             
            if res[0] == 1:
                n_pos += 1
            else:
                n_neg += 1
                 
            pos_percent = round((n_pos/n_cust)*100, 1)
            neg_percent = round((n_neg/n_cust)*100, 1)
            c.execute("""UPDATE item SET Item_name=:item_name,No_of_customers\
            =:no_of_customers,No_of_positive_reviews=:no_of_positives,\
            No_of_negative_reviews=:no_of_negatives,Positive_percentage\
            =:pos_perc,Negative_percentage=:neg_perc  where oid=:Oid""",
                      {
                          'item_name': rec[0],
                          'no_of_customers': str(n_cust),
                          'no_of_positives': str(n_pos),
                          'no_of_negatives': str(n_neg),
                          'pos_perc': str(pos_percent)+"%",
                          'neg_perc': str(neg_percent)+"%",
                          'Oid': foods.index(rec[0])+1
                      }
                      )
    selected_foods = []
 
    conn.commit()
    conn.close()

def take_review():
    root2 = Toplevel()
    root2.title(main + "Give Review")

    # Main label
    label = Label(root2, text="RESTAURANT REVIEW ANALYSIS SYSTEM",
                  bd=2, font=('Arial', 47, 'bold', 'underline'))

    # Label for review input
    req2 = Label(root2, text="Give your review below....")
    req2.config(font=("Helvetica", 20))
    
    # Entry widget for review text
    rev_tf = Entry(root2, width=125, borderwidth=5)

    # Note for the review input
    req3 = Label(root2, text="NOTE: Use 'not' instead of 'n't'.")
    
    # Submit button
    submit_review = Button(root2, text="Submit Review", font=(
        'Arial', 20), padx=100, pady=20, command=lambda: [
        estimate(rev_tf.get()), root2.destroy()])
    
    root2.attributes("-zoomed", True)
    label.grid(row=0, column=0, columnspan=4)
    req2.grid(row=1, column=0, columnspan=4, sticky=W + E)
    rev_tf.grid(row=2, column=0, columnspan=4, padx=10, pady=10)
    req3.grid(row=3, column=0, columnspan=4, padx=10, pady=10)
    submit_review.grid(row=4, column=0, columnspan=4, padx=10, pady=10)


        
    root2.mainloop()
def login():
    root3 = Toplevel()
    root3.title(main+"owner verification")
     
    label = Label(root3, text="RESTAURANT REVIEW ANALYSIS SYSTEM",
                  bd=2, font=('Arial', 47, 'bold', 'underline'))
     
    label2 = Label(root3, text="VERIFY OWNERSHIP", bd=1,
                   font=('Helvetica', 30, 'bold', 'underline'))
     
    label3 = Label(root3, text="To verify your ownership, please \
    enter your restaurant's private rras code....",
                   bd=1, font=('Helvetica', 20, 'bold'))
    ent = Entry(root3, show="*", borderwidth=2)
    submit_code = Button(root3, text="Submit", font=('Arial', 20), padx=80,
                         pady=20, command=lambda: [
                           view_details(ent.get()), root3.destroy()])
     
    root3.attributes("-zoomed", True)
    label.grid(row=0, column=0, columnspan=3)
    label2.grid(row=1, column=0, sticky=W+E, columnspan=3)
    label3.grid(row=2, column=0, sticky=W, columnspan=3)
    ent.grid(row=3, column=1, columnspan=1)
    submit_code.grid(row=4, column=1, columnspan=1)

 
cust = Button(root1, text="Customer", font=('Arial', 20),
              padx=80, pady=20, command=take_review)
owner = Button(root1, text="Owner", font=('Arial', 20),
               padx=100, pady=20, command=login)

conn.commit()
conn.close()
root1.mainloop()

