#!/usr/bin/env python3
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

    # 先移除行首所有 "*" 與前導空白（假設行首可能有多個 "*"）
    line = re.sub(r'^[ \t]*\*+[ \t]*', '', line)
    if not line:
        return None

    # 假設目標字串（第一欄）位於行首，並以至少兩個空白作為分隔符
    m = re.match(r'^(.*?)\s{2,}(.*)$', line)
    if not m:
        # 若找不到兩個以上的空白分隔，則無法判斷目標欄，跳過此行
        return None

    target_field = m.group(1).strip()
    rest = m.group(2).strip()

    # 若目標欄位含有多個單詞，則忽略該行
    if len(target_field.split()) != 1:
        return None

    # 將剩餘部分移除 < 與 > 符號
    rest = re.sub(r'[<>]', '', rest)
    # 以空白拆分取得所有可能的正確拼寫項目
    correct_spellings = rest.split()
    second = "\n".join(correct_spellings)

    return (target_field, second)

def main():
    # 讀取檔案名稱參數，預設 input.txt
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'output.csv'

    rows = []
    with open(input_file, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            processed = process_line(line)
            if processed:
                rows.append(processed)

    # 輸出 CSV 檔案，第二欄的換行符號將自動以引號處理
    with open(output_file, 'w', newline='', encoding='utf-8') as f_out:
        writer = csv.writer(f_out)
        for row in rows:
            writer.writerow(row)

if __name__ == '__main__':
    main()
