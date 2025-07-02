import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!doctype html>
<title>SmartPrice Scanner</title>
<h2>Product Search</h2>
<form method="post">
  Search term: <input name="q" required>
  <input type="submit" value="Scan">
</form>
{% if results %}
  <h3>Results</h3>
  <ul>
  {% for item in results %}
    <li>
      <b>{{item['title']}}</b><br>
      Price: ${{item['price']}}<br>
      Amazon: ${{item['amazon_price']}}<br>
      Sold/month: {{item['sold']}}
    </li>
  {% endfor %}
  </ul>
{% endif %}
"""

def fake_scrape(term):
    return [
        {"title": f"{term} Example Product", "price": 30, "amazon_price": 120, "sold": 25},
        {"title": f"{term} Cheap Find", "price": 20, "amazon_price": 100, "sold": 40},
    ]

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        q = request.form['q']
        items = fake_scrape(q)
        results = [
            item for item in items
            if item['price'] <= 0.3 * item['amazon_price'] and item['sold'] > 20
        ]
    return render_template_string(HTML, results=results)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # ✅ Use Railway's PORT
    app.run(host='0.0.0.0', port=port, debug=False)
