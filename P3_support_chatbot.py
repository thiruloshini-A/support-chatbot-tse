"""
ZohoSupport Bot — Rule-Based L1 Technical Support Chatbot
==========================================================
A rule-based chatbot that handles common technical support queries.
Simulates L1 support workflows with escalation logic.

Author: Thiruloshini Arasalingam
GitHub: github.com/thiruloshini-A
"""

import tkinter as tk
from tkinter import scrolledtext
import threading
import time

# ── Knowledge Base ────────────────────────────────────────────
KB = [
    {
        "keywords": ["password", "reset", "forgot", "change password"],
        "tag": "Account",
        "response": """Password Reset Steps:
  1. Go to login page → click 'Forgot Password'
  2. Enter your registered email address
  3. Check inbox for reset link (valid 15 mins)
  4. Create new password (min 8 chars + number)

  Still not received? Check Spam/Junk folder
  or contact support@zoho.com"""
    },
    {
        "keywords": ["login", "can't login", "unable to login", "sign in", "access denied"],
        "tag": "Login",
        "response": """Login Troubleshooting:
  1. Clear browser cache & cookies (Ctrl+Shift+Del)
  2. Try a different browser (Chrome recommended)
  3. Disable VPN or proxy temporarily
  4. Check if Caps Lock is ON
  5. Account locked after 3 failed attempts (30 min lock)

  Tip: Try Incognito mode first."""
    },
    {
        "keywords": ["slow", "lagging", "performance", "loading slow", "freeze"],
        "tag": "Performance",
        "response": """Performance Issue — Quick Fixes:
  1. Check internet speed (min 5 Mbps recommended)
  2. Close unused browser tabs
  3. Clear browser cache (Ctrl+Shift+Del → All time)
  4. Disable browser extensions temporarily
  5. Try mobile hotspot to isolate network issue

  Still slow? Check status.zoho.com for incidents."""
    },
    {
        "keywords": ["email", "mail", "not receiving", "not sending", "inbox", "smtp"],
        "tag": "Email",
        "response": """Email Issue Checklist:
  1. Check Spam/Junk folder first
  2. SMTP settings: smtp.zoho.com, Port 587 (TLS)
  3. Check email quota (Settings → Storage)
  4. Check forwarding rules
  5. Test sending to a different email address"""
    },
    {
        "keywords": ["billing", "invoice", "payment", "charge", "subscription", "plan", "upgrade"],
        "tag": "Billing",
        "response": """Billing & Subscription Help:
  1. View invoices: Account Settings → Billing → Invoices
  2. Update payment: Billing → Payment Method
  3. Upgrade plan: Subscription → Change Plan
  4. Refund processed in 5-7 business days

  For disputes: billing@zoho.com (with invoice number)"""
    },
    {
        "keywords": ["api", "integration", "webhook", "connect", "rest", "token"],
        "tag": "API",
        "response": """API / Integration Support:
  1. Get API key: Settings → API → Generate Token
  2. Base URL: https://www.zohoapis.com/crm/v2/
  3. Rate limit: 200 API calls/minute per org
  4. 401 error = token expired, regenerate token
  5. Test with Postman before integrating

  Full docs: www.zoho.com/crm/developer/docs/"""
    },
    {
        "keywords": ["error", "500", "404", "bug", "crash", "not working", "broken"],
        "tag": "Error",
        "response": """Error Troubleshooting Steps:
  1. Note the exact error code and screenshot it
  2. Refresh the page (Ctrl+F5 for hard refresh)
  3. Try in a different browser / device
  4. Check status.zoho.com for ongoing incidents
  5. 500 error = server-side, usually fixed in < 1 hour

  Report bugs with steps → support.zoho.com"""
    },
    {
        "keywords": ["hi", "hello", "hey", "hii", "help", "start", "support"],
        "tag": "Greeting",
        "response": """Hello! I'm ZohoSupport Bot — your L1 Support Assistant.

  I can help you with:
  • Login & Password issues
  • Email problems
  • Billing & Subscriptions
  • API & Integrations
  • Performance issues
  • Error troubleshooting

  Type your issue below!"""
    },
]

QUICK_TOPICS = [
    "Password Reset", "Login Issue", "Slow Performance",
    "Email Problem", "Billing", "API Error"
]

# ── Chatbot logic ─────────────────────────────────────────────
def get_response(user_input):
    lower = user_input.lower()
    for entry in KB:
        if any(k in lower for k in entry["keywords"]):
            return f"[{entry['tag']}]\n\n{entry['response']}"
    return f"""Sorry, I couldn't find an answer for: "{user_input}"

  Please try:
  • Rephrasing your question
  • Visiting support.zoho.com
  • Calling +1-888-900-9646 (24/7)
  • Email support@zoho.com with your account ID

  [Ticket Raised] Your query has been logged for L2 review."""

