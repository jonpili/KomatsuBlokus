# KomatsuBlokus
## プロジェクトの概要
これは早稲田大学小松幸夫研究室の「建築のジョー」がBlokusが好きすぎてPC上で開発しようと考え、  
研究室の仲間と共にゲームシステムとAIの開発を目指すプロジェクトです！

## 開発環境
- Python3
- pygame

## Blokusとは
- 4色のブロックを盤面に広げていくボードゲーム
- ルールは単純でブロック同士が頂点で接するように置いていくだけ
- 他のピースをすり抜けて相手の陣地に侵入したり、相手のピースを置けないように妨害するなど様々な戦略がある
- 詳しくは[この記事](https://boku-boardgame.net/blokus)にて

## ブロック一覧表
- 全21種のブロックとそれに対応するアルファベット（黒マスは回転軸）
- ルール引用元：[ブロックスデュオ プログラム対戦 要領](http://hp.vector.co.jp/authors/VA003988/gpcc/07g1.htm)
- 画像引用元：[古川 晋也（2014）C 言語による BlokusDuo 対戦プログラムの作成](http://www.hpc.se.ritsumei.ac.jp/papers/b14/furukawa.pdf)
![ブロック一覧表](https://github.com/JoeTakasuna/KomatsuBlokus/blob/master/%E3%83%96%E3%83%AD%E3%83%83%E3%82%AF%E4%B8%80%E8%A6%A7%E8%A1%A8.png)

## 命名規則
| 対象 | ルール | 例 |
|:---:|:-----:|:--:|
| ファイル | 最初大文字 + 大文字区切り | BlockTable.py |
| クラス | 最初大文字 + 大文字区切り | BlockTable |
| メソッド | 全小文字 + アンダースコア区切り | make_board |
| 関数 | 全小文字 + アンダースコア区切り | change_turn |
| 変数 | 全小文字 + アンダースコア区切り | current_player |
| 定数 | 全大文字 + アンダースコア区切り | TILE_LENGTH |

## 簡単で網羅的なテスト方法
1. 緑：j0
2. 黄：x(check_input：パス)
3. 緑：j0(check_input：使用済みチェック)
4. 緑：e0(start_my_turn：置ける場所があるかのチェック)
5. 緑：a0→zでキャンセル(cancel_selected：キャンセル)
6. 緑：x(check_input：パス, score_check：点数計算)
