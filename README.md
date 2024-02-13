# Vectara 24h Hallucinations Hackathon

This is a proof of concept which gets integrated in a basic chat bot. 
The main idea is to genearate multiple customer responses, evaluate the grade of hallucination and choose the closest one. 

## Introduction

Based on Vectara leaderboard, each model has a percentil of possible hallucination responses. To avoid this scenario, this application is basically trying in background to generate multiple responses for a specific question, evaluate and choose the one with better result.

## UI

Simple chatbot UI using streamlit.

## Model

We are using Google Gemini for this proof of concept and vectara for RAG. 

## Data

We have generated some documents to simulate a company information. This company doesn't exists and all data is just some data example to feed the RAG uploaded into Vectara. 

## How to

