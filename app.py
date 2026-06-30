import os
import threading
import warnings
from pathlib import Path

import gradio as gr

from cache_utils import setup_cache
from pipeline import VisionGuardPipeline

setup_cache()
warnings.filterwarnings("ignore", category=DeprecationWarning, module="gradio.*")
warnings.filterwarnings("ignore", category=UserWarning, message="The parameters have been moved from the Blocks constructor to the launch\\(\\) method in Gradio 6\\.0: theme, css.*")
warnings.filterwarnings("ignore", message="The 'theme' parameter in the Blocks constructor will be removed in Gradio 6\\.0.*")
warnings.filterwarnings("ignore", message="The 'css' parameter in the Blocks constructor will be removed in Gradio 6\\.0.*")

ROOT = Path(__file__).resolve().parent
pipe = VisionGuardPipeline()
threading.Thread(target=pipe.warmup_models, daemon=True).start()

theme = gr.themes.Base(
    primary_hue=gr.themes.colors.blue,
    secondary_hue=gr.themes.colors.blue,
    neutral_hue=gr.themes.colors.slate,
    font=(gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"),
    font_mono=(gr.themes.GoogleFont("JetBrains Mono"), "ui-monospace", "Menlo", "monospace"),
).set(
    body_background_fill="#0a0d12",
    background_fill_primary="#11151c",
    background_fill_secondary="#0a0d12",
    border_color_primary="#1f2733",
    block_background_fill="#11151c",
    block_border_color="#1f2733",
    block_label_text_color="#aeb8c4",
    block_title_text_color="#4d9bd9",
    body_text_color="#f3f5f7",
    body_text_color_subdued="#aeb8c4",
    input_background_fill="#0d1117",
    input_border_color="#1f2733",
    button_primary_background_fill="#2b7fc7",
    button_primary_background_fill_hover="#4d9bd9",
    button_primary_text_color="#06080c",
    button_secondary_background_fill="#0d1117",
    button_secondary_border_color="#1f2733",
    button_secondary_text_color="#f3f5f7",
)

css = """
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap');

:root{
  --vg-bg:#0a0d12;
  --vg-panel:#11151c;
  --vg-panel-2:#0d1117;
  --vg-blue:#2b7fc7;
  --vg-blue-bright:#4d9bd9;
  --vg-blue-soft:#1d4f73;
  --vg-line:#1f2733;
  --vg-line-soft:#171d27;
  --vg-ink:#f3f5f7;
  --vg-ink-dim:#aeb8c4;
  --vg-mono:'JetBrains Mono',ui-monospace,monospace;
  --vg-sans:'Inter',ui-sans-serif,system-ui,sans-serif;
  --vg-radius:14px;
  --vg-radius-sm:9px;
  --vg-glow-btn:0 0 0 1px rgba(43,127,199,0.55), 0 4px 18px -2px rgba(43,127,199,0.45);
  --vg-glow-btn-hover:0 0 0 1px rgba(77,155,217,0.75), 0 6px 26px -2px rgba(77,155,217,0.6);
}

.gradio-container{max-width:860px!important;margin:0 auto!important;background:var(--vg-bg)!important}
.gradio-container,.gradio-container *{box-sizing:border-box}
body, .gradio-container{font-family:var(--vg-sans);color:var(--vg-ink)}
body{
  display:flex;justify-content:center;
  background:
    radial-gradient(ellipse 900px 420px at 50% -10%, rgba(43,127,199,0.16), transparent 60%),
    var(--vg-bg);
}

/* ---------- hero ---------- */
.hero{
  position:relative;
  padding:34px 32px 30px;
  border-radius:var(--vg-radius);
  background:linear-gradient(180deg, rgba(17,21,28,0.9), rgba(13,17,23,0.85));
  border:1px solid var(--vg-line);
  margin-bottom:20px;
  overflow:hidden;
}
.hero::after{
  content:"";
  position:absolute;top:-40%;left:50%;transform:translateX(-50%);
  width:480px;height:200px;border-radius:50%;
  background:radial-gradient(circle, rgba(43,127,199,0.30), transparent 70%);
  filter:blur(40px);
  pointer-events:none;
}
.hero .vg-eyebrow{
  position:relative;z-index:1;
  font-family:var(--vg-mono);
  font-size:11px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--vg-ink-dim);margin:0 0 14px 0;
  display:flex;align-items:center;gap:8px;
}
.hero .vg-eyebrow .vg-dot{
  width:7px;height:7px;border-radius:50%;
  background:var(--vg-blue-bright);
  box-shadow:0 0 6px 1px rgba(77,155,217,0.8);
  animation:vg-blink 2s ease-in-out infinite;
}
@keyframes vg-blink{50%{opacity:.35}}
.hero h1{
  position:relative;z-index:1;
  margin:0 0 10px 0;font-size:34px;font-weight:800;letter-spacing:-0.02em;
  color:var(--vg-ink);
  line-height:1.15;
}
.hero h1 .vg-accent{color:var(--vg-blue-bright)}
.hero p.vg-sub{
  position:relative;z-index:1;margin:0;font-size:15px;color:var(--vg-ink-dim);
  max-width:560px;line-height:1.6;font-weight:400;
}

/* stepper, refined as a clean numbered row instead of loud pills */
.hero-steps{
  position:relative;z-index:1;
  display:flex;flex-wrap:wrap;align-items:center;gap:0;
  margin-top:22px;
  border-top:1px solid var(--vg-line);
  padding-top:18px;
}
.hero-steps .vg-step{
  display:flex;align-items:center;gap:9px;
  font-family:var(--vg-mono);font-size:12px;letter-spacing:.01em;
  color:var(--vg-ink-dim);
  padding:4px 16px 4px 0;
}
.hero-steps .vg-step b{
  display:inline-flex;align-items:center;justify-content:center;
  flex:none;width:20px;height:20px;border-radius:50%;
  background:rgba(43,127,199,0.15);color:var(--vg-blue-bright);
  font-size:11px;font-weight:700;border:1px solid rgba(43,127,199,0.4);
}
.hero-steps .vg-arrow{
  color:var(--vg-line);font-size:13px;margin-right:6px;
}

/* ---------- single-column layout ---------- */
.app-shell{gap:20px;display:flex;flex-direction:column}
.panel{
  border:1px solid var(--vg-line);
  border-radius:var(--vg-radius);
  background:var(--vg-panel);
  padding:24px;
  position:relative;
  box-shadow:0 1px 0 rgba(255,255,255,0.02) inset, 0 16px 40px -16px rgba(0,0,0,0.6);
}

.tight-md{margin-top:10px}
.tight-md p{margin:0;color:var(--vg-ink-dim);font-family:var(--vg-mono);font-size:12.5px;line-height:1.6}
.result-stack{gap:18px}
.export-files{gap:12px}
.hidden-empty{min-height:0!important}

/* sub-section headers: quiet label + rule, not a loud HUD badge */
.vg-section{
  display:flex;align-items:center;gap:10px;
  font-family:var(--vg-mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--vg-ink-dim);margin:0 0 16px 0;
}
.vg-section .vg-badge{
  display:inline-flex;align-items:center;justify-content:center;
  width:20px;height:20px;border-radius:6px;flex:none;
  background:rgba(43,127,199,0.14);color:var(--vg-blue-bright);
  font-size:11px;font-weight:700;border:1px solid rgba(43,127,199,0.35);
}
.vg-section .vg-label{color:var(--vg-ink);font-weight:600;letter-spacing:.06em}
.vg-section::after{
  content:"";flex:1;height:1px;background:var(--vg-line);
}
.vg-divider{
  height:1px;background:var(--vg-line);
  margin:24px 0 18px 0;border:none;
}

/* ---------- media elements ---------- */
.gradio-container .gr-video, .gradio-container video,
.gradio-container .image-frame, .gradio-container .gallery,
.gradio-container [data-testid="image"]{
  border-radius:var(--vg-radius-sm)!important;
}

label span, .label-wrap span{
  font-family:var(--vg-mono)!important;
  text-transform:uppercase;letter-spacing:.07em;font-size:11px!important;
  color:var(--vg-ink-dim)!important;font-weight:500!important;
}

.result-stack h2{
  font-family:var(--vg-mono);
  color:var(--vg-ink);
  font-size:13px;letter-spacing:.04em;text-transform:uppercase;
  border-bottom:1px solid var(--vg-line);
  padding-bottom:8px;margin-bottom:10px;
}
.result-stack code{
  background:rgba(43,127,199,0.12);color:var(--vg-blue-bright);
  border:1px solid rgba(43,127,199,0.25);padding:1px 6px;border-radius:4px;
  font-size:0.92em;
}

/* ---------- buttons ---------- */
.gradio-container button.primary{
  font-family:var(--vg-sans);font-weight:600;
  letter-spacing:.01em;text-transform:none;font-size:14px;
  background:linear-gradient(180deg, var(--vg-blue-bright), var(--vg-blue))!important;
  border:none!important;color:#06080c!important;
  box-shadow:var(--vg-glow-btn);
  transition:box-shadow .2s ease, transform .15s ease, filter .15s ease;
}
.gradio-container button.primary:hover{
  box-shadow:var(--vg-glow-btn-hover);
  transform:translateY(-1px);
  filter:brightness(1.05);
}
.gradio-container button.primary:active{transform:translateY(0)}
.gradio-container button.primary:disabled{
  background:var(--vg-panel-2)!important;color:var(--vg-ink-dim)!important;
  box-shadow:none;filter:none;cursor:not-allowed;opacity:.55;
}
.gradio-container button.secondary{
  font-family:var(--vg-sans);font-weight:500;
  letter-spacing:.01em;text-transform:none;font-size:13.5px;
  background:var(--vg-panel-2)!important;
  border:1px solid var(--vg-line)!important;color:var(--vg-ink)!important;
  transition:border-color .2s ease, box-shadow .2s ease;
}
.gradio-container button.secondary:hover{
  border-color:rgba(43,127,199,0.5)!important;
  box-shadow:0 0 0 1px rgba(43,127,199,0.25);
}

/* inputs */
.gradio-container textarea, .gradio-container input[type="text"]{
  font-family:var(--vg-sans)!important;font-size:14px!important;
}
.gradio-container textarea:focus, .gradio-container input[type="text"]:focus{
  box-shadow:0 0 0 2px rgba(43,127,199,0.3)!important;
  border-color:var(--vg-blue)!important;
}

/* dataframe / table */
.gradio-container table{font-family:var(--vg-mono);font-size:12.5px;color:var(--vg-ink)}
.gradio-container thead th{
  color:var(--vg-ink-dim)!important;text-transform:uppercase;letter-spacing:.05em;
  font-size:11px!important;font-weight:600!important;
}

/* status line */
#vg-status-wrap p{
  font-family:var(--vg-mono);font-size:12px;
  color:var(--vg-ink-dim);
  display:flex;align-items:center;gap:7px;
}
"""


def _in_colab():
    return bool(
        os.getenv("COLAB_RELEASE_TAG")
        or os.getenv("COLAB_BACKEND_VERSION")
        or os.getenv("COLAB_GPU")
        or (os.getenv("JPY_PARENT_PID") and str(ROOT).startswith("/content/"))
    )


def _server_name():
    override = os.getenv("VISION_GUARD_HOST", "").strip()
    if override:
        return override
    if _in_colab() or os.getenv("KAGGLE_KERNEL_RUN_TYPE"):
        return "0.0.0.0"
    return "127.0.0.1"


def _share_enabled():
    raw = os.getenv("GRADIO_SHARE", "").strip().lower()
    if raw in {"1", "true", "yes", "on"}:
        return True
    if raw in {"0", "false", "no", "off"}:
        return False
    return False


def _sample_videos():
    assets = ROOT / "assets"
    if not assets.exists():
        return []
    return [str(p) for p in sorted(assets.glob("*.mp4"))]


def _meta(meta):
    out = (
        f"video: `{os.path.basename(meta['video'])}`\n\n"
        f"- duration: `{meta['duration']:.2f}s`\n"
        f"- fps: `{meta['fps']:.2f}`\n"
        f"- sampled every: `{meta['sample_sec']:.2f}s`\n"
        f"- indexed windows: `{meta['segments']}`\n"
        f"- retriever: `{meta.get('retriever', 'numpy')}`\n"
        f"- verifier: `{meta.get('verifier', 'none')}`"
    )
    counts = meta.get("object_counts", {})
    if counts:
        lines = [f"**{name}**: {n}" for name, n in counts.items()]
        obj_md = "  ".join(lines)
        out += "\n\n**Objects detected:**\n" + obj_md
    return out


def _ans(q, rows):
    out = [f"## answer for `{q}`", ""]
    if not rows:
        out.append("no strong matches found")
        return "\n".join(out)
    for i, x in enumerate(rows, 1):
        out.append(f"{i}. `best frame {x.get('peak_ts', x['start']):.2f}s | clip {x['start']:.2f}s - {x['end']:.2f}s`")
        prefix = "low confidence: " if x.get("low_confidence") else ""
        out.append(f"   {prefix}{x['summary']}")
    return "\n".join(out)


def _gallery(rows):
    out = []
    for i, x in enumerate(rows):
        frame_path = x.get("gallery_frame") if i == 0 else x.get("representative_frame_path")
        frame_path = frame_path or x.get("frame_path")
        if not frame_path:
            continue
        prefix = "low confidence | " if x.get("low_confidence") else ""
        caption = f"{x['query']} | {x.get('peak_ts', x['start']):.2f}s | {prefix}{x['summary']}" if i == 0 else f"{x['label']} | {prefix}{x['summary']}"
        out.append((frame_path, caption))
    return out


def scan_only(video):
    if not video:
        yield "upload a video first", None, "", gr.update(interactive=False), "", []
        return
    yield "starting scan", None, "", gr.update(interactive=False), "", []
    meta = None
    for ev in pipe.index_video_iter(video):
        if ev["kind"] == "preview":
            yield ev["status"], ev["image"], "", gr.update(interactive=False), "", []
        else:
            meta = ev["meta"]
    yield "scan complete", None, _meta(meta), gr.update(interactive=True), "", []


def _find_payload(status, q, seg):
    rows = [[round(x.get("peak_ts", x["start"]), 2), f"{x['start']:.2f}s - {x['end']:.2f}s", ", ".join(x["objects"]), x["summary"]] for x in seg]
    ans = _ans(q.strip(), seg)
    choices = [x["label"] for x in seg]
    gal = _gallery(seg)
    if not seg:
        note = "### matched frames\n\nNo strong frame matches were found for this query."
    elif any(x.get("low_confidence") for x in seg):
        note = "### matched frames\n\nThe gallery below shows the nearest available sampled frames. These results are low confidence, so review them carefully before export."
    else:
        note = "### matched frames\n\nThe gallery below shows the top sampled frames for your query. Select any rows you want to export as clips and reports."
    return status, ans, f"Searched for: {', '.join(pipe._query_variants(q.strip()))}", rows, gr.update(choices=choices, value=choices[:1]), gal, note, q.strip(), seg, gr.update(visible=False, value=None), gr.update(visible=False, value=None), gr.update(visible=False, value=None)


def find_query(q):
    blank_pick = gr.update(choices=[], value=[])
    if not pipe.idx:
        yield "scan a video first", "", "", [], blank_pick, [], "", "", [], gr.update(visible=False, value=None), gr.update(visible=False, value=None), gr.update(visible=False, value=None)
        return
    if not q or not q.strip():
        yield "enter a natural-language query", "", "", [], blank_pick, [], "", "", [], gr.update(visible=False, value=None), gr.update(visible=False, value=None), gr.update(visible=False, value=None)
        return
    yield "searching...", "", "", [], blank_pick, [], "", q.strip(), [], gr.update(visible=False, value=None), gr.update(visible=False, value=None), gr.update(visible=False, value=None)
    yielded = False
    for hits in pipe.search_stream(q.strip(), top_k=4):
        seg = pipe.prepare_hits(hits, q.strip())
        status = "matches ready" if seg else "search complete"
        yield _find_payload(status, q.strip(), seg)
        yielded = True
    if not yielded:
        seg = pipe.prepare_hits(pipe.search(q.strip(), top_k=4), q.strip())
        yield _find_payload("matches ready" if seg else "search complete", q.strip(), seg)


def export_selected(picks, q, hits):
    if not hits or not picks:
        return gr.update(visible=False, value=None), gr.update(visible=False, value=None), gr.update(visible=False, value=None)
    pipe.last_hits = hits
    zipf, html, csv = pipe.export_selected(picks, q)
    return gr.update(visible=True, value=zipf), gr.update(visible=True, value=html), gr.update(visible=True, value=csv)


def get_system_status():
    return pipe.warmup_status()


with gr.Blocks(title="Vision Guard", css=css, theme=theme) as demo:
    gr.HTML(
        """
<div class="hero">
  <p class="vg-eyebrow"><span class="vg-dot"></span>VIDEO INTELLIGENCE</p>
  <h1>Vision <span class="vg-accent">Guard</span></h1>
  <p class="vg-sub">Upload a video, index it once, then search for any object, person, or moment using plain language — and export only the clips that matter.</p>
  <div class="hero-steps">
    <div class="vg-step"><b>1</b>Scan video</div>
    <span class="vg-arrow">&rarr;</span>
    <div class="vg-step"><b>2</b>Search in plain language</div>
    <span class="vg-arrow">&rarr;</span>
    <div class="vg-step"><b>3</b>Review &amp; export clips</div>
  </div>
</div>
"""
    )
    q_state = gr.State("")
    hits_state = gr.State([])

    with gr.Column(elem_classes="app-shell"):
        with gr.Group(elem_classes="panel"):
            gr.HTML('<div class="vg-section"><span class="vg-badge">1</span><span class="vg-label">Upload &amp; Scan</span></div>')
            video = gr.Video(label="cctv video", elem_classes="hidden-empty")
            good = [x for x in _sample_videos() if os.path.exists(x)]
            if good:
                gr.Examples(good, inputs=video, label="sample videos")
            scan_btn = gr.Button("step 1: scan video", variant="primary")
            status = gr.Markdown("ready", elem_id="vg-status-wrap")

            gr.HTML('<hr class="vg-divider"/><div class="vg-section"><span class="vg-label">Indexing Detail</span></div>')
            live = gr.Image(label="live indexing preview", interactive=False, elem_classes="hidden-empty")
            info = gr.Markdown(elem_classes="tight-md")

            gr.HTML('<hr class="vg-divider"/><div class="vg-section"><span class="vg-badge">2</span><span class="vg-label">Search</span></div>')
            query = gr.Textbox(label="query", placeholder="person near gate, white car entering, blue truck, umbrella, backpack", interactive=False)
            find_btn = gr.Button("step 2: find matches", variant="primary", interactive=False)
            searched = gr.Markdown(elem_classes="tight-md")

        with gr.Group(elem_classes="panel result-stack"):
            gr.HTML('<div class="vg-section"><span class="vg-badge">3</span><span class="vg-label">Results</span></div>')
            answer = gr.Markdown(elem_classes="tight-md")
            table = gr.Dataframe(headers=["Best Frame At", "Clip Window", "Objects", "Summary"], interactive=False, wrap=True)
            gallery = gr.Gallery(label="matched frames", columns=2, height="auto")
            match_md = gr.Markdown(elem_classes="tight-md")

            gr.HTML('<hr class="vg-divider"/><div class="vg-section"><span class="vg-badge">4</span><span class="vg-label">Export</span></div>')
            pick = gr.CheckboxGroup(label="choose clips to export")
            export_btn = gr.Button("export selected", variant="primary")
            with gr.Row(elem_classes="export-files"):
                zipf = gr.File(label="zip", visible=False)
                html = gr.File(label="html report", visible=False)
                csv = gr.File(label="csv report", visible=False)

    scan_btn.click(scan_only, [video], [status, live, info, query, q_state, hits_state])
    scan_btn.click(lambda: gr.update(interactive=True), None, find_btn)
    scan_btn.click(lambda: "", None, searched)
    find_btn.click(find_query, [query], [status, answer, searched, table, pick, gallery, match_md, q_state, hits_state, zipf, html, csv])
    export_btn.click(export_selected, [pick, q_state, hits_state], [zipf, html, csv])
    demo.load(fn=get_system_status, inputs=None, outputs=status)


import gradio as gr

if __name__ == "__main__":
    # Force share=True to generate a public live link
    share = True 
    server_name = _server_name()
    
    if server_name == "127.0.0.1":
        print("Open Vision Guard at http://127.0.0.1:7860")
        
    # The share=True parameter creates a temporary public gradio.live URL
    demo.launch(server_name=server_name, share=share, show_error=True)
