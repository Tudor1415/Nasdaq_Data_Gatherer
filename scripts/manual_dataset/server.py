import requests
from bs4 import BeautifulSoup
from flask import Flask

app = Flask(__name__)

form = f"""
<form action="/class">
     <input type="radio" name="field" value="political"> <br>
     <input type="radio" name="field" value="product"> <br>
     <input type="radio" name="field" value="launch"> <br>
     <input type="radio" name="field" value="scandal"> <br>
     <input type="radio" name="field" value="stock"> <br>
     <input type="radio" name="field" value="failure"> <br>
     <input type="radio" name="field" value="sucess"> <br>
     <input type="radio" name="field" value="positive"> <br>
     <input type="radio" name="field" value="negative"> <br>
     <input type="radio" name="field" value="neutral"> <br>
     <input type="radio" name="field" value="leak"> <br>
     <input type="radio" name="field" value="developpement"> <br>
     <input type="radio" name="field" value="product_upgrade"> <br>
     <input type="radio" name="field" value="negotiation"> <br>
     <input type="radio" name="field" value="problem"> <br>
     <input type="radio" name="field" value="board_members"> <br>
     <input type="radio" name="field" value="event"> <br>
     <input type="radio" name="field" value=""> <br>
     <input type="radio" name="field" value=""> <br>
     <input type="radio" name="field" value=""> <br>
     <input type="radio" name="field" value=""> <br>
     <input type="radio" name="field" value=""> <br>
     <input type="radio" name="field" value=""> <br>
     <input type="radio" name="field" value=""> <br>
     <input type="radio" name="field" value=""> <br>
     <input type="radio" name="field" value=""> <br>
     <input type="radio" name="field" value=""> <br>
     <input type="radio" name="field" value=""> <br>
  <input type="submit" value="Next" />
</form>
"""
def get_content(text):
    soup = BeautifulSoup(text, 'html.parser')
    form = soup.new_tag('form')
    form.string="abcdef"
    content = soup.select(".MNK4Vd")[0]
    content.insert(0, form)
    return content.prettify()

@app.route('/story/')
@app.route('/story/<name>')
def get_story(name):
    text = requests.get(f"https://news.google.com/stories/{name}").text
    content = get_content(text)
    return content
