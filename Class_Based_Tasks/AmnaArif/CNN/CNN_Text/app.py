"""Movie Review Sentiment dashboard.

Run the notebook first (it writes the `artifacts/` folder), then start the app with:

    streamlit run app.py
"""
import json
from pathlib import Path

import pandas as pd
import streamlit as st

# Theme colours, shared by the notebook plots and the Streamlit app
OFFWHITE = "#F7F4EF"
PURPLE_DARK = "#2E1A47"
PURPLE = "#4B2A7B"
LAVENDER = "#E4DCEE"
RASPBERRY = "#A63D56"
MUTED = "#6B5B7F"

import re
import html as html_lib
from collections import Counter

PAD, UNK = "<pad>", "<unk>"
MAX_LEN = 24  # every review is cut or padded to exactly this many tokens


def normalize(text):
    """Lower-case the text and expand contractions: wasn't -> was not."""
    text = text.replace("\u2019", "'").lower().strip()
    text = text.replace("can't", "can not").replace("cannot", "can not").replace("won't", "will not")
    return re.sub(r"n't\b", " not", text)


def tokenize(text):
    """Split a review into word tokens. The word 'not' is kept on purpose: it flips the meaning."""
    return re.findall(r"[a-z]+(?:'[a-z]+)?", normalize(text))


def build_vocab(texts, min_freq=1):
    """Map every word seen in `texts` to an integer id. 0 = padding, 1 = unknown word."""
    counts = Counter(tok for t in texts for tok in tokenize(t))
    words = sorted(w for w, c in counts.items() if c >= min_freq)
    return {w: i for i, w in enumerate([PAD, UNK] + words)}


def encode_tokens(tokens, stoi, max_len=MAX_LEN):
    """Tokens -> list of ids, padded with 0 (or cut) to max_len."""
    ids = [stoi.get(tok, stoi[UNK]) for tok in tokens][:max_len]
    return ids + [stoi[PAD]] * (max_len - len(ids))


def encode(text, stoi, max_len=MAX_LEN):
    """Review text -> list of token ids of length max_len."""
    return encode_tokens(tokenize(text), stoi, max_len)


def importance_chips_html(tokens, scores, threshold=0.03):
    """HTML chips: purple = pushes toward positive, raspberry = toward negative, lavender = little effect."""
    chips = []
    for tok, s in zip(tokens, scores):
        if s > threshold:
            bg, fg = PURPLE, "#FFFFFF"
        elif s < -threshold:
            bg, fg = RASPBERRY, "#FFFFFF"
        else:
            bg, fg = LAVENDER, PURPLE_DARK
        chips.append(
            "<span style='display:inline-block;text-align:center;margin:0 6px 10px 0;'>"
            f"<span style='display:block;background:{bg};color:{fg};padding:5px 12px;"
            f"border-radius:8px;font-size:16px;'>{html_lib.escape(tok)}</span>"
            f"<span style='display:block;font-size:12px;color:{MUTED};margin-top:3px;'>{s:+.2f}</span>"
            "</span>"
        )
    return (
        f"<div style='background:{OFFWHITE};padding:14px 14px 4px 14px;border-radius:10px;"
        f"line-height:1.4;'>{''.join(chips)}</div>"
    )

import torch
import torch.nn as nn
import torch.nn.functional as F


class TextCNN(nn.Module):
    """Embedding -> parallel 1D convolutions (n-gram detectors) -> max over time -> linear."""

    def __init__(self, vocab_size, embed_dim=64, num_filters=64, kernel_sizes=(2, 3, 4), dropout=0.4, pad_idx=0):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=pad_idx)
        self.convs = nn.ModuleList([nn.Conv1d(embed_dim, num_filters, k) for k in kernel_sizes])
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(num_filters * len(kernel_sizes), 1)

    def forward(self, x):                              # x: (batch, seq_len) of token ids
        emb = self.embedding(x).transpose(1, 2)        # (batch, embed_dim, seq_len)
        pooled = [F.relu(conv(emb)).max(dim=2).values for conv in self.convs]
        features = self.dropout(torch.cat(pooled, dim=1))
        return self.fc(features).squeeze(1)            # one logit per review: > 0 means positive


def probs_from_token_lists(model, stoi, token_lists, device="cpu"):
    """Probability of 'positive' for each list of tokens."""
    model.eval()
    ids = [encode_tokens(tokens, stoi) for tokens in token_lists]
    x = torch.tensor(ids, dtype=torch.long, device=device)
    with torch.no_grad():
        return torch.sigmoid(model(x)).cpu().tolist()


