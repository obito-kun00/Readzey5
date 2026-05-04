import os
import sys
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to sys.path to ensure 'models' is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from models import db, User, Book, ReadingProgress, Profile, UserFavorite, ContactUs, UserActivity, UserAchievement, Admin, FriendRequest, ReadingInvite
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
import PyPDF2

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_super_secret_key_here')
basedir = os.path.abspath(os.path.dirname(__file__))

# Database configuration for PostgreSQL
PG_USER = os.getenv('PG_USER', 'postgres')
PG_PASSWORD = os.getenv('PG_PASSWORD', '')
PG_HOST = os.getenv('PG_HOST', 'localhost')
PG_PORT = os.getenv('PG_PORT', '5432')
PG_DBNAME = os.getenv('PG_DBNAME', 'Readsmart')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'Uploads')

db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Track online users in memory: {user_id: connection_count}
online_users_count = {}

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
return User.query.get(int(user_id))

@app.route('/')
def index():
books = Book.query.limit(20).all()
books_data = []
if current_user.is_authenticated:
favorites = [f.book_id for f in UserFavorite.query.filter_by(user_id=current_user.id).all()]
else:
favorites = []

for book in books:
books_data.append({
'book': book,
'is_favourite': book.id in favorites
})
return render_template('index.html', books=books_data)

@app.route('/library')
def library():
books = Book.query.all()
books_data = []
if current_user.is_authenticated:
favorites = [f.book_id for f in UserFavorite.query.filter_by(user_id=current_user.id).all()]
else:
favorites = []

for book in books:
books_data.append({
'book': book,
'is_favourite': book.id in favorites
})
return render_template('library.html', books_data=books_data)

@app.route('/favourite_books')
@login_required
def favourite_books():
favorites = UserFavorite.query.filter_by(user_id=current_user.id).all()
book_ids = [f.book_id for f in favorites]
books = Book.query.filter(Book.id.in_(book_ids)).all() if book_ids else []

books_data = []
for book in books:
books_data.append({
'book': book,
'is_favourite': True
})
return render_template('library.html', books_data=books_data, page_title="Your Favourite Books")

@app.route('/toggle_favourite/<int:book_id>')
@login_required
def toggle_favourite(book_id):
fav = UserFavorite.query.filter_by(user_id=current_user.id, book_id=book_id).first()
if fav:
db.session.delete(fav)
flash('Removed from favorites.', 'info')
else:
new_fav = UserFavorite(user_id=current_user.id, book_id=book_id)
db.session.add(new_fav)
flash('Added to favorites!', 'success')
db.session.commit()
return redirect(request.referrer or url_for('library'))


@app.route('/read/<int:book_id>')
@login_required
def read(book_id):
book = Book.query.get_or_404(book_id)
progress = ReadingProgress.query.filter_by(user_id=current_user.id, book_id=book_id).first()
if not progress:
progress = ReadingProgress(user_id=current_user.id, book_id=book_id, current_page=1, total_pages=book.total_pages)
db.session.add(progress)
db.session.commit()

room_id = request.args.get('room')
partner_id = request.args.get('partner_id')
partner = None
if partner_id:
partner = User.query.get(partner_id)

all_books = Book.query.all()
return render_template('read.html', book=book, current_page=progress.current_page, room_id=room_id, partner=partner, all_books=all_books)

@app.route('/update_progress', methods=['POST'])
@login_required
def update_progress():
book_id = request.form.get('book_id')
current_page = request.form.get('current_page')
if book_id and current_page:
progress = ReadingProgress.query.filter_by(user_id=current_user.id, book_id=book_id).first()
if progress:
progress.current_page = int(current_page)
db.session.commit()
return jsonify({'status': 'success'})
return jsonify({'status': 'error'}), 400

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
is_edit_mode = request.args.get('edit') == '1'
user_profile = Profile.query.filter_by(user_id=current_user.id).first()

if request.method == 'POST':
current_user.username = request.form.get('username')
current_user.email = request.form.get('email')

photo = request.files.get('photo')
if photo and photo.filename:
if not os.path.exists(app.config['UPLOAD_FOLDER']):
os.makedirs(app.config['UPLOAD_FOLDER'])
filename = f"user_{current_user.id}_{photo.filename}"
photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
if not user_profile:
user_profile = Profile(user_id=current_user.id, profile_photo=filename)
db.session.add(user_profile)
else:
user_profile.profile_photo = filename

