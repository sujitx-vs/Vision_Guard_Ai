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
    font=(gr.themes.GoogleFont("Archivo"), "ui-sans-serif", "system-ui", "sans-serif"),
    font_mono=(gr.themes.GoogleFont("JetBrains Mono"), "ui-monospace", "Menlo", "monospace"),
).set(
    body_background_fill="#06080c",
    background_fill_primary="#0d1117",
    background_fill_secondary="#06080c",
    border_color_primary="#1c2b3a",
    block_background_fill="#0d1117",
    block_border_color="#1c2b3a",
    block_label_text_color="#ffffff",
    block_title_text_color="#5aa3d6",
    body_text_color="#ffffff",
    body_text_color_subdued="#c7d0d8",
    input_background_fill="#10161f",
    input_border_color="#1c2b3a",
    button_primary_background_fill="#2c7fc1",
    button_primary_background_fill_hover="#5aa3d6",
    button_primary_text_color="#06080c",
    button_secondary_background_fill="#10161f",
    button_secondary_border_color="#1d4f73",
    button_secondary_text_color="#ffffff",
)

css = """
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Archivo:wght@600;700;800&display=swap');

:root{
  --vg-bg:#06080c;
  --vg-panel:#0d1117;
  --vg-blue:#2c7fc1;
  --vg-blue-bright:#5aa3d6;
  --vg-blue-dim:#1d4f73;
  --vg-line:#1c2b3a;
  --vg-ink:#ffffff;
  --vg-ink-dim:#c7d0d8;
  --vg-glow:0 0 18px rgba(44,127,193,0.30), 0 0 48px rgba(44,127,193,0.10);
}

.gradio-container{max-width:880px!important;margin:0 auto!important;background:var(--vg-bg)!important}
.gradio-container,.gradio-container *{box-sizing:border-box}
body, .gradio-container{font-family:'Archivo',ui-sans-serif,system-ui,sans-serif;color:var(--vg-ink)}
body{
  display:flex;justify-content:center;
  background:
    radial-gradient(circle at 15% 0%, rgba(44,127,193,0.09), transparent 45%),
    radial-gradient(circle at 85% 20%, rgba(44,127,193,0.07), transparent 40%),
    var(--vg-bg);
}

/* ---------- hero ---------- */
.hero{
  position:relative;
  padding:30px 28px 26px;
  border-radius:10px;
  background:rgba(13,17,23,0.85);
  border:1px solid var(--vg-line);
  margin-bottom:18px;
  overflow:hidden;
  backdrop-filter:blur(14px);
  box-shadow:var(--vg-glow);
}
.hero::before{
  content:"";
  position:absolute;inset:0;
  background:repeating-linear-gradient(0deg, rgba(44,127,193,0.035) 0px, rgba(44,127,193,0.035) 1px, transparent 1px, transparent 3px);
  pointer-events:none;
}
.hero::after{
  content:"";
  position:absolute;top:-60px;right:-60px;
  width:220px;height:220px;border-radius:50%;
  background:radial-gradient(circle, rgba(44,127,193,0.35), transparent 70%);
  filter:blur(30px);
  pointer-events:none;
}
.hero .vg-eyebrow{
  position:relative;z-index:1;
  font-family:'JetBrains Mono',monospace;
  font-size:11px;letter-spacing:.18em;text-transform:uppercase;
  color:var(--vg-blue-dim);margin:0 0 8px 0;
  display:flex;align-items:center;gap:8px;
}
.hero .vg-eyebrow .vg-dot{
  width:8px;height:8px;border-radius:50%;
  background:var(--vg-blue-bright);
  box-shadow:0 0 8px 2px rgba(90,163,214,0.9);
  animation:vg-blink 1.6s steps(2,jump-none) infinite;
}
@keyframes vg-blink{50%{opacity:.2}}
.hero h1{
  position:relative;z-index:1;
  margin:0 0 4px 0;font-size:36px;font-weight:800;letter-spacing:-0.01em;
  color:var(--vg-blue-bright);
  text-shadow:0 0 24px rgba(44,127,193,0.45), 0 0 60px rgba(44,127,193,0.2);
  line-height:1.1;
}
.hero p.vg-sub{position:relative;z-index:1;margin:0;font-size:14px;color:var(--vg-ink);max-width:640px;line-height:1.5}

/* step pills */
.hero-steps{
  position:relative;z-index:1;
  display:flex;flex-wrap:wrap;align-items:center;gap:10px;
  margin-top:16px;
}
.hero-steps .vg-step{
  display:flex;align-items:center;gap:8px;
  font-family:'JetBrains Mono',monospace;font-size:12.5px;letter-spacing:.02em;
  background:rgba(44,127,193,0.07);border:1px solid var(--vg-line);border-radius:6px;
  padding:8px 14px 8px 8px;color:#ffffff;
  white-space:nowrap;
  backdrop-filter:blur(6px);
}
.hero-steps .vg-step b{
  display:inline-flex;align-items:center;justify-content:center;
  flex:none;width:18px;height:18px;border-radius:50%;
  background:var(--vg-blue-bright);color:#06080c;font-size:11px;font-weight:700;
  box-shadow:0 0 10px 1px rgba(90,163,214,0.7);
}
.hero-steps .vg-arrow{
  color:var(--vg-blue-dim);font-family:'JetBrains Mono',monospace;font-size:13px;
}

/* ---------- single-column layout ---------- */
.app-shell{gap:18px;display:flex;flex-direction:column}
.panel{
  border:1px solid var(--vg-line);
  border-radius:10px;
  background:rgba(13,17,23,0.78);
  backdrop-filter:blur(14px);
  padding:18px;
  position:relative;
  box-shadow:0 0 0 1px rgba(44,127,193,0.04), 0 12px 40px rgba(0,0,0,0.35);
}
.panel.vg-glow-panel{box-shadow:var(--vg-glow), 0 12px 40px rgba(0,0,0,0.35);}

.tight-md{margin-top:8px}
.tight-md p{margin:0;color:#ffffff;font-family:'JetBrains Mono',monospace;font-size:13px}
.result-stack{gap:16px}
.export-files{gap:14px}
.hidden-empty{min-height:0!important}

/* sub-section headers */
.vg-section{
  display:flex;align-items:center;gap:8px;
  font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--vg-blue-bright);margin:4px 0 12px 0;
  text-shadow:0 0 12px rgba(44,127,193,0.4);
}
.vg-section .vg-badge{
  display:inline-flex;align-items:center;justify-content:center;
  width:18px;height:18px;border-radius:5px;flex:none;
  background:var(--vg-blue-bright);color:#06080c;font-size:11px;font-weight:700;
  box-shadow:0 0 10px 1px rgba(90,163,214,0.6);
}
.vg-section::after{
  content:"";flex:1;height:1px;
  background:linear-gradient(90deg, var(--vg-line), transparent);
}
.vg-divider{
  height:1px;
  background:linear-gradient(90deg, transparent, var(--vg-line) 20%, var(--vg-line) 80%, transparent);
  margin:18px 0 14px 0;border:none;
}
.vg-block{margin-bottom:2px}

/* ---------- viewfinder treatment ---------- */
.gradio-container .gr-video, .gradio-container video,
.gradio-container .image-frame, .gradio-container .gallery,
.gradio-container [data-testid="image"]{
  border-radius:8px!important;
}

label span, .label-wrap span{
  font-family:'JetBrains Mono',monospace!important;
  text-transform:uppercase;letter-spacing:.08em;font-size:12px!important;
  color:#ffffff!important;
}

.result-stack h2{
  font-family:'JetBrains Mono',monospace;
  color:var(--vg-blue-bright);
  font-size:15px;letter-spacing:.04em;text-transform:uppercase;
  border-bottom:1px dashed var(--vg-line);
  padding-bottom:6px;
}
.result-stack code{
  background:rgba(44,127,193,0.10);color:var(--vg-blue-bright);
  border:1px solid var(--vg-line);padding:1px 5px;border-radius:4px;
}

/* buttons with luminous glow */
.gradio-container button.primary{
  font-family:'JetBrains Mono',monospace;font-weight:700;
  letter-spacing:.04em;text-transform:uppercase;font-size:13px;
  box-shadow:0 0 16px 1px rgba(44,127,193,0.55), 0 0 0 1px rgba(44,127,193,0.4);
  transition:box-shadow .2s ease, transform .15s ease;
}
.gradio-container button.primary:hover{
  box-shadow:0 0 26px 4px rgba(90,163,214,0.7), 0 0 0 1px rgba(90,163,214,0.6);
  transform:translateY(-1px);
}
.gradio-container button.secondary{
  font-family:'JetBrains Mono',monospace;font-weight:500;
  letter-spacing:.04em;text-transform:uppercase;font-size:13px;
  box-shadow:0 0 0 1px rgba(44,127,193,0.15);
}

/* dataframe / table rows */
.gradio-container table{font-family:'JetBrains Mono',monospace;font-size:12.5px;color:#ffffff}
.gradio-container thead th{color:#ffffff!important;text-transform:uppercase;letter-spacing:.04em}

/* status pill */
#vg-status-wrap p{
  font-family:'JetBrains Mono',monospace;font-size:12px;
  color:#ffffff;
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
  <p class="vg-eyebrow"><span class="vg-dot"></span>// surveillance video intelligence</p>
  <h1>VISION&nbsp;GUARD</h1>
  <p class="vg-sub">Scan a video to index it, then search it in plain language and export only the clips you need.</p>
  <div class="hero-steps">
    <div class="vg-step"><b>1</b>scan the video</div>
    <span class="vg-arrow">&rarr;</span>
    <div class="vg-step"><b>2</b>write a query &amp; find matches</div>
    <span class="vg-arrow">&rarr;</span>
    <div class="vg-step"><b>3</b>review &amp; export selected clips</div>
  </div>
</div>
"""
    )
    q_state = gr.State("")
    hits_state = gr.State([])

    with gr.Column(elem_classes="app-shell"):
        with gr.Group(elem_classes="panel vg-glow-panel"):
            gr.HTML('<div class="vg-section"><span class="vg-badge">1</span>upload &amp; scan</div>')
            video = gr.Video(label="cctv video", elem_classes="hidden-empty")
            good = [x for x in _sample_videos() if os.path.exists(x)]
            if good:
                gr.Examples(good, inputs=video, label="sample videos")
            scan_btn = gr.Button("step 1: scan video", variant="primary")
            status = gr.Markdown("ready", elem_id="vg-status-wrap")

            gr.HTML('<hr class="vg-divider"/><div class="vg-section"><span class="vg-badge">2</span>search</div>')
            query = gr.Textbox(label="query", placeholder="person near gate, white car entering, blue truck, umbrella, backpack", interactive=False)
            find_btn = gr.Button("step 2: find matches", interactive=False)
            searched = gr.Markdown(elem_classes="tight-md")

            gr.HTML('<hr class="vg-divider"/><div class="vg-section">indexing detail</div>')
            live = gr.Image(label="live indexing preview", interactive=False, elem_classes="hidden-empty")
            info = gr.Markdown(elem_classes="tight-md")

        with gr.Group(elem_classes="panel result-stack"):
            gr.HTML('<div class="vg-section"><span class="vg-badge">3</span>results</div>')
            answer = gr.Markdown(elem_classes="tight-md")
            table = gr.Dataframe(headers=["Best Frame At", "Clip Window", "Objects", "Summary"], interactive=False, wrap=True)
            gallery = gr.Gallery(label="matched frames", columns=2, height="auto")
            match_md = gr.Markdown(elem_classes="tight-md")

            gr.HTML('<hr class="vg-divider"/><div class="vg-section"><span class="vg-badge">4</span>export</div>')
            pick = gr.CheckboxGroup(label="choose clips to export")
            export_btn = gr.Button("export selected")
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
