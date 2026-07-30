import os
import sys
import sqlite3
import json
import webbrowser
import threading
import traceback
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# Resolve database path dynamically for both Python script and PyInstaller .exe
def find_db_file():
    candidates = []
    
    # 1. PyInstaller MEIPASS temporary folder
    if getattr(sys, 'frozen', False):
        meipass_dir = getattr(sys, '_MEIPASS', '')
        if meipass_dir:
            candidates.append(os.path.join(meipass_dir, "quiz_bank.db"))
            candidates.append(os.path.join(meipass_dir, "fcps_mcqs.db"))

        # Executable directory
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
        candidates.append(os.path.join(exe_dir, "quiz_bank.db"))
        candidates.append(os.path.join(exe_dir, "fcps_mcqs.db"))
        candidates.append(os.path.join(exe_dir, "_internal", "quiz_bank.db"))

    # 2. Script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates.append(os.path.join(script_dir, "quiz_bank.db"))
    candidates.append(os.path.join(script_dir, "fcps_mcqs.db"))
    candidates.append(os.path.join(os.getcwd(), "quiz_bank.db"))

    for path in candidates:
        if os.path.exists(path):
            print(f"[DB FOUND]: Using database at {path}")
            return path
            
    print(f"[WARNING]: Database file not found in candidates, falling back to script dir")
    return os.path.join(script_dir, "quiz_bank.db")

DB_FILE = find_db_file()

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

class MCQRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress noisy HTTP logs in console
        pass

    def do_GET(self):
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            query = parse_qs(parsed_path.query)

            if path == "/" or path == "/index.html":
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.end_headers()
                self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
                return

            elif path == "/favicon.ico":
                self.send_response(204) # No Content
                self.end_headers()
                return

            elif path == "/api/mcqs":
                limit = int(query.get("limit", [50])[0])
                offset = int(query.get("offset", [0])[0])
                search = query.get("search", [""])[0].strip()

                conn = get_db_connection()
                c = conn.cursor()
                
                if search:
                    count_query = "SELECT COUNT(*) FROM mcqs WHERE question LIKE ? OR explanation LIKE ?"
                    c.execute(count_query, (f"%{search}%", f"%{search}%"))
                    total = c.fetchone()[0]

                    data_query = "SELECT id, question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation FROM mcqs WHERE question LIKE ? OR explanation LIKE ? LIMIT ? OFFSET ?"
                    c.execute(data_query, (f"%{search}%", f"%{search}%", limit, offset))
                else:
                    c.execute("SELECT COUNT(*) FROM mcqs")
                    total = c.fetchone()[0]

                    data_query = "SELECT id, question, option_a, option_b, option_c, option_d, option_e, correct_answer, explanation FROM mcqs LIMIT ? OFFSET ?"
                    c.execute(data_query, (limit, offset))

                rows = c.fetchall()
                conn.close()

                mcqs = []
                for r in rows:
                    mcqs.append({
                        "id": r["id"],
                        "question": r["question"],
                        "options": {
                            "A": r["option_a"],
                            "B": r["option_b"],
                            "C": r["option_c"],
                            "D": r["option_d"],
                            "E": r["option_e"]
                        },
                        "correct_answer": r["correct_answer"],
                        "explanation": r["explanation"]
                    })

                response = {
                    "total": total,
                    "mcqs": mcqs
                }
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return

            elif path == "/api/stats":
                total = 0
                db_name = os.path.basename(DB_FILE)
                if os.path.exists(DB_FILE):
                    try:
                        conn = get_db_connection()
                        c = conn.cursor()
                        c.execute("SELECT COUNT(*) FROM mcqs")
                        total = c.fetchone()[0]
                        conn.close()
                    except Exception as err:
                        print(f"Error reading stats: {err}")

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                self.wfile.write(json.dumps({"total_mcqs": total, "db_file": db_name}).encode('utf-8'))
                return

            # Default catch-all for unknown paths
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 Not Found")

        except Exception as e:
            print(f"[SERVER ERROR]: {e}")
            traceback.print_exc()
            try:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            except Exception:
                pass

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MBBS & FCPS High-Yield MCQ Quiz Software</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col">
    <!-- Header -->
    <header class="bg-slate-900/80 border-b border-slate-800 backdrop-blur-md sticky top-0 z-50 px-6 py-4 flex items-center justify-between shadow-lg">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-gradient-to-tr from-blue-600 to-indigo-500 rounded-xl flex items-center justify-center font-extrabold text-white text-xl shadow-lg shadow-blue-500/30">
                🩺
            </div>
            <div>
                <h1 class="text-xl font-bold text-white tracking-tight">MBBS & FCPS Quiz Master</h1>
                <p class="text-xs text-slate-400">High-Yield Medical Question Bank & Practice System</p>
            </div>
        </div>

        <div class="flex items-center gap-4">
            <div id="statsBadge" class="bg-slate-800 px-3 py-1.5 rounded-xl border border-slate-700 text-xs font-semibold text-emerald-400 flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                <span>Loading Bank...</span>
            </div>
            <button onclick="startExamMode()" class="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-lg shadow-indigo-600/30">
                ⏱️ Start Exam Mode (50 MCQs)
            </button>
        </div>
    </header>

    <!-- Main Container -->
    <main class="flex-1 max-w-6xl w-full mx-auto p-6 space-y-6">
        <!-- Controls & Search -->
        <div class="bg-slate-900 border border-slate-800 p-4 rounded-2xl flex flex-col md:flex-row gap-4 items-center justify-between shadow-xl">
            <div class="relative w-full md:w-96">
                <input type="text" id="searchInput" oninput="handleSearch()" placeholder="🔍 Search MCQs by keyword (e.g., drug, heart, liver)..." class="w-full bg-slate-950 border border-slate-800 px-4 py-2.5 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>

            <div class="flex items-center gap-3">
                <button onclick="loadMCQs(0)" class="bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-xl text-xs font-semibold border border-slate-700">
                    🔄 Refresh
                </button>
                <button onclick="window.print()" class="bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-2 rounded-xl text-xs font-bold shadow-md">
                    🖨️ Print / Export PDF
                </button>
            </div>
        </div>

        <!-- Exam Timer & Score Banner (Hidden by default) -->
        <div id="examBanner" class="hidden bg-gradient-to-r from-indigo-900/80 to-blue-900/80 border border-indigo-500/30 p-4 rounded-2xl flex items-center justify-between text-white shadow-xl">
            <div class="flex items-center gap-4">
                <div class="text-2xl font-black font-mono text-amber-400" id="timerDisplay">45:00</div>
                <div>
                    <h3 class="font-bold text-sm">Exam Mode Active</h3>
                    <p class="text-xs text-indigo-200" id="examProgress">Answered: 0 / 50</p>
                </div>
            </div>
            <button onclick="finishExam()" class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold px-5 py-2 rounded-xl text-xs shadow-lg">
                ✅ Submit Exam
            </button>
        </div>

        <!-- MCQ List -->
        <div id="mcqContainer" class="space-y-6">
            <!-- MCQ Card Skeleton -->
            <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl animate-pulse space-y-4">
                <div class="h-5 bg-slate-800 rounded w-3/4"></div>
                <div class="space-y-2">
                    <div class="h-4 bg-slate-800/60 rounded w-1/2"></div>
                    <div class="h-4 bg-slate-800/60 rounded w-2/3"></div>
                </div>
            </div>
        </div>

        <!-- Pagination -->
        <div class="flex items-center justify-between pt-4 border-t border-slate-800 text-xs font-semibold">
            <button id="prevBtn" onclick="changePage(-1)" class="bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-xl border border-slate-700 disabled:opacity-40">
                ← Previous
            </button>
            <span id="pageIndicator" class="text-slate-400">Page 1</span>
            <button id="nextBtn" onclick="changePage(1)" class="bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-xl border border-slate-700 disabled:opacity-40">
                Next →
            </button>
        </div>
    </main>

    <script>
        let currentOffset = 0;
        const limit = 20;
        let totalMCQs = 0;
        let isExamMode = false;
        let examTimer = null;
        let examTimeLeft = 45 * 60;
        let userAnswers = {};
        let activeMCQsData = [];

        async function fetchStats() {
            try {
                const res = await fetch('/api/stats');
                const data = await res.json();
                totalMCQs = data.total_mcqs;
                document.getElementById('statsBadge').innerHTML = `
                    <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                    <span>Total Question Bank: <b>${totalMCQs} MCQs</b> (${data.db_file})</span>
                `;
            } catch(e) { console.error(e); }
        }

        async function loadMCQs(offset = 0) {
            currentOffset = offset;
            const search = document.getElementById('searchInput').value;
            const container = document.getElementById('mcqContainer');
            container.innerHTML = '<div class="text-center py-12 text-slate-500 font-semibold">Loading MCQs...</div>';

            try {
                const res = await fetch(`/api/mcqs?limit=${limit}&offset=${offset}&search=${encodeURIComponent(search)}`);
                const data = await res.json();
                activeMCQsData = data.mcqs;
                renderMCQs(data.mcqs);
                updatePagination(data.total);
            } catch (e) {
                container.innerHTML = '<div class="text-rose-400 text-center py-8">Failed to load MCQs from database.</div>';
            }
        }

        function renderMCQs(mcqs) {
            const container = document.getElementById('mcqContainer');
            if (!mcqs || mcqs.length === 0) {
                container.innerHTML = '<div class="text-center py-12 text-slate-400">No MCQs found matching your query.</div>';
                return;
            }

            container.innerHTML = mcqs.map((q, idx) => {
                const qNum = currentOffset + idx + 1;
                const opts = q.options;

                return `
                <div class="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl transition-all" id="mcq-card-${q.id}">
                    <div class="flex items-start justify-between gap-4 mb-4">
                        <span class="bg-blue-500/10 border border-blue-500/30 text-blue-400 font-extrabold text-xs px-3 py-1 rounded-lg">
                            Q${qNum}
                        </span>
                        <span class="text-xs font-mono text-slate-500">ID: #${q.id}</span>
                    </div>

                    <h2 class="text-base font-bold text-slate-100 mb-5 leading-relaxed">${escapeHtml(q.question)}</h2>

                    <div class="grid grid-cols-1 gap-2.5 mb-5">
                        ${Object.keys(opts).map(key => {
                            const val = opts[key];
                            if (!val || val === 'None' || val.endsWith('None')) return '';
                            return `
                            <button onclick="selectOption(${q.id}, '${key}', '${q.correct_answer}')" 
                                id="opt-${q.id}-${key}"
                                class="w-full text-left px-4 py-3 rounded-xl border border-slate-800 bg-slate-950/60 hover:bg-slate-800 text-slate-300 text-sm font-semibold transition-all flex items-center justify-between group">
                                <div class="flex items-center gap-3">
                                    <span class="w-6 h-6 rounded-lg bg-slate-800 text-slate-400 font-bold text-xs flex items-center justify-center group-hover:bg-blue-600 group-hover:text-white transition-colors">
                                        ${key}
                                    </span>
                                    <span>${escapeHtml(val)}</span>
                                </div>
                                <span class="indicator text-xs font-bold hidden"></span>
                            </button>
                            `;
                        }).join('')}
                    </div>

                    <!-- Explanation Dropdown -->
                    <div id="exp-${q.id}" class="hidden mt-4 p-4 bg-slate-950 border border-indigo-500/20 rounded-xl text-xs text-slate-300 space-y-1">
                        <div class="font-extrabold text-indigo-400 flex items-center gap-1.5 mb-1">
                            💡 High-Yield Explanation:
                        </div>
                        <p class="leading-relaxed italic">${escapeHtml(q.explanation || 'No explanation provided.')}</p>
                    </div>
                </div>
                `;
            }).join('');
        }

        function selectOption(qId, key, correctKey) {
            userAnswers[qId] = key;

            // Highlight chosen & correct answers
            ['A', 'B', 'C', 'D', 'E'].forEach(k => {
                const btn = document.getElementById(`opt-${qId}-${k}`);
                if (!btn) return;
                btn.className = 'w-full text-left px-4 py-3 rounded-xl border border-slate-800 bg-slate-950/60 text-slate-400 text-sm font-semibold opacity-50 cursor-not-allowed flex items-center justify-between';

                if (k === correctKey) {
                    btn.className = 'w-full text-left px-4 py-3 rounded-xl border border-emerald-500/50 bg-emerald-500/10 text-emerald-300 text-sm font-bold flex items-center justify-between shadow-md shadow-emerald-500/10';
                }
                if (k === key && key !== correctKey) {
                    btn.className = 'w-full text-left px-4 py-3 rounded-xl border border-rose-500/50 bg-rose-500/10 text-rose-300 text-sm font-bold flex items-center justify-between';
                }
            });

            // Show explanation
            const expEl = document.getElementById(`exp-${qId}`);
            if (expEl) expEl.classList.remove('hidden');

            if (isExamMode) {
                const answered = Object.keys(userAnswers).length;
                document.getElementById('examProgress').innerText = `Answered: ${answered} / 50`;
            }
        }

        let searchTimeout;
        function handleSearch() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => loadMCQs(0), 300);
        }

        function updatePagination(total) {
            const page = Math.floor(currentOffset / limit) + 1;
            const maxPage = Math.ceil(total / limit) || 1;
            document.getElementById('pageIndicator').innerText = `Page ${page} of ${maxPage} (${total} items)`;
            document.getElementById('prevBtn').disabled = currentOffset === 0;
            document.getElementById('nextBtn').disabled = (currentOffset + limit) >= total;
        }

        function changePage(dir) {
            const newOffset = currentOffset + (dir * limit);
            if (newOffset >= 0) loadMCQs(newOffset);
        }

        function startExamMode() {
            isExamMode = true;
            userAnswers = {};
            document.getElementById('examBanner').classList.remove('hidden');
            loadMCQs(0);

            examTimeLeft = 45 * 60;
            clearInterval(examTimer);
            examTimer = setInterval(() => {
                examTimeLeft--;
                const mins = Math.floor(examTimeLeft / 60);
                const secs = examTimeLeft % 60;
                document.getElementById('timerDisplay').innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
                if (examTimeLeft <= 0) {
                    clearInterval(examTimer);
                    finishExam();
                }
            }, 1000);
        }

        function finishExam() {
            clearInterval(examTimer);
            let score = 0;
            activeMCQsData.forEach(q => {
                if (userAnswers[q.id] === q.correct_answer) score++;
            });
            alert(`Exam Submitted!\\nYour Score: ${score} / ${activeMCQsData.length} (${Math.round((score/activeMCQsData.length)*100)}%)`);
        }

        function escapeHtml(text) {
            if (!text) return '';
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        }

        fetchStats();
        loadMCQs(0);
    </script>
</body>
</html>
"""

def run_server(port=5500):
    server = HTTPServer(('127.0.0.1', port), MCQRequestHandler)
    print(f"==========================================")
    print(f" MBBS & FCPS MCQ Quiz Software Running!")
    print(f" Server URL: http://127.0.0.1:{port}")
    print(f"==========================================")
    
    # Open browser or pywebview GUI
    try:
        import webview
        threading.Thread(target=server.serve_forever, daemon=True).start()
        webview.create_window("MBBS & FCPS High-Yield MCQ Quiz Master", f'http://127.0.0.1:{port}', width=1280, height=850)
        webview.start()
    except ImportError:
        threading.Thread(target=server.serve_forever, daemon=True).start()
        webbrowser.open(f'http://127.0.0.1:{port}')
        # Keep main thread alive
        try:
            while True:
                threading.Event().wait(3600)
        except KeyboardInterrupt:
            print("Server shutting down...")

if __name__ == '__main__':
    run_server(5500)
