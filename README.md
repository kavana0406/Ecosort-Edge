♻️ EcoSort Edge

AI-Powered E-Waste Identification, Condition Assessment and Recycling Assistant

1. Project Overview

EcoSort Edge is an AI-assisted e-waste management application that identifies electronic waste using image classification and provides recommendations for reuse, repair and responsible recycling.

The application combines MobileNetV3 image classification, a Python-based decision engine, a local knowledge base and Llama 3.2 for supplementary AI-generated guidance.

2. Objectives

- Identify electronic waste from uploaded images.
- Classify electronic items into seven categories.
- Distinguish e-waste from non-e-waste.
- Assess device working condition and visible damage.
- Provide recommendations for reuse, repair and recycling.
- Generate additional guidance using a locally running Llama model.

3. Technologies Used

Technology| Purpose
Python| Core development
Streamlit| User interface
PyTorch| Deep learning
MobileNetV3-Small| Image classification
Llama 3.2 1B| AI-generated guidance
Ollama| Local Llama execution
Pandas| Assessment history and CSV export
JSON| Local knowledge base

4. Classification Categories

1. Mobile / Tablet
2. Charger / Adapter
3. Cable
4. Circuit Board
5. Computer Accessory
6. Other E-waste
7. Non-E-waste

5. Main Features

- Image upload and AI-based classification.
- Non-e-waste rejection based on model prediction.
- Manual condition assessment.
- Python decision engine for recommendations.
- Llama AI e-waste advisor.
- Local recycling knowledge base.
- Assessment history.
- CSV report download.

6. System Workflow

1. Upload an image.
2. MobileNetV3 analyses the image.
3. The predicted category is displayed.
4. Non-e-waste predictions are rejected.
5. The user confirms the e-waste category.
6. The user provides condition details.
7. The Python decision engine evaluates the item.
8. Llama generates supplementary guidance.
9. Knowledge-base recommendations are displayed.
10. Assessment results can be downloaded as a CSV report.

7. Project Structure

EcoSort-Edge/
│
├── app.py
├── llama_helper.py
├── requirements.txt
├── test_model.py
│
├── dataset/
│   ├── train/
│   └── val/
│
├── knowledge_base/
│   └── ewaste_guidance.json
│
├── models/
│   ├── class_names.json
│   └── ewaste_mobilenetv3.pth
│
├── pages/
│   └── 1_Condition_Assessment.py
│
├── rules/
│   └── decision_engine.py
│
└── vision/
    ├── check_dataset.py
    ├── predict.py
    └── train_model.py

8. Installation and Execution

Prerequisites

- Python
- Git
- Ollama
- Llama 3.2 1B model

Clone the repository

git clone https://github.com/kavana0406/Ecosort-Edge.git
cd Ecosort-Edge

Create a virtual environment

python -m venv venv

Activate the environment (Windows)

.\venv\Scripts\Activate.ps1

Install dependencies

pip install -r requirements.txt

Download the Llama model

ollama pull llama3.2:1b

Ensure Ollama is running locally.

Launch the application

streamlit run app.py

9. Model and Testing

The project uses MobileNetV3-Small with a seven-class classification layer.

The model was trained and tested using the available project dataset. The current dataset is small, so the reported validation accuracy should be treated as preliminary rather than a reliable measure of real-world performance.

10. Limitations

- Classification performance depends on dataset size and image quality.
- More diverse training and testing images are required.
- AI-generated guidance should be treated as supplementary.
- Physical device safety must be verified by qualified personnel.

11. Future Enhancements

- Expand and improve the labelled image dataset.
- Improve model accuracy and robustness.
- Add more electronic waste categories.
- Integrate verified recycling-centre information.
- Explore deployment on edge/ARM devices.

12. Project Information

Project: EcoSort Edge
Challenge: Bharat AI-SoC Student Challenge
Repository: https://github.com/kavana0406/Ecosort-Edge

---

EcoSort Edge – Supporting responsible electronic waste management through AI.
