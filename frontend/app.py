import os


import html

import requests
import streamlit as st

API_BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
CATEGORIES = ["prepared_meal", "bakery", "produce", "packaged"]

st.set_page_config(
    page_title="FoodLoop AI",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --plum: #42243d;
        --plum-light: #603a56;
        --cream: #f7f4ee;
        --paper: #fffefa;
        --ink: #28252a;
        --muted: #77717a;
        --line: #e8e1e5;
    }

    .stApp {
        background: var(--cream);
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
    }

    [data-testid="stHeader"] { background: transparent; }

    .block-container {
        max-width: 1380px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        font-family: 'Manrope', sans-serif !important;
        color: var(--plum) !important;
        letter-spacing: -0.03em;
    }

    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label {
        color: var(--plum) !important;
        font-weight: 600 !important;
    }

    [data-testid="stMarkdownContainer"] p { color: var(--ink); }

    section[data-testid="stSidebar"] {
        background: #eee7eb;
        border-right: 1px solid var(--line);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid var(--line);
    }

    .stTabs [data-baseweb="tab"] {
        background: #e9dfe6 !important;
        color: var(--plum) !important;
        border-radius: 9px 9px 0 0;
        padding: 10px 14px;
    }

    .stTabs [data-baseweb="tab"] p { color: var(--plum) !important; }

    .stTabs [aria-selected="true"] {
        background: var(--plum) !important;
        color: white !important;
    }

    .stTabs [aria-selected="true"] p { color: white !important; }

    div[data-testid="stForm"] {
        background: var(--paper);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 5px 18px #30202b08;
    }

    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        background: var(--paper) !important;
        color: var(--ink) !important;
        border: 1px solid #d8cbd5 !important;
        border-radius: 9px !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: var(--muted) !important;
        opacity: 1 !important;
    }

    .stSelectbox [data-baseweb="select"] > div,
    .stMultiSelect [data-baseweb="select"] > div {
        background: var(--paper) !important;
        color: var(--ink) !important;
        border-color: #d8cbd5 !important;
        border-radius: 9px !important;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        background: var(--plum);
        color: white !important;
        border: 1px solid var(--plum);
        border-radius: 10px;
        font-weight: 700;
        padding: 0.55rem 1rem;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background: var(--plum-light);
        color: white !important;
        border-color: var(--plum-light);
    }

    div[data-testid="stAlert"] { border-radius: 12px; }

    div[data-testid="stExpander"] {
        background: var(--paper);
        border: 1px solid var(--line);
        border-radius: 12px;
    }

    .metric-card {
        background: var(--paper);
        border: 1px solid var(--line);
        border-radius: 15px;
        padding: 19px;
        min-height: 125px;
        box-shadow: 0 4px 15px #30202b06;
    }

    .metric-label {
        color: #665b68 !important;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .metric-value {
        color: #42243d !important;
        font-family: 'Manrope', sans-serif;
        font-size: 27px;
        font-weight: 800;
        line-height: 1.25;
        overflow-wrap: anywhere;
    }

    .metric-note {
        color: #77717a !important;
        font-size: 11px;
        margin-top: 8px;
    }

    .section-heading {
        color: #42243d !important;
        font-family: 'Manrope', sans-serif;
        font-size: 21px;
        font-weight: 800;
        margin: 10px 0 3px 0;
    }

    .section-sub {
        color: #77717a !important;
        font-size: 12px;
        margin-bottom: 15px;
    }

    .hero-title {
        color: white !important;
        font-family: 'Manrope', sans-serif;
        font-size: 36px;
        font-weight: 800;
        margin: 12px 0;
    }

    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# API HELPERS
# ============================================================

def api_get(path):
    try:
        response = requests.get(f"{API_BASE}{path}", timeout=5)
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as exc:
        return None, f"Backend connection failed: {exc}"
    except ValueError as exc:
        return None, f"Invalid JSON response: {exc}"


def api_post(path, payload=None):
    try:
        response = requests.post(
            f"{API_BASE}{path}",
            json=payload,
            timeout=10,
        )
        if not response.ok:
            return None, f"API {response.status_code}: {response.text}"
        return response.json(), None
    except requests.RequestException as exc:
        return None, f"Backend connection failed: {exc}"
    except ValueError as exc:
        return None, f"Invalid JSON response: {exc}"


def api_patch(path, payload=None):
    try:
        response = requests.patch(
            f"{API_BASE}{path}",
            json=payload,
            timeout=10,
        )
        if not response.ok:
            return None, f"API {response.status_code}: {response.text}"
        return response.json(), None
    except requests.RequestException as exc:
        return None, f"Backend connection failed: {exc}"
    except ValueError as exc:
        return None, f"Invalid JSON response: {exc}"

