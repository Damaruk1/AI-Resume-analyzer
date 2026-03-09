AI Resume Analyzer

An AI-powered web application that analyzes resumes against job descriptions and provides actionable feedback to improve ATS compatibility.

The system evaluates resumes using keyword matching and skill extraction techniques to simulate how modern recruitment systems filter candidates.

It helps job seekers understand how well their resumes align with specific job requirements and provides recommendations to improve their chances of passing automated resume screening.

Problem Statement

Modern recruitment processes rely heavily on Applicant Tracking Systems (ATS) to automatically filter resumes before they reach recruiters. While ATS systems improve efficiency for organizations, they create a major challenge for job seekers.

Many qualified candidates are rejected because their resumes are not optimized for ATS keyword detection or job description alignment.

This project addresses that gap by creating a system that simulates ATS-style resume analysis and provides users with feedback on:

resume–job description alignment

missing skills and keywords

overall ATS compatibility score

Features

Resume upload (PDF)

Job description input

ATS compatibility scoring

Skill extraction

Missing skill detection

Resume improvement suggestions

Analysis history tracking

Modern web interface

System Architecture

Frontend: React + Vite
Backend: FastAPI (Python)
Database: MongoDB
Deployment: Vercel (Frontend) + Railway (Backend)

Workflow:

User uploads resume

User provides job description

Backend extracts resume text

System compares resume with job description

ATS score and recommendations are generated

Results are stored in database

Tech Stack

Frontend
React
Vite
Axios
React Router

Backend
Python
FastAPI
PyPDF2 (PDF text extraction)
Uvicorn

Database
MongoDB

Deployment
Vercel
Railway
