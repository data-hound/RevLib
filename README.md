# PSBot
Cookie - All Smartphones Informator

MOTIVATION 
Now a days people ask their friends for suggestions about smart phones and laptops as there are just so many!
The amount of data present in the form of reviews on various e commerce sites is humungous, and no human can read and acquire that much knowledge in a systematic way. We aim to build a software automation for the process and develop a product that can use all its knowledge acquired from the reviews to make suggestions to humans

ABSTRACT
We are building a chatbot that would suggest the best phones according to the user interaction. 
The model we  
implement would replace a sales prp/shopkeeper responding at the other end in the best case. 
We would be scraping data from multiple e-commerce sites and make a database on which we would make our suggestions. On the data obtained from the various
sites we would apply data analytics to mine opinions about specific features of the phone. We would also use sentiment analysis on the reviews, along with the user ratings on the reviews to compute a parameter that gives us a continuous score distribution for every phone in our database. This score would be used by the chatbot to give suggestions for the phone. 
The chatbot would be rule based to begin with and would proceed to incorporate advanced NLP and ML features as we receive good datasets.
The back end of the site supports email subscription and storage of feedbacks posted by the user. This helps us to accumulate data that would be used later for training purposes

IMPLEMENTATION
Cookie(the chatbot) is implemented as a generic bot at 
http://www.reviewlib.zulipchat.com

Due to time limitations, it could not be implemented on the live server
The site is live at,
https://reviewlib.herokuapp.com/

