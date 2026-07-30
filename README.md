# 🩺 MedPrep Pro — Global Medical Board Examination Platform

> **MedPrep Pro** is an advanced, high-performance medical exam preparation web application designed for medical candidates preparing for international licensing and residency board examinations including **FCPS Part 1 (Pakistan)**, **USMLE Step 1 & Step 2 CK (USA)**, **PLAB 1 / UKMLA (UK)**, **NEET PG / INI-CET (India)**, and **MRCS Part A (Surgery)**.

---

## 🌟 Key Features

### 1. 📱 Mobile-First Touch & Responsive Interface
- **Mobile Bottom Navigation Bar**: Floating glassmorphism tab switcher for handheld mobile devices.
- **Sticky Exam Engine Footer**: Touch-optimized action bar with large target controls (`Prev`, `Mark for Review`, `Next/Finish`).
- **Touch Choice Cards**: High-contrast A-E option selection with touch feedback and visual badges.

### 2. 📊 Visual Performance Analytics & Graphs
- **Accuracy Trend Line & Bar Chart**: Visual progress tracking across recent practice tests.
- **Subject Mastery Breakdown**: Real-time accuracy metrics across Pathology, Pharmacology, Anatomy, Physiology, Surgery, and Clinical Medicine.
- **Daily Target Ring Gauge**: Interactive daily target tracker with customizable goals (20, 35, 50, 75, or 100 MCQs/day).

### 3. ⚖️ Multi-Exam Track Comparison Hub
- **Side-by-Side Readiness Scores**: Compare accuracy, QBank coverage percentage, and pass probability across 6 international medical board tracks.
- **Detailed Board Comparison Matrix**: Benchmark progress across FCPS, USMLE, PLAB, NEET PG, and MRCS.

### 4. 🏆 Gamified Candidate Rank & Milestones
- **Level & XP System**: Earn 10 XP per question solved + 50 XP per passed mock exam.
- **Unlocked Milestones**: Earn badges such as *First Step Doctor*, *Dedicated Scholar*, *Century Master*, *Precision Specialist*, and *Medical Fellow*.

---

## 🛠️ Technology Stack

- **Frontend**: React 18, Vite 5, JavaScript (ES2023)
- **Styling**: Vanilla CSS3, Glassmorphism, CSS Custom Properties, FontAwesome 6 Icons
- **State & Storage**: React Hooks, `localStorage` with SHA-256 password hashing security
- **Effects & UI**: Canvas Confetti, Custom SVG Charts

---

## 🚀 Getting Started

### Prerequisites
- [Node.js](https://nodejs.org/) (v16.0 or higher)
- npm or yarn

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/muhammadokashapak/medprep.git
   cd medprep
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the local development server**:
   ```bash
   npm run dev -- --host
   ```
   Open `http://localhost:3000/` or `http://<your-ip>:3000/` on your mobile device.

4. **Build for production**:
   ```bash
   npm run build
   ```

---

## 📜 License

Created with ❤️ for medical candidates worldwide by **Muhammad Okasha**.
