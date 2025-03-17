from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_session import Session
import ollama

app = Flask(__name__, static_folder='static', static_url_path='/')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'cuhk'  # Do not expose this
app.config['PERMANENT_SESSION_LIFETIME'] = 1800 # Expiry: 30 mins
app.config['SESSION_TYPE'] = 'cachelib' # Session as files in flask_session folder
Session(app)  # Initialize session in flask app
CHAT_MODEL = 'llama3.2:1b'
SYSTEM_MSG = {'role': 'system',
              'content': 'You are a helpful assistant who keeps answer super concise.'}

@app.route('/')
def default():
    return redirect(url_for('chat'))

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    prompt = request.form.get('prompt')
    if prompt:
        # Get history
        history = session.get('history', [SYSTEM_MSG])
        # Get response
        user_msg = {'role': 'user', 'content': prompt}
        history.append(user_msg)
        response = ollama.chat(CHAT_MODEL, history)
        bot_msg = {'role': 'assistant', 'content': response.message.content}
        # Append message
        history.append(bot_msg)
        # Update history in session
        session['history'] = history
    return render_template('chat.html')

@app.route('/clear_session')
def clear_session():
    if 'history' in session:
        # Alternatively: session.clear() can clear everything
        session.pop('history')
        # Optionally: create a pop-up message (see "Flash message handler" in layout.html)
        flash(message='Session cleared', category='success')
    else:
        flash(message='Nothing to clear', category='danger')
    # Go back to main page
    return redirect(url_for('chat'))

if __name__ == '__main__':
    app.run()
