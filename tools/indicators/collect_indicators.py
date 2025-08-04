#!/usr/bin/env python3
"""
Инструмент для сбора ключевых макро‑/ликвидити‑индикаторов.
Источники: TWS, FRED, Treasury FiscalData, CoinGecko.

Версия v0.4 – фикс масштабов, сортировки и sentinel‑значений.
"""

import os
import sys
import json
import argparse
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# ------------------------------------------------------------------ #
# 1.  I M P O R T S   &   E N V
# ------------------------------------------------------------------ #
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    from ib_insync import IB, Index, Stock
    import requests
    from fredapi import Fred
    from pycoingecko import CoinGeckoAPI
except ImportError as e:
    print(f"Ошибка импорта: {e}")
    print("Установите зависимости: pip install -r requirements.txt")
    sys.exit(1)

# ------------------------------------------------------------------ #
# 2.  L O G G I N G
# ------------------------------------------------------------------ #
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------ #
# 3.  C L A S S
# ------------------------------------------------------------------ #
class IndicatorCollector:
    """
    Собирает и агрегирует индикаторы:
      • ликвидность (Net Liquidity, TGA, RRP)
      • макро (WALCL, M2, UST‑yields, DXY, VIX)
      • крипто (BTC price & dominance)
    """

    # --- init ------------------------------------------------------ #
    def __init__(self) -> None:
        # 3.1  единицы измерения  ---------------------------------- #
        # приводим всё к миллиардам $, проценты – как есть
        self.unit_scale: dict[str, float] = {
            "WALCL": 1e-3,      # млн → млрд
            "RRPONTSYD": 1e-3,  # млн → млрд
            "M2SL": 1,          # млрд
            "GFDEBTN": 1,       # млрд
            "GDP": 1,           # млрд
        }

        # 3.2  внешние клиенты  ------------------------------------ #
        self.ib: IB = IB()

        fred_key = os.getenv("FRED_API_KEY")
        if fred_key:
            self.fred = Fred(api_key=fred_key)
            logger.info("FRED API подключен")
        else:
            self.fred = None
            logger.warning("FRED_API_KEY не найден")

        self.cg = CoinGeckoAPI()

        # 3.3  контейнер данных  ----------------------------------- #
        self.data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(timespec="seconds"),
            "indicators": {"liquidity": {}, "macro": {}, "crypto": {}, "risk": {}},
        }

    # ------------------------------------------------------------------ #
    # 4.  H E L P E R S
    # ------------------------------------------------------------------ #
    def fred_last(self, series_id: str) -> tuple[float, str]:
        """
        Возвращает (значение, дата) последней опубликованной точки
        с учётом масштабирования unit_scale.
        """
        s = self.fred.get_series_latest_release(series_id)
        val = float(s.iloc[-1]) * self.unit_scale.get(series_id, 1)
        date = s.index[-1].strftime("%Y-%m-%d")
        return val, date

    @staticmethod
    def _latest_row(url: str, filt: str) -> dict:
        """Берём последнюю строку (record_date DESC) с заданным фильтром."""
        params = {
            "filter": filt,
            "sort": "-record_date",
            "page[size]": 1,
            "format": "json",
        }
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()["data"]
        if not data:
            raise ValueError("No data returned from Treasury API")
        return data[0]

    # ------------------------------------------------------------------ #
    # 5.  T W S
    # ------------------------------------------------------------------ #
    def connect_tws(self) -> bool:
        try:
            self.ib.connect("127.0.0.1", 7496, clientId=1)
            self.ib.reqMarketDataType(4)  # delayed‑frozen
            logger.info("Подключен к TWS")
            return True
        except Exception as e:
            logger.error(f"TWS connect: {e}")
            return False

    def disconnect_tws(self) -> None:
        if self.ib.isConnected():
            self.ib.disconnect()
            logger.info("TWS отключён")

    def get_tws_indicators(self) -> Dict[str, Any]:
        """UST yields, DXY, VIX, GLD, BITO через TWS."""
        if not self.ib.isConnected():
            return {}

        contracts = {
            "ust_30y": Index("TYX", "CBOE"),     # yield × 10
            "ust_10y": Index("TNX", "CBOE"),
            "dxy_ice": Index("DXY", "NYBOT"),    # ICE DXY (Futures)
            "vix": Index("VIX", "CBOE"),
            "gold": Stock("GLD", "ARCA"),
            "btc": Stock("BITO", "ARCA"),
        }

        ind: Dict[str, Any] = {}

        for name, c in contracts.items():
            try:
                self.ib.qualifyContracts(c)
                t = self.ib.reqMktData(c, "", False, False)
                self.ib.sleep(0.5)

                price = None if (t.last is None or t.last == -1) else t.last
                if price is not None and name.startswith("ust_"):
                    price = price / 10  # TYX/TNX scale fix

                ind[name] = {
                    "value": price,
                    "status": "ok" if price is not None else "no_data",
                    "source": "tws",
                    "bid": None if t.bid == -1 else t.bid,
                    "ask": None if t.ask == -1 else t.ask,
                }

                self.ib.cancelMktData(c)
            except Exception as e:
                logger.error(f"TWS {name}: {e}")
                ind[name] = {"status": "error", "source": "tws"}

        return ind

    # ------------------------------------------------------------------ #
    # 6.  F R E D
    # ------------------------------------------------------------------ #
    def get_fred_indicators(self) -> Dict[str, Any]:
        if not self.fred:
            return {}

        series_map = {
            "m2_money_stock": "M2SL",
            "fed_balance_sheet": "WALCL",
            "federal_debt": "GFDEBTN",
            "gdp": "GDP",
            "dxy_fred": "DTWEXBGS",  # FRED DXY (Broad Dollar Index)
        }

        ind: Dict[str, Any] = {}

        for name, sid in series_map.items():
            try:
                val, d = self.fred_last(sid)
                ind[name] = {"value": val, "date": d, "status": "ok", "source": "fred"}
            except Exception as e:
                logger.error(f"FRED {sid}: {e}")
                ind[name] = {"status": "error", "source": "fred"}

        return ind

    # ------------------------------------------------------------------ #
    # 7.  T R E A S U R Y
    # ------------------------------------------------------------------ #
    def get_treasury_indicators(self) -> Dict[str, Any]:
        ind: Dict[str, Any] = {}

        # 7.1  TGA
        try:
            url = ("https://api.fiscaldata.treasury.gov/services/api/"
                   "fiscal_service/v1/accounting/dts/operating_cash_balance")
            row = self._latest_row(url, "account_type:eq:TGA Closing Balance")
            tga = float(row["open_today_bal"]) * 1e-3  # млн → млрд
            ind["tga_balance"] = {
                "value": tga,
                "date": row["record_date"],
                "status": "ok",
                "source": "treasury",
            }
        except Exception as e:
            logger.error(f"TGA Treasury API failed: {e}")
            # Fallback to FRED WTREGEN (Weekly Treasury General Account)
            try:
                if self.fred:
                    tga, d = self.fred_last("WTREGEN")  # уже в млрд $
                    ind["tga_balance"] = {
                        "value": tga,
                        "date": d,
                        "status": "ok",
                        "source": "fred",
                    }
                    logger.info("TGA fallback to FRED WTREGEN successful")
                else:
                    ind["tga_balance"] = {"status": "error", "source": "treasury"}
            except Exception as fe:
                logger.error(f"TGA FRED fallback failed: {fe}")
                ind["tga_balance"] = {"status": "error", "source": "treasury"}

        # 7.2  RRP (через FRED)
        try:
            rrp, d = self.fred_last("RRPONTSYD")
            ind["rrp_volume"] = {
                "value": rrp,
                "date": d,
                "status": "ok",
                "source": "fred",
            }
        except Exception as e:
            logger.error(f"RRP fetch: {e}")
            ind["rrp_volume"] = {"status": "error", "source": "fred"}

        return ind

    # ------------------------------------------------------------------ #
    # 8.  C O I N G E C K O
    # ------------------------------------------------------------------ #
    def get_coingecko_indicators(self) -> Dict[str, Any]:
        ind: Dict[str, Any] = {}
        try:
            btc = self.cg.get_coin_by_id("bitcoin")
            glob = self.cg.get_global()

            ind["btc_price"] = {
                "value": btc["market_data"]["current_price"]["usd"],
                "status": "ok",
                "source": "coingecko",
            }

            btc_mcap = btc["market_data"]["market_cap"]["usd"]
            total_mcap = glob["total_market_cap"]["usd"]
            ind["btc_dominance"] = {
                "value": btc_mcap / total_mcap * 100,
                "status": "ok",
                "source": "coingecko",
            }
        except Exception as e:
            logger.error(f"CoinGecko: {e}")
            ind["btc_price"] = {"status": "error", "source": "coingecko"}
            ind["btc_dominance"] = {"status": "error", "source": "coingecko"}
        return ind

    # ------------------------------------------------------------------ #
    # 9.  C U S T O M
    # ------------------------------------------------------------------ #
    def calculate_custom_indicators(self) -> Dict[str, Any]:
        liq = self.data["indicators"]["liquidity"]
        mac = self.data["indicators"]["macro"]

        fed = mac.get("fed_balance_sheet", {}).get("value")
        tga = liq.get("tga_balance", {}).get("value")
        rrp = liq.get("rrp_volume", {}).get("value")

        if all(x is not None for x in (fed, tga, rrp)):
            net = fed - tga - rrp
            return {
                "net_liquidity": {
                    "value": net,
                    "status": "ok",
                    "source": "custom",
                    "components": {"fed": fed, "tga": tga, "rrp": rrp},
                }
            }
        return {"net_liquidity": {"status": "no_data", "source": "custom"}}

    # ------------------------------------------------------------------ #
    # 10.  M A I N   W O R K F L O W
    # ------------------------------------------------------------------ #
    def collect_all(self, sources: Optional[list[str]] = None) -> Dict[str, Any]:
        if sources is None:
            sources = ["tws", "fred", "treasury", "coingecko", "custom"]
        logger.info(f"Сбор из: {sources}")

        if "tws" in sources and not self.connect_tws():
            sources.remove("tws")

        try:
            if "tws" in sources:
                self.data["indicators"]["macro"].update(self.get_tws_indicators())

            if "fred" in sources:
                self.data["indicators"]["macro"].update(self.get_fred_indicators())

            if "treasury" in sources:
                self.data["indicators"]["liquidity"].update(
                    self.get_treasury_indicators()
                )

            if "coingecko" in sources:
                self.data["indicators"]["crypto"].update(
                    self.get_coingecko_indicators()
                )

            if "custom" in sources:
                self.data["indicators"]["liquidity"].update(
                    self.calculate_custom_indicators()
                )
        finally:
            if "tws" in sources:
                self.disconnect_tws()

        return self.data

    # ------------------------------------------------------------------ #
    # 11.  I/O
    # ------------------------------------------------------------------ #
    def save_to_file(self, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved → {filename}")

    def print_summary(self) -> None:
        print("\n===  С В О Д К А  ===")
        for cat, ind in self.data["indicators"].items():
            print(f"\n{cat.upper()}:")
            for k, v in ind.items():
                status = v.get("status")
                val = v.get("value")
                if status == "ok":
                    print(f"  ✅ {k}: {val}")
                elif status == "error":
                    print(f"  ❌ {k}: ERROR")
                else:
                    print(f"  ⚠️  {k}: no data")

# ------------------------------------------------------------------ #
# 12.  C L I
# ------------------------------------------------------------------ #
def main() -> None:
    p = argparse.ArgumentParser("Сбор индикаторов")
    p.add_argument("--source", nargs="+",
                   choices=["tws", "fred", "treasury", "coingecko", "custom"],
                   help="ограничить источники")
    p.add_argument("--output", help="файл JSON для сохранения")
    args = p.parse_args()

    ic = IndicatorCollector()
    ic.collect_all(args.source or None)
    ic.print_summary()

    fname = args.output or f"indicators_{datetime.utcnow():%Y-%m-%d_%H-%M}.json"
    ic.save_to_file(fname)

if __name__ == "__main__":
    main()
