import os

import streamlit as st
import requests

st.set_page_config(page_title="LLM Playground", layout="wide")
st.title("Multi-LLM Playground")

API_URL = os.getenv("API_URL", "http://localhost:8080")

# ---------------------------------------------------------------------------
# Sidebar: Model selection
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Model Selection")

    try:
        models_resp = requests.get(f"{API_URL}/models/", timeout=5)
        models_resp.raise_for_status()
        models_data = models_resp.json()
    except requests.RequestException:
        st.error("Cannot reach API. Is the server running?")
        st.stop()

    model_options = [m["id"] for m in models_data["models"]]

    selected = st.selectbox("Active Model", model_options)

    model_info = next(m for m in models_data["models"] if m["id"] == selected)
    st.caption(f"Size: {model_info['size']} | Tier: {model_info['tier']}")

    st.divider()
    st.header("Parameters")
    temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
    max_tokens = st.slider("Max Tokens", 64, 2048, 512, 64)

    st.divider()
    # Health check
    try:
        health = requests.get(f"{API_URL}/health", timeout=5).json()
        ollama_status = health.get("ollama", "unknown")
        color = "green" if ollama_status == "connected" else "red"
        st.markdown(f"Ollama: :{color}[{ollama_status}]")
    except requests.RequestException:
        st.markdown("Ollama: :red[unreachable]")

# ---------------------------------------------------------------------------
# Main area: tabs for Generate and Compare
# ---------------------------------------------------------------------------
tab_generate, tab_compare = st.tabs(["Generate", "Compare Models"])

# --- Generate Tab ---
with tab_generate:
    prompt = st.text_area("Enter your prompt:", height=150, key="gen_prompt")

    if st.button("Generate", type="primary", disabled=not prompt):
        with st.spinner(f"Generating with {selected}..."):
            try:
                resp = requests.post(
                    f"{API_URL}/inference/generate",
                    json={
                        "prompt": prompt,
                        "model": selected,
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                    },
                    timeout=120,
                )
                resp.raise_for_status()
                result = resp.json()

                st.markdown("### Response")
                st.write(result["response"])
                st.caption(
                    f"Model: {result['model']} | "
                    f"Latency: {result['latency_ms']}ms | "
                    f"Tokens: {result['tokens_generated']}"
                )
            except requests.RequestException as e:
                st.error(f"Generation failed: {e}")

# --- Compare Tab ---
with tab_compare:
    compare_prompt = st.text_area(
        "Enter your prompt:", height=150, key="cmp_prompt"
    )

    compare_models = st.multiselect(
        "Select models to compare",
        model_options,
        default=["llama3.2:3b", "qwen2.5:3b", "phi3.5:3.8b"],
    )

    if st.button("Compare", type="primary", disabled=not compare_prompt):
        if len(compare_models) < 2:
            st.warning("Select at least 2 models to compare.")
        else:
            with st.spinner("Comparing models..."):
                try:
                    resp = requests.post(
                        f"{API_URL}/inference/compare",
                        params={
                            "prompt": compare_prompt,
                            "models": compare_models,
                        },
                        timeout=300,
                    )
                    resp.raise_for_status()
                    results = resp.json()

                    cols = st.columns(len(results["comparisons"]))
                    for col, r in zip(cols, results["comparisons"]):
                        with col:
                            st.markdown(f"### {r['model']}")
                            st.write(r["response"])
                            st.caption(
                                f"Latency: {r['latency_ms']}ms | "
                                f"Tokens: {r['tokens_generated']}"
                            )
                except requests.RequestException as e:
                    st.error(f"Comparison failed: {e}")
