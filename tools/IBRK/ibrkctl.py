"""
IB helper wrappers around ib_insync.
Exposes ~16 utility functions plus a JSON schema (TOOLS) for the Cursor agent.
"""

from __future__ import annotations
import pathlib, datetime, textwrap, csv
from typing import Dict, Any, List, Literal
from ib_insync import *

# --- Connect to TWS ---
ib = IB()
ib.connect("127.0.0.1", 7496, clientId=1)   # change clientId if needed
ib.reqMarketDataType(4)  # 4 = delayed-frozen quotes (15-minute delay)

# --- Basic helper functions ---
def get_option_chain(symbol: str):
    p = ib.reqSecDefOptParams(symbol, "", "STK", 0)[0]
    return {"expirations": sorted(p.expirations), "strikes": sorted(p.strikes)}


def get_greeks(symbol: str, expiry: str, strike: float, right: Literal["C", "P"]):
    """Return real-time option greeks as a dictionary. Requires an active OPRA subscription."""
    opt = Option(symbol, expiry, strike, right, "SMART"); ib.qualifyContracts(opt)
    ticker = ib.reqMktData(opt, "", False, False); ib.sleep(2)
    greeks = ticker.modelGreeks
    result = {
        "impliedVol": greeks.impliedVol if greeks else None,
        "delta": greeks.delta if greeks else None,
        "gamma": greeks.gamma if greeks else None,
        "theta": greeks.theta if greeks else None,
        "vega": greeks.vega if greeks else None,
        "rho": getattr(greeks, 'rho', None) if greeks else None,
    }
    ib.cancelMktData(opt)
    return result


def get_option_price(symbol: str, expiry: str, strike: float, right: Literal["C", "P"]):
    """Return current option prices."""
    opt = Option(symbol, expiry, strike, right, "SMART"); ib.qualifyContracts(opt)
    ticker = ib.reqMktData(opt, "", False, False); ib.sleep(2)
    result = {
        "bid": ticker.bid,
        "ask": ticker.ask,
        "last": ticker.last,
        "close": ticker.close,
        "mark": (ticker.bid + ticker.ask) / 2 if ticker.bid and ticker.ask else ticker.last,
    }
    ib.cancelMktData(opt)
    return result


def get_positions():
    """Return portfolio as a list of dictionaries.
    For stocks the dict contains account, symbol, secType, currency, position and avgCost.
    For options the dict additionally has strike, expiry (YYYYMMDD) and right (C/P).
    """
    res = []
    for p in ib.positions():
        base = {
            "account": p.account,
            "symbol": p.contract.symbol,
            "secType": p.contract.secType,
            "currency": p.contract.currency,
            "position": p.position,
            "avgCost": p.avgCost,
        }
        if p.contract.secType == "OPT":
            base.update({
                "expiry": p.contract.lastTradeDateOrContractMonth,
                "strike": p.contract.strike,
                "right": p.contract.right,
            })
        res.append(base)
    return res


def get_account_summary():
    return {r.tag: r.value for r in ib.accountSummary()}


def place_order(
    symbol: str,
    qty: int,
    side: Literal["BUY", "SELL"],
    orderType: Literal["MKT", "LMT"] = "MKT",
    limitPrice: float | None = None,
):
    c = Stock(symbol, "SMART", "USD"); ib.qualifyContracts(c)
    o = MarketOrder(side, qty) if orderType == "MKT" else LimitOrder(side, qty, limitPrice)
    tr = ib.placeOrder(c, o); ib.sleep(1)
    s = tr.orderStatus
    return {
        "id": tr.order.orderId,
        "status": s.status,
        "filled": s.filled,
        "avgPrice": s.avgFillPrice,
    }


