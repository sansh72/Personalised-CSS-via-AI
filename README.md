# 🎯 AI-Personalized React UI with GPT-4

This project uses **GPT-4** to dynamically update a React app's CSS based on real-time user click interactions. It analyzes user behavior from a CSV file and regenerates the layout to improve usability — all through OpenAI.

---

## 📁 Project Structure

```
.
├── backend/
│   ├── clicks.csv
│   ├── usernames.csv
│   ├── server.js
│   └── package.json
├── my-app/
│   ├── src/
│   │   ├── App.css
│   │   ├── App.js
│   │   ├── index.js
│   │   ├── component1.js ... component5.js
│   └── package.json
├── python/
│   ├── app.txt             # Original CSS backup
│   └── main.py             # GPT-4 CSS updater
└── README.md
```

---

## 🚀 How It Works

- User click data is stored in `clicks.csv`.
- A Python script runs every 10 seconds:
  - Reads the last user interaction.
  - If the user has past data, it sends the CSV + CSS to GPT-4 to regenerate `App.css`.
  - If it’s a new user, it resets `App.css` using `app.txt`.
- Only **component positions** change — font, size, style remain the same.

---

## ⚙️ Setup

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/yourreponame.git
cd yourreponame
```

### 2. Install Dependencies

**Backend**

```bash
cd backend
npm install
```

**Frontend**

```bash
cd ../my-app
npm install
```

**Python**

```bash
pip install openai pandas python-dotenv
```

---

## 🔐 Add OpenAI API Key

Create a `.env` file in the `python/` folder:

```env
OPENAI_API_KEY=your_openai_key_here
```

---

## 🏃 Run the App

Start React app:

```bash
cd my-app
npm start
```

Start the GPT-powered CSS engine:

```bash
cd ../python
python main.py
```

---

## 📌 Notes

- `app.txt` is used to restore original styles if no past data exists for a user.
- CSS is updated live in `my-app/src/App.css`.
- GPT-4 prompt ensures consistent styling with changed positions only.

---

## 📄 License

MIT — free to use and modify.
