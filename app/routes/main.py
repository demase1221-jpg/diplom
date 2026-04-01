from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import QRCode
import qrcode
import os
import uuid

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def home():
    user_qr = QRCode.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', qrcodes=user_qr)


@main.route('/qr', methods=['GET', 'POST'])
@login_required
def qr():
    if request.method == 'POST':
        link = request.form.get('link')

        filename = f"{uuid.uuid4()}.png"
        filepath = os.path.join('app/static', filename)

        img = qrcode.make(link)
        img.save(filepath)

        new_qr = QRCode(
            link=link,
            image=filename,
            user_id=current_user.id
        )

        db.session.add(new_qr)
        db.session.commit()

        return redirect('/')

    return render_template('qr.html')


@main.route('/delete/<int:id>')
@login_required
def delete_qr(id):
    qr = QRCode.query.get_or_404(id)

    if qr.user_id != current_user.id:
        return "Нет доступа"

    filepath = os.path.join('app/static', qr.image)
    if os.path.exists(filepath):
        os.remove(filepath)

    db.session.delete(qr)
    db.session.commit()

    return redirect('/')