from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="PAM Trading Assistant API", version="1.0.0")

# -------- MODELLER -------- #

class PamModeConfig(BaseModel):
    name: str = "Vur-Kaç PAM Modu"
    target_holding_minutes: dict = {"min": 45, "max": 60}
    timeout_no_move_minutes: int = 30
    leverage_range: dict = {"typical_min": 20, "typical_max": 40, "hard_cap": 50}
    target_price_move_pct: dict = {"min": 4.0, "max": 9.0}
    fomo_rule: str = "Fiyat kısa sürede aşırı koşmuşsa, PAM modu kovalamaz."
    risk_per_trade_hint_pct: float = 1.0
    notes: list = ["İşlem süresi 1 saati geçerse PAM dışı kabul edilir."]

class LeverageQaRequest(BaseModel):
    question: str
    symbol: Optional[str] = None
    account_size: Optional[float] = None
    max_leverage: Optional[float] = None
    risk_per_trade_pct: Optional[float] = 1.0
    additional_context: Optional[str] = None

class LeverageQaResponse(BaseModel):
    answer: str
    pam_decision: str
    pam_reasons: List[str]
    risk_notes: List[str]
    suggested_scenarios: List[dict]

# -------- ENDPOINTLER -------- #

@app.get("/")
def root():
    return {"message": "PAM Trading Assistant API aktif 🔥"}

@app.get("/pam/mode", response_model=PamModeConfig)
def get_pam_mode():
    """PAM modu temel yapılandırması"""
    return PamModeConfig()

@app.post("/leverage/qa", response_model=LeverageQaResponse)
def leverage_qa(req: LeverageQaRequest):
    symbol = req.symbol or "Belirtilmedi"
    decision = "consider_with_caution" if req.max_leverage and req.max_leverage > 30 else "watch_only"
    return LeverageQaResponse(
        answer=f"{symbol} için analiz: {req.question}",
        pam_decision=decision,
        pam_reasons=["Trend inceleniyor", "Hacim artışı gözlemlenmiş"],
        risk_notes=["Yüksek kaldıraçta likidasyon riski artar."],
        suggested_scenarios=[
            {
                "direction": "long",
                "rationale": "Trend yukarı ve EMA21 üzerinde.",
                "example_sl_comment": "Son dip altı SL (örnek senaryo)",
                "example_tp_comment": "%4-9 arası hedefleme önerilir"
            }
        ]
    )
