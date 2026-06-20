import asyncio
import io
import re
import traceback
from contextlib import redirect_stdout, redirect_stderr

from flask import Flask, request, jsonify

import user_script

app = Flask(__name__)

# Strips terminal color codes (e.g. from colorama) so they don't show
# up as garbage like "[32m" in the browser.
ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*m")

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Python Runner</title>
<style>
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  body {
    margin: 0; min-height: 100vh; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
    background: radial-gradient(1200px 800px at 20% -10%, #1e293b, #0b0f17 60%); color: #e5e7eb;
    display: flex; align-items: center; justify-content: center; padding: 24px;
  }
  .card {
    width: 100%; max-width: 760px; background: rgba(17,24,39,.8); backdrop-filter: blur(8px);
    border: 1px solid rgba(148,163,184,.15); border-radius: 16px; padding: 28px;
    box-shadow: 0 20px 60px rgba(0,0,0,.45);
  }
  h1 { margin: 0 0 6px; font-size: 22px; }
  p.sub { margin: 0 0 20px; color: #94a3b8; font-size: 14px; }
  label { display: block; font-size: 13px; color: #cbd5e1; margin: 0 0 6px; }
  input[type=text] {
    width: 100%; padding: 12px 14px; border-radius: 10px; border: 1px solid rgba(148,163,184,.25);
    background: #0b0f17; color: #e5e7eb; font-size: 14px; margin-bottom: 16px;
  }
  button {
    appearance: none; border: 0; border-radius: 10px; padding: 12px 20px; font-size: 14px; font-weight: 600;
    background: linear-gradient(180deg, #3b82f6, #2563eb); color: white; cursor: pointer;
  }
  button:disabled { opacity: .6; cursor: default; }
  pre {
    margin: 20px 0 0; padding: 16px; background: #0b0f17; border: 1px solid rgba(148,163,184,.15);
    border-radius: 10px; white-space: pre-wrap; word-break: break-word; font-size: 13px;
    line-height: 1.5; min-height: 80px; color: #d1d5db; font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  }
  .ok { color: #34d399; } .err { color: #f87171; }
  .row { display: flex; align-items: center; gap: 12px; }
  .spinner { width:16px;height:16px;border:2px solid rgba(255,255,255,.3);border-top-color:#fff;border-radius:50%;display:none;animation:spin .7s linear infinite;}
  @keyframes spin { to { transform: rotate(360deg);} }
</style>
</head>
<body>
  <div class="card">
    <h1>Python Runner</h1>
    <p class="sub">Runs <code>main()</code> from <code>api/user_script.py</code> on Vercel and shows the output below.</p>
    <label for="inp">Input (optional, passed to your script)</label>
    <input id="inp" type="text" placeholder="Type something for your script...">
    <div class="row">
      <button id="run">Run script</button>
      <div id="spin" class="spinner"></div>
    </div>
    <pre id="out">Output will appear here.</pre>
  </div>
<script>
  const btn = document.getElementById('run');
  const out = document.getElementById('out');
  const spin = document.getElementById('spin');
  const inp = document.getElementById('inp');
  btn.addEventListener('click', async () => {
    btn.disabled = true; spin.style.display = 'block';
    out.className = ''; out.textContent = 'Running...';
    try {
      const res = await fetch('/run', {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify({ input: inp.value })
      });
      const data = await res.json();
      out.textContent = data.output || '(no output)';
      out.className = data.ok ? 'ok' : 'err';
    } catch (e) {
      out.textContent = 'Request failed: ' + e; out.className = 'err';
    } finally {
      btn.disabled = false; spin.style.display = 'none';
    }
  });
</script>
</body>
</html>
"""


def _run_user_main(user_input):
    """Calls user_script.main(), supporting both sync and async definitions.
    Captures stdout/stderr and returns the text."""
    buffer = io.StringIO()
    with redirect_stdout(buffer), redirect_stderr(buffer):
        result = user_script.main(user_input)
        if asyncio.iscoroutine(result):
            result = asyncio.run(result)
        if result is not None:
            print(result)
    return buffer.getvalue()


@app.route("/")
def home():
    return PAGE


@app.route("/run", methods=["POST"])
def run():
    payload = request.get_json(silent=True) or {}
    user_input = payload.get("input", "")
    try:
        raw = _run_user_main(user_input)
        clean = ANSI_ESCAPE.sub("", raw)
        return jsonify(ok=True, output=clean or "(script produced no output)")
    except Exception:
        err = ANSI_ESCAPE.sub("", traceback.format_exc())
        return jsonify(ok=False, output=err)


if __name__ == "__main__":
    app.run(debug=True, port=3000)
