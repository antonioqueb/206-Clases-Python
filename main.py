from io import BytesIO
from flask import Flask, render_template, request, send_file, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from wtforms import TextAreaField


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SECRET_KEY'] = 'somesecretkey'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String, nullable=False)

class NameForm(FlaskForm):
    name = StringField('Nombre Completo', validators=[DataRequired()])
    submit = SubmitField('Confirmar')

class CodeForm(FlaskForm):
    code1 = TextAreaField('Ejercicio #1', validators=[DataRequired()])
    code2 = TextAreaField('Ejercicio #2', validators=[DataRequired()])
    code3 = TextAreaField('Ejercicio #3', validators=[DataRequired()])
    code4 = TextAreaField('Ejercicio #4', validators=[DataRequired()])
    submit = SubmitField('Confirmar')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        student = Student(name=form.name.data, code='')
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('pdf_view', pdf_number=1))
    return render_template('index.html', form=form)


@app.route('/1')
def view_pdf1():
    pdf_path = '1.pdf'

    with open(pdf_path, 'rb') as pdf_file:
        pdf_content = pdf_file.read()
        pdf_stream = BytesIO(pdf_content)
        response = make_response(pdf_stream.getvalue())
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Disposition', 'inline', filename='1.pdf')
        return response

@app.route('/2')
def view_pdf2():
    pdf_path = '2.pdf'

    with open(pdf_path, 'rb') as pdf_file:
        pdf_content = pdf_file.read()
        pdf_stream = BytesIO(pdf_content)
        response = make_response(pdf_stream.getvalue())
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Disposition', 'inline', filename='2.pdf')
        return response

@app.route('/3')
def view_pdf3():
    pdf_path = '3.pdf'

    with open(pdf_path, 'rb') as pdf_file:
        pdf_content = pdf_file.read()
        pdf_stream = BytesIO(pdf_content)
        response = make_response(pdf_stream.getvalue())
        response.headers.set('Content-Type', 'application/pdf')
        response.headers.set('Content-Disposition', 'inline', filename='3.pdf')
        return response



@app.route('/prueba', methods=['GET', 'POST'])
def prueba():
    form = CodeForm()
    if form.validate_on_submit():
        student = Student.query.order_by(Student.id.desc()).first()
        if student:
            # Estoy suponiendo que tienes las columnas code2, code3 y code4 en tu base de datos.
            # Si no es así, tendrías que crear esas columnas.
            student.code = form.code1.data
            student.code2 = form.code2.data
            student.code3 = form.code3.data
            student.code4 = form.code4.data
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('prueba.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('students.db'):
            db.create_all()
    app.run(debug=False, host='0.0.0.0', port=7000)