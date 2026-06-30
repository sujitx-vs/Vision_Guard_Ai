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
    primary_hue=gr.themes.colors.yellow,
    secondary_hue=gr.themes.colors.yellow,
    neutral_hue=gr.themes.colors.neutral,
    font=(gr.themes.GoogleFont("Archivo"), "ui-sans-serif", "system-ui", "sans-serif"),
    font_mono=(gr.themes.GoogleFont("JetBrains Mono"), "ui-monospace", "Menlo", "monospace"),
).set(
    body_background_fill="#0a0a08",
    background_fill_primary="#121210",
    background_fill_secondary="#0a0a08",
    border_color_primary="#3a3420",
    block_background_fill="#121210",
    block_border_color="#3a3420",
    block_label_text_color="#f5c518",
    block_title_text_color="#f5c518",
    body_text_color="#e9e6da",
    body_text_color_subdued="#9b9474",
    input_background_fill="#181814",
    input_border_color="#3a3420",
    button_primary_background_fill="#f5c518",
    button_primary_background_fill_hover="#ffd83d",
    button_primary_text_color="#0a0a08",
    button_secondary_background_fill="#181814",
    button_secondary_border_color="#5c5430",
    button_secondary_text_color="#f5c518",
)

css = """
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Archivo:wght@600;700;800&display=swap');

:root{
  --vg-bg:#0a0a08;
  --vg-panel:#121210;
  --vg-yellow:#f5c518;
  --vg-yellow-bright:#ffd83d;
  --vg-yellow-dim:#6b6024;
  --vg-line:#3a3420;
  --vg-ink:#e9e6da;
  --vg-ink-dim:#9b9474;
  --vg-hazard:repeating-linear-gradient(135deg,#f5c518 0 10px,#0a0a08 10px 20px);
}

.gradio-container{max-width:1240px!important;background:var(--vg-bg)!important}
.gradio-container,.gradio-container *{box-sizing:border-box}
body, .gradio-container{font-family:'Archivo',ui-sans-serif,system-ui,sans-serif}

/* ---------- hero ---------- */
.hero{
  position:relative;
  padding:28px 28px 24px;
  border-radius:4px;
  background:#0d0d0a;
  border:1px solid var(--vg-line);
  border-left:4px solid var(--vg-yellow);
  margin-bottom:18px;
  overflow:hidden;
}
.hero::before{
  content:"";
  position:absolute;inset:0;
  background:repeating-linear-gradient(0deg, rgba(245,197,24,0.035) 0px, rgba(245,197,24,0.035) 1px, transparent 1px, transparent 3px);
  pointer-events:none;
}
.hero::after{
  content:"";
  position:absolute; top:14px; right:18px;
  width:10px;height:10px;border-radius:50%;
  background:var(--vg-yellow);
  box-shadow:0 0 10px 2px rgba(245,197,24,0.8);
  animation:vg-blink 1.6s steps(2,jump-none) infinite;
}
@keyframes vg-blink{50%{opacity:.15}}
.hero .vg-eyebrow{
  font-family:'JetBrains Mono',monospace;
  font-size:11px;letter-spacing:.18em;text-transform:uppercase;
  color:var(--vg-yellow-dim);margin:0 0 8px 0;
}
.hero h1{
  margin:0 0 8px 0;font-size:38px;font-weight:800;letter-spacing:-0.01em;
  color:var(--vg-yellow);
  text-shadow:0 0 24px rgba(245,197,24,0.25);
}
.hero p{margin:0;font-size:15px;color:var(--vg-ink-dim);max-width:640px;line-height:1.5}

/* ---------- layout ---------- */
.app-shell{gap:18px}
.panel{
  border:1px solid var(--vg-line);
  border-radius:4px;
  background:var(--vg-panel);
  padding:16px;
  position:relative;
}
.panel::before, .panel::after{
  content:"";position:absolute;width:14px;height:14px;
  border-top:2px solid var(--vg-yellow-dim);border-left:2px solid var(--vg-yellow-dim);
  top:-1px;left:-1px;pointer-events:none;
}
.panel::after{
  border-top:none;border-left:none;
  border-bottom:2px solid var(--vg-yellow-dim);border-right:2px solid var(--vg-yellow-dim);
  top:auto;left:auto;bottom:-1px;right:-1px;
}

.tight-md{margin-top:8px}
.tight-md p{margin:0;color:var(--vg-ink-dim);font-family:'JetBrains Mono',monospace;font-size:13px}
.result-stack{gap:14px}
.export-files{gap:14px}
.hidden-empty{min-height:0!important}

/* ---------- viewfinder / reticle treatment on visual elements ---------- */
.gradio-container .gr-video, .gradio-container video,
.gradio-container .image-frame, .gradio-container .gallery,
.gradio-container [data-testid="image"]{
  border-radius:2px!important;
}

label span, .label-wrap span{
  font-family:'JetBrains Mono',monospace!important;
  text-transform:uppercase;letter-spacing:.08em;font-size:12px!important;
  color:var(--vg-yellow)!important;
}

/* markdown headings/answer block read like a terminal readout */
.result-stack h2{
  font-family:'JetBrains Mono',monospace;
  color:var(--vg-yellow);
  font-size:15px;letter-spacing:.04em;text-transform:uppercase;
  border-bottom:1px dashed var(--vg-line);
  padding-bottom:6px;
}
.result-stack code{
  background:#1c1a10;color:var(--vg-yellow-bright);
  border:1px solid var(--vg-line);padding:1px 5px;border-radius:2px;
}

/* buttons */
.gradio-container button.primary{
  font-family:'JetBrains Mono',monospace;font-weight:700;
  letter-spacing:.04em;text-transform:uppercase;font-size:13px;
  box-shadow:0 0 0 1px rgba(245,197,24,0.4);
}
.gradio-container button.secondary{
  font-family:'JetBrains Mono',monospace;font-weight:500;
  letter-spacing:.04em;text-transform:uppercase;font-size:13px;
}

/* dataframe / table rows feel like a log */
.gradio-container table{font-family:'JetBrains Mono',monospace;font-size:12.5px}
.gradio-container thead th{color:var(--vg-yellow)!important;text-transform:uppercase;letter-spacing:.04em}

/* status pill */
#vg-status-wrap p{
  font-family:'JetBrains Mono',monospace;font-size:12px;
  color:var(--vg-yellow-dim);
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
  <p class="vg-eyebrow">// surveillance video intelligence</p>
  <h1>VISION&nbsp;GUARD</h1>
  <p>Step 1: scan the video. Step 2: write a query and find matches. Then review each match and export only what you want.</p>
</div>
"""
    )
    q_state = gr.State("")
    hits_state = gr.State([])

    with gr.Row(elem_classes="app-shell"):
        with gr.Column(scale=1, elem_classes="panel"):
            video = gr.Video(label="cctv video", elem_classes="hidden-empty")
            good = [x for x in _sample_videos() if os.path.exists(x)]
            if good:
                gr.Examples(good, inputs=video, label="sample videos")
            scan_btn = gr.Button("step 1: scan video", variant="primary")
            status = gr.Markdown("ready", elem_id="vg-status-wrap")
            live = gr.Image(label="live indexing preview", interactive=False, elem_classes="hidden-empty")
            info = gr.Markdown(elem_classes="tight-md")
            query = gr.Textbox(label="query", placeholder="person near gate, white car entering, blue truck, umbrella, backpack", interactive=False)
            searched = gr.Markdown(elem_classes="tight-md")
            find_btn = gr.Button("step 2: find matches", interactive=False)

        with gr.Column(scale=2, elem_classes="panel result-stack"):
            answer = gr.Markdown(elem_classes="tight-md")
            table = gr.Dataframe(headers=["Best Frame At", "Clip Window", "Objects", "Summary"], interactive=False, wrap=True)
            pick = gr.CheckboxGroup(label="choose clips to export")
            export_btn = gr.Button("export selected")
            with gr.Row(elem_classes="export-files"):
                zipf = gr.File(label="zip", visible=False)
                html = gr.File(label="html report", visible=False)
                csv = gr.File(label="csv report", visible=False)
            gallery = gr.Gallery(label="matched frames", columns=2, height="auto")
            match_md = gr.Markdown(elem_classes="tight-md")

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