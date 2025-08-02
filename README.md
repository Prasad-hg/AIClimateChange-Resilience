
# 🌍 AIClimateChange Resilience

An AI-powered platform that forecasts weather patterns and promotes climate resilience through eco-awareness. This project integrates machine learning models to provide real-time, region-specific climate forecasts for India and globally. It also features an interactive chatbot for sustainability tips and user engagement.

![Project Screenshot](https://i.postimg.cc/L6SM9Kwf/image.png)

---

## 🚀 Features

- ✅ **AI/ML-based climate forecasting** using pre-trained models
- 🌦️ **India and Global weather prediction** by location and date
- 🤖 **EcoBot chatbot** integration for eco-friendly living tips
- 📅 **Date-specific forecasting** using user input
- 📊 Real-time results powered by `Flask`, `joblib`, and `MySQL`
- 💬 Friendly, interactive chatbot powered by **Botpress**
- 🌐 **Responsive UI** with clean, modern layout

---

## 🧠 Machine Learning

- **Model type**: Supervised ML models (e.g., Decision Trees / Random Forest / Regression)
- **Frameworks**: `scikit-learn`, `joblib`
- **Trained on**: Historical weather/climate datasets (India + Global)
- **Model loading**: Using `.pkl` via `joblib.load()`

---

## 🛠️ Tech Stack

| Category        | Tech Used |
|-----------------|------------|
| Frontend        | HTML, CSS, JavaScript |
| Backend         | Python, Flask |
| Machine Learning| scikit-learn, joblib |
| Database        | MySQL |
| Hosting         | GitHub (code), Firebase (optional), PostImage (image) |
| Chatbot         | Botpress |
| Others          | Firebase (future scalability) |

---

## 🔧 Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/Prasad-hg/AIClimateChange-Resilience
cd AIClimateChange-Resilience
```

2. **Create Virtual Environment & Install Dependencies**

```bash
python -m venv .venv
.venv\Scripts\activate  # (Windows)
pip install -r requirements.txt
```

3. **Start Flask Server**

```bash
python app.py
```

4. **Access Web App**

Open `http://127.0.0.1:5000/` in your browser.

---

## 📂 Folder Structure

```
AIClimateChange-Resilience/
│
├── static/                # Static files (CSS, JS)
├── templates/             # HTML Templates
├── models/                # Trained ML models (.pkl)
├── app.py                 # Main Flask app
├── requirements.txt       # Python dependencies
└── README.md
```

---

## 🧪 Example Use Cases

- 📍 Enter a state (e.g., Maharashtra) and a date to get predictions
- 🌍 Choose a global country and get future forecasts
- 💡 Chat with **EcoBot** for climate-saving tips

---

## 📦 Download ML Models

To run this project successfully, download the ML models from the link below and place them inside the `/models` directory.

🔗 [Download Models](https://drive.google.com/drive/folders/1VNQbzWiyK59KjVfZPuNnn3WE_5IpHpa-?usp=drive_link)

---

## 🌱 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve this project further.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

- Inspired by real-time climate awareness needs
- Botpress for interactive chatbot tools
- Open-source datasets and frameworks

---

## 🔗 Connect with Me

**GitHub**: [Prasad-hg](https://github.com/Prasad-hg)  
**LinkedIn**: *(Add your profile link here)*  
**Portfolio**: *(Add if available)*