db.session.commit()
flash('Profile updated successfully.', 'success')
return redirect(url_for('profile'))

progress = ReadingProgress.query.filter_by(user_id=current_user.id).all()
stats = {
'books': len(set(p.book_id for p in progress)),
'pages': sum(p.current_page for p in progress),
'total_pages': sum(p.total_pages for p in progress)
}

activities = UserActivity.query.filter_by(user_id=current_user.id).order_by(UserActivity.created_at.desc()).limit(5).all()
badges = UserAchievement.query.filter_by(user_id=current_user.id).all()

books_progress = []
for p in progress:
book = Book.query.get(p.book_id)
if book:
books_progress.append({
'book_id': book.id,
'title': book.title,
'current_page': p.current_page,
'total_pages': p.total_pages
})

return render_template('profile.html',
current_user_profile=user_profile,
is_edit_mode=is_edit_mode,
stats=stats,
activities=activities,
badges=badges,
books=books_progress)

@app.route('/login', methods=['GET', 'POST'])
def login():
if request.method == 'POST':
login_input = request.form.get('email') # this might be email or admin username
password = request.form.get('password')

# Check if admin
admin = Admin.query.filter_by(username=login_input).first()
if admin and check_password_hash(admin.password, password):
session['admin_logged_in'] = True
return redirect(url_for('admin_dashboard'))

# Check if regular user
user = User.query.filter_by(email=login_input).first()
if user and check_password_hash(user.password, password):
login_user(user)
return redirect(url_for('index'))

return render_template('login.html', error='Invalid email/username or password.')

return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
if current_user.is_authenticated:
return redirect(url_for('index'))
if request.method == 'POST':
username = request.form.get('username')
email = request.form.get('email')
password = request.form.get('password')

if User.query.filter_by(email=email).first():
return render_template('register.html', error='Email already registered.', username=username, email=email)

if User.query.filter_by(username=username).first():
return render_template('register.html', error='Username already taken.', username=username, email=email)

new_user = User(
username=username,
email=email,
password=generate_password_hash(password),
is_verified=True
)
db.session.add(new_user)
db.session.commit()

db.session.add(Profile(user_id=new_user.id))
db.session.add(UserActivity(user_id=new_user.id, activity_type='Account Created', description='Welcome to ReadSmart!'))
db.session.commit()

login_user(new_user)
return redirect(url_for('index'))
return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
logout_user()
return redirect(url_for('index'))

@app.route('/admin_upload', methods=['GET', 'POST'])
def admin_upload():
if not session.get('admin_logged_in'):
return redirect(url_for('admin_login'))

if request.method == 'POST':
title = request.form.get('title')
cover = request.files.get('cover')
pdf_file = request.files.get('file')

if cover and pdf_file and title:
cover_filename = cover.filename
pdf_filename = pdf_file.filename

cover_path = os.path.join(app.root_path, 'static', 'cover', cover_filename)
pdf_path = os.path.join(app.root_path, 'static', 'pdfs', pdf_filename)

os.makedirs(os.path.dirname(cover_path), exist_ok=True)
os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

cover.save(cover_path)
pdf_file.save(pdf_path)

total_pages = 0
try:
with open(pdf_path, 'rb') as f:
reader = PyPDF2.PdfReader(f)
total_pages = len(reader.pages)
except Exception as e:
print("Error reading PDF:", e)

new_book = Book(title=title, cover=f"cover/{cover_filename}", pdfs=f"pdfs/{pdf_filename}", total_pages=total_pages)
db.session.add(new_book)
db.session.commit()
flash(f"Book uploaded successfully with {total_pages} pages!", "success")
return redirect(url_for('admin_upload'))

return render_template('admin_upload.html')

