from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import requests

app = Flask(__name__)
@app.route('/', methods = ['POST', 'GET'])
def home_page():
    if request.method == 'POST':
        try:
            input_product = request.form['product_name'].replace(" ", "")
            global l
            global l_name
        
            l = []
            l_name = []
            for i in range(5):
                urls = "https://www.flipkart.com/search?q=" + input_product + "&page=" + str(i)
                getting_url = requests.get(urls)
                html_par = BeautifulSoup(getting_url.content, 'html.parser')
                bigboxes = html_par.find_all("div", {"class": "bhgxx2"}) 
                del bigboxes[0:3]
                for box in bigboxes:
                    try:
                        product = box.div.div.div.a['href']
                        ln = product.split("/")
                        ln[2] = 'product-reviews'
                        l.append("/".join(ln))
                        l_name.append(ln[1])
                    except:
                        pass
            return render_template("home.html", list_name = l_name, input_product = input_product)
        except:
            return render_template("error.html")
    else:
        return render_template("home.html")
    
@app.route('/reviews_page', methods = ['POST'])    
def review_page():
    if request.method == "POST":
        try:
            prod_name = request.form['selected_product_name']
            comment = []
            name = []
            rating = []
            review_with_rm = []
            likes_dislikes = []
            likes = []
            dislikes = []
            for i in range(20):
                l = globals()['l']
                for splitter in l:
                    l_r = splitter.split("/")
                    if prod_name == l_r[1]:
                        link = splitter
                        break
                fin_url = requests.get("https://flipkart.com"+ link + "&page=" + str(i))
                fin_product_source = BeautifulSoup(fin_url.content, 'html.parser')
                review_source = fin_product_source.find_all('div',{'class':"ooJZfD"})
                for j in review_source:
                    u_comment = j.find_all('p', {"class":"_2xg6Ul"})
                    comment.append([k.get_text() for k in u_comment])
                    u_name = j.find_all('p', {'class' :"_3LYOAd _3sxSiS"})
                    name.append([k.get_text() for k in u_name])
                    u_review = j.find_all('div', {'class' : "qwjRop"})
                    review_with_rm.append([k.get_text() for k in u_review])
                    u_rating = j.find_all('div', {'class':"hGSR34"})
                    rating.append([k.get_text() for k in u_rating])
                    c_likes_dislikes = j.find_all('span',{'class':"_1_BQL8"})
                    likes_dislikes.append(c_likes_dislikes)
            name = [item for sublist in name for item in sublist]
            comment = [item for sublist in comment for item in sublist]
            rating = [item for sublist in rating for item in sublist]
            review_with_rm = [item for sublist in review_with_rm for item in sublist]
            likes_dislikes = [item for sublist in likes_dislikes for item in sublist]
            for i in range(len(likes_dislikes)):
                if i%2 !=0:
                    likes.append(i)
                else:
                    dislikes.append(i)
                    review = []
            for i in review_with_rm:
                val = i.replace("READ MORE", "")
                review.append(val)
            my_dict = []
            for i in range(len(name)):
                dicts = {'Name' : name[i], "Comment" : comment[i], "Review" : review[i], "Rating" : rating[i], "likes" : likes[i], "dislikes" : dislikes[i]}
                my_dict.append(dicts)
            lens = list(range(len(my_dict)))
            return render_template("home.html", reviews = my_dict, prod_name = prod_name, lens = lens)
        except:
            return render_template("error.html")
    else:
        return render_template("home.html")

if __name__ == "__main__":
    app.run(port=8000,debug=True) 