def predict_text(model, stoi, text, device="cpu"):
    """Predict one review. Returns None when the text has no readable words."""
    tokens = tokenize(text)
    if not tokens:
        return None
    p = probs_from_token_lists(model, stoi, [tokens], device)[0]
    return {
        "label": "Positive" if p >= 0.5 else "Negative",
        "prob_positive": p,
        "confidence": max(p, 1 - p),
        "tokens": tokens,
        "unknown_words": [t for t in tokens if t not in stoi],
        "truncated": len(tokens) > MAX_LEN,
    }


def word_importance(model, stoi, text, device="cpu"):
    """Remove each word in turn and measure how P(positive) changes.
    A positive score means the word pushes the review toward positive."""
    tokens = tokenize(text)[:MAX_LEN]
    variants = [tokens] + [tokens[:i] + tokens[i + 1:] for i in range(len(tokens))]
    probs = probs_from_token_lists(model, stoi, variants, device)
    base = probs[0]
    return tokens, [base - p for p in probs[1:]], base

ARTIFACT_DIR = Path(__file__).parent / "artifacts"
PLACEHOLDER = "Select an example"
EXAMPLES = {
    PLACEHOLDER: "",
    "Plain: the movie was masterclass": "the movie was masterclass",
    "Plain: the movie was good": "the movie was good",
    "Plain: a dull and lifeless film": "a dull and lifeless film",
    "Tricky: the movie was not so bad": "the movie was not so bad",
    "Tricky: the movie was not good": "the movie was not good",
    "Tricky: the film was not boring at all": "the film was not boring at all",
    "Contrast: weak plot but brilliant acting": "the plot was weak but the acting was brilliant",
    "Contrast: great start but a boring finish": "the film started great but ended up boring",
}

st.set_page_config(page_title="Review Sentiment", layout="centered")

