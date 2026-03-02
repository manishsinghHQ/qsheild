import streamlit as st
import re
import matplotlib.pyplot as plt

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="QShield – Post-Quantum Cryptography Scanner",
    layout="wide"
)

# --------------------------------------------------
# Knowledge Base
# --------------------------------------------------
CRYPTO_PATTERNS = {
    "RSA": r"\bRSA\b|genrsa",
    "ECC": r"ECDSA|EC_KEY|secp",
    "Diffie-Hellman": r"DiffieHellman|\bDH\b",
    "AES": r"\bAES\b",
    "SHA-1": r"SHA1|sha1"
}

ALGO_DESCRIPTION = {
    "RSA": "RSA is a public-key cryptographic algorithm used for secure key exchange and digital signatures.",
    "ECC": "Elliptic Curve Cryptography provides strong security using smaller key sizes.",
    "Diffie-Hellman": "Diffie-Hellman enables secure key exchange over insecure channels.",
    "AES": "AES is a symmetric encryption algorithm used to protect sensitive data.",
    "SHA-1": "SHA-1 is a hashing algorithm that is already considered cryptographically broken."
}

QUANTUM_RISK = {
    "RSA": 90,
    "ECC": 85,
    "Diffie-Hellman": 80,
    "AES": 15,
    "SHA-1": 95
}

RISK_EXPLANATION = {
    "RSA": "Shor’s Algorithm allows quantum computers to factor large integers efficiently, breaking RSA.",
    "ECC": "Quantum algorithms can solve elliptic curve discrete logarithms efficiently.",
    "Diffie-Hellman": "Quantum computers can break discrete logarithm–based systems.",
    "AES": "AES is only partially affected by Grover’s Algorithm and remains secure with large keys.",
    "SHA-1": "SHA-1 is already broken even without quantum attacks."
}

PQC_RECOMMENDATION = {
    "RSA": "CRYSTALS-Kyber (Quantum-safe Key Exchange)",
    "ECC": "CRYSTALS-Dilithium (Quantum-safe Digital Signatures)",
    "Diffie-Hellman": "CRYSTALS-Kyber (Key Exchange)",
    "SHA-1": "SHA-3 / SHAKE",
}

PQC_EXPLANATION = {
    "RSA": "Kyber is lattice-based and resistant to Shor’s Algorithm.",
    "ECC": "Dilithium provides quantum-resistant digital signatures.",
    "Diffie-Hellman": "Kyber is designed specifically for post-quantum key exchange.",
    "SHA-1": "SHA-3 is designed to resist both classical and quantum attacks."
}

# --------------------------------------------------
# Utility Functions
# --------------------------------------------------
def scan_code(code):
    detected = []
    for algo, pattern in CRYPTO_PATTERNS.items():
        if re.search(pattern, code, re.IGNORECASE):
            detected.append(algo)
    return detected

def calculate_risk_score(algorithms):
    if not algorithms:
        return 0
    return int(sum(QUANTUM_RISK[a] for a in algorithms) / len(algorithms))

# --------------------------------------------------
# UI Layout
# --------------------------------------------------
st.title("🛡️ QShield – AI-Powered Post-Quantum Readiness Scanner")
st.subheader("Explainable Quantum Risk Assessment for Software Systems")

st.info(
    "QShield scans software code to detect cryptographic algorithms that may become insecure "
    "in the post-quantum era and provides explainable migration guidance."
)

# --------------------------------------------------
# Step 1: Code Input
# --------------------------------------------------
st.header("📂 Step 1: Upload or Paste Source Code")

uploaded_file = st.file_uploader(
    "Upload a source code file",
    type=["py", "java", "js", "c", "cpp"]
)

code_input = st.text_area(
    "Or paste your code here",
    height=220,
    placeholder="Paste your source code here..."
)

code = ""
if uploaded_file:
    code = uploaded_file.read().decode("utf-8", errors="ignore")
elif code_input.strip():
    code = code_input

# --------------------------------------------------
# Run Analysis
# --------------------------------------------------
if st.button("🔍 Analyze Code") and code:
    detected_algos = scan_code(code)

    # --------------------------------------------------
    # Step 2: Detection Results
    # --------------------------------------------------
    st.header("🔍 Step 2: Detected Cryptographic Algorithms")

    if not detected_algos:
        st.success("No cryptographic algorithms detected.")
    else:
        for algo in detected_algos:
            st.success(f"Detected: {algo}")
            st.caption(ALGO_DESCRIPTION[algo])

    # --------------------------------------------------
    # Step 3: Quantum Risk Analysis
    # --------------------------------------------------
    st.header("⚠️ Step 3: Quantum Vulnerability Analysis")

    risk_score = calculate_risk_score(detected_algos)
    st.metric("Quantum Vulnerability Score", f"{risk_score}/100")
    st.progress(risk_score)

    for algo in detected_algos:
        st.warning(f"{algo}: {RISK_EXPLANATION[algo]}")

    # --------------------------------------------------
    # Step 4: Classical vs Quantum Comparison
    # --------------------------------------------------
    st.header("📊 Step 4: Classical vs Quantum Attack Comparison")

    algos = ["RSA-2048", "ECC-256", "Kyber"]
    classical_time = [1e9, 1e8, 1e12]
    quantum_time = [10, 8, 1e12]

    fig, ax = plt.subplots()
    ax.bar(algos, classical_time, label="Classical Attack Time")
    ax.bar(algos, quantum_time, bottom=quantum_time, label="Quantum Attack Time")
    ax.set_yscale("log")
    ax.set_ylabel("Time to Break (log scale)")
    ax.legend()

    st.pyplot(fig)

    st.caption(
        "Quantum computers drastically reduce the time required to break RSA and ECC, "
        "while post-quantum algorithms like Kyber remain secure."
    )

    # --------------------------------------------------
    # Step 5: Post-Quantum Recommendations
    # --------------------------------------------------
    st.header("🛡️ Step 5: Post-Quantum Cryptography Recommendations")

    for algo in detected_algos:
        if algo in PQC_RECOMMENDATION:
            st.success(f"Replace {algo} → {PQC_RECOMMENDATION[algo]}")
            st.caption(PQC_EXPLANATION[algo])

    # --------------------------------------------------
    # Step 6: Migration Roadmap
    # --------------------------------------------------
    st.header("🗺️ Step 6: Migration Roadmap")

    roadmap = []
    for algo in detected_algos:
        if algo in PQC_RECOMMENDATION:
            roadmap.append(
                f"Identify {algo} usage and migrate to {PQC_RECOMMENDATION[algo]}"
            )

    roadmap.append("Deploy hybrid cryptography (classical + PQC)")
    roadmap.append("Perform security and compatibility testing")
    roadmap.append("Gradually phase out classical cryptography")

    for step in roadmap:
        st.write(f"✔️ {step}")

    st.success("Quantum readiness assessment completed successfully.")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption(
    "QShield is an educational research tool designed to raise awareness "
    "about post-quantum cryptography readiness."
)
