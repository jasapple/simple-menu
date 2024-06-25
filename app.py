#!/usr/bin/env python3
"""
Author: Joshua Singh

"""
import argparse
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.jinja_env.add_extension('jinja2.ext.do')
db = SQLAlchemy(app)


legal_disclaimer_file = "legal.txt"
legal_disclaimer = ""

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    available = db.Column(db.Boolean, default=True, nullable=False)
    items = db.relationship('Item', backref='section', lazy=True, cascade="all, delete-orphan")

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "available": self.available,
            "items": self.items
        }

class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(50), nullable=False)  # e.g., "Small", "Large"
    amount = db.Column(db.Float, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def as_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "amount": self.amount,
            "item_id": self.item_id
        }

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    available = db.Column(db.Boolean, default=True, nullable=False)
    prices = db.relationship('Price', backref='item', lazy=True, cascade="all, delete-orphan")

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "available": self.available,
            "section_id": self.section_id,
            "prices": self.prices
        }


@app.route('/')
def display_menu():
    sections = Section.query.all()
    return render_template('display.html', 
                           sections=sections, disclaimer=legal_disclaimer,
                           background="#ff0000")

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if 'section_name' in request.form:
            section_name = request.form['section_name']
            section_description = request.form.get('section_description')
            new_section = Section(name=section_name, description=section_description)
            db.session.add(new_section)
            db.session.commit()
        elif 'item_name' in request.form:
            item_name = request.form['item_name']
            item_description = request.form.get('item_description')
            section_id = request.form['section_id']
            new_item = Item(name=item_name, description=item_description, section_id=int(section_id))
            db.session.add(new_item)
            db.session.commit()
        return redirect(url_for('admin'))

    sections = Section.query.all()
    return render_template('admin.html', sections=sections)

@app.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        item.name = request.form['item_name']
        item.description = request.form.get('item_description')
        item.section_id = request.form['section_id']
        db.session.commit()
        return redirect(url_for('edit_item', item_id = item_id))

    sections = Section.query.all()
    return render_template('edit_item.html', item = item, sections = sections)

@app.route('/edit_section/<int:section_id>', methods=['GET', 'POST'])
def edit_section(section_id):
    section = Section.query.get_or_404(section_id)
    if request.method == 'POST':
        section.name = request.form['section_name']
        section.description = request.form.get('section_description')
        db.session.commit()
        return redirect(url_for('edit_section', section_id = section_id))

    return render_template('edit_section.html', section = section)

@app.route('/toggle_availability/<int:item_id>', methods=['POST'])
def toggle_availability(item_id):
    item = Item.query.get_or_404(item_id)
    item.available = not item.available
    db.session.commit()
    return redirect(url_for('edit_item', item_id = item_id))

@app.route('/toggle_section/<int:section_id>', methods=['POST'])
def toggle_section(section_id):
    section = Section.query.get_or_404(section_id)
    section.available = not section.available
    db.session.commit()
    return redirect(url_for('edit_section', section_id = section_id))

@app.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/delete_section/<int:section_id>', methods=['POST'])
def delete_section(section_id):
    section = Section.query.get_or_404(section_id)
    db.session.delete(section)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/edit_price/<int:item_id>', methods=['GET', 'POST'])
def edit_price(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        price_id = request.form.get('price_id')
        if price_id:
            price = Price.query.get_or_404(price_id)
            price.label = request.form['price_label']
            price.amount = request.form['price_amount']
        else:
            price_label = request.form['price_label']
            price_amount = request.form['price_amount']
            new_price = Price(label=price_label, amount=float(price_amount), item_id=item.id)
            db.session.add(new_price)
        db.session.commit()
        return redirect(url_for('edit_price', item_id=item.id))

    return render_template('edit_price.html', item=item)

@app.route('/delete_price/<int:price_id>', methods=['POST'])
def delete_price(price_id):
    price = Price.query.get_or_404(price_id)
    item_id = price.item_id
    db.session.delete(price)
    db.session.commit()
    return redirect(url_for('edit_price', item_id=item_id))

def get_legal_disclosure():
    if os.path.isfile(legal_disclaimer_file) and os.access(legal_disclaimer_file, os.R_OK):
        print(legal_disclaimer_file)
        with open(legal_disclaimer_file) as file:
            global legal_disclaimer
            legal_disclaimer = file.read()
            print(legal_disclaimer)

@app.route("/sections", methods=["GET"])
def get_sections():
    sections = Section.query.all()

    # Manually producing a Dictionary of all values from the DB
    # This is NOT ideal but a workaround for experimental functionality to retrieve data as JSON
    data = []
    for s in sections:
        d = s.as_dict()
        i = []
        for item in d['items']:
            p = []
            id = item.as_dict()
            for price in id['prices']:
                p.append(price.as_dict())
            id['prices'] = p
            i.append(id)
        d['items'] = i

        data.append(d)
    
    return jsonify(data)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Cool script description here.')
    parser.add_argument("--legal", action='store', help="path to legal disclosure file")
    parser.add_argument("-d", "--debug", action="store_true", default=False, help="Add debug content to webpage")

    args = parser.parse_args()
    
    if args.legal:
        legal_disclaimer_file = args.legal
        pass

    get_legal_disclosure()
    app.run(host="0.0.0.0", debug=args.debug)
    

