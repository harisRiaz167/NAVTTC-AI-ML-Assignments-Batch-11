# Week 06 - NLP Preprocessing & Convolutional Neural Networks (CNN)

**Student Name:** Muhammad Ahmed Nadeem  
**Course:** NAVTTC AI & Machine Learning - Batch 11  
**Special Submission:** Monday Review Assignment  

---

## Overview

This module covers deep learning foundations for natural language processing and computer vision:
1. **NLP Text Preprocessing Pipeline:** Tokenization, integer index vocabulary building, sequence length standardization via fixed-length padding and truncation.
2. **1D-CNN for Text & Sentiment Analysis:** Applying 1D convolutional filters over word embedding vectors to extract local contextual n-grams for text classification.
3. **2D-CNN for Computer Vision:** Spatial feature learning with 2D convolution (`Conv2D`), spatial downsampling with `MaxPooling2D`, and multi-class classification.

---

## Files in this Directory

| Notebook | Topic | Framework & Architecture | Purpose / Status |
|---|---|---|---|
| **`Class_08_NLP_Tokenization_and_Padding.ipynb`** | Class Lecture 08 | Python, NumPy sequence padding & LeetCode string problems | Daily live class notebook |
| **`CNN_1D_Text_Classification.ipynb`** | 1D-CNN Text Classifier | TensorFlow/Keras: `Embedding` + `Conv1D` + `GlobalMaxPooling1D` + `Dense` | **Monday Submission Task (Text)** |
| **`CNN_2D_Image_Classification.ipynb`** | 2D-CNN Image Classifier | TensorFlow/Keras: `Conv2D` + `MaxPooling2D` + `Flatten` + `Dense` | **Monday Submission Task (Image)** |

---

## Key Highlights of the CNN Models
- **Text CNN (1D):** Direct continuation of Class 8's tokenization and padding pipeline. Achieves sentiment classification on sentence reviews.
- **Image CNN (2D):** Standard deep vision model with 99%+ accuracy on normalized visual digit patterns.
