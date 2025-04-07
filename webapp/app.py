from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Liste pour stocker les items
items = [1, 2]

@app.route('/', methods=['GET', 'POST'])
def item_view():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            items.append(name)  # Ajouter l'item à la liste
            return redirect('/')  # Rediriger après le POST
    return render_template('item_form.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)