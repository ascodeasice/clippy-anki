#!/usr/bin/env python3
import os
import re
import csv
import sys

def remove_ansi(s):
    """
    移除字串中的 ANSI escape 序列。
    """
    ansi_escape = re.compile(r'\x1B\[[0-9;]*[A-Za-z]')
    return ansi_escape.sub('', s)

def process_line(line):
    # 移除 ANSI 色彩碼
    line = remove_ansi(line)

    # 略過包含 START 或 STOP 的行
    if 'START' in line or 'STOP' in line:
        return None

    # 移除行首所有 "*" 與前導空白（可能有多個 "*"）
    line = re.sub(r'^[ \t]*\*+[ \t]*', '', line)
    if not line:
        return None

    # 假設目標字串位於行首，並以至少兩個空白分隔後，餘下部分為正確拼寫資訊
    m = re.match(r'^(.*?)\s{2,}(.*)$', line)
    if not m:
        return None

    target_field = m.group(1).strip()
    rest = m.group(2).strip()

    # 若目標欄位含有多個單詞，則忽略該行
    if len(target_field.split()) != 1:
        return None

    # 移除剩餘部分中的 < 與 > 符號
    rest = re.sub(r'[<>]', '', rest)
    # 以空白拆分取得所有可能正確拼寫項目
    correct_spellings = rest.split()
    second = "\n".join(correct_spellings)

    return (target_field, second)

def main():
    # 若未提供檔案名稱，預設讀取 ~/.config/plover/clippy_2.org
    input_file = sys.argv[1] if len(sys.argv) > 1 else f"{os.path.expanduser('~')}/.config/plover/clippy_2.org"
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'output.csv'

    rows = []
    seen_targets = set()  # 用以避免重複目標字
    with open(input_file, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            processed = process_line(line)
            if processed:
                target, second = processed
                if target in seen_targets:
                    continue
                seen_targets.add(target)
                rows.append((target, second))

    # 輸出 CSV 檔案，CSV 模組會自動處理欄位中包含換行符號的情況
    with open(output_file, 'w', newline='', encoding='utf-8') as f_out:
        writer = csv.writer(f_out)
        for row in rows:
            writer.writerow(row)

if __name__ == '__main__':
    main()