# ── GUI ───────────────────────────────────────────────────────
class SupportChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("ZohoSupport Bot — L1 Technical Support")
        self.root.geometry("700x600")
        self.root.configure(bg="#0f0f1a")
        self.root.resizable(True, True)

        # Header
        header = tk.Frame(root, bg="#1a1a2e", pady=12)
        header.pack(fill="x", padx=10, pady=(10, 0))

        tk.Label(header, text="🤖 ZohoSupport Bot",
                 font=("Helvetica", 14, "bold"),
                 fg="#e94560", bg="#1a1a2e").pack(side="left", padx=14)

        tk.Label(header, text="● Online",
                 font=("Helvetica", 10),
                 fg="#4ecdc4", bg="#1a1a2e").pack(side="right", padx=14)

        tk.Label(header, text="L1 Technical Support Assistant",
                 font=("Helvetica", 9),
                 fg="#888888", bg="#1a1a2e").pack(side="left")

        # Quick topic buttons
        topics_frame = tk.Frame(root, bg="#0f0f1a", pady=6)
        topics_frame.pack(fill="x", padx=10)

        tk.Label(topics_frame, text="Quick Topics:",
                 font=("Helvetica", 9), fg="#888", bg="#0f0f1a").pack(side="left", padx=(4, 8))

        for topic in QUICK_TOPICS:
            btn = tk.Button(topics_frame, text=topic,
                            font=("Helvetica", 8),
                            fg="#e0e0e0", bg="#1a1a2e",
                            activebackground="#e94560",
                            activeforeground="white",
                            relief="flat", bd=0,
                            padx=8, pady=3, cursor="hand2",
                            command=lambda t=topic: self.quick_send(t))
            btn.pack(side="left", padx=3)

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            root, wrap=tk.WORD,
            font=("Courier", 10),
            bg="#1a1a2e", fg="#e0e0e0",
            insertbackground="#e0e0e0",
            relief="flat", padx=12, pady=12,
            state="disabled"
        )
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=6)

        # Tag styles
        self.chat_display.tag_config("bot_name",  foreground="#e94560", font=("Courier", 10, "bold"))
        self.chat_display.tag_config("user_name", foreground="#4ecdc4", font=("Courier", 10, "bold"))
        self.chat_display.tag_config("bot_text",  foreground="#e0e0e0")
        self.chat_display.tag_config("user_text", foreground="#f7b731")
        self.chat_display.tag_config("divider",   foreground="#333355")

        # Input area
        input_frame = tk.Frame(root, bg="#0f0f1a", pady=8)
        input_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.input_box = tk.Entry(
            input_frame,
            font=("Helvetica", 11),
            bg="#1a1a2e", fg="#e0e0e0",
            insertbackground="#e0e0e0",
            relief="flat", bd=0
        )
        self.input_box.pack(side="left", fill="x", expand=True,
                            ipady=10, padx=(10, 8))
        self.input_box.bind("<Return>", lambda e: self.send_message())

        send_btn = tk.Button(
            input_frame, text="Send ➤",
            font=("Helvetica", 10, "bold"),
            bg="#e94560", fg="white",
            activebackground="#c0392b",
            relief="flat", bd=0,
            padx=16, pady=8, cursor="hand2",
            command=self.send_message
        )
        send_btn.pack(side="right", padx=(0, 4))

        # Footer
        tk.Label(root,
                 text="Built by Thiruloshini Arasalingam | TSE Portfolio Project | github.com/thiruloshini-A",
                 font=("Helvetica", 8), fg="#444466", bg="#0f0f1a").pack(pady=(0, 6))

        # Welcome message
        self.root.after(400, self.welcome)

    def append_message(self, sender, text, name_tag, text_tag):
        self.chat_display.config(state="normal")
        self.chat_display.insert("end", f"\n{sender}\n", name_tag)
        self.chat_display.insert("end", f"{text}\n", text_tag)
        self.chat_display.insert("end", "─" * 60 + "\n", "divider")
        self.chat_display.config(state="disabled")
        self.chat_display.see("end")

    def welcome(self):
        self.append_message(
            "🤖 ZohoSupport Bot",
            "Hello! Type your issue or click a quick topic above.\nI can help with Login, Password, Billing, API, Email & more!",
            "bot_name", "bot_text"
        )

    def typing_then_reply(self, user_text):
        self.chat_display.config(state="normal")
        self.chat_display.insert("end", "\n🤖 ZohoSupport Bot\n", "bot_name")
        self.chat_display.insert("end", "Analyzing your issue...\n", "bot_text")
        self.chat_display.config(state="disabled")
        self.chat_display.see("end")
        time.sleep(0.8)

        # Remove "Analyzing..." and add real response
        self.chat_display.config(state="normal")
        self.chat_display.delete("end-3l", "end-1l")
        response = get_response(user_text)
        self.chat_display.insert("end", f"{response}\n", "bot_text")
        self.chat_display.insert("end", "─" * 60 + "\n", "divider")
        self.chat_display.config(state="disabled")
        self.chat_display.see("end")

    def send_message(self):
        text = self.input_box.get().strip()
        if not text:
            return
        self.input_box.delete(0, "end")
        self.append_message("🧑 You", text, "user_name", "user_text")
        threading.Thread(target=self.typing_then_reply, args=(text,), daemon=True).start()

    def quick_send(self, topic):
        self.input_box.delete(0, "end")
        self.input_box.insert(0, topic)
        self.send_message()

# ── Main ──────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = SupportChatbot(root)
    root.mainloop()