st.markdown(
    f"""
<style>
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{ background: {OFFWHITE}; }}
.stApp, .stApp p, .stApp label, .stApp li, .stApp span, .stApp h1, .stApp h2, .stApp h3 {{ color: {PURPLE_DARK}; }}
.block-container {{ max-width: 820px; padding-top: 2.6rem; padding-bottom: 4rem; }}
.eyebrow {{ text-transform: uppercase; letter-spacing: .16em; font-size: 12px; font-weight: 600; color: {MUTED}; margin: 0 0 6px 0; }}
.app-title {{ font-size: 42px; font-weight: 700; line-height: 1.1; letter-spacing: -.02em; color: {PURPLE_DARK}; margin: 0 0 10px 0; }}
.app-sub {{ font-size: 17px; line-height: 1.5; color: {MUTED}; margin: 0 0 26px 0; max-width: 600px; }}
.result-card {{ background: #FFFFFF; border: 1px solid {LAVENDER}; border-left: 8px solid {PURPLE}; border-radius: 14px; padding: 22px 26px 20px 26px; margin: 20px 0 10px 0; }}
.result-kicker {{ font-size: 12px; font-weight: 600; letter-spacing: .14em; text-transform: uppercase; color: {MUTED}; margin-bottom: 4px; }}
.result-label {{ font-size: 38px; font-weight: 700; letter-spacing: -.02em; line-height: 1.1; margin-bottom: 4px; }}
.result-review {{ font-size: 16px; color: {PURPLE_DARK}; margin: 8px 0 18px 0; font-style: italic; }}
.meter {{ display: flex; height: 14px; border-radius: 7px; overflow: hidden; background: {LAVENDER}; }}
.meter-labels {{ display: flex; justify-content: space-between; font-size: 14px; font-weight: 600; margin-top: 8px; }}
.note {{ background: {LAVENDER}; border-radius: 10px; padding: 12px 16px; font-size: 15px; color: {PURPLE_DARK}; margin: 10px 0; }}
.section-title {{ font-size: 22px; font-weight: 700; letter-spacing: -.01em; margin: 30px 0 4px 0; color: {PURPLE_DARK}; }}
.section-sub {{ font-size: 15px; color: {MUTED}; margin: 0 0 12px 0; }}
.legend-dot {{ display: inline-block; width: 11px; height: 11px; border-radius: 3px; margin-right: 6px; vertical-align: -1px; }}
div[data-testid="stTextArea"] textarea {{ background: #FFFFFF; color: {PURPLE_DARK}; border: 1px solid #CFC3DF; border-radius: 10px; font-size: 17px; }}
div[data-testid="stTextArea"] textarea:focus {{ border-color: {PURPLE}; box-shadow: 0 0 0 1px {PURPLE}; }}
div.stButton > button[kind="primary"], div.stButton > button[data-testid="stBaseButton-primary"] {{ background: {PURPLE}; color: #FFFFFF; border: none; border-radius: 10px; padding: .55rem 1.6rem; font-weight: 600; font-size: 16px; }}
div.stButton > button[kind="primary"]:hover, div.stButton > button[data-testid="stBaseButton-primary"]:hover {{ background: {PURPLE_DARK}; color: #FFFFFF; }}
div.stButton > button[kind="primary"] p, div.stButton > button[data-testid="stBaseButton-primary"] p {{ color: #FFFFFF; }}
div[data-baseweb="select"] > div {{ background: #FFFFFF; color: {PURPLE_DARK}; border-color: #CFC3DF; border-radius: 10px; }}
button[data-baseweb="tab"][aria-selected="true"] p {{ color: {PURPLE}; font-weight: 700; }}
div[data-baseweb="tab-highlight"] {{ background-color: {PURPLE}; }}
[data-testid="stMetric"] {{ background: #FFFFFF; border: 1px solid {LAVENDER}; border-radius: 12px; padding: 14px 16px; }}
footer, #MainMenu {{ visibility: hidden; }}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner="Loading model")
def load_bundle():
    weights, vocab, metrics = (ARTIFACT_DIR / n for n in ("cnn_sentiment.pt", "vocab.json", "metrics.json"))
    if not (weights.exists() and vocab.exists()):
        return None
    checkpoint = torch.load(weights, map_location="cpu", weights_only=True)
    cfg = checkpoint["config"]
    model = TextCNN(cfg["vocab_size"], cfg["embed_dim"], cfg["num_filters"], tuple(cfg["kernel_sizes"]), cfg["dropout"])
    model.load_state_dict(checkpoint["state_dict"])
    model.eval()
    return {
        "model": model,
        "stoi": json.loads(vocab.read_text()),
        "metrics": json.loads(metrics.read_text()) if metrics.exists() else {},
        "max_len": cfg.get("max_len", MAX_LEN),
    }


def set_review_from_example():
    choice = st.session_state["example_choice"]
    if choice != PLACEHOLDER:
        st.session_state["review_text"] = EXAMPLES[choice]
        st.session_state["submitted"] = EXAMPLES[choice]


def submit_review():
    st.session_state["submitted"] = st.session_state["review_text"].strip()


def render_result(bundle, review):
    result = predict_text(bundle["model"], bundle["stoi"], review)
    if result is None:
        st.markdown("<div class='note'>No readable words were found. Try a full sentence.</div>", unsafe_allow_html=True)
        return

    positive = result["label"] == "Positive"
    accent = PURPLE if positive else RASPBERRY
    p_pos = result["prob_positive"] * 100
    p_neg = 100 - p_pos
    st.markdown(
        "".join([
            f"<div class='result-card' style='border-left-color:{accent};'>",
            "<div class='result-kicker'>Predicted sentiment</div>",
            f"<div class='result-label' style='color:{accent};'>{result['label']}</div>",
            f"<div class='result-review'>&ldquo;{html_lib.escape(review)}&rdquo;</div>",
            "<div class='meter'>",
            f"<div style='width:{p_pos:.2f}%;background:{PURPLE};'></div>",
            f"<div style='width:{p_neg:.2f}%;background:{RASPBERRY};'></div>",
            "</div>",
            "<div class='meter-labels'>",
            f"<span style='color:{PURPLE};'>Positive {p_pos:.1f}%</span>",
            f"<span style='color:{RASPBERRY};'>Negative {p_neg:.1f}%</span>",
            "</div>",
            "</div>",
        ]),
        unsafe_allow_html=True,
    )

    notes = []
    if result["confidence"] < 0.65:
        notes.append("The model is not very sure about this one. Treat the result as a lean, not a verdict.")
    if result["unknown_words"]:
        words = ", ".join(sorted(set(result["unknown_words"])))
        notes.append(f"Words the model has not seen: {html_lib.escape(words)}. They are ignored, so the result may be less reliable.")
    if result["truncated"]:
        notes.append(f"Only the first {MAX_LEN} words are used.")
    for note in notes:
        st.markdown(f"<div class='note'>{note}</div>", unsafe_allow_html=True)

    tokens, scores, _ = word_importance(bundle["model"], bundle["stoi"], review)
    st.markdown("<div class='section-title'>What drove this result</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-sub'>Each word is removed in turn and the change in the positive probability is shown below it. "
        f"<span class='legend-dot' style='background:{PURPLE};'></span>pushes toward positive "
        f"<span class='legend-dot' style='background:{RASPBERRY};margin-left:10px;'></span>pushes toward negative</div>",
        unsafe_allow_html=True,
    )
    st.markdown(importance_chips_html(tokens, scores), unsafe_allow_html=True)

    with st.expander("Token ids the model saw"):
        stoi = bundle["stoi"]
        table = pd.DataFrame({
            "Position": range(1, len(tokens) + 1),
            "Token": tokens,
            "Id": [stoi.get(t, stoi[UNK]) for t in tokens],
            "Known word": ["yes" if t in stoi else "no" for t in tokens],
        }).set_index("Position")
        st.table(table)
        st.code(str(encode_tokens(tokens, stoi)), language="text")
        st.caption(f"Padded with 0 to {MAX_LEN} ids. Id 1 stands for an unknown word.")


def render_model_tab(bundle):
    m = bundle["metrics"]
    st.markdown("<div class='section-title'>How the model did</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-sub'>Measured by the notebook after training. The test split comes from the same file as the "
        "training data, so it is an easy exam; the check set is a small group of hand-written sentences.</div>",
        unsafe_allow_html=True,
    )

    def pct(key):
        return f"{m[key] * 100:.1f}%" if key in m else "n/a"

    c1, c2, c3 = st.columns(3)
    c1.metric("Test accuracy", pct("test_accuracy"))
    c2.metric(f"Check set ({m.get('check_set_size', '?')} sentences)", pct("check_set_accuracy"))
    c3.metric("Unseen-word sentences", pct("unseen_words_accuracy"))
    c4, c5, c6 = st.columns(3)
    c4.metric("Vocabulary", f"{m.get('vocab_size', 'n/a')}")
    c5.metric("Parameters", f"{m['parameters']:,}" if "parameters" in m else "n/a")
    c6.metric("Epochs trained", f"{m.get('epochs_trained', 'n/a')}")

    groups = m.get("check_set_by_group")
    if groups:
        st.markdown("<div class='section-title'>Check set by type of sentence</div>", unsafe_allow_html=True)
        table = pd.DataFrame({"Type": list(groups), "Accuracy": [f"{v * 100:.0f}%" for v in groups.values()]})
        st.table(table.set_index("Type"))

    st.markdown("<div class='section-title'>How it works</div>", unsafe_allow_html=True)
    st.markdown(
        "1. The review is lower-cased and split into words. Contractions such as *wasn't* become *was not*.\n"
        "2. Each word becomes an id from the vocabulary; unknown words become a neutral placeholder.\n"
        "3. The ids pass through an embedding layer, then convolutions with window sizes 2, 3 and 4 that act as phrase detectors, "
        "so a pair like *not bad* can be recognised as one unit.\n"
        "4. The strongest signal from each detector is combined into a single score, which becomes the probability of a positive review."
    )
    st.markdown("<div class='section-title'>Limits</div>", unsafe_allow_html=True)
    aug = "plus synthetic sentences covering everyday words and negation" if m.get("augmentation") else "without synthetic sentences"
    st.markdown(
        f"The model was trained on 600 short reviews {aug}. It works best on short, single-idea reviews. "
        "Sarcasm, long reviews, slang and words it has never seen can fool it."
    )


bundle = load_bundle()

st.markdown(
    "<div class='eyebrow'>Text CNN</div>"
    "<div class='app-title'>Movie Review Sentiment</div>"
    "<div class='app-sub'>Type a review and the model tells you whether it reads as positive or negative. "
    "It also copes with negation, so &ldquo;not so bad&rdquo; is not mistaken for a complaint.</div>",
    unsafe_allow_html=True,
)

if bundle is None:
    st.markdown(
        "<div class='note'>The trained model was not found. Run every cell of <b>movie_review_cnn.ipynb</b> first; "
        "it creates an <b>artifacts</b> folder next to this file. Then refresh this page.</div>",
        unsafe_allow_html=True,
    )
    st.stop()

if bundle["max_len"] != MAX_LEN:
    st.error(f"The saved model expects {bundle['max_len']} tokens per review but this app uses {MAX_LEN}. Set MAX_LEN to match.")
    st.stop()

st.session_state.setdefault("review_text", "")
st.session_state.setdefault("submitted", None)

predict_tab, model_tab = st.tabs(["Predict", "About the model"])

with predict_tab:
    st.selectbox("Try an example", list(EXAMPLES), key="example_choice", on_change=set_review_from_example)
    st.text_area("Your review", key="review_text", height=130, placeholder="Type a movie review here...")
    st.button("Analyze review", type="primary", on_click=submit_review)

    submitted = st.session_state["submitted"]
    if submitted is not None:
        if submitted:
            render_result(bundle, submitted)
        else:
            st.markdown("<div class='note'>Type a review first, then press Analyze review.</div>", unsafe_allow_html=True)

with model_tab:
    render_model_tab(bundle)