def close_option_spread(
    symbol: str,
    expiry: str,
    long_strike: float,
    short_strike: float,
    qty: int,
    orderType: Literal["MKT", "LMT"] = "MKT",
    limitPrice: float | None = None,
):
    """Close an option spread: sell the long leg, buy the short leg."""
    # Create contracts for both legs of the spread
    long_leg = Option(symbol, expiry, long_strike, "C", "SMART")
    short_leg = Option(symbol, expiry, short_strike, "C", "SMART")
    
    # Qualify contracts
    ib.qualifyContracts(long_leg, short_leg)
    
    # Create spread contract
    spread = Contract()
    spread.symbol = symbol
    spread.secType = "BAG"
    spread.currency = "USD"
    spread.exchange = "SMART"
    
    # Add combo legs
    spread.comboLegs = [
        ComboLeg(conId=long_leg.conId, ratio=1, action="SELL"),  # Sell long leg
        ComboLeg(conId=short_leg.conId, ratio=1, action="BUY"),  # Buy short leg
    ]
    
    # Create order
    if orderType == "MKT":
        order = MarketOrder("SELL", qty)
    else:
        order = LimitOrder("SELL", qty, limitPrice)
    
    # Place order
    tr = ib.placeOrder(spread, order)
    ib.sleep(2)
    
    s = tr.orderStatus
    return {
        "id": tr.order.orderId,
        "status": s.status,
        "filled": s.filled,
        "avgPrice": s.avgFillPrice,
        "message": f"Closing {qty} {symbol} {expiry} {long_strike}C/{short_strike}C spread"
    }


def cancel_order(orderId: int):
    ts = [t for t in ib.trades() if t.order.orderId == orderId]
    if ts:
        ib.cancelOrder(ts[0].order)
    return "cancel_requested"


def save_markdown(filename: str, content: str):
    text = f"# {filename}\n\n_{datetime.datetime.now()}_\n\n" + textwrap.dedent(content)
    p = pathlib.Path(filename).with_suffix(".md"); p.write_text(text, encoding="utf-8")
    return str(p.resolve())


def save_csv(filename: str, rows: List[Dict[str, Any]]):
    p = pathlib.Path(filename).with_suffix(".csv")
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    return str(p.resolve())

# --- Advanced helper functions ---
def get_hist_data(symbol: str, endDate: str, duration: str, barSize: str):
    c = Stock(symbol, "SMART", "USD"); ib.qualifyContracts(c)
    bars = ib.reqHistoricalData(c, endDate, duration, barSize, "TRADES", 1, 1, False)
    return [b.__dict__ for b in bars]


def get_real_time_bars(symbol: str):
    c = Stock(symbol, "SMART", "USD"); ib.qualifyContracts(c)
    bars = []

    def onBar(bar, _):
        bars.append(bar.__dict__)

    ib.reqRealTimeBars(c, 5, "TRADES", True, onBar); ib.sleep(10); ib.cancelRealTimeBars(c)
    return bars


def get_mkt_depth(symbol: str, numRows: int = 5):
    c = Stock(symbol, "SMART", "USD"); ib.qualifyContracts(c)
    t = ib.reqMktDepth(c, numRows, False, []); ib.sleep(2)
    return {
        "bids": [l.__dict__ for l in t.domBids],
        "asks": [l.__dict__ for l in t.domAsks],
    }


def get_scanner(industry: str = "STK", scanCode: str = "TOP_PERC_GAIN"):
    scan = ScannerSubscription(instrument=industry, scanCode=scanCode)
    return [r.__dict__ for r in ib.reqScannerResults(scan)]


def get_fundamentals(symbol: str, reportType: str = "ReportsFinSummary"):
    c = Stock(symbol, "SMART", "USD"); ib.qualifyContracts(c)
    return {"xml": ib.reqFundamentalData(c, reportType)}


def get_news_headlines(symbol: str, providerCode: str = "BRFG", last: int = 10):
    news = ib.reqHistoricalNews(0, symbol, providerCode, "", 0, "")
    return [h.__dict__ for h in news[:last]]


def get_news_article(articleId: int):
    return {"articleId": articleId, "text": ib.reqNewsArticle(0, "", articleId, "")}


def get_open_orders():
    return [t.order.__dict__ for t in ib.openTrades()]


def get_order_status(orderId: int):
    ts = [t for t in ib.trades() if t.order.orderId == orderId]
    return ts[0].orderStatus.__dict__ if ts else {"error": "not_found"}


def get_contract_details(symbol: str):
    c = Stock(symbol, "SMART", "USD"); ib.qualifyContracts(c)
    return [d.__dict__ for d in ib.reqContractDetails(c)]