# ============================================================
# UI HELPERS
# ============================================================

def show_metric(label, value, note, icon):
    safe_label = html.escape(str(label))
    safe_value = html.escape(str(value))
    safe_note = html.escape(str(note))
    safe_icon = html.escape(str(icon))

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{safe_icon} &nbsp; {safe_label}</div>
            <div class="metric-value">{safe_value}</div>
            <div class="metric-note">{safe_note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def category_label(category):
    return str(category).replace("_", " ").title()


def section_heading(title, subtitle=""):
    safe_title = html.escape(title)
    safe_subtitle = html.escape(subtitle)
    st.markdown(
        f'<div class="section-heading">{safe_title}</div>'
        f'<div class="section-sub">{safe_subtitle}</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div style="background:linear-gradient(115deg,#42243d,#603a56);
            padding:28px 30px;border-radius:18px;margin-bottom:24px;">
    <div style="font-size:11px;font-weight:700;letter-spacing:2px;
                color:#f0d8e8;text-transform:uppercase;">
        KOKRAJHAR  FOOD RESCUE COORDINATION
    </div>
    <div style="color:#ffffff;font-family:'Manrope',sans-serif;
            font-size:36px;font-weight:800;margin:12px 0;">
         FoodLoop AI
    </div>
    <p style="color:white;margin:0;">
        Good food deserves another destination.
    </p>
    <div style="display:inline-block;margin-top:15px;padding:6px 11px;
                border:1px solid #b9d9c5;border-radius:25px;
                font-size:12px;color:white;">
         Human-in-the-loop safety enabled
    </div>
</div>
    """,
    unsafe_allow_html=True,
)




# ============================================================
# SIDEBAR / BACKEND HEALTH
# ============================================================

with st.sidebar:
    st.markdown("##  FoodLoop AI")
    st.caption("RESCUE OPERATIONS")
    st.divider()

    st.markdown("**Backend status**")
    health, health_error = api_get("/health")

    if health and health.get("status") == "healthy":
        st.success("API connected")
    else:
        st.error("API unavailable")
        if health_error:
            st.caption(health_error)

    st.code(API_BASE)
    st.caption("Hackathon prototype  Human review required")

    if st.button("Refresh data", use_container_width=True):
        st.rerun()


# ============================================================
# NAVIGATION
# ============================================================

overview_tab, donor_tab, recipient_tab, match_tab, logs_tab = st.tabs(
    [
        "Overview",
        "List food",
        "Register recipient",
        "Agent decisions",
        "Decision logs",
    ]
)


# ============================================================
# OVERVIEW
# ============================================================

with overview_tab:
    donations, donation_error = api_get("/donations")
    recipients, recipient_error = api_get("/recipients")

    donations = donations if isinstance(donations, list) else []
    recipients = recipients if isinstance(recipients, list) else []

    if donation_error:
        st.error(donation_error)
    if recipient_error:
        st.error(recipient_error)

    total_kg = sum(
        float(item.get("quantity_kg", 0) or 0)
        for item in donations
    )

    # Illustrative estimate only, not measured meals delivered.
    meal_estimate = int(total_kg * 4)

    review_count = sum(
        1 for item in donations
        if item.get("requires_human_review", True)
    )

    section_heading(
        "Operations at a glance",
        "Snapshot of records in the local prototype database.",
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        show_metric(
            "Food listed",
            f"{total_kg:,.1f} kg",
            "Recorded donation quantity",
            "",
        )

    with c2:
        show_metric(
            "Meal equivalents",
            f"{meal_estimate:,}",
            "Illustrative estimate  4 per kg",
            "",
        )

    with c3:
        show_metric(
            "Needs review",
            review_count,
            "Records flagged for human review",
            "",
        )

    with c4:
        show_metric(
            "Recipient partners",
            len(recipients),
            "Registered organisations",
            "",
        )

    left, right = st.columns([1.6, 1])

    with left:
        section_heading(
            "Rescue queue",
            "Recently recorded donations.",
        )

        if donations:
            table_data = [
                {
                    "ID": f'FL-{d.get("id", "")}',
                    "Food": d.get("food_name", "Unnamed"),
                    "Category": category_label(
                        d.get("food_category", "")
                    ),
                    "Quantity": (
                        f'{float(d.get("quantity_kg", 0) or 0):g} kg'
                    ),
                    "Location": d.get("location", ""),
                    "Status": category_label(
                        d.get("status", "pending_review")
                    ),
                    "Safety": (
                        "Human review required"
                        if d.get("requires_human_review", True)
                        else "Review flag off"
                    ),
                }
                for d in donations[:10]
            ]

            st.dataframe(
                table_data,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No donations yet. Use List food to create one.")

    with right:
        section_heading(
            "Agent brief",
            "Current system safeguards.",
        )

        show_metric(
            "Agent mode",
            "Match  Explain  Review",
            "Deterministic rule-based matching",
            "",
        )

        st.warning(
            "Matching does not verify food safety, recipient acceptance "
            "or delivery. Human review remains mandatory."
        )


# ============================================================
# LIST DONATION
# ============================================================

with donor_tab:
    st.subheader("List surplus food")
    st.caption("Record surplus food for candidate matching.")

    with st.form("donation_form"):
        food_name = st.text_input("Food name")

        quantity = st.number_input(
            "Quantity (kg)",
            min_value=0.1,
            max_value=10000.0,
            value=5.0,
        )

        category = st.selectbox("Category", CATEGORIES)
        location = st.text_input("Pickup location")

        prepared_at = st.text_input(
            "Prepared at (ISO datetime)",
            "2026-10-21T10:00:00",
        )

        deadline = st.text_input(
            "Pickup deadline (ISO datetime)",
            "2026-10-21T14:00:00",
        )

        storage_notes = st.text_area("Storage/handling notes")

        submit_donation = st.form_submit_button(
            " Submit donation",
            use_container_width=True,
        )

    if submit_donation:
        if (
            not food_name.strip()
            or not location.strip()
            or not storage_notes.strip()
        ):
            st.error(
                "Food name, pickup location and storage notes are required."
            )
        else:
            payload = {
                "food_name": food_name.strip(),
                "quantity_kg": quantity,
                "food_category": category,
                "location": location.strip(),
                "prepared_at": prepared_at.strip(),
                "pickup_deadline": deadline.strip(),
                "storage_notes": storage_notes.strip(),
            }

            result, error = api_post("/donations", payload)

            if error:
                st.error(error)
            else:
                st.success("Donation saved. Human review is required.")
                st.json(result)


# ============================================================
# REGISTER RECIPIENT
# ============================================================

with recipient_tab:
    st.subheader("Register recipient organisation")
    st.caption("Declare accepted food categories and available capacity.")

    with st.form("recipient_form"):
        organisation = st.text_input("Organisation name")

        categories = st.multiselect(
            "Accepted categories",
            CATEGORIES,
        )

        capacity = st.number_input(
            "Declared capacity (kg)",
            min_value=0.1,
            max_value=10000.0,
            value=20.0,
        )

        recipient_location = st.text_input("Organisation location")
        contact_name = st.text_input("Contact person's name")

        submit_recipient = st.form_submit_button(
            " Register recipient",
            use_container_width=True,
        )

    if submit_recipient:
        if (
            not organisation.strip()
            or not recipient_location.strip()
            or not contact_name.strip()
        ):
            st.error(
                "Organisation name, location and contact name are required."
            )
        elif not categories:
            st.error("Select at least one accepted category.")
        else:
            payload = {
                "organisation_name": organisation.strip(),
                "food_categories": categories,
                "capacity_kg": capacity,
                "location": recipient_location.strip(),
                "contact_name": contact_name.strip(),
            }

            result, error = api_post("/recipients", payload)

            if error:
                st.error(error)
            else:
                st.success("Recipient registered.")
                st.json(result)


# ============================================================
# AGENT DECISIONS
# ============================================================

with match_tab:
    st.subheader("Explainable agent decisions")
    st.caption(
        "Inspect eligible matches, rejection reasons and the decision trace."
    )

    current_donations, error = api_get("/donations")

    if error:
        st.error(error)
    elif not current_donations:
        st.info("Create a donation before running matching.")
    else:
        labels = {
            (
                f'#{d["id"]}  {d["food_name"]} '
                f'({d["quantity_kg"]} kg)  '
                f'{category_label(d.get("status", "pending_review"))}'
            ): d["id"]
            for d in current_donations
        }

        selected_label = st.selectbox(
            "Select donation",
            list(labels),
        )
        selected_id = labels[selected_label]

        st.markdown("### Donation workflow status")
        status_options = [
            "pending_review",
            "match_proposed",
            "accepted",
            "completed",
            "cancelled",
        ]

        current_donation = next(
            (d for d in current_donations if d["id"] == selected_id),
            None,
        )
        current_status = (
            current_donation.get("status", "pending_review")
            if current_donation else "pending_review"
        )

        st.caption(f"Current status: {category_label(current_status)}")
        new_status = st.selectbox(
            "Select new status",
            status_options,
            index=(
                status_options.index(current_status)
                if current_status in status_options else 0
            ),
            format_func=category_label,
            key=f"status_choice_{selected_id}",
        )

        if st.button("Update donation status", key=f"update_status_{selected_id}"):
            updated, update_error = api_patch(
                f"/donations/{selected_id}/status",
                {"status": new_status},
            )
            if update_error:
                st.error(update_error)
            else:
                st.success(
                    f"Donation status updated to {category_label(updated.get('status', new_status))}."
                )
                st.rerun()

        if st.button("Run candidate matching"):
            result, error = api_post(
                f"/donations/{selected_id}/match"
            )

            if error:
                st.error(error)
            else:
                st.session_state["foodloop_match_result"] = result
                st.session_state["foodloop_match_id"] = selected_id
                st.rerun()

        result = st.session_state.get("foodloop_match_result")
        result_id = st.session_state.get("foodloop_match_id")

        if result and result_id == selected_id:
            matches = result.get("matches", [])
            rejected = result.get("rejected_candidates", [])

            section_heading(
                "Decision summary",
                "Candidate eligibility and safety review status.",
            )

            c1, c2, c3 = st.columns(3)

            with c1:
                show_metric(
                    "Eligible candidates",
                    len(matches),
                    "Passed current matching rules",
                    "",
                )

            with c2:
                show_metric(
                    "Rejected candidates",
                    len(rejected),
                    "Did not pass matching rules",
                    "",
                )

            with c3:
                show_metric(
                    "Food safety",
                    "NOT VERIFIED",
                    "Human verification required",
                    "",
                )

            st.info(
                result.get(
                    "rationale",
                    "No decision rationale was returned.",
                )
            )

            st.caption(
                f'Action: {result.get("action", "unknown")}  '
                f'Status: {category_label(result.get("status", "pending_review"))}  '
                "Human review required."
            )

            st.markdown("### Eligible matches")

            if matches:
                for match in matches:
                    with st.container(border=True):
                        left, right = st.columns([3, 1])

                        with left:
                            st.markdown(
                                f'**{match.get("organisation_name", "Unknown organisation")}**'
                            )
                            st.caption(
                                f'Location: {match.get("location", "Not provided")}'
                            )

                        with right:
                            show_metric(
                                "Heuristic score",
                                f'{match.get("score", "")}/100',
                                "Ranking score, not probability",
                                "",
                            )

                        reasons = match.get("reasons", [])

                        if reasons:
                            st.markdown("**Why this candidate matched**")
                            for reason in reasons:
                                st.markdown(f"- {reason}")

                        st.warning(
                            "Suggested match only. Recipient confirmation "
                            "and human food-safety review are required."
                        )
            else:
                st.info("No recipient passed the current matching rules.")

            st.markdown("### Rejected candidates")

            if rejected:
                for candidate in rejected:
                    with st.container(border=True):
                        st.markdown(
                            f'**{candidate.get("organisation_name", "Unknown organisation")}**'
                        )

                        rejection_reasons = candidate.get(
                            "rejection_reasons", []
                        )

                        if rejection_reasons:
                            for reason in rejection_reasons:
                                st.markdown(f"- {reason}")
                        else:
                            st.caption(
                                "The API did not provide rejection reasons "
                                "for this candidate."
                            )
            else:
                st.info(
                    "No rejected candidates were returned by the API."
                )

            st.markdown("### Agent tool trace")

            tool_log = result.get("tool_log", [])

            if tool_log:
                for item in tool_log:
                    tool_name = item.get("tool", "Tool execution")

                    with st.expander(tool_name):
                        st.write(
                            item.get("reason", "No explanation recorded.")
                        )
                        st.json(item)
            else:
                st.caption("No tool trace was returned by the API.")

            with st.expander("View raw API response"):
                st.json(result)


# ============================================================
# DECISION LOGS
# ============================================================

with logs_tab:
    st.subheader("Stored agent decision logs")

    current_runs, error = api_get("/agent-runs")

    if error:
        st.error(error)
    elif current_runs:
        st.json(current_runs)
    else:
        st.info("No agent decision logs recorded yet.")


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "FoodLoop AI  Hackathon prototype. Matching is rule-based; "
    "it does not certify food safety, recipient consent or delivery. "
    "Meal equivalents are illustrative estimates, not measured outcomes."
)



