#!/usr/bin/env python3
"""
Тестовый скрипт для проверки сбора индикаторов без TWS
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from collect_indicators import IndicatorCollector

def test_sources():
    """Тестирование различных источников данных"""
    
    print("=== ТЕСТИРОВАНИЕ ИНДИКАТОРОВ ===\n")
    
    collector = IndicatorCollector()
    
    # Тест 1: FRED API
    print("1. Тестирование FRED API...")
    fred_data = collector.get_fred_indicators()
    if fred_data:
        print(f"   Получено {len(fred_data)} индикаторов")
        for name, data in fred_data.items():
            if data['status'] == 'ok':
                print(f"   ✅ {name}: {data['value']}")
            else:
                print(f"   ❌ {name}: {data['status']}")
    else:
        print("   FRED API недоступен (нужен API ключ)")
    
    print()
    
    # Тест 2: Treasury.gov
    print("2. Тестирование Treasury.gov...")
    treasury_data = collector.get_treasury_indicators()
    if treasury_data:
        print(f"   Получено {len(treasury_data)} индикаторов")
        for name, data in treasury_data.items():
            if data['status'] == 'ok':
                print(f"   ✅ {name}: {data['value']}")
            else:
                print(f"   ❌ {name}: {data['status']}")
    
    print()
    
    # Тест 3: CoinGecko
    print("3. Тестирование CoinGecko...")
    coingecko_data = collector.get_coingecko_indicators()
    if coingecko_data:
        print(f"   Получено {len(coingecko_data)} индикаторов")
        for name, data in coingecko_data.items():
            if data['status'] == 'ok':
                print(f"   ✅ {name}: {data['value']}")
            else:
                print(f"   ❌ {name}: {data['status']}")
    
    print()
    
    # Тест 4: Кастомные индикаторы (с мок-данными)
    print("4. Тестирование кастомных индикаторов...")
    # Добавляем мок-данные для теста
    collector.data['indicators']['macro']['fed_balance_sheet'] = {'value': 8000.0, 'source': 'mock'}
    collector.data['indicators']['liquidity']['tga_balance'] = {'value': 500.0, 'source': 'mock'}
    collector.data['indicators']['liquidity']['rrp_volume'] = {'value': 2000.0, 'source': 'mock'}
    collector.data['indicators']['macro']['ust_10y_yield'] = {'value': 4.5, 'source': 'mock'}
    
    custom_data = collector.calculate_custom_indicators()
    if custom_data:
        print(f"   Получено {len(custom_data)} индикаторов")
        for name, data in custom_data.items():
            if data['status'] == 'ok':
                print(f"   ✅ {name}: {data['value']}")
                if 'components' in data:
                    print(f"      Компоненты: {data['components']}")
            else:
                print(f"   ❌ {name}: {data['status']}")
    
    print("\n=== ТЕСТ ЗАВЕРШЕН ===")

if __name__ == "__main__":
    test_sources() 