@app.route('/about_us')
def about_us():
return render_template('about_us.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
if request.method == 'POST':
email = request.form.get('email')
problem = request.form.get('problem')
msg = ContactUs(user_id=current_user.id if current_user.is_authenticated else None, user_email=email, problem=problem)
db.session.add(msg)
db.session.commit()
flash("Message sent! We'll get back to you.", "success")
return redirect(url_for('contact_us'))
return render_template('contact_us.html')

@app.route('/privacy_policy')
def privacy_policy():
return render_template('privacy_policy.html')

@app.route('/terms_of_service')
def terms_of_service():
return render_template('terms_of_service.html')

@app.route('/featured')
def featured():
# Fetch top 12 books as "featured"
books = Book.query.limit(12).all()
books_data = []

if current_user.is_authenticated:
favorites = [f.book_id for f in UserFavorite.query.filter_by(user_id=current_user.id).all()]
else:
favorites = []

for book in books:
books_data.append({
'book': book,
'is_favourite': book.id in favorites
})
return render_template('featured.html', featured_books=books_data)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
if session.get('admin_logged_in'):
return redirect(url_for('admin_dashboard'))
if request.method == 'POST':
username = request.form.get('username')
password = request.form.get('password')
admin = Admin.query.filter_by(username=username).first()
if admin and check_password_hash(admin.password, password):
session['admin_logged_in'] = True
return redirect(url_for('admin_dashboard'))
else:
return render_template('admin_login.html', error="Invalid credentials")
return render_template('admin_login.html')

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
if not session.get('admin_logged_in'):
return redirect(url_for('admin_login'))

if request.method == 'POST':
user_id = request.form.get('user_id')
action = request.form.get('action')
user = User.query.get(user_id)
if user and action in ['active', 'blocked']:
user.status = action
db.session.commit()
return redirect(url_for('admin_dashboard'))

users = User.query.all()
total_books = Book.query.count()
return render_template('admin_dashboard.html', users=users, total_books=total_books, total_users=len(users))

@app.route('/admin_delete_book')
def admin_delete_book_view():
if not session.get('admin_logged_in'):
return redirect(url_for('admin_login'))
books = Book.query.all()
return render_template('admin_delete_book.html', books=books, message=request.args.get('message'))

@app.route('/admin_delete_book', methods=['POST'])
def admin_delete_book():
if not session.get('admin_logged_in'):
return redirect(url_for('admin_login'))
book_id = request.form.get('book_id')
book = Book.query.get(book_id)
if book:
# Delete local files (skip checking if it's default sample for safety)
if book.cover and os.path.exists(os.path.join(app.root_path, 'static', book.cover)):
os.remove(os.path.join(app.root_path, 'static', book.cover))
if book.pdfs and os.path.exists(os.path.join(app.root_path, 'static', book.pdfs)):
os.remove(os.path.join(app.root_path, 'static', book.pdfs))

db.session.delete(book)
db.session.commit()
return redirect(url_for('admin_delete_book_view', message='Book deleted successfully!'))
return redirect(url_for('admin_delete_book_view', message='Book not found!'))

@app.route('/admin_logout')
def admin_logout():
session.pop('admin_logged_in', None)
return redirect(url_for('admin_login'))

# --- FRIEND SYSTEM AND READING SESSIONS ---

@app.route('/friends', methods=['GET'])
@login_required
def friends():
search_query = request.args.get('search')
users = []
if search_query:
users = User.query.filter(User.username.ilike(f'%{search_query}%'), User.id != current_user.id).all()

sent_requests = FriendRequest.query.filter_by(sender_id=current_user.id, status='pending').all()
received_requests = FriendRequest.query.filter_by(receiver_id=current_user.id, status='pending').all()

# Get friends (both where user is sender or receiver)
accepted_sent = FriendRequest.query.filter_by(sender_id=current_user.id, status='accepted').all()
accepted_received = FriendRequest.query.filter_by(receiver_id=current_user.id, status='accepted').all()

friends_list = []
for req in accepted_sent:
friends_list.append(req.receiver)
for req in accepted_received:
friends_list.append(req.sender)

friend_ids = [u.id for u in friends_list]
sent_req_ids = [r.receiver_id for r in sent_requests]
rec_req_ids = [r.sender_id for r in received_requests]

reading_invites = ReadingInvite.query.filter_by(receiver_id=current_user.id, status='pending').all()
accepted_invites = ReadingInvite.query.filter(
(ReadingInvite.status == 'accepted') &
((ReadingInvite.sender_id == current_user.id) | (ReadingInvite.receiver_id == current_user.id))
).all()

# Pass the book library to invite friends to read
all_books = Book.query.all()

# Get currently online friends
online_user_ids = list(online_users_count.keys())

return render_template('friends.html',
users=users,
sent_requests=sent_requests,
received_requests=received_requests,
friends_list=friends_list,
friend_ids=friend_ids,
sent_req_ids=sent_req_ids,
rec_req_ids=rec_req_ids,
reading_invites=reading_invites,
accepted_invites=accepted_invites,
all_books=all_books,
online_user_ids=online_user_ids)

@app.route('/send_friend_request/<int:user_id>', methods=['POST'])
@login_required
def send_friend_request(user_id):
existing = FriendRequest.query.filter(
((FriendRequest.sender_id == current_user.id) & (FriendRequest.receiver_id == user_id)) |
((FriendRequest.sender_id == user_id) & (FriendRequest.receiver_id == current_user.id))
).first()

status_type = 'info'
if not existing:
req = FriendRequest(sender_id=current_user.id, receiver_id=user_id)
db.session.add(req)
db.session.commit()
msg = 'Friend request sent!'
status_type = 'success'
else:
msg = 'Request already exists or you are already friends.'

if request.headers.get('Accept') == 'application/json' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
return jsonify({'status': status_type, 'message': msg})

flash(msg, status_type)
return redirect(url_for('friends'))

@app.route('/accept_friend_request/<int:request_id>', methods=['POST'])
@login_required
def accept_friend_request(request_id):
req = FriendRequest.query.get(request_id)
if req and req.receiver_id == current_user.id:
req.status = 'accepted'
db.session.commit()
flash('Friend request accepted!', 'success')
return redirect(url_for('friends'))

@app.route('/invite_to_read', methods=['POST'])
@login_required
def invite_to_read():
friend_id = request.form.get('friend_id')
book_id = request.form.get('book_id')
if friend_id and book_id:
friend_id = int(friend_id)
invite = ReadingInvite(sender_id=current_user.id, receiver_id=friend_id, book_id=book_id)
db.session.add(invite)
db.session.commit()

# Check if user is online for specific flash message
if friend_id in online_users_count:
flash('Reading invite sent! Your friend is online and has been notified.', 'success')
else:
flash('Friend is offline. They will see your invite once they log in.', 'info')

return redirect(url_for('friends'))

@app.route('/accept_invite/<int:invite_id>', methods=['POST'])
@login_required
def accept_invite(invite_id):
invite = ReadingInvite.query.get(invite_id)
if invite and invite.receiver_id == current_user.id:
invite.status = 'accepted'
db.session.commit()
# Create a unique room ID for these two users
room_id = f"book_{invite.book_id}_users_{min(invite.sender_id, invite.receiver_id)}_{max(invite.sender_id, invite.receiver_id)}"

# Tell the sender's browser to redirect to the room automatically!
from flask_socketio import emit
sender_url = url_for('read', book_id=invite.book_id, room=room_id, partner_id=invite.receiver_id)
print("Emitting redirect to sender:", invite.sender_id)
# Using socketio instead of emit because we are outside a direct socket request handler sometimes
socketio.emit('redirect_to_session', {'url': sender_url}, room=f'user_{invite.sender_id}')

return redirect(url_for('read', book_id=invite.book_id, room=room_id, partner_id=invite.sender_id))
return redirect(url_for('friends'))

@app.route('/join_my_session/<int:invite_id>', methods=['GET'])
@login_required
def join_my_session(invite_id):
invite = ReadingInvite.query.get(invite_id)
if invite and invite.status == 'accepted' and (invite.sender_id == current_user.id or invite.receiver_id == current_user.id):
room_id = f"book_{invite.book_id}_users_{min(invite.sender_id, invite.receiver_id)}_{max(invite.sender_id, invite.receiver_id)}"
partner_id = invite.receiver_id if invite.sender_id == current_user.id else invite.sender_id
return redirect(url_for('read', book_id=invite.book_id, room=room_id, partner_id=partner_id))
return redirect(url_for('friends'))

@app.route('/end_session/<int:invite_id>', methods=['POST'])
@login_required
def end_session(invite_id):
invite = ReadingInvite.query.get(invite_id)
if invite and (invite.sender_id == current_user.id or invite.receiver_id == current_user.id):
db.session.delete(invite)
db.session.commit()
flash('Session ended.', 'info')
return redirect(url_for('friends'))


@app.route('/api/books', methods=['GET'])
def api_get_books():
books = Book.query.all()
book_list = []
for book in books:
cover_filename = book.cover.split('/')[-1] if book.cover and '/' in book.cover else book.cover
# Assuming the emulator accesses the host's localhost via 10.0.2.2
# So we return the fully qualified android-accessible URL:
cover_url = f"http://10.0.2.2:8000/static/cover/{cover_filename}" if cover_filename else None

book_list.append({
'id': book.id,
'title': book.title,
'author': getattr(book, 'author', 'Unknown Author'),
'description': getattr(book, 'description', 'Explore this title on our platform.'),
'cover_url': cover_url
})
return jsonify({'books': book_list})

@app.route('/api/book/<int:book_id>', methods=['GET'])
def api_get_book(book_id):
book = Book.query.get_or_404(book_id)
cover_filename = book.cover.split('/')[-1] if book.cover and '/' in book.cover else book.cover
pdf_filename = book.pdfs.split('/')[-1] if book.pdfs and '/' in book.pdfs else book.pdfs

# 10.0.2.2 is the standard loopback for Android Emulators to the host machine
cover_url = f"http://10.0.2.2:8000/static/cover/{cover_filename}" if cover_filename else None
pdf_url = f"http://10.0.2.2:8000/static/pdfs/{pdf_filename}" if pdf_filename else None

return jsonify({
'success': True,
'id': book.id,
'title': book.title,
'author': getattr(book, 'author', 'Unknown Author'),
'description': getattr(book, 'description', 'No description available.'),
'cover_url': cover_url,
'pdf_url': pdf_url,
'total_pages': book.total_pages
})

@app.route('/api/login', methods=['POST'])
def api_login():
data = request.get_json()
if not data or not data.get('email') or not data.get('password'):
return jsonify({'success': False, 'message': 'Missing credentials'})
login_input = data.get('email')
password = data.get('password')

# Check Admin
admin = Admin.query.filter_by(username=login_input).first()
if admin and check_password_hash(admin.password, password):
return jsonify({
'success': True,
'is_admin': True,
'user_id': admin.id,
'username': admin.username,
'token': f'admin-token-{admin.id}'
})

# Check User
user = User.query.filter_by(email=login_input).first()
if user and check_password_hash(user.password, password):
return jsonify({
'success': True,
'is_admin': False,
'token': f'user-token-{user.id}',
'user_id': user.id,
'username': user.username
})
return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/api/register', methods=['POST'])
def api_register():
data = request.get_json()
if User.query.filter_by(email=data.get('email')).first():
return jsonify({'success': False, 'message': 'Email already registered'})
new_user = User(
username=data.get('username'),
email=data.get('email'),
password=generate_password_hash(data.get('password'), method='pbkdf2:sha256')
)
db.session.add(new_user)
db.session.commit()
return jsonify({'success': True, 'message': 'Account created successfully'})

@app.route('/api/friends/<int:user_id>', methods=['GET'])
def api_get_friends(user_id):
user = User.query.get(user_id)
if not user:
return jsonify({'success': False, 'message': 'User not found'})

# Get friends list (sender or receiver is the user and status is accepted)
friends = FriendRequest.query.filter(
((FriendRequest.sender_id == user_id) | (FriendRequest.receiver_id == user_id)),
(FriendRequest.status == 'accepted')
).all()

# Get pending requests to show in app too
requests = FriendRequest.query.filter_by(receiver_id=user_id, status='pending').all()

# Get reading invites
invites = ReadingInvite.query.filter_by(receiver_id=user_id, status='pending').all()

# Get accepted invites for currently active sessions
active_invites = ReadingInvite.query.filter(
(ReadingInvite.status == 'accepted') &
((ReadingInvite.sender_id == user_id) | (ReadingInvite.receiver_id == user_id))
).all()

friends_list = []
for req in friends:
friend = req.sender if req.receiver_id == user_id else req.receiver
friends_list.append({
'id': friend.id,
'username': friend.username,
'is_online': friend.id in online_users_count
})

request_list = [{
'id': req.id,
'sender_id': req.sender_id,
'sender_username': req.sender.username
} for req in requests]

invite_list = [{
'id': inv.id,
'sender_name': inv.sender.username,
'book_title': inv.book.title,
'book_id': inv.book_id
} for inv in invites]

active_session_list = [{
'id': inv.id,
'book_id': inv.book_id,
'book_title': inv.book.title,
'partner_name': inv.receiver.username if inv.sender_id == user_id else inv.sender.username,
'partner_id': inv.receiver_id if inv.sender_id == user_id else inv.sender_id
} for inv in active_invites]

return jsonify({
'success': True,
'friends': friends_list,
'requests': request_list,
'invites': invite_list,
'active_sessions': active_session_list
})

@app.route('/api/friend_requests/<int:user_id>', methods=['GET'])
def api_get_friend_requests(user_id):
requests = FriendRequest.query.filter_by(receiver_id=user_id, status='pending').all()
request_list = [{
'id': req.id,
'sender_id': req.sender_id,
'sender_username': req.sender.username
} for req in requests]
return jsonify({'success': True, 'requests': request_list})

@app.route('/api/reading_invites/<int:user_id>', methods=['GET'])
def api_get_invites(user_id):
invites = ReadingInvite.query.filter_by(receiver_id=user_id, status='pending').all()
invite_list = [{
'id': inv.id,
'sender_name': inv.sender.username,
'book_title': inv.book.title,
'book_id': inv.book_id
} for inv in invites]
return jsonify({'success': True, 'invites': invite_list})

@app.route('/api/profile/<int:user_id>', methods=['GET'])
def api_get_profile(user_id):
user = User.query.get(user_id)
if not user:
return jsonify({'success': False, 'message': 'User not found'})

friends_count = FriendRequest.query.filter(
((FriendRequest.sender_id == user_id) | (FriendRequest.receiver_id == user_id)),
(FriendRequest.status == 'accepted')
).count()

progress = ReadingProgress.query.filter_by(user_id=user_id).all()
stats = {
'total_books': len(set(p.book_id for p in progress)),
'pages_read': sum(p.current_page for p in progress),
'total_pages_goal': sum(p.total_pages for p in progress)
}

activities = UserActivity.query.filter_by(user_id=user_id).order_by(UserActivity.created_at.desc()).limit(5).all()
activity_list = [{'type': a.activity_type, 'desc': a.description, 'date': a.created_at.strftime('%Y-%m-%d')} for a in activities]

badges = UserAchievement.query.filter_by(user_id=user_id).all()
badge_list = [{'name': b.badge_name, 'icon': b.badge_icon} for b in badges]

profile_obj = Profile.query.filter_by(user_id=user_id).first()
photo_url = None
if profile_obj and profile_obj.profile_photo:
photo_url = url_for('static', filename='Uploads/' + profile_obj.profile_photo, _external=True)

return jsonify({
'success': True,
'username': user.username,
'email': user.email,
'friends_count': friends_count,
'profile_photo': photo_url,
'stats': stats,
'activities': activity_list,
'badges': badge_list
})

@app.route('/api/update_profile', methods=['POST'])
def api_update_profile():
user_id = request.form.get('user_id')
if not user_id:
return jsonify({'success': False, 'message': 'User ID missing'})

user = User.query.get(user_id)
if not user:
return jsonify({'success': False, 'message': 'User not found'})

profile_obj = Profile.query.filter_by(user_id=user_id).first()
if not profile_obj:
profile_obj = Profile(user_id=user_id)
db.session.add(profile_obj)

if 'photo' in request.files:
file = request.files['photo']
if file.filename != '':
filename = f"user_{user_id}_{int(datetime.utcnow().timestamp())}.png"
file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
profile_obj.profile_photo = filename

username = request.form.get('username')
email = request.form.get('email')
if username: user.username = username
if email: user.email = email

db.session.commit()
return jsonify({'success': True, 'message': 'Profile updated successfully'})

@app.route('/api/search_users', methods=['GET'])
def api_search_users():
query = request.args.get('q', '')
if not query:
return jsonify({'users': []})
users = User.query.filter(User.username.ilike(f'%{query}%')).limit(10).all()
return jsonify({'users': [{'id': u.id, 'username': u.username} for u in users]})

@app.route('/api/send_friend_request', methods=['POST'])
def api_send_friend_request():
data = request.get_json()
sender_id = data.get('sender_id')
receiver_id = data.get('receiver_id')
if not sender_id or not receiver_id:
return jsonify({'success': False, 'message': 'Missing IDs'})

existing = FriendRequest.query.filter(
((FriendRequest.sender_id == sender_id) & (FriendRequest.receiver_id == receiver_id)) |
((FriendRequest.sender_id == receiver_id) & (FriendRequest.receiver_id == sender_id))
).first()

if existing:
return jsonify({'success': False, 'message': 'Request already exists'})

req = FriendRequest(sender_id=sender_id, receiver_id=receiver_id)
db.session.add(req)
db.session.commit()
return jsonify({'success': True, 'message': 'Request sent'})

@app.route('/api/get_info', methods=['GET'])
def api_get_info():
return jsonify({
'about': 'ReadZey is your ultimate social reading companion. Discover thousands of books, track your progress, and read together with friends in real-time.',
'contact_email': 'support@readzey.com',
'contact_phone': '+1 (555) 012-3456',
'address': '123 Reader Lane, Booktown'
})

# --- SOCKET.IO EVENTS ---

@app.route('/api/accept_friend_request/<int:request_id>', methods=['POST'])
def api_accept_friend_request(request_id):
req = FriendRequest.query.get(request_id)
if req:
req.status = 'accepted'
db.session.commit()
return jsonify({'success': True, 'message': 'Friend request accepted'})
return jsonify({'success': False, 'message': 'Request not found'})

@app.route('/api/invite_to_read', methods=['POST'])
def api_invite_to_read():
data = request.get_json()
sender_id = data.get('sender_id')
friend_id = data.get('friend_id')
book_id = data.get('book_id')
if sender_id and friend_id and book_id:
invite = ReadingInvite(sender_id=sender_id, receiver_id=friend_id, book_id=book_id)
db.session.add(invite)
db.session.commit()
return jsonify({'success': True, 'message': 'Invite sent'})
return jsonify({'success': False, 'message': 'Missing parameters'})

@app.route('/api/accept_invite/<int:invite_id>', methods=['POST'])
def api_accept_invite(invite_id):
invite = ReadingInvite.query.get(invite_id)
if invite:
invite.status = 'accepted'
db.session.commit()
# Note: Socket redirection logic would go here if we had mobile socket support ready
return jsonify({'success': True, 'message': 'Invite accepted'})
return jsonify({'success': False, 'message': 'Invite not found'})

@socketio.on('connect')
def handle_global_connect():
if current_user.is_authenticated:
join_room(f'user_{current_user.id}')
if current_user.id not in online_users_count:
online_users_count[current_user.id] = 1
emit('user_online', {'user_id': current_user.id}, broadcast=True)
else:
online_users_count[current_user.id] += 1

@socketio.on('disconnect')
def handle_global_disconnect():
if current_user.is_authenticated:
leave_room(f'user_{current_user.id}')
if current_user.id in online_users_count:
online_users_count[current_user.id] -= 1
if online_users_count[current_user.id] <= 0:
del online_users_count[current_user.id]
emit('user_offline', {'user_id': current_user.id}, broadcast=True)

@socketio.on('join_reading_room')
def handle_join(data):
room = data.get('room')
user_name = data.get('username')
if room:
join_room(room)
emit('chat_message', {'user': 'System', 'msg': f'{user_name} has joined the room.'}, room=room)

@socketio.on('leave_reading_room')
def handle_leave(data):
room = data.get('room')
user_name = data.get('username')
if room:
leave_room(room)
emit('chat_message', {'user': 'System', 'msg': f'{user_name} has left the room.'}, room=room)

@socketio.on('chat_message')
def handle_chat_message(data):
room = data.get('room')
user_name = data.get('username')
msg = data.get('msg')
if room and msg:
# Broadcast to everyone else in the room
emit('chat_message', {'user': user_name, 'msg': msg}, room=room, include_self=False)

@socketio.on('page_turn')
def handle_page_turn(data):
room = data.get('room')
page = data.get('page')
if room and page:
# Broadcast to everyone else in the room
emit('sync_page', {'page': page}, room=room, include_self=False)

def init_db():
with app.app_context():
db.create_all()
# Create some sample books if empty
if not Book.query.first():
b1 = Book(title='Sample Book 1', cover='cover/sample1.jpg', pdfs='pdfs/sample.pdf', total_pages=10)
db.session.add(b1)
db.session.commit()

# Create default admin if missing
if not Admin.query.filter_by(username='yash').first():
badmin = Admin(username='yash', password=generate_password_hash('aloneyash'))
db.session.add(badmin)
db.session.commit()

if __name__ == '__main__':
init_db()
socketio.run(app, debug=True, port=8000)