# ───── executions
def get_executions(symbol: str = "", date: str = ""):
    """Return a list of executions for the given day.
    symbol — optional ticker filter, date — 'YYYY-MM-DD'.
    Empty arguments mean no filtering."""
    ex_details = ib.reqExecutions()
    if not date:
        date = datetime.datetime.now().strftime("%Y-%m-%d")
    rows: List[Dict[str, Any]] = []
    for d in ex_details:
        exec = d.execution
        contract = d.contract
        trade_date = exec.time.date().isoformat()
        if symbol and contract.symbol != symbol:
            continue
        if date and trade_date != date:
            continue
        rows.append({
            "time": exec.time.isoformat(),
            "symbol": contract.symbol,
            "secType": contract.secType,
            "expiry": getattr(contract, "lastTradeDateOrContractMonth", ""),
            "strike": getattr(contract, "strike", ""),
            "right": getattr(contract, "right", ""),
            "side": "BUY" if exec.side == "BOT" else "SELL",
            "qty": exec.shares,
            "price": exec.price,
            "commission": d.commissionReport.commission if d.commissionReport else None,
        })
    return rows

# --- JSON-Schema (used by the Cursor agent) ---

def _schema(obj):
    return {"type": "object", "properties": obj, "required": list(obj)}

TOOLS = [
    {"name": "get_option_chain", "description": "Option chain", "parameters": _schema({"symbol": {"type": "string"}})},
    {"name": "get_greeks", "description": "Option greeks", "parameters": _schema({
        "symbol": {"type": "string"}, "expiry": {"type": "string"},
        "strike": {"type": "number"}, "right": {"type": "string", "enum": ["C", "P"]}})},
    {"name": "get_positions", "description": "Open positions", "parameters": {"type": "object", "properties": {}}},
    {"name": "get_account_summary", "description": "Account summary", "parameters": {"type": "object", "properties": {}}},
    {"name": "place_order", "description": "Place order", "parameters": _schema({
        "symbol": {"type": "string"}, "qty": {"type": "integer"},
        "side": {"type": "string", "enum": ["BUY", "SELL"]},
        "orderType": {"type": "string", "enum": ["MKT", "LMT"]},
        "limitPrice": {"type": "number"}})},
    {"name": "cancel_order", "description": "Cancel order", "parameters": _schema({"orderId": {"type": "integer"}})},
    {"name": "save_markdown", "description": "Save Markdown", "parameters": _schema({
        "filename": {"type": "string"}, "content": {"type": "string"}})},
    {"name": "save_csv", "description": "Save CSV", "parameters": _schema({
        "filename": {"type": "string"}, "rows": {"type": "array", "items": {"type": "object"}}})},
    {"name": "get_hist_data", "description": "Historical bars", "parameters": _schema({
        "symbol": {"type": "string"}, "endDate": {"type": "string"},
        "duration": {"type": "string"}, "barSize": {"type": "string"}})},
    {"name": "get_real_time_bars", "description": "Real-time bars (10 s)", "parameters": _schema({"symbol": {"type": "string"}})},
    {"name": "get_mkt_depth", "description": "Market depth (Level II)", "parameters": _schema({
        "symbol": {"type": "string"}, "numRows": {"type": "integer"}})},
    {"name": "get_scanner", "description": "Scanner", "parameters": _schema({
        "industry": {"type": "string"}, "scanCode": {"type": "string"}})},
    {"name": "get_fundamentals", "description": "Fundamental XML", "parameters": _schema({
        "symbol": {"type": "string"}, "reportType": {"type": "string"}})},
    {"name": "get_news_headlines", "description": "News headlines", "parameters": _schema({
        "symbol": {"type": "string"}, "providerCode": {"type": "string"}, "last": {"type": "integer"}})},
    {"name": "get_news_article", "description": "News article text", "parameters": _schema({
        "articleId": {"type": "integer"}})},
    {"name": "get_open_orders", "description": "Open orders", "parameters": {"type": "object", "properties": {}}},
    {"name": "get_order_status", "description": "Order status", "parameters": _schema({"orderId": {"type": "integer"}})},
    {"name": "get_contract_details", "description": "Contract details", "parameters": _schema({"symbol": {"type": "string"}})},
    {"name": "get_executions", "description": "Executions history", "parameters": {"type": "object", "properties": {"symbol": {"type": "string"}, "date": {"type": "string"}}}}
